from __future__ import annotations

import argparse
import json
from pathlib import Path

from book_db import BookDB
from generator import (
    canonical_root,
    generation_profile,
    _legacy_generation_profile,
    _profile_differences,
)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare an existing .nbook with a generator config."
    )
    parser.add_argument("book")
    parser.add_argument("config")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    root_spec = canonical_root(
        config["book"].get(
            "root",
            {"type": "startpos"},
        )
    )

    with BookDB(args.book, readonly=True) as db:
        print(f"Book: {args.book}")
        print(f"Positions: {db.count_positions():,}")
        print(f"Stored root: {db.get_meta('root_spec')}")
        print(f"Current root: {root_spec}")

        raw = db.get_meta("config_json")
        if not raw:
            print("No stored config_json metadata is available.")
            return

        old_config = json.loads(raw)
        old_profile = _legacy_generation_profile(
            old_config,
            db.get_meta("root_spec", root_spec) or root_spec,
        )
        new_profile = generation_profile(
            config,
            root_spec,
        )

        diffs = _profile_differences(
            old_profile,
            new_profile,
        )

        if not diffs:
            print("Compatible: YES")
            print(
                "Only safe/non-book-defining settings differ, "
                "or the configs are equivalent."
            )
            return

        print("Compatible: NO")
        print("Book-defining differences:")
        for key, old, new in diffs:
            print(
                f"  {key}: existing={old!r} -> current={new!r}"
            )

if __name__ == "__main__":
    main()
