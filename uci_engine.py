from __future__ import annotations

import os
import queue
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from book_types import BookMove

@dataclass(slots=True)
class UCIInfo:
    multipv: int
    depth: int
    seldepth: int
    score_kind: str
    score: int
    pv: list[str]
    is_bound: bool = False

class UCIEngine:
    def __init__(
        self,
        executable: str,
        options: dict[str, object] | None = None,
        multipv: int = 4,
        timeout_sec: float = 60.0,
        cwd: str | None = None,
    ) -> None:
        self.executable = str(Path(executable))
        self.options = options or {}
        self.multipv = int(multipv)
        self.timeout_sec = float(timeout_sec)
        self.cwd = cwd

        self.proc: subprocess.Popen[str] | None = None
        self._lines: queue.Queue[str | None] = queue.Queue()
        self._reader: threading.Thread | None = None
        self.name = "Unknown UCI Engine"
        self.author = ""

    def __enter__(self) -> "UCIEngine":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def start(self) -> None:
        if self.proc is not None:
            return

        creation_flags = 0

        if os.name == "nt":
            creation_flags = getattr(
                subprocess,
                "CREATE_NEW_PROCESS_GROUP",
                0x00000200,
            )

        self.proc = subprocess.Popen(
            [self.executable],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            cwd=self.cwd,
            creationflags=creation_flags,
        )

        self._reader = threading.Thread(
            target=self._read_stdout,
            name="book-uci-stdout",
            daemon=True,
        )
        self._reader.start()

        self.send("uci")
        self._wait_for_uciok()

        for name, value in self.options.items():
            self.set_option(name, value)

        self.set_option("MultiPV", self.multipv)
        self.send("isready")
        self._wait_for_exact("readyok")

    def _read_stdout(self) -> None:
        proc = self.proc
        if proc is None or proc.stdout is None:
            self._lines.put(None)
            return

        try:
            for raw in proc.stdout:
                self._lines.put(raw.rstrip("\r\n"))
        finally:
            self._lines.put(None)

    def send(self, command: str) -> None:
        proc = self.proc
        if proc is None:
            raise RuntimeError("Engine is not running.")

        if proc.poll() is not None:
            raise RuntimeError(
                f"Engine has already exited with code {proc.returncode}."
            )

        if proc.stdin is None or proc.stdin.closed:
            raise RuntimeError("Engine stdin is closed.")

        try:
            proc.stdin.write(command + "\n")
            proc.stdin.flush()
        except (OSError, BrokenPipeError, ValueError) as exc:
            raise RuntimeError(
                "Could not write to the UCI engine; it may have exited."
            ) from exc

    def _get_line(self, deadline: float) -> str:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("Timed out waiting for UCI engine output.")

        try:
            line = self._lines.get(timeout=remaining)
        except queue.Empty as exc:
            raise TimeoutError("Timed out waiting for UCI engine output.") from exc

        if line is None:
            code = self.proc.poll() if self.proc else None
            raise RuntimeError(
                f"UCI engine exited unexpectedly. Exit code: {code}"
            )

        return line

    def _wait_for_exact(self, expected: str) -> None:
        deadline = time.monotonic() + self.timeout_sec
        while True:
            line = self._get_line(deadline)
            if line.strip() == expected:
                return

    def _wait_for_uciok(self) -> None:
        deadline = time.monotonic() + self.timeout_sec

        while True:
            line = self._get_line(deadline)
            if line.startswith("id name "):
                self.name = line[8:].strip()
            elif line.startswith("id author "):
                self.author = line[10:].strip()
            elif line.strip() == "uciok":
                return

    def set_option(self, name: str, value: object | None = None) -> None:
        if value is None:
            self.send(f"setoption name {name}")
        else:
            self.send(f"setoption name {name} value {value}")

    @staticmethod
    def _parse_info(line: str) -> UCIInfo | None:
        tokens = line.split()
        if not tokens or tokens[0] != "info":
            return None

        def int_after(token: str, default: int) -> int:
            try:
                i = tokens.index(token)
                return int(tokens[i + 1])
            except (ValueError, IndexError):
                return default

        try:
            score_i = tokens.index("score")
            score_kind = tokens[score_i + 1]
            if score_kind not in ("cp", "mate"):
                return None
            score = int(tokens[score_i + 2])
        except (ValueError, IndexError):
            return None

        try:
            pv_i = tokens.index("pv")
            pv = tokens[pv_i + 1 :]
        except ValueError:
            pv = []

        if not pv:
            return None

        return UCIInfo(
            multipv=int_after("multipv", 1),
            depth=int_after("depth", 0),
            seldepth=int_after("seldepth", 0),
            score_kind=score_kind,
            score=score,
            pv=pv,
            is_bound=("lowerbound" in tokens or "upperbound" in tokens),
        )

    def _collect_analysis(
        self,
        position_command: str,
        *,
        limit_type: str,
        limit: int,
    ) -> dict[int, UCIInfo]:
        if self.proc is None:
            raise RuntimeError("Engine is not running.")

        self.send(position_command)
        self.send(f"go {limit_type} {int(limit)}")

        deadline = time.monotonic() + self.timeout_sec
        best: dict[int, UCIInfo] = {}

        while True:
            line = self._get_line(deadline)

            if line.startswith("bestmove"):
                break

            info = self._parse_info(line)
            if info is None:
                continue

            current = best.get(info.multipv)

            if (
                current is None
                or info.depth > current.depth
                or (
                    info.depth == current.depth
                    and current.is_bound
                    and not info.is_bound
                )
            ):
                best[info.multipv] = info

        return best

    @staticmethod
    def _to_book_moves(
        best: dict[int, UCIInfo],
    ) -> list[tuple[BookMove, bool]]:
        result: list[tuple[BookMove, bool]] = []
        seen_moves: set[str] = set()

        for mpv in sorted(best):
            info = best[mpv]
            move = info.pv[0]

            if move in seen_moves:
                continue
            seen_moves.add(move)

            result.append(
                (
                    BookMove(
                        move=move,
                        score_kind=info.score_kind,
                        score=info.score,
                        depth=info.depth,
                        seldepth=info.seldepth,
                        multipv=info.multipv,
                    ),
                    info.is_bound,
                )
            )

        return result

    def analyze(
        self,
        position_command: str,
        *,
        limit_type: str,
        limit: int,
    ) -> list[BookMove]:
        return [
            move
            for move, _is_bound in self.analyze_with_bounds(
                position_command,
                limit_type=limit_type,
                limit=limit,
            )
        ]

    def analyze_with_bounds(
        self,
        position_command: str,
        *,
        limit_type: str,
        limit: int,
    ) -> list[tuple[BookMove, bool]]:
        best = self._collect_analysis(
            position_command,
            limit_type=limit_type,
            limit=limit,
        )
        return self._to_book_moves(best)

    def get_current_fen(
        self,
        *,
        command: str = "getfen",
        prefix: str = "fen ",
        timeout_sec: float | None = None,
    ) -> str:
        """
        Ask the engine to serialize its CURRENT position.

        Required custom engine protocol:
            GUI -> getfen
            engine -> fen <FEN4>

        `prefix` is configurable, so an engine may instead use e.g. "fen4 ".
        """
        timeout = self.timeout_sec if timeout_sec is None else float(timeout_sec)
        deadline = time.monotonic() + timeout

        self.send(command)

        while True:
            line = self._get_line(deadline)

            if line.startswith(prefix):
                fen = line[len(prefix):].strip()
                if not fen:
                    raise RuntimeError(
                        f"Engine returned an empty FEN after {command!r}."
                    )
                return fen

            lower = line.lower()
            if "unknown command" in lower or "unrecognized command" in lower:
                raise RuntimeError(
                    f"Engine does not support the required {command!r} command."
                )

    def get_fen_for_position(
        self,
        position_command: str,
        *,
        command: str = "getfen",
        prefix: str = "fen ",
        timeout_sec: float | None = None,
    ) -> str:
        self.send(position_command)
        return self.get_current_fen(
            command=command,
            prefix=prefix,
            timeout_sec=timeout_sec,
        )

    def new_game(self) -> None:
        self.send("ucinewgame")
        self.send("isready")
        self._wait_for_exact("readyok")

    def close(self) -> None:
        """
        Windows-safe shutdown.

        Ctrl+C can invalidate the subprocess pipe before this context manager is
        finalized. Cleanup errors are therefore swallowed after attempting a
        graceful UCI quit.
        """
        proc = self.proc
        if proc is None:
            return

        self.proc = None

        try:
            if proc.poll() is None:
                try:
                    if proc.stdin is not None and not proc.stdin.closed:
                        proc.stdin.write("quit\n")
                        proc.stdin.flush()
                except (OSError, BrokenPipeError, ValueError):
                    pass

                try:
                    proc.wait(timeout=3.0)
                except subprocess.TimeoutExpired:
                    try:
                        proc.terminate()
                    except OSError:
                        pass

                    try:
                        proc.wait(timeout=2.0)
                    except subprocess.TimeoutExpired:
                        try:
                            proc.kill()
                        except OSError:
                            pass
                        try:
                            proc.wait(timeout=2.0)
                        except (subprocess.TimeoutExpired, OSError):
                            pass
        finally:
            try:
                if proc.stdin is not None:
                    proc.stdin.close()
            except (OSError, ValueError):
                pass

            try:
                if proc.stdout is not None:
                    proc.stdout.close()
            except (OSError, ValueError):
                pass
