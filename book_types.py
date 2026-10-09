from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ScoreKind = Literal["cp", "mate"]

@dataclass(frozen=True, slots=True)
class BookMove:
    move: str
    score_kind: ScoreKind
    score: int
    depth: int = 0
    seldepth: int = 0
    multipv: int = 1

    @property
    def score_pawns(self) -> float | None:
        if self.score_kind != "cp":
            return None
        return self.score / 100.0

    def display_score(self) -> str:
        if self.score_kind == "mate":
            return f"mate {self.score}"
        return f"{self.score / 100.0:+.2f}"

    def rated_key(self) -> tuple[int, int]:
        """
        Higher tuple is better, assuming the engine reports scores from the
        current/root team perspective for every independent analysis.

        Positive mate  > centipawn score > negative mate.
        Among winning mates, a shorter mate is better.
        Among losing mates, a longer mate is better.
        """
        if self.score_kind == "mate":
            if self.score > 0:
                return (3, -self.score)
            if self.score < 0:
                return (1, abs(self.score))
            return (3, 0)
        return (2, self.score)
