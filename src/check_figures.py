"""Verify the numbered figure set is internally consistent.

Figure numbers are assigned by hand across ~20 scripts, and nothing checked them.
Two collisions reached the repository that way: stale 11_/12_ HTML outputs left
behind when merge_correlations.py was renumbered to 24/25, and a fresh clash when
incidence_vs_homicide.py took 26 while international_comparison.py already had it.

Checks, all cheap and standard-library only:

1. No two scripts write the same figure number.
2. No two files on disk share a figure number.
3. Every numbered figure on disk is written by some script (no orphans).
4. Numbers are contiguous from 01, so a gap means something was lost silently.

Run:  python src/check_figures.py
Exits non-zero on any failure.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
FIGDIR = ROOT / "reports" / "figures"

# Scripts name figures in several ways: a full "reports/figures/NN_x.png" path, a
# bare "NN_x.png" handed to a save helper, or a Path built from parts. Match the
# filename inside any string literal rather than assuming one style.
WRITTEN = re.compile(
    r"""["'](?:[^"']*/)?(\d{2})_([A-Za-z0-9_]+)\.(png|html)["']"""
)
# The same, as a filename on disk.
ON_DISK = re.compile(r"""^(\d{2})_([A-Za-z0-9_]+)\.(png|html)$""")


def main() -> None:
    errors: list[str] = []

    # ---- what the scripts claim to write -----------------------------------
    by_number: dict[str, set[str]] = defaultdict(set)
    writers: dict[str, set[str]] = defaultdict(set)
    for script in sorted(SRC.glob("*.py")):
        text = script.read_text(encoding="utf-8")
        for num, slug, ext in WRITTEN.findall(text):
            by_number[num].add(f"{num}_{slug}.{ext}")
            writers[num].add(script.name)

    for num, names in sorted(by_number.items()):
        if len(names) > 1:
            errors.append(
                f"figure {num} is written under {len(names)} different names: "
                f"{sorted(names)} (by {sorted(writers[num])})"
            )

    # ---- what is actually on disk ------------------------------------------
    disk: dict[str, list[str]] = defaultdict(list)
    for path in sorted(FIGDIR.glob("*")):
        m = ON_DISK.match(path.name)
        if m:
            disk[m.group(1)].append(path.name)

    for num, names in sorted(disk.items()):
        if len(names) > 1:
            errors.append(f"figure {num} exists as {len(names)} files on disk: {names}")

    orphans = sorted(set(disk) - set(by_number))
    if orphans:
        detail = ", ".join(f"{n} ({disk[n][0]})" for n in orphans)
        errors.append(f"figures on disk that no script writes: {detail}")

    if by_number:
        expected = set(f"{i:02d}" for i in range(1, max(int(n) for n in by_number) + 1))
        gaps = sorted(expected - set(by_number))
        if gaps:
            errors.append(f"gaps in the numbering: {gaps}")

    if errors:
        print("FAIL: figure numbering is inconsistent")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    print(
        f"PASS: {len(by_number)} figure numbers, no collisions, no orphans, "
        f"contiguous 01-{max(by_number):s}."
    )


if __name__ == "__main__":
    main()
