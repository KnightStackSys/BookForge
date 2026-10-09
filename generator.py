from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import queue
import threading
import time
import traceback
from dataclasses import dataclass
from pathlib import Path

from book_db import BookDB, position_key
from book_types import BookMove
from uci_engine import UCIEngine

def log(message: str = "") -> None:
    print(message, flush=True)

def load_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def canonical_root(root_cfg: dict) -> str:
    kind = root_cfg.get("type", "startpos").lower()

    if kind == "startpos":
        return "startpos"

    if kind == "fen":
        fen = root_cfg.get("fen")
        if not fen:
            raise ValueError(
                "book.root.fen is required when root.type='fen'."
            )
        return f"fen {fen}"

    raise ValueError(
        "book.root.type must be 'startpos' or 'fen'."
    )

def make_position_command(
    root_spec: str,
    moves: tuple[str, ...],
) -> str:
    cmd = f"position {root_spec}"

    if moves:
        cmd += " moves " + " ".join(moves)

    return cmd

def normalize_analysis_config(
    analysis_cfg: dict,
) -> tuple[str, int]:
    """
    Normalize the analysis limit.

    Preferred modern form:
        "analysis": {
            "multipv": 6,
            "depth": 10
        }

    Legacy form remains supported:
        "limit_type": "depth",
        "limit": 10

    If `depth` is present, it takes precedence.
    """
    if "depth" in analysis_cfg:
        depth = int(analysis_cfg["depth"])

        if depth < 1:
            raise ValueError(
                "analysis.depth must be at least 1."
            )

        analysis_cfg["limit_type"] = "depth"
        analysis_cfg["limit"] = depth

        return "depth", depth

    limit_type = str(
        analysis_cfg.get(
            "limit_type",
            "depth",
        )
    ).lower()

    limit = int(
        analysis_cfg.get(
            "limit",
            10,
        )
    )

    if limit < 1:
        raise ValueError(
            "analysis.limit must be at least 1."
        )

    analysis_cfg["limit_type"] = limit_type
    analysis_cfg["limit"] = limit

    if limit_type == "depth":
        analysis_cfg["depth"] = limit

    return limit_type, limit

def generation_profile(
    config: dict,
    root_spec: str,
) -> dict:
    """
    Settings that affect the actual stored move/evaluation data.

    These are intentionally NOT included:
      - parallel worker count
      - debug options
      - output filename
      - max_positions
      - commit frequency
      - vacuum setting
      - max_book_depth
      - engine executable path / cwd / timeout
      - analysis depth / nodes / time limit

    Therefore you can enable more workers, change logging, adjust search
    effort, or extend the
    book deeper without invalidating an existing compatible .nbook.
    """
    engine_cfg = config["engine"]
    analysis_cfg = config["analysis"]
    book_cfg = config["book"]

    return {
        "root_spec": root_spec,
        "engine_options": engine_cfg.get("options", {}),
        "multipv": int(analysis_cfg["multipv"]),
        "min_eval_pawns": float(
            book_cfg["min_eval_pawns"]
        ),
        "max_eval_pawns": float(
            book_cfg["max_eval_pawns"]
        ),
        "include_forced_mates": bool(
            book_cfg.get(
                "include_forced_mates",
                True,
            )
        ),
        "include_losing_mates": bool(
            book_cfg.get(
                "include_losing_mates",
                False,
            )
        ),
        "max_children_per_position": int(
            book_cfg.get(
                "max_children_per_position",
                analysis_cfg["multipv"],
            )
        ),
        "reject_bound_scores": bool(
            book_cfg.get(
                "reject_bound_scores",
                True,
            )
        ),
        "score_perspective": str(
            book_cfg.get(
                "score_perspective",
                "side_to_move_team",
            )
        ),
        "cp_per_pawn": int(
            book_cfg.get(
                "cp_per_pawn",
                100,
            )
        ),
    }

def generation_signature(
    config: dict,
    root_spec: str,
) -> str:
    profile = generation_profile(
        config,
        root_spec,
    )

    raw = json.dumps(
        profile,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()

    return hashlib.sha256(raw).hexdigest()

def _legacy_generation_profile(
    stored_config: dict,
    stored_root_spec: str,
) -> dict:
    return generation_profile(
        stored_config,
        stored_root_spec,
    )

def _profile_differences(
    old: dict,
    new: dict,
) -> list[tuple[str, object, object]]:
    keys = sorted(
        set(old) | set(new)
    )

    diffs: list[
        tuple[str, object, object]
    ] = []

    for key in keys:
        old_value = old.get(
            key,
            "<missing>",
        )
        new_value = new.get(
            key,
            "<missing>",
        )

        if old_value != new_value:
            diffs.append(
                (
                    key,
                    old_value,
                    new_value,
                )
            )

    return diffs

def _format_profile_differences(
    diffs: list[
        tuple[str, object, object]
    ],
) -> str:
    return "\n".join(
        f"  {key}: existing={old!r} -> current={new!r}"
        for key, old, new in diffs
    )

def filter_lines(
    analyzed: list[
        tuple[BookMove, bool]
    ],
    *,
    min_cp: int,
    max_cp: int,
    include_forced_mates: bool,
    include_losing_mates: bool,
    reject_bound_scores: bool,
    max_children: int,
) -> list[BookMove]:
    result: list[BookMove] = []

    for move, is_bound in analyzed:
        if (
            reject_bound_scores
            and is_bound
        ):
            continue

        if move.score_kind == "mate":
            if not include_forced_mates:
                continue

            if (
                move.score < 0
                and not include_losing_mates
            ):
                continue

            result.append(move)

        elif min_cp <= move.score <= max_cp:
            result.append(move)

        if len(result) >= max_children:
            break

    return result

@dataclass(frozen=True, slots=True)
class AnalysisTask:
    moves: tuple[str, ...]
    ply: int
    key: bytes
    position_command: str


@dataclass(slots=True)
class AnalysisResult:
    worker_id: int
    task: AnalysisTask
    analyzed: (
        list[tuple[BookMove, bool]]
        | None
    )
    error: BaseException | None = None

class ParallelAnalyzer:
    """
    One Python coordinator controlling N independent BookForge processes.

    Worker threads only communicate with their own UCI process.
    SQLite is NEVER touched by worker threads; generator.py's main thread is
    the only book writer.
    """
    def __init__(
        self,
        *,
        engine_cfg: dict,
        analysis_cfg: dict,
        multipv: int,
        workers: int,
    ) -> None:
        self.engine_cfg = engine_cfg
        self.analysis_cfg = analysis_cfg
        self.multipv = int(multipv)
        self.workers = max(
            1,
            int(workers),
        )

        self._task_queue: queue.Queue[
            AnalysisTask | None
        ] = queue.Queue()

        self._result_queue: queue.Queue[
            AnalysisResult
        ] = queue.Queue()

        self._ready_queue: queue.Queue[
            tuple[
                int,
                str,
                str,
                BaseException | None,
            ]
        ] = queue.Queue()

        self._threads: list[
            threading.Thread
        ] = []

        self.engine_name = ""
        self.engine_author = ""

        self._started = False
        self._closed = False

    def __enter__(
        self,
    ) -> "ParallelAnalyzer":
        self.start()
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:
        self.close()

    def start(self) -> None:
        if self._started:
            return

        self._started = True

        for worker_id in range(
            1,
            self.workers + 1,
        ):
            thread = threading.Thread(
                target=self._worker_loop,
                args=(worker_id,),
                name=f"book-worker-{worker_id}",
                daemon=True,
            )

            self._threads.append(thread)
            thread.start()

        startup_errors: list[
            tuple[int, BaseException]
        ] = []

        names: list[str] = []
        authors: list[str] = []

        for _ in range(self.workers):
            (
                worker_id,
                name,
                author,
                error,
            ) = self._ready_queue.get()

            if error is not None:
                startup_errors.append(
                    (worker_id, error)
                )
            else:
                names.append(name)
                authors.append(author)

        if startup_errors:
            self.close()

            details = "\n".join(
                f"  worker {worker_id}: {error}"
                for worker_id, error
                in startup_errors
            )

            raise RuntimeError(
                "One or more UCI workers failed to start:\n"
                + details
            )

        if names:
            self.engine_name = names[0]

        if authors:
            self.engine_author = authors[0]

    def _worker_loop(
        self,
        worker_id: int,
    ) -> None:
        engine: UCIEngine | None = None

        try:
            engine = UCIEngine(
                executable=self.engine_cfg["path"],
                options=self.engine_cfg.get(
                    "options",
                    {},
                ),
                multipv=self.multipv,
                timeout_sec=float(
                    self.engine_cfg.get(
                        "timeout_sec",
                        120,
                    )
                ),
                cwd=self.engine_cfg.get(
                    "cwd"
                ),
            )

            engine.start()

            self._ready_queue.put(
                (
                    worker_id,
                    engine.name,
                    engine.author,
                    None,
                )
            )

        except BaseException as exc:
            self._ready_queue.put(
                (
                    worker_id,
                    "",
                    "",
                    exc,
                )
            )
            return

        try:
            while True:
                task = self._task_queue.get()

                if task is None:
                    return

                try:
                    analyzed = (
                        engine.analyze_with_bounds(
                            task.position_command,
                            limit_type=self.analysis_cfg[
                                "limit_type"
                            ],
                            limit=int(
                                self.analysis_cfg[
                                    "limit"
                                ]
                            ),
                        )
                    )

                    self._result_queue.put(
                        AnalysisResult(
                            worker_id=worker_id,
                            task=task,
                            analyzed=analyzed,
                        )
                    )

                except BaseException as exc:
                    self._result_queue.put(
                        AnalysisResult(
                            worker_id=worker_id,
                            task=task,
                            analyzed=None,
                            error=exc,
                        )
                    )

        finally:
            if engine is not None:
                engine.close()

    def submit(
        self,
        task: AnalysisTask,
    ) -> None:
        if not self._started:
            self.start()

        if self._closed:
            raise RuntimeError(
                "ParallelAnalyzer is closed."
            )

        self._task_queue.put(task)

    def get_result(
        self,
        timeout: float | None = None,
    ) -> AnalysisResult:
        return self._result_queue.get(
            timeout=timeout
        )

    def analyze_batch(
        self,
        tasks: list[AnalysisTask],
    ) -> tuple[
        list[AnalysisResult],
        bool,
    ]:
        """
        Submit at most one task per worker and wait for that batch.

        Ctrl+C stops NEW work immediately, but the positions already being
        analyzed are allowed to finish so their results can be safely saved.
        """
        if not tasks:
            return [], False

        if len(tasks) > self.workers:
            raise ValueError(
                "analyze_batch() received more tasks "
                "than available workers."
            )

        for task in tasks:
            self.submit(task)

        results: list[
            AnalysisResult
        ] = []

        interrupted = False
        remaining = len(tasks)

        while remaining:
            try:
                result = self.get_result(
                    timeout=0.20
                )

            except queue.Empty:
                continue

            except KeyboardInterrupt:
                if not interrupted:
                    print(
                        "\nStop requested. "
                        "No new positions will be started."
                    )
                    print(
                        "Waiting for the current worker batch "
                        "to finish so completed results can be saved..."
                    )

                interrupted = True
                continue

            results.append(result)
            remaining -= 1

        return results, interrupted

    def close(self) -> None:
        if self._closed:
            return

        self._closed = True

        for _ in self._threads:
            self._task_queue.put(None)

        for thread in self._threads:
            while thread.is_alive():
                try:
                    thread.join(timeout=0.20)
                except KeyboardInterrupt:
                    continue

def prepare_book(
    db: BookDB,
    config: dict,
    root_spec: str,
    engine_name: str,
    engine_author: str,
    overwrite: bool,
) -> None:
    book_cfg = config["book"]

    current_profile = (
        generation_profile(
            config,
            root_spec,
        )
    )

    signature = (
        generation_signature(
            config,
            root_spec,
        )
    )

    if overwrite:
        db.clear()
    else:
        db.create_schema()

    existing_count = (
        db.count_positions()
    )

    if (
        existing_count > 0
        and not overwrite
    ):
        stored_root = (
            db.get_meta(
                "root_spec",
                root_spec,
            )
            or root_spec
        )

        if stored_root != root_spec:
            raise RuntimeError(
                "Existing book uses a different root position.\n"
                f"  existing root: {stored_root}\n"
                f"  current root:  {root_spec}\n"
                "Use the original root or --overwrite."
            )

        stored_config_json = (
            db.get_meta(
                "config_json"
            )
        )

        if stored_config_json:
            try:
                stored_config = json.loads(
                    stored_config_json
                )

                old_profile = (
                    _legacy_generation_profile(
                        stored_config,
                        stored_root,
                    )
                )

            except Exception as exc:
                raise RuntimeError(
                    "Existing book contains config metadata, "
                    "but it could not be interpreted safely."
                ) from exc

            diffs = (
                _profile_differences(
                    old_profile,
                    current_profile,
                )
            )

            if diffs:
                raise RuntimeError(
                    "Existing book was generated with settings "
                    "that change stored move/evaluation data:\n"
                    + _format_profile_differences(
                        diffs
                    )
                    + "\n\n"
                    "Safe changes such as search depth, parallel.workers, "
                    "debug settings, max_book_depth, max_positions, "
                    "commit_every, and vacuum_when_done are allowed.\n"
                    "Restore the listed settings or use --overwrite."
                )

            existing_sig = (
                db.get_meta(
                    "generation_signature"
                )
            )

            if existing_sig != signature:
                print(
                    "*** Existing book metadata is compatible "
                    "with this generator."
                )
                print(
                    "*** Migrating generation signature without "
                    "rebuilding stored positions."
                )

        else:
            existing_sig = (
                db.get_meta(
                    "generation_signature"
                )
            )

            if (
                existing_sig
                and existing_sig != signature
            ):
                raise RuntimeError(
                    "Existing book uses legacy metadata and "
                    "does not contain config_json, so compatibility "
                    "cannot be verified automatically."
                )

    db.set_meta(
        "generation_signature",
        signature,
    )

    db.set_meta(
        "generation_profile_json",
        json.dumps(
            current_profile,
            sort_keys=True,
        ),
    )

    db.set_meta(
        "root_spec",
        root_spec,
    )

    db.set_meta(
        "engine_name",
        engine_name,
    )

    db.set_meta(
        "engine_author",
        engine_author,
    )

    db.set_meta(
        "score_perspective",
        book_cfg.get(
            "score_perspective",
            "side_to_move_team",
        ),
    )

    db.set_meta(
        "config_json",
        json.dumps(
            config,
            sort_keys=True,
        ),
    )

    db.commit()

def debug_position_save(
    *,
    enabled: bool,
    show_history: bool,
    show_analyzed_moves: bool,
    save_number: int,
    worker_id: int,
    key: bytes,
    ply: int,
    max_book_depth: int,
    moves: tuple[str, ...],
    analyzed: list[
        tuple[BookMove, bool]
    ],
    stored: list[BookMove],
) -> None:
    if not enabled:
        return

    print(
        f"[BOOK SAVE #{save_number:,}] "
        f"worker={worker_id} "
        f"ply={ply}/{max_book_depth} "
        f"key={key.hex()} "
        f"stored_moves={len(stored)}"
    )

    if show_history:
        history = (
            " ".join(moves)
            if moves
            else "(root)"
        )

        print(
            f"  history: {history}"
        )

    if stored:
        print("  saved:")

        for index, entry in enumerate(
            stored,
            start=1,
        ):
            print(
                f"    {index:>2}. "
                f"{entry.move:<10} "
                f"eval={entry.display_score():>9} "
                f"depth={entry.depth:<3} "
                f"seldepth={entry.seldepth:<3} "
                f"multipv={entry.multipv}"
            )

    else:
        print(
            "  saved: "
            "(no moves passed the book filters; leaf position)"
        )

    if show_analyzed_moves:
        stored_names = {
            entry.move
            for entry in stored
        }

        print("  analyzed:")

        for entry, is_bound in analyzed:
            result = (
                "KEEP"
                if entry.move in stored_names
                else "DROP"
            )

            bound = (
                " bound"
                if is_bound
                else ""
            )

            print(
                f"    [{result}] "
                f"mpv={entry.multipv:<2} "
                f"{entry.move:<10} "
                f"eval={entry.display_score():>9} "
                f"depth={entry.depth:<3} "
                f"seldepth={entry.seldepth:<3}"
                f"{bound}"
            )

    print()

def _add_children(
    *,
    parent_moves: tuple[str, ...],
    stored: list[BookMove],
    next_frontier: list[
        tuple[str, ...]
    ],
    queued: set[bytes],
    root_spec: str,
) -> None:
    for entry in stored:
        child_moves = (
            parent_moves
            + (entry.move,)
        )

        child_key = position_key(
            root_spec,
            child_moves,
        )

        if child_key in queued:
            continue

        queued.add(child_key)
        next_frontier.append(
            child_moves
        )

def generate(
    config_path: str,
    overwrite: bool = False,
    search_depth: int | None = None,
    book_depth: int | None = None,
) -> None:
    config_path_obj = Path(config_path).resolve()

    log("=== BookForge Opening Book Generator ===")
    log(f"Python: {sys.executable}")
    log(f"Implementation: {sys.implementation.name}")
    log(f"Version: {sys.version.split()[0]}")
    log(f"Config: {config_path_obj}")
    log(f"Overwrite: {'YES' if overwrite else 'NO'}")

    if not config_path_obj.exists():
        raise FileNotFoundError(
            f"Config file does not exist: {config_path_obj}"
        )

    config = load_config(
        config_path_obj
    )

    engine_cfg = config["engine"]
    analysis_cfg = config["analysis"]
    book_cfg = config["book"]

    if search_depth is not None:
        if search_depth < 1:
            raise ValueError(
                "--depth must be at least 1."
            )

        analysis_cfg["depth"] = int(search_depth)

    if book_depth is not None:
        if book_depth < 1:
            raise ValueError(
                "--book-depth must be at least 1."
            )

        book_cfg["max_book_depth"] = int(book_depth)

    analysis_limit_type, analysis_limit = (
        normalize_analysis_config(
            analysis_cfg
        )
    )
    parallel_cfg = config.get(
        "parallel",
        {},
    )
    debug_cfg = config.get(
        "debug",
        {},
    )

    debug_position_saves = bool(
        debug_cfg.get(
            "position_saves",
            False,
        )
    )

    debug_show_history = bool(
        debug_cfg.get(
            "show_history",
            True,
        )
    )

    debug_show_analyzed_moves = bool(
        debug_cfg.get(
            "show_analyzed_moves",
            False,
        )
    )

    parallel_enabled = bool(
        parallel_cfg.get(
            "enabled",
            True,
        )
    )

    worker_count = (
        int(
            parallel_cfg.get(
                "workers",
                1,
            )
        )
        if parallel_enabled
        else 1
    )

    if worker_count < 1:
        raise ValueError(
            "parallel.workers must be at least 1."
        )

    perspective = book_cfg.get(
        "score_perspective",
        "side_to_move_team",
    )

    if perspective not in (
        "side_to_move_team",
        "root_team",
    ):
        raise ValueError(
            "Rated selection requires scores that are "
            "higher-is-better for the team whose position "
            "is being analyzed."
        )

    multipv = int(
        analysis_cfg["multipv"]
    )

    max_children = int(
        book_cfg.get(
            "max_children_per_position",
            multipv,
        )
    )

    if (
        max_children < 1
        or max_children > multipv
    ):
        raise ValueError(
            "book.max_children_per_position must be between "
            "1 and analysis.multipv."
        )

    min_eval = float(
        book_cfg["min_eval_pawns"]
    )

    max_eval = float(
        book_cfg["max_eval_pawns"]
    )

    if min_eval > max_eval:
        raise ValueError(
            "book.min_eval_pawns cannot exceed "
            "max_eval_pawns."
        )

    cp_per_pawn = int(
        book_cfg.get(
            "cp_per_pawn",
            100,
        )
    )

    min_cp = round(
        min_eval
        * cp_per_pawn
    )

    max_cp = round(
        max_eval
        * cp_per_pawn
    )

    max_book_depth = int(
        book_cfg["max_book_depth"]
    )

    max_positions = int(
        book_cfg.get(
            "max_positions",
            0,
        )
    )

    commit_every = max(
        1,
        int(
            book_cfg.get(
                "commit_every",
                500,
            )
        ),
    )

    root_spec = canonical_root(
        book_cfg.get(
            "root",
            {
                "type": "startpos"
            },
        )
    )

    output = Path(
        book_cfg["output"]
    )

    output = output.resolve()

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    log(f"Book file: {output}")
    log(f"Engine: {Path(engine_cfg['path']).resolve()}")
    log(
        f"Search: {analysis_limit_type} {analysis_limit} | "
        f"book depth {max_book_depth} | "
        f"MultiPV {multipv}"
    )
    log(f"Workers requested: {worker_count}")

    options = engine_cfg.get(
        "options",
        {},
    )

    engine_threads = int(
        options.get(
            "Threads",
            1,
        )
    )

    engine_hash_mb = int(
        options.get(
            "Hash",
            0,
        )
    )

    total_engine_threads = (
        worker_count
        * engine_threads
    )

    total_hash_mb = (
        worker_count
        * engine_hash_mb
    )

    logical_cpus = (
        os.cpu_count()
        or 1
    )

    frontier: list[
        tuple[str, ...]
    ] = [
        tuple()
    ]

    queued: set[bytes] = {
        position_key(
            root_spec,
            tuple(),
        )
    }

    newly_analyzed = 0
    visited = 0
    interrupted = False
    started_at = time.monotonic()

    log("Opening book database...")

    with BookDB(output) as db:
        if overwrite:
            log("Clearing existing book...")
            db.clear()
            log("Existing book cleared.")

        log(
            f"Starting {worker_count} BookForge worker"
            f"{'s' if worker_count != 1 else ''}..."
        )

        with ParallelAnalyzer(
            engine_cfg=engine_cfg,
            analysis_cfg=analysis_cfg,
            multipv=multipv,
            workers=worker_count,
        ) as analyzer:

            log("All BookForge workers are ready.")

            prepare_book(
                db,
                config,
                root_spec,
                analyzer.engine_name,
                analyzer.engine_author,
                False,
            )

            log(
                f"Engine: {analyzer.engine_name}"
            )

            log(
                f"Book:   {output}"
            )

            log(
                f"Filter: "
                f"{min_eval:+.2f} .. "
                f"{max_eval:+.2f} pawns "
                f"({min_cp:+d} .. "
                f"{max_cp:+d} cp)"
            )

            if analysis_limit_type == "depth":
                log(
                    f"Search depth: {analysis_limit} | "
                    f"Book depth: {max_book_depth} plies | "
                    f"MultiPV: {multipv} | "
                    f"max children: {max_children}"
                )
            else:
                log(
                    f"Search limit: {analysis_limit_type} "
                    f"{analysis_limit} | "
                    f"Book depth: {max_book_depth} plies | "
                    f"MultiPV: {multipv} | "
                    f"max children: {max_children}"
                )

            log(
                f"Parallel workers: {worker_count} | "
                f"BookForge Threads/worker: {engine_threads} | "
                f"estimated engine threads: {total_engine_threads}"
            )

            if engine_hash_mb:
                log(
                    f"Hash/worker: {engine_hash_mb} MB | "
                    f"estimated total hash: {total_hash_mb} MB"
                )

            if total_engine_threads > logical_cpus:
                log(
                    "*** WARNING: configured engine threads "
                    f"({total_engine_threads}) exceed detected logical CPUs "
                    f"({logical_cpus}). This may reduce performance."
                )

            if debug_position_saves:
                print(
                    "Debug position saves: ON"
                    + (
                        " | showing analyzed/filtered moves"
                        if debug_show_analyzed_moves
                        else ""
                    )
                )

            current_ply = 0

            while (
                frontier
                and current_ply < max_book_depth
            ):
                log(
                    f"*** Generating book depth "
                    f"{current_ply} / "
                    f"{max_book_depth} | "
                    f"frontier={len(frontier):,}"
                )

                next_frontier: list[
                    tuple[str, ...]
                ] = []

                pending: list[
                    AnalysisTask
                ] = []

                for moves in frontier:
                    key = position_key(
                        root_spec,
                        moves,
                    )

                    visited += 1

                    stored = db.get_moves(
                        key
                    )

                    if stored is not None:
                        _add_children(
                            parent_moves=moves,
                            stored=stored,
                            next_frontier=next_frontier,
                            queued=queued,
                            root_spec=root_spec,
                        )
                        continue

                    pending.append(
                        AnalysisTask(
                            moves=moves,
                            ply=current_ply,
                            key=key,
                            position_command=make_position_command(
                                root_spec,
                                moves,
                            ),
                        )
                    )

                pending_index = 0

                while pending_index < len(
                    pending
                ):
                    if max_positions:
                        remaining_capacity = (
                            max_positions
                            - db.count_positions()
                        )

                        if remaining_capacity <= 0:
                            print(
                                f"Reached max_positions="
                                f"{max_positions} at book "
                                f"depth {current_ply}/"
                                f"{max_book_depth}; "
                                "stopping cleanly."
                            )

                            interrupted = True
                            break

                    else:
                        remaining_capacity = (
                            worker_count
                        )

                    batch_size = min(
                        worker_count,
                        len(pending)
                        - pending_index,
                        remaining_capacity,
                    )

                    if batch_size <= 0:
                        interrupted = True
                        break

                    batch = pending[
                        pending_index:
                        pending_index
                        + batch_size
                    ]

                    results, stop_requested = (
                        analyzer.analyze_batch(
                            batch
                        )
                    )

                    pending_index += (
                        batch_size
                    )

                    interrupted_worker_failures = 0

                    for result in results:
                        if result.error is not None:
                            if stop_requested:
                                interrupted_worker_failures += 1

                                print(
                                    f"[W{result.worker_id}] "
                                    "Interrupted position was not saved: "
                                    f"ply {result.task.ply} "
                                    f"{' '.join(result.task.moves) or '(root)'}",
                                    flush=True,
                                )
                                continue

                            raise RuntimeError(
                                f"Worker {result.worker_id} "
                                "failed while analyzing "
                                f"ply {result.task.ply} "
                                f"history "
                                f"{' '.join(result.task.moves) or '(root)'}"
                            ) from result.error

                        analyzed = (
                            result.analyzed
                            or []
                        )

                        stored = filter_lines(
                            analyzed,
                            min_cp=min_cp,
                            max_cp=max_cp,
                            include_forced_mates=bool(
                                book_cfg.get(
                                    "include_forced_mates",
                                    True,
                                )
                            ),
                            include_losing_mates=bool(
                                book_cfg.get(
                                    "include_losing_mates",
                                    False,
                                )
                            ),
                            reject_bound_scores=bool(
                                book_cfg.get(
                                    "reject_bound_scores",
                                    True,
                                )
                            ),
                            max_children=max_children,
                        )

                        db.put_moves(
                            result.task.key,
                            result.task.ply,
                            stored,
                        )

                        newly_analyzed += 1

                        debug_position_save(
                            enabled=debug_position_saves,
                            show_history=debug_show_history,
                            show_analyzed_moves=debug_show_analyzed_moves,
                            save_number=newly_analyzed,
                            worker_id=result.worker_id,
                            key=result.task.key,
                            ply=result.task.ply,
                            max_book_depth=max_book_depth,
                            moves=result.task.moves,
                            analyzed=analyzed,
                            stored=stored,
                        )

                        _add_children(
                            parent_moves=result.task.moves,
                            stored=stored,
                            next_frontier=next_frontier,
                            queued=queued,
                            root_spec=root_spec,
                        )

                        if (
                            newly_analyzed
                            % commit_every
                            == 0
                        ):
                            db.commit()

                            elapsed = max(
                                0.001,
                                time.monotonic()
                                - started_at,
                            )

                            speed = (
                                newly_analyzed
                                / elapsed
                            )

                            pending_left = (
                                len(pending)
                                - pending_index
                            )

                            print(
                                f"Analyzed "
                                f"{newly_analyzed:,} "
                                f"new positions | "
                                f"depth "
                                f"{current_ply}/"
                                f"{max_book_depth} | "
                                f"DB total "
                                f"{db.count_positions():,} | "
                                f"pending this depth "
                                f"{pending_left:,} | "
                                f"next frontier "
                                f"{len(next_frontier):,} | "
                                f"{speed:.2f} pos/s"
                            )

                    if stop_requested:
                        db.commit()

                        if interrupted_worker_failures:
                            print(
                                f"Skipped {interrupted_worker_failures} "
                                "interrupted position"
                                f"{'s' if interrupted_worker_failures != 1 else ''}; "
                                "they will be retried when generation resumes.",
                                flush=True,
                            )

                        print(
                            "Completed results from the interrupted batch "
                            "have been saved.",
                            flush=True,
                        )

                        interrupted = True
                        break

                db.commit()

                if interrupted:
                    break

                frontier = (
                    next_frontier
                )

                current_ply += 1

            total = (
                db.count_positions()
            )

            size_mb = (
                output.stat().st_size
                / (1024 * 1024)
            )

            if interrupted:
                print(
                    "\nStop requested. "
                    "Saving completed book positions..."
                )

                db.commit()

                print(
                    f"Stopped safely. "
                    f"{total:,} positions are saved "
                    f"({newly_analyzed:,} newly analyzed "
                    f"this run), "
                    f"{size_mb:.2f} MiB."
                )

                print(
                    "Run the same command again to resume generation. "
                    "Do NOT use --overwrite when resuming."
                )

                return

            if bool(
                book_cfg.get(
                    "vacuum_when_done",
                    True,
                )
            ):
                db.vacuum()

                size_mb = (
                    output.stat().st_size
                    / (1024 * 1024)
                )

            elapsed = max(
                0.001,
                time.monotonic()
                - started_at,
            )

            speed = (
                newly_analyzed
                / elapsed
                if newly_analyzed
                else 0.0
            )

            print(
                f"Done. "
                f"{total:,} book positions, "
                f"{newly_analyzed:,} newly analyzed, "
                f"{size_mb:.2f} MiB, "
                f"{speed:.2f} positions/sec."
            )

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a compressed BookForge 4PC "
            "MultiPV opening book using one or more "
            "parallel BookForge workers."
        )
    )

    parser.add_argument(
        "config",
        nargs="?",
        default="config.json",
        help="Path to config.json",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Delete/rebuild the existing "
            ".nbook."
        ),
    )

    parser.add_argument(
        "--depth",
        "--search-depth",
        dest="search_depth",
        type=int,
        default=None,
        help=(
            "Override the engine search depth for this run. "
            "Example: --depth 12"
        ),
    )

    parser.add_argument(
        "--book-depth",
        type=int,
        default=None,
        help=(
            "Override the maximum opening-book ply depth for this run. "
            "Example: --book-depth 28"
        ),
    )

    args = parser.parse_args()

    generate(
        args.config,
        overwrite=args.overwrite,
        search_depth=args.search_depth,
        book_depth=args.book_depth,
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\nInterrupted.")
        raise SystemExit(130)
    except Exception:
        print(
            "\n*** BookForge generator failed ***",
            file=sys.stderr,
            flush=True,
        )
        traceback.print_exc()
        sys.stderr.flush()
        raise SystemExit(1)
