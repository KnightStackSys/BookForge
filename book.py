#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

"""
Runtime adapter between the existing BookForge worker and the compressed
BookForge/BookForge .nbook opening-book reader.

The generator keys positions by exact UCI move history. The Chess.com worker
may receive coordinate SAN-ish forms such as h2-h3 or Bi1xc7, so this module
normalizes those tokens before probing the book.
"""

from __future__ import annotations

import re
from pathlib import Path
from time import sleep
from typing import Iterable

from book_types import BookMove
from reader import OpeningBook

_COORD_MOVE_RE = re.compile(
    r"([a-n](?:[1-9]|1[0-4]))"
    r"([a-n](?:[1-9]|1[0-4]))"
    r"([qrbnQRBN]?)"
)

def normalize_move(token: str) -> str | None:
    """
    Convert UCI or coordinate-SAN-ish 4PC notation to compact UCI.

    Examples:
        h2-h3      -> h2h3
        Bi1xc7     -> i1c7
        g13-g11    -> g13g11
        a13-a14=Q  -> a13a14q
        h2h3       -> h2h3

    Plain SAN without a source square cannot be converted safely and returns
    None. In that case the worker simply falls back to engine search.
    """
    if token is None:
        return None

    token = str(token).strip()
    token = re.sub(r"^\d+\.(?:\.\.)?", "", token)
    token = token.strip(". ")

    if not token:
        return None

    token = re.sub(r"[+#?!]+$", "", token)

    if token and token[0] in "KQRBN":
        token = token[1:]

    token = token.replace("x", "")
    token = token.replace("-", "")
    token = token.replace("=", "")

    match = _COORD_MOVE_RE.fullmatch(token)
    if not match:
        return None

    return (
        match.group(1)
        + match.group(2)
        + match.group(3).lower()
    )

def normalize_history(history: str | Iterable[str]) -> list[str] | None:
    if isinstance(history, str):
        tokens = history.split()
    else:
        tokens = list(history)

    normalized: list[str] = []

    for token in tokens:
        move = normalize_move(token)
        if move is None:
            return None
        normalized.append(move)

    return normalized

def get_book_eval(entry: BookMove | None) -> str | None:
    """Format a stored book score like Engine.get_eval()."""
    if entry is None:
        return None

    if entry.score_kind == "mate":
        if entry.score > 0:
            return f"Mate in {entry.score}"
        if entry.score < 0:
            return f"Mated in {abs(entry.score)}"
        return "Mate"

    return f"{entry.score / 100.0:+.2f}"

class Book:
    """
    Runtime .nbook reader used by server.py.

    mode="rated":
        choose the stored move with the best evaluation.

    mode="random":
        uniformly choose one stored move from the position.
    """

    def __init__(
        self,
        file: str,
        delay: float = 0,
        mode: str = "rated",
        seed: int | None = None,
    ) -> None:
        self.file = str(file)
        self.delay = float(delay or 0)
        self.mode = str(mode or "rated").strip().lower()
        self.seed = seed

        if self.mode not in ("rated", "random"):
            raise ValueError(
                f"Unsupported book mode {self.mode!r}; "
                "expected 'rated' or 'random'."
            )

        self.reader = OpeningBook(self.file, seed=seed)
        self.last_entry: BookMove | None = None
        self.last_history: list[str] = []

        print(
            "*** loaded .nbook: "
            + Path(self.file).name
            + " | "
            + f"{self.reader.db.count_positions():,}"
            + " positions | mode="
            + self.mode
        )

    @property
    def rated(self) -> bool:
        return self.mode == "rated"

    def get_book_entry(
        self,
        history: str | Iterable[str],
    ) -> BookMove | None:
        normalized = normalize_history(history)

        if normalized is None:
            self.last_entry = None
            return None

        self.last_history = normalized
        self.last_entry = self.reader.choose_move(
            normalized,
            rated=self.rated,
        )

        if self.last_entry is not None and self.delay > 0:
            sleep(self.delay)

        return self.last_entry

    def get_book_move(self, history: str | Iterable[str]) -> str:
        """Backward-compatible helper returning only the move string."""
        entry = self.get_book_entry(history)
        return entry.move if entry is not None else ""

    def get_book_eval(self) -> str | None:
        return get_book_eval(self.last_entry)

    def get_book_moves(
        self,
        history: str | Iterable[str],
    ) -> list[BookMove]:
        normalized = normalize_history(history)
        if normalized is None:
            return []
        return self.reader.moves(normalized)

    def close(self) -> None:
        self.reader.close()
