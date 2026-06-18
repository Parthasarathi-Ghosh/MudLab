#!/usr/bin/env python
# coding=UTF-8
"""
excel_xrd_to_xy.py — convert XRD scans pasted into an Excel workbook into
plain two-column .xy files that MudLab can import (Import Specimen).

Why this exists
---------------
XRD data are sometimes delivered as an Excel workbook with one scan per
sheet (for example a PANalytical HighScore / X'Pert export pasted into
columns: "No. | Pos. [°2Th.] | Iobs [cts] | CT [s]"). MudLab's bundled
runtime has no Excel reader, and there is no reliable way to recognise
every format that might be pasted into a spreadsheet — so instead of a
fragile in-app importer, this standalone tool converts each sheet to a
MudLab-readable .xy file.

What it does
------------
* Reads every sheet of an .xls or .xlsx workbook (via pandas).
* For each sheet it locates the 2-theta column and the intensity column by
  their header text ("2Th"/"Pos"/"Angle" and "Iobs"/"cts"/"Int"/"Counts"),
  and an optional counting-time column ("CT"/"time").
* Writes "<sheet name>.xy" — a 2-column CSV: angle, intensity. Each file
  imports as one, distinctly-named specimen.
* Intensities are normalised to counts-per-second (Iobs / CT) when a
  counting-time column is present, matching how MudLab's CPI and XRDML
  parsers import data. Use --raw to keep raw counts instead.

Requirements
------------
    pip install pandas
    pip install xlrd        # needed for old-style .xls workbooks
    pip install openpyxl    # needed for .xlsx workbooks

(Install only the engine matching your files; pandas selects it
automatically.)

Usage
-----
    python excel_xrd_to_xy.py "scan data.xls"
    python excel_xrd_to_xy.py "scan data.xlsx" -o out_folder
    python excel_xrd_to_xy.py "scan data.xls" --raw      # keep raw counts

By default the .xy files are written to a "converted_xy" folder next to the
input workbook.
"""

import argparse
import os
import re
import sys


def _find_column(headers, patterns):
    """Return the index of the first header matching any regex in *patterns*."""
    for i, h in enumerate(headers):
        text = ("" if h is None else str(h)).strip().lower()
        for pat in patterns:
            if re.search(pat, text):
                return i
    return None


def _detect_layout(raw):
    """
    Given a sheet as a list of rows (each a list of cells), find the header
    row and the angle / intensity / counting-time column indices.
    Returns (header_row_index, angle_col, intensity_col, ct_col) or None.
    """
    for r, row in enumerate(raw[:25]):           # header is near the top
        headers = list(row)
        angle = _find_column(headers, [r"2\s*th", r"\bpos\b", r"angle", r"\bdeg"])
        inten = _find_column(headers, [r"iobs", r"\bcts\b", r"counts", r"\bint"])
        if angle is not None and inten is not None:
            ct = _find_column(headers, [r"\bct\b", r"count.*time", r"\btime\b"])
            return r, angle, inten, ct
    return None


def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def convert_sheet(name, raw, outdir, normalise=True):
    """Convert one sheet (list-of-rows) to a .xy file. Returns a status string."""
    layout = _detect_layout(raw)
    if layout is None:
        return "skipped (no 2-theta / intensity columns found)"
    header_row, ac, ic, ctc = layout

    rows = []
    cts = set()
    for row in raw[header_row + 1:]:
        if ac >= len(row) or ic >= len(row):
            continue
        x = _to_float(row[ac])
        y = _to_float(row[ic])
        if x is None or y is None:
            continue                              # blank/non-numeric line
        if normalise and ctc is not None and ctc < len(row):
            ct = _to_float(row[ctc])
            if ct and ct > 0:
                y = y / ct
                cts.add(round(ct, 4))
        rows.append((x, y))

    if not rows:
        return "skipped (no numeric data rows)"

    safe = re.sub(r'[<>:"/\\|?*]', "_", name).strip()
    path = os.path.join(outdir, "%s.xy" % safe)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("Angle,%s\n" % name)
        for x, y in rows:
            f.write("%.4f,%.6f\n" % (x, y))

    note = ""
    if normalise and cts:
        note = "  CPS (/%s s)" % ";".join("%g" % c for c in sorted(cts))
    return "%d pts  x=[%.4f..%.4f]%s -> %s" % (
        len(rows), rows[0][0], rows[-1][0], note, os.path.basename(path))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Convert XRD scans in an Excel workbook to MudLab .xy files.")
    ap.add_argument("workbook", help="Path to the .xls or .xlsx file")
    ap.add_argument("-o", "--outdir", default=None,
                    help="Output folder (default: 'converted_xy' next to the workbook)")
    ap.add_argument("--raw", action="store_true",
                    help="Keep raw counts instead of normalising to counts-per-second")
    args = ap.parse_args(argv)

    try:
        import pandas as pd
    except ImportError:
        sys.exit("This tool needs pandas:  pip install pandas xlrd openpyxl")

    if not os.path.isfile(args.workbook):
        sys.exit("File not found: %s" % args.workbook)

    outdir = args.outdir or os.path.join(
        os.path.dirname(os.path.abspath(args.workbook)), "converted_xy")
    os.makedirs(outdir, exist_ok=True)

    try:
        sheets = pd.read_excel(args.workbook, sheet_name=None, header=None)
    except ImportError as e:
        sys.exit("Missing Excel engine for this file type (%s).\n"
                 "Install:  pip install xlrd   (.xls)   or   pip install openpyxl   (.xlsx)"
                 % e)

    print("Converting %d sheet(s) from %s" % (len(sheets), os.path.basename(args.workbook)))
    for name, df in sheets.items():
        raw = df.values.tolist()
        status = convert_sheet(name, raw, outdir, normalise=not args.raw)
        print("  %-28s %s" % (name, status))
    print("Output folder: %s" % outdir)


if __name__ == "__main__":
    main()
