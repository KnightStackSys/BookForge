from __future__ import annotations

import gzip
import hashlib
from pathlib import Path

class BalancedFenWriter:
    """
    Streaming gzip writer for balanced FEN/FEN4 positions.

    The gzip payload contains ONLY:
        <fen>\n
        <fen>\n
        ...

    No JSON, scores, comments, headers, or other metadata are written.

    When deduplicate=True, existing FENs are hashed on startup so generation
    can resume without appending duplicates.
    """
    def __init__(
        self,
        path: str | Path,
        *,
        deduplicate: bool = True,
        overwrite: bool = False,
        compresslevel: int = 9,
        flush_every: int = 100,
    ) -> None:
        self.path = Path(path)
        self.deduplicate = bool(deduplicate)
        self.compresslevel = max(0, min(9, int(compresslevel)))
        self.flush_every = max(1, int(flush_every))

        self.path.parent.mkdir(parents=True, exist_ok=True)

        if overwrite and self.path.exists():
            self.path.unlink()

        self._seen: set[bytes] = set()
        self._written_this_run = 0
        self._total_known = 0
        self._file = None

        if self.deduplicate and self.path.exists():
            self._load_existing_hashes()

        self._file = gzip.open(
            self.path,
            mode="at",
            encoding="utf-8",
            newline="\n",
            compresslevel=self.compresslevel,
        )

    @staticmethod
    def _normalize(fen: str) -> str:
        return fen.strip().replace("\r", "").replace("\n", "")

    @staticmethod
    def _hash(fen: str) -> bytes:
        return hashlib.blake2b(
            fen.encode("utf-8"),
            digest_size=16,
            person=b"BookForgeBalFEN",
        ).digest()

    def _load_existing_hashes(self) -> None:
        try:
            with gzip.open(
                self.path,
                mode="rt",
                encoding="utf-8",
                errors="strict",
            ) as f:
                for raw in f:
                    fen = self._normalize(raw)
                    if not fen:
                        continue
                    self._seen.add(self._hash(fen))
        except (OSError, EOFError) as exc:
            raise RuntimeError(
                f"Could not read existing balanced FEN file: {self.path}"
            ) from exc

        self._total_known = len(self._seen)

    @property
    def written_this_run(self) -> int:
        return self._written_this_run

    @property
    def total_known(self) -> int:
        if self.deduplicate:
            return len(self._seen)
        return self._total_known + self._written_this_run

    def add(self, fen: str) -> bool:
        """
        Add one FEN.

        Returns True if a new line was written, False if it was empty or already
        present with deduplication enabled.
        """
        fen = self._normalize(fen)
        if not fen:
            return False

        digest = self._hash(fen)

        if self.deduplicate and digest in self._seen:
            return False

        if self._file is None:
            raise RuntimeError("BalancedFenWriter is closed.")

        self._file.write(fen + "\n")
        self._written_this_run += 1

        if self.deduplicate:
            self._seen.add(digest)

        if self._written_this_run % self.flush_every == 0:
            self.flush()

        return True

    def flush(self) -> None:
        if self._file is not None:
            self._file.flush()

    def close(self) -> None:
        if self._file is None:
            return

        try:
            self._file.flush()
        finally:
            self._file.close()
            self._file = None

    def __enter__(self) -> "BalancedFenWriter":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
