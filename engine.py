#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

from __future__ import annotations

import re
import subprocess
import threading
from collections import deque
from typing import Optional

_SCORE_RE = re.compile(r"\bscore\s+(cp|mate)\s+([+-]?\d+)\b")
_PV_RE = re.compile(r"\bpv\s+(.+)$")
_MULTIPV_RE = re.compile(r"\bmultipv\s+(\d+)\b")
_BOUND_RE = re.compile(r"\b(?:lowerbound|upperbound)\b")

class Engine:
    """
    Thread-safe UCI/XBoard process wrapper.
    """
    def __init__(
        self,
        engine_path: str,
        *,
        verbose: bool = True,
        max_info_lines: int = 5000,
        stop_drain_timeout: float = 2.0,
    ):
        self.verbose = bool(verbose)
        self.max_info_lines = max(100, int(max_info_lines))
        self.stop_drain_timeout = max(0.1, float(stop_drain_timeout))

        self.engine = subprocess.Popen(
            [engine_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )

        if self.engine.stdin is None or self.engine.stdout is None:
            raise RuntimeError("Failed to open engine stdin/stdout pipes.")

        self.move_info = []

        self.best_move_line: Optional[str] = None
        self.ponder_hint: Optional[str] = None

        self._move_event = threading.Event()
        self._hint_event = threading.Event()
        self._engine_closed_event = threading.Event()

        self._reader_thread: Optional[threading.Thread] = None
        self._reader_started = False
        self._reader_exception: Optional[BaseException] = None

        self._state_lock = threading.RLock()
        self._write_lock = threading.Lock()
        self._reader_start_lock = threading.Lock()

        self._mate_stop_requested = False
        self._discard_bestmove_once = False
        self._search_mode: Optional[str] = None

        self._stopped_search_drained = threading.Event()
        self._stopped_search_drained.set()

        self.latest_eval: Optional[str] = None
        self.latest_score_type: Optional[str] = None
        self.latest_score_value: Optional[int] = None

    def _log_out(self, line: str) -> None:
        if self.verbose:
            print(">>", line)

    def _log_in(self, line: str) -> None:
        if self.verbose:
            print("<<", line)

    def is_alive(self) -> bool:
        return self.engine.poll() is None

    def _check_alive(self) -> None:
        code = self.engine.poll()
        if code is not None:
            raise RuntimeError(f"Engine process is not running (exit code {code}).")

    def put(self, command: str):
        """
        Send one command atomically to the engine.

        Multiple worker threads can call put(); command lines will not interleave.
        """
        if not isinstance(command, str):
            command = str(command)

        command = command.rstrip("\r\n")
        self._check_alive()

        with self._write_lock:
            self._check_alive()
            stdin = self.engine.stdin
            if stdin is None:
                raise RuntimeError("Engine stdin is closed.")

            self._log_out(command)

            try:
                stdin.write(command + "\n")
                stdin.flush()
            except (BrokenPipeError, OSError) as exc:
                self._engine_closed_event.set()
                raise RuntimeError("Failed to write to engine process.") from exc

    def start_reader(self):
        """
        Start the single stdout consumer.

        Safe to call repeatedly. Once started, no other code may call
        engine.stdout.readline() directly.
        """
        with self._reader_start_lock:
            if self._reader_started:
                return

            self._reader_started = True
            self._reader_thread = threading.Thread(
                target=self._reader_loop,
                name="engine-stdout",
                daemon=True,
            )
            self._reader_thread.start()

    def _append_info_line(self, line: str) -> None:
        with self._state_lock:
            self.move_info.append(line)

            excess = len(self.move_info) - self.max_info_lines
            if excess > 0:
                del self.move_info[:excess]

    @staticmethod
    def _multipv_number(line: str) -> int:
        match = _MULTIPV_RE.search(line)
        if not match:
            return 1
        return int(match.group(1))

    @classmethod
    def _is_primary_pv(cls, line: str) -> bool:
        return cls._multipv_number(line) == 1

    @staticmethod
    def _format_score(score_type: str, score_value: int) -> str:
        if score_type == "cp":
            return f"{score_value / 100.0:+.2f}"

        if score_value > 0:
            return f"Mate in {score_value}"
        if score_value < 0:
            return f"Mated in {abs(score_value)}"
        return "Mate"

    def _handle_info_line(self, line: str) -> None:
        """
        Track only the root/primary PV evaluation.

        MultiPV 2+ lines are useful diagnostics but must not overwrite the score
        associated with the move the engine is actually choosing.
        """
        if not self._is_primary_pv(line):
            return

        score_match = _SCORE_RE.search(line)
        if score_match:
            score_type = score_match.group(1)
            score_value = int(score_match.group(2))

            with self._state_lock:
                self.latest_score_type = score_type
                self.latest_score_value = score_value
                self.latest_eval = self._format_score(
                    score_type,
                    score_value,
                )

        self._maybe_return_forced_mate(line)

    def _maybe_return_forced_mate(self, line: str) -> None:
        """
        Return a synthetic bestmove as soon as an EXACT primary-PV mate is known.

        Do not use:
          - MultiPV 2+
          - lowerbound / upperbound mate scores
          - ponder searches

        Those can otherwise make the worker instantly play the wrong move.
        """
        if not self._is_primary_pv(line):
            return

        if _BOUND_RE.search(line):
            return

        score_match = _SCORE_RE.search(line)
        if not score_match or score_match.group(1) != "mate":
            return

        pv_match = _PV_RE.search(line)
        if not pv_match:
            return

        pv_moves = pv_match.group(1).split()
        if not pv_moves:
            return

        with self._state_lock:
            if self._search_mode != "normal":
                return
            if self._mate_stop_requested:
                return

            synthetic = "bestmove " + pv_moves[0]

            if len(pv_moves) >= 2:
                synthetic += " ponder " + pv_moves[1]
                self.ponder_hint = pv_moves[1]
                self._hint_event.set()

            self.best_move_line = synthetic
            self._mate_stop_requested = True
            self._discard_bestmove_once = True
            self._stopped_search_drained.clear()

        if self.verbose:
            print(
                "Mate score detected on primary PV - returning immediately:",
                synthetic,
            )

        try:
            self.put("stop")
        except RuntimeError:
            pass

        self._move_event.set()

    def _handle_bestmove(self, line: str) -> None:
        with self._state_lock:
            if self._discard_bestmove_once:
                self._discard_bestmove_once = False
                self._mate_stop_requested = False
                self._stopped_search_drained.set()

                if self.verbose:
                    print("Discarding stopped-search bestmove:", line)
                return

            self.best_move_line = line
            self._mate_stop_requested = False
            self._search_mode = None

            parts = line.split()
            if len(parts) >= 4 and parts[2] == "ponder":
                self.ponder_hint = parts[3]
                self._hint_event.set()

        self._move_event.set()

    def _handle_xboard_move(self, line: str) -> None:
        with self._state_lock:
            self.best_move_line = line
            self._search_mode = None
        self._move_event.set()

    def _reader_loop(self):
        try:
            stdout = self.engine.stdout
            if stdout is None:
                raise RuntimeError("Engine stdout is closed.")

            while True:
                line = stdout.readline()

                if line == "":
                    if self.verbose:
                        print(
                            "Engine closed or produced EOF "
                            f"(exit code {self.engine.poll()})"
                        )
                    break

                line = line.strip()
                if not line:
                    continue

                self._log_in(line)
                self._append_info_line(line)

                if line.startswith("info "):
                    self._handle_info_line(line)
                    continue

                if line.startswith("Hint:"):
                    with self._state_lock:
                        self.ponder_hint = line.split(":", 1)[1].strip()
                    self._hint_event.set()
                    continue

                if line.startswith("bestmove "):
                    self._handle_bestmove(line)
                    continue

                if line.startswith("move "):
                    self._handle_xboard_move(line)
                    continue

        except BaseException as exc:
            self._reader_exception = exc
            if self.verbose:
                print("Engine reader thread failed:", repr(exc))
        finally:
            self._engine_closed_event.set()
            self._move_event.set()
            self._hint_event.set()
            self._stopped_search_drained.set()

    def read_until(self, stop_token: str):
        """
        Synchronous reader for startup handshakes only.

        The existing server can keep using this BEFORE start_reader().
        """
        if self._reader_started:
            raise RuntimeError(
                "read_until() cannot be used after start_reader(); "
                "the background reader owns stdout."
            )

        output = []
        stdout = self.engine.stdout
        if stdout is None:
            raise RuntimeError("Engine stdout is closed.")

        while True:
            line = stdout.readline()

            if line == "":
                self._engine_closed_event.set()
                if self.verbose:
                    print("Engine closed or produced EOF")
                break

            line = line.strip()
            if line:
                self._log_in(line)
                output.append(line)

            if line == stop_token or line.startswith(stop_token):
                break

        return output

    def _wait_for_forced_stop_drain(self) -> None:
        """
        If an earlier mate shortcut sent `stop`, wait for that search's real
        bestmove before starting another search.

        Without this, the acknowledgement bestmove can arrive during the next
        search and accidentally consume the next search result.
        """
        with self._state_lock:
            pending = self._discard_bestmove_once

        if not pending:
            return

        if not self._stopped_search_drained.wait(self.stop_drain_timeout):
            raise TimeoutError(
                "Timed out waiting for the previous stopped search to drain."
            )

    def _reset_eval(self) -> None:
        with self._state_lock:
            self.latest_eval = None
            self.latest_score_type = None
            self.latest_score_value = None

    def clear_move_info(self):
        """
        Reset state for a brand-new normal search.

        Pending forced-stop acknowledgements are intentionally not cleared here;
        _begin_new_search() drains them first.
        """
        with self._state_lock:
            self.move_info = []
            self.best_move_line = None
            self.ponder_hint = None
            self._mate_stop_requested = False
            self.latest_eval = None
            self.latest_score_type = None
            self.latest_score_value = None

        self._move_event.clear()
        self._hint_event.clear()

    def _prepare_for_next_move(
        self,
        clear_hint: bool = True,
        *,
        clear_eval: bool = False,
    ):
        with self._state_lock:
            self.move_info = []
            self.best_move_line = None
            self._mate_stop_requested = False

            if clear_eval:
                self.latest_eval = None
                self.latest_score_type = None
                self.latest_score_value = None

            if clear_hint:
                self.ponder_hint = None

        self._move_event.clear()

        if clear_hint:
            self._hint_event.clear()

    def _begin_new_search(
        self,
        mode: str,
        *,
        clear_hint: bool = True,
    ) -> None:
        self._wait_for_forced_stop_drain()
        self._prepare_for_next_move(
            clear_hint=clear_hint,
            clear_eval=True,
        )

        with self._state_lock:
            self._search_mode = mode

    def wait_for_move(self, timeout=None):
        if not self._reader_started:
            self.start_reader()

        if not self._move_event.wait(timeout):
            return "search timeout"

        with self._state_lock:
            has_move = self.best_move_line is not None

        if has_move:
            return "search complete"

        if self._engine_closed_event.is_set():
            return "engine closed"

        return "search interrupted"

    def wait_for_hint(self, timeout=0.25):
        with self._state_lock:
            if self.ponder_hint:
                return self.ponder_hint

        self._hint_event.wait(timeout)

        with self._state_lock:
            return self.ponder_hint

    def get_eval(self):
        """Return the latest formatted PRIMARY-PV evaluation."""
        with self._state_lock:
            return self.latest_eval

    def get_score(self):
        """
        Return raw score information as (type, value), e.g. ("cp", 34).
        """
        with self._state_lock:
            return self.latest_score_type, self.latest_score_value

    def get_move_info(self):
        """Return a thread-safe snapshot of recent engine output."""
        with self._state_lock:
            return list(self.move_info)

    def get(self):
        return self.wait_for_move()

    def search_fen_str_with_clocks(
        self,
        fen: str,
        clocks: dict,
        increments: dict,
        delays: dict = None,
        timeout=None,
    ):
        if delays is None:
            delays = {c: 0 for c in ("r", "b", "y", "g")}

        self._begin_new_search("normal")

        self.put("position fen " + fen)

        go_cmd = (
            "go depth 64"
            " clocks {rtime} {btime} {ytime} {gtime}"
            " incs {rinc} {binc} {yinc} {ginc}"
        ).format(
            rtime=clocks.get("r", 60000),
            btime=clocks.get("b", 60000),
            ytime=clocks.get("y", 60000),
            gtime=clocks.get("g", 60000),
            rinc=increments.get("r", 0),
            binc=increments.get("b", 0),
            yinc=increments.get("y", 0),
            ginc=increments.get("g", 0),
        )

        self.put(go_cmd)
        return self.wait_for_move(timeout)

    def search_fen_str(
        self,
        fen: str,
        time_allowed: str,
        uci_allowed=True,
        timeout=None,
    ):
        self._begin_new_search("normal")

        if uci_allowed:
            self.put("position fen " + fen)
            self.put("go movetime " + str(time_allowed))
        else:
            self.put("post")
            self.put("setboard " + fen)
            self.put("st " + str(time_allowed))
            self.put("go")

        return self.wait_for_move(timeout)

    def start_ponder(
        self,
        fen: str,
        moves: str,
        ponder_move: str = None,
    ):
        self._begin_new_search("ponder", clear_hint=True)
        self.put("position fen " + fen + " moves " + moves)
        self.put("go ponder")

    def ponder_hit(self, timeout=None):
        self._prepare_for_next_move(clear_hint=False, clear_eval=False)

        with self._state_lock:
            self._search_mode = "normal"

        self.put("ponderhit")
        return self.wait_for_move(timeout)

    def xboard_ponder_hit(self, opponent_move: str, timeout=None):
        self._prepare_for_next_move(clear_hint=True, clear_eval=False)

        with self._state_lock:
            self._search_mode = "normal"

        self.put(opponent_move)
        return self.wait_for_move(timeout)

    def stop(self, uci_allowed=True, timeout=1.0):
        """
        Stop the active search and reset move/ponder state.

        This remains compatible with the old server, but handles an engine that
        exits during stop without hanging indefinitely.
        """
        if not self.is_alive():
            self._prepare_for_next_move(clear_hint=True, clear_eval=False)
            return

        if uci_allowed:
            self._move_event.clear()

            with self._state_lock:
                self.best_move_line = None

            try:
                self.put("stop")
            except RuntimeError:
                pass

            self._move_event.wait(timeout)
        else:
            try:
                self.put("force")
            except RuntimeError:
                pass

        self._prepare_for_next_move(clear_hint=True, clear_eval=False)

        with self._state_lock:
            self._search_mode = None

    def quit(self, timeout=2.0):
        """
        Shut down cleanly.

        UCI quit is attempted first. If the engine ignores it, terminate(), then
        kill() is used as a final fallback.
        """
        if self.engine.poll() is not None:
            return

        try:
            self.put("quit")
        except RuntimeError:
            pass

        try:
            self.engine.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            self.engine.terminate()

            try:
                self.engine.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                self.engine.kill()
                self.engine.wait(timeout=1.0)
        finally:
            self._engine_closed_event.set()
            self._move_event.set()
            self._hint_event.set()
            self._stopped_search_drained.set()

    close = quit

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.quit()
