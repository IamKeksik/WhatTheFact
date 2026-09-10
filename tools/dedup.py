#!/usr/bin/env python3
"""Deduplicate the soundbite library collected with prompts/SBER-HLASEK.md.

The prompt's own Deduplication section only holds inside a single run: the model
keeps the ids it has emitted in its own context, so a fresh chat starts from
nothing and re-mines seams it already exhausted. This script is the gate that
works across runs.

Rows are keyed on normalised quote text rather than on `id`, because the id is a
slug the model invents -- the same line found in a later run usually comes back
under a different one.

    python3 tools/dedup.py hlasky.jsonl                 # report only, writes nothing
    python3 tools/dedup.py hlasky.jsonl --write         # rewrite it, keeping a .bak
    python3 tools/dedup.py batch-*.jsonl -o hlasky.jsonl

Exits 1 when a line could not be parsed, so a malformed batch is never merged in
silently.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

# Rank for the `verification` field. A value the prompt does not define sits
# between the two known ones: unrecognised is not as trustworthy as a stated
# transcript, but not as weak as an admitted guess.
VERIFICATION_RANK = {"verified_transcript": 2, "unverified": 0}
UNKNOWN_VERIFICATION_RANK = 1

# Why a row lost, in the same order as the tuple built by score(). The first
# component where the winner scores higher is the reason reported.
REASONS = (
    "superseded by {winner} ({winner_where})",
    "{winner} has the stronger verification -- {winner_v} over {loser_v}",
    "{winner} carries a real start_time",
    "{winner} carries a measured duration",
    "identical on every tiebreak, kept the first occurrence {winner_where}",
)


def normalise(quote):
    """Collapse a quote to its comparable core, or None if there is nothing to compare.

    Rows without a usable quote are never merged into each other -- two entries
    that cannot be compared are not evidence of a duplicate.
    """
    if not isinstance(quote, str):
        return None
    stripped = " ".join(re.sub(r"[^a-z0-9]+", " ", quote.lower()).split())
    return stripped or None


class Row:
    __slots__ = ("source", "lineno", "seq", "data", "key")

    def __init__(self, source, lineno, seq, data):
        self.source = source
        self.lineno = lineno
        self.seq = seq
        self.data = data
        self.key = normalise(data.get("quote"))

    @property
    def id(self):
        return self.data.get("id") or "<no id>"

    @property
    def where(self):
        return f"{self.source}:{self.lineno}"


def load(paths):
    rows, broken = [], []
    seq = 0
    for path in paths:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as exc:
                broken.append((f"{path}:{lineno}", str(exc)))
                continue
            if not isinstance(data, dict):
                broken.append((f"{path}:{lineno}", "line is valid JSON but not an object"))
                continue
            rows.append(Row(path.name, lineno, seq, data))
            seq += 1
    return rows, broken


def score(row, group_ids):
    """Higher is better. Ordered by the tiebreaks documented in REASONS."""
    data = row.data
    supersedes = data.get("supersedes")
    return (
        1 if supersedes and supersedes in group_ids else 0,
        VERIFICATION_RANK.get(data.get("verification"), UNKNOWN_VERIFICATION_RANK),
        1 if data.get("start_time") else 0,
        0 if data.get("duration_estimated") else 1,
        -row.seq,
    )


def explain(winner, loser, winner_score, loser_score):
    for index, reason in enumerate(REASONS[:-1]):
        if winner_score[index] > loser_score[index]:
            return reason.format(
                winner=winner.id,
                winner_where=winner.where,
                winner_v=winner.data.get("verification", "unset"),
                loser_v=loser.data.get("verification", "unset"),
            )
    return REASONS[-1].format(winner=winner.id, winner_where=winner.where)


def dedupe(rows):
    groups = {}
    keep = []
    for row in rows:
        if row.key is None:
            keep.append(row)  # nothing to compare on, so never a duplicate
            continue
        groups.setdefault(row.key, []).append(row)

    dropped = []
    for group in groups.values():
        if len(group) == 1:
            keep.append(group[0])
            continue
        group_ids = {row.data.get("id") for row in group if row.data.get("id")}
        scored = [(score(row, group_ids), row) for row in group]
        winner_score, winner = max(scored, key=lambda pair: pair[0])
        keep.append(winner)
        for loser_score, loser in scored:
            if loser is winner:
                continue
            dropped.append((loser, winner, explain(winner, loser, winner_score, loser_score)))

    keep.sort(key=lambda row: row.seq)
    dropped.sort(key=lambda item: item[0].seq)
    return keep, dropped


def id_collisions(rows):
    """Same id used for two different quotes -- the editor references rows by id."""
    seen = {}
    for row in rows:
        if row.key is None or not row.data.get("id"):
            continue
        seen.setdefault(row.data["id"], {})[row.key] = row
    return {rid: list(keys.values()) for rid, keys in seen.items() if len(keys) > 1}


def report(rows, keep, dropped, collisions, missing_quote, broken):
    print(f"{len(rows)} rows read, {len(keep)} kept, {len(dropped)} dropped")

    if dropped:
        print("\ndropped:")
        for loser, _winner, reason in dropped:
            print(f"  {loser.id} ({loser.where})")
            print(f"    {reason}")

    if collisions:
        print("\nsame id on different quotes -- rename one of each pair by hand:")
        for rid, examples in collisions.items():
            print(f"  {rid}")
            for row in examples:
                print(f"    {row.where}  {row.data.get('quote', '')[:60]}")

    if missing_quote:
        print(f"\n{len(missing_quote)} row(s) with no usable quote, all kept:")
        for row in missing_quote:
            print(f"  {row.id} ({row.where})")

    if broken:
        print(f"\n{len(broken)} line(s) could not be parsed and are NOT in the output:")
        for where, error in broken:
            print(f"  {where}  {error}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", default=None, help="JSONL files to read (default: hlasky.jsonl)")
    parser.add_argument("-o", "--output", help="write the deduplicated rows here")
    parser.add_argument("--write", action="store_true", help="rewrite the single input file in place, keeping a .bak copy")
    args = parser.parse_args()

    paths = [Path(p) for p in (args.paths or ["hlasky.jsonl"])]
    for path in paths:
        if not path.is_file():
            parser.error(f"no such file: {path}")
    if args.write and args.output:
        parser.error("--write and --output are alternatives, not a pair")
    if args.write and len(paths) > 1:
        parser.error("--write needs exactly one input file; use --output to merge several")

    rows, broken = load(paths)
    keep, dropped = dedupe(rows)
    collisions = id_collisions(rows)
    missing_quote = [row for row in keep if row.key is None]

    report(rows, keep, dropped, collisions, missing_quote, broken)

    destination = Path(args.output) if args.output else (paths[0] if args.write else None)
    if destination is None:
        if dropped:
            print("\nnothing written -- re-run with --write or -o to apply")
    else:
        if args.write:
            backup = destination.with_suffix(destination.suffix + ".bak")
            shutil.copy2(destination, backup)
            print(f"\nbacked up to {backup}")
        destination.write_text(
            "".join(json.dumps(row.data, ensure_ascii=False) + "\n" for row in keep),
            encoding="utf-8",
        )
        print(f"wrote {len(keep)} rows to {destination}")

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
