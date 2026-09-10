#!/usr/bin/env python3
"""Print the baseline block to paste under prompts/SBER-HLASEK.md when starting a new run.

A fresh chat has no memory of earlier runs, so without this the model restarts at
BATCH 1 and re-mines seams it already exhausted. This does not guarantee anything
-- tools/dedup.py is the actual gate -- it just stops the model wasting batches on
ground already covered.

    python3 tools/prime.py hlasky.jsonl              # print it
    python3 tools/prime.py hlasky.jsonl > primer.txt

Rows are sorted by id so the block stays stable between runs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HEADER = """ALREADY COLLECTED -- {count} entries. Do not emit these again.

Emit one of these a second time only with "supersedes": "<id>", and only for a
genuinely better source: a real timestamp where there was none, or public domain
where the entry was rights-reserved. Say why in verification_note."""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", default=None, help="JSONL files to read (default: hlasky.jsonl)")
    parser.add_argument("--width", type=int, default=90, help="truncate quotes to this many characters (default: 90)")
    args = parser.parse_args()

    paths = [Path(p) for p in (args.paths or ["hlasky.jsonl"])]
    entries = {}
    skipped = 0
    for path in paths:
        if not path.is_file():
            parser.error(f"no such file: {path}")
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                skipped += 1
                continue
            if not isinstance(row, dict) or not row.get("id"):
                skipped += 1
                continue
            quote = " ".join(str(row.get("quote") or "").split())
            if len(quote) > args.width:
                quote = quote[: args.width - 1].rstrip() + "…"
            # First occurrence wins, so the block stays stable when an id was
            # reused for two different quotes -- dedup.py reports those.
            entries.setdefault(row["id"], quote or "(no quote recorded)")

    if not entries:
        print("no usable rows found -- nothing to prime with", file=sys.stderr)
        return 1

    print(HEADER.format(count=len(entries)))
    print()
    for entry_id in sorted(entries):
        print(f"{entry_id} | {entries[entry_id]}")

    if skipped:
        print(f"\n{skipped} line(s) skipped as unparseable or id-less -- run tools/dedup.py to see them", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
