#!/usr/bin/env python3
"""CableCalc MVP command-line interface.

Usage:
    python cli.py sample_cable_schedule.csv --project "AWS DC - Bldg A" \\
        --revision B --author "D. Martin" --out report.html

Input CSV columns (header required):
    tag, load_kw, voltage_v, length_m, phases, power_factor,
    conductor, insulation, method, ambient_c, circuits_grouped, vd_limit_pct

Only tag, load_kw, voltage_v and length_m are mandatory; the rest fall back
to sensible defaults (3-phase, pf 0.9, Cu/XLPE, method E, 30 C, 1 circuit, 5%).
"""

import argparse
import csv
import sys

from cablecalc import CableInput, size_cable
from cablecalc import report as report_mod


def _f(row, key, default):
    val = row.get(key, "")
    return type(default)(val) if val not in ("", None) else default


def load_schedule(path):
    cables = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            row = {k.strip(): (v.strip() if isinstance(v, str) else v)
                   for k, v in row.items()}
            if not row.get("tag"):
                continue
            cables.append(CableInput(
                tag=row["tag"],
                load_kw=float(row["load_kw"]),
                voltage_v=float(row["voltage_v"]),
                length_m=float(row["length_m"]),
                phases=_f(row, "phases", 3),
                power_factor=_f(row, "power_factor", 0.9),
                conductor=_f(row, "conductor", "Cu"),
                insulation=_f(row, "insulation", "XLPE"),
                method=_f(row, "method", "E"),
                ambient_c=_f(row, "ambient_c", 30.0),
                circuits_grouped=_f(row, "circuits_grouped", 1),
                vd_limit_pct=_f(row, "vd_limit_pct", 5.0),
            ))
    return cables


def main(argv=None):
    p = argparse.ArgumentParser(description="LV cable sizing (IEC 60364 basis)")
    p.add_argument("schedule", help="CSV cable schedule")
    p.add_argument("--project", default="Untitled project")
    p.add_argument("--revision", default="A")
    p.add_argument("--author", default="")
    p.add_argument("--out", default="report.html", help="HTML output path")
    args = p.parse_args(argv)

    cables = load_schedule(args.schedule)
    if not cables:
        print("No cables found in schedule.", file=sys.stderr)
        return 1

    results = [size_cable(c) for c in cables]

    html = report_mod.render_html(
        results, project=args.project, revision=args.revision, author=args.author)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(html)

    print(report_mod.render_markdown(
        results, project=args.project, revision=args.revision))
    n_fail = sum(1 for r in results if not r.ok)
    print(f"\nHTML report written to {args.out}  "
          f"({len(results)} cables, {n_fail} fail)")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
