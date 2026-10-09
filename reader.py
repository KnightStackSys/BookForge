from __future__ import annotations

import argparse
import random
from pathlib import Path

from book_db import BookDB, position_key
from book_types import BookMove

class OpeningBook:
    def __init__(self, path: str | Path, seed: int | None = None) -> None:
        self.db = BookDB(path, readonly=True)
        self.root_spec = self.db.get_meta("root_spec")
        if not self.root_spec:
            raise ValueError("Book is missing root_spec metadata.")

        self.score_perspective = self.db.get_meta(
            "score_perspective", "side_to_move_team"
        )
        if self.score_perspective not in ("side_to_move_team", "root_team"):
            raise ValueError(
                "This reader's rated mode requires a higher-is-better "
                "root/current-team score perspective."
            )

        self.rng = random.Random(seed)

    def close(self) -> None:
        self.db.close()

    def __enter__(self) -> "OpeningBook":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def moves(self, history: list[str] | tuple[str, ...]) -> list[BookMove]:
        key = position_key(self.root_spec, history)
        return self.db.get_moves(key) or []

    def choose_move(
        self,
        history: list[str] | tuple[str, ...],
        *,
        rated: bool = True,
    ) -> BookMove | None:
        candidates = self.moves(history)
        if not candidates:
            return None

        if rated:
            return max(candidates, key=lambda m: m.rated_key())

        return self.rng.choice(candidates)

    def contains(self, history: list[str] | tuple[str, ...]) -> bool:
        return bool(self.moves(history))

def main() -> None:
    parser = argparse.ArgumentParser(description="Probe a BookForge .nbook file.")
    parser.add_argument("book", help="Path to .nbook")
    parser.add_argument(
        "--moves",
        nargs="*",
        default=[],
        help="Move history from the book root, e.g. f4f6 a8g2 ...",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Choose randomly instead of rated/best-eval mode.",
    )
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    with OpeningBook(args.book, seed=args.seed) as book:
        choices = book.moves(args.moves)

        if not choices:
            print("No book entry for this position.")
            return

        print("Book moves:")
        for item in choices:
            print(
                f"  {item.move:10s} {item.display_score():>10s} "
                f"depth={item.depth} seldepth={item.seldepth} "
                f"multipv={item.multipv}"
            )

        chosen = book.choose_move(args.moves, rated=not args.random)
        if chosen:
            mode = "random" if args.random else "rated"
            print(
                f"\nChosen ({mode}): {chosen.move} "
                f"[{chosen.display_score()}]"
            )

if __name__ == "__main__":
    main()
