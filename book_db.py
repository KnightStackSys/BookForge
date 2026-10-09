from __future__ import annotations

import hashlib
import json
import sqlite3
import struct
import zlib
from pathlib import Path
from typing import Iterable

from book_types import BookMove


SCHEMA_VERSION = 1
RAW_PAYLOAD = 0
ZLIB_PAYLOAD = 1

DEFAULT_BUSY_TIMEOUT_MS = 30_000

def position_key(root_spec: str, moves: Iterable[str]) -> bytes:
    """
    Stable 128-bit key for a book node.

    This intentionally keys by root + move history instead of board state,
    because plain UCI does not provide a standard command for retrieving the
    engine's canonical FEN4/Zobrist key. This is correct but does not merge
    transpositions reached by different move orders.
    """
    h = hashlib.blake2b(digest_size=16, person=b"BookForgeBook")
    h.update(root_spec.encode("utf-8"))
    h.update(b"\x00")
    for move in moves:
        h.update(move.encode("ascii"))
        h.update(b"\x00")
    return h.digest()

def _pack_moves(moves: list[BookMove]) -> bytes:
    out = bytearray(struct.pack("<BH", 1, len(moves)))

    for item in moves:
        move_bytes = item.move.encode("ascii")
        if len(move_bytes) > 255:
            raise ValueError(f"Move string is too long: {item.move!r}")

        kind = 0 if item.score_kind == "cp" else 1
        out += struct.pack(
            "<BBiHHH",
            len(move_bytes),
            kind,
            int(item.score),
            max(0, min(65535, int(item.depth))),
            max(0, min(65535, int(item.seldepth))),
            max(0, min(65535, int(item.multipv))),
        )
        out += move_bytes

    raw = bytes(out)
    compressed = zlib.compress(raw, level=9)

    if len(compressed) + 1 < len(raw) + 1:
        return bytes([ZLIB_PAYLOAD]) + compressed
    return bytes([RAW_PAYLOAD]) + raw


def _unpack_moves(payload: bytes) -> list[BookMove]:
    if not payload:
        return []

    mode = payload[0]
    data = payload[1:]
    if mode == ZLIB_PAYLOAD:
        data = zlib.decompress(data)
    elif mode != RAW_PAYLOAD:
        raise ValueError(f"Unknown payload compression mode: {mode}")

    offset = 0
    version, count = struct.unpack_from("<BH", data, offset)
    offset += struct.calcsize("<BH")

    if version != 1:
        raise ValueError(f"Unsupported move payload version: {version}")

    result: list[BookMove] = []
    entry_size = struct.calcsize("<BBiHHH")

    for _ in range(count):
        move_len, kind, score, depth, seldepth, multipv = struct.unpack_from(
            "<BBiHHH", data, offset
        )
        offset += entry_size

        move = data[offset : offset + move_len].decode("ascii")
        offset += move_len

        result.append(
            BookMove(
                move=move,
                score_kind="cp" if kind == 0 else "mate",
                score=score,
                depth=depth,
                seldepth=seldepth,
                multipv=multipv,
            )
        )

    return result

class BookDB:
    """
    SQLite-backed opening book.

    PyPy note:
        Do not rely on connection.execute(...) temporary cursors being
        finalized immediately. PyPy's GC may keep them alive long enough for
        SQLite to report:

            cannot commit transaction - SQL statements in progress

        All statements in this class therefore use explicit cursors that are
        fetched (when applicable) and closed deterministically.
    """
    def __init__(
        self,
        path: str | Path,
        readonly: bool = False,
    ) -> None:
        self.path = Path(path)
        self.readonly = readonly

        if readonly:
            uri = (
                f"file:"
                f"{self.path.resolve().as_posix()}"
                f"?mode=ro"
            )

            self.conn = sqlite3.connect(
                uri,
                uri=True,
            )
        else:
            self.conn = sqlite3.connect(
                self.path
            )

            self._pragma(
                "PRAGMA journal_mode=WAL",
                consume_result=True,
            )

            self._pragma(
                "PRAGMA synchronous=NORMAL"
            )

            self._pragma(
                "PRAGMA temp_store=MEMORY"
            )

        self._pragma(
            f"PRAGMA busy_timeout="
            f"{DEFAULT_BUSY_TIMEOUT_MS}"
        )

        self._pragma(
            "PRAGMA foreign_keys=ON"
        )

    def _pragma(
        self,
        sql: str,
        *,
        consume_result: bool = False,
    ) -> list[tuple]:
        cur = self.conn.cursor()

        try:
            cur.execute(sql)

            if consume_result:
                return cur.fetchall()

            if cur.description is not None:
                return cur.fetchall()

            return []

        finally:
            cur.close()

    def _execute_write(
        self,
        sql: str,
        params: tuple = (),
    ) -> None:
        cur = self.conn.cursor()

        try:
            cur.execute(
                sql,
                params,
            )
        finally:
            cur.close()

    def _fetchone(
        self,
        sql: str,
        params: tuple = (),
    ):
        cur = self.conn.cursor()

        try:
            cur.execute(
                sql,
                params,
            )

            return cur.fetchone()

        finally:
            cur.close()

    def _fetchall(
        self,
        sql: str,
        params: tuple = (),
    ) -> list[tuple]:
        cur = self.conn.cursor()

        try:
            cur.execute(
                sql,
                params,
            )

            return cur.fetchall()

        finally:
            cur.close()

    def _executescript(
        self,
        script: str,
    ) -> None:
        cur = self.conn.cursor()

        try:
            cur.executescript(
                script
            )
        finally:
            cur.close()

    def close(self) -> None:
        self.conn.close()

    def __enter__(
        self,
    ) -> "BookDB":
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:
        try:
            if (
                not self.readonly
                and exc_type is None
            ):
                self.conn.commit()
        finally:
            self.close()

    def create_schema(self) -> None:
        if self.readonly:
            raise RuntimeError(
                "Cannot create schema in readonly mode."
            )

        self._executescript(
            """
            CREATE TABLE IF NOT EXISTS meta (
                key   TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS positions (
                pos_key BLOB PRIMARY KEY,
                ply     INTEGER NOT NULL,
                payload BLOB NOT NULL
            ) WITHOUT ROWID;

            CREATE INDEX IF NOT EXISTS idx_positions_ply
                ON positions(ply);
            """
        )

        self.set_meta(
            "schema_version",
            str(SCHEMA_VERSION),
        )

        self.conn.commit()

    def clear(self) -> None:
        """
        Clear the existing book without DROP TABLE.

        This avoids SQLite schema-lock contention and is also safe for PyPy's
        sqlite3 implementation because every statement cursor is explicitly
        finalized before COMMIT.
        """
        if self.readonly:
            raise RuntimeError(
                "Cannot clear a readonly book."
            )

        self.create_schema()

        try:
            self._execute_write(
                "BEGIN IMMEDIATE"
            )

            self._execute_write(
                "DELETE FROM positions"
            )

            self._execute_write(
                "DELETE FROM meta"
            )

            self.conn.commit()

        except sqlite3.OperationalError as exc:
            try:
                self.conn.rollback()
            except sqlite3.Error:
                pass

            message = str(exc).lower()

            if (
                "locked" in message
                or "busy" in message
            ):
                raise RuntimeError(
                    f"Could not overwrite book database "
                    f"{self.path!s} because another process "
                    "still has a conflicting SQLite lock. "
                    "Close any other running generator/writer "
                    "and retry."
                ) from exc

            if (
                "statements in progress"
                in message
            ):
                raise RuntimeError(
                    "PyPy/SQLite reported an unfinished SQL statement "
                    "during overwrite. This version explicitly closes every "
                    "BookDB cursor; if you still see this message, another "
                    "module is keeping a cursor open on the same connection."
                ) from exc

            raise

        self.set_meta(
            "schema_version",
            str(SCHEMA_VERSION),
        )

        self.conn.commit()

    def set_meta(
        self,
        key: str,
        value: str,
    ) -> None:
        if self.readonly:
            raise RuntimeError(
                "Cannot modify a readonly book."
            )

        self._execute_write(
            """
            INSERT INTO meta(key, value)
            VALUES(?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value=excluded.value
            """,
            (
                key,
                value,
            ),
        )

    def get_meta(
        self,
        key: str,
        default: str | None = None,
    ) -> str | None:
        row = self._fetchone(
            """
            SELECT value
            FROM meta
            WHERE key=?
            """,
            (key,),
        )

        return (
            row[0]
            if row
            else default
        )

    def get_all_meta(
        self,
    ) -> dict[str, str]:
        rows = self._fetchall(
            "SELECT key, value FROM meta"
        )

        return dict(rows)

    def has_position(
        self,
        key: bytes,
    ) -> bool:
        row = self._fetchone(
            """
            SELECT 1
            FROM positions
            WHERE pos_key=?
            LIMIT 1
            """,
            (key,),
        )

        return row is not None

    def get_moves(
        self,
        key: bytes,
    ) -> list[BookMove] | None:
        row = self._fetchone(
            """
            SELECT payload
            FROM positions
            WHERE pos_key=?
            """,
            (key,),
        )

        if row is None:
            return None

        return _unpack_moves(
            row[0]
        )

    def put_moves(
        self,
        key: bytes,
        ply: int,
        moves: list[BookMove],
    ) -> None:
        if self.readonly:
            raise RuntimeError(
                "Cannot modify a readonly book."
            )

        self._execute_write(
            """
            INSERT INTO positions(
                pos_key,
                ply,
                payload
            )
            VALUES(?, ?, ?)
            ON CONFLICT(pos_key) DO UPDATE SET
                ply=excluded.ply,
                payload=excluded.payload
            """,
            (
                key,
                ply,
                _pack_moves(moves),
            ),
        )

    def count_positions(
        self,
    ) -> int:
        row = self._fetchone(
            "SELECT COUNT(*) FROM positions"
        )

        return int(
            row[0]
        )

    def commit(self) -> None:
        if not self.readonly:
            self.conn.commit()

    def vacuum(self) -> None:
        if self.readonly:
            return

        self.conn.commit()

        cur = self.conn.cursor()

        try:
            cur.execute(
                "VACUUM"
            )

            if cur.description is not None:
                cur.fetchall()

        finally:
            cur.close()
