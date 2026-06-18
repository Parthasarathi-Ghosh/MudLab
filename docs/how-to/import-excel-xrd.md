# Importing XRD data that was pasted into Excel

[← Back to User Manual](../index.md)

> **Printing to PDF:** Open this page in your browser and use **File → Print → Save as PDF**.

Sometimes XRD scans arrive as an **Excel workbook** rather than an instrument
file — typically one scan per sheet, pasted from a PANalytical HighScore /
X'Pert export with columns like `No. | Pos. [°2Th.] | Iobs [cts] | CT [s]`.

MudLab cannot open Excel workbooks directly: the application has no
spreadsheet reader, and there is no dependable way to recognise every format
that someone might paste into a spreadsheet. Instead, MudLab ships a small
**converter script** that turns each sheet into a `.xy` file you can import.

---

## Step 1 — Convert the workbook

The script lives in the MudLab source tree at
[`scripts/excel_xrd_to_xy.py`](../../scripts/excel_xrd_to_xy.py)
(see [`scripts/README.md`](../../scripts/README.md) for the full reference).

It needs **pandas** plus an Excel engine:

```
pip install pandas
pip install xlrd        # for old-style .xls workbooks
pip install openpyxl    # for .xlsx workbooks
```

Run it on your workbook:

```
python excel_xrd_to_xy.py "A15-03498_Clay anchor scan data.xls"
```

This writes one file per sheet into a **`converted_xy`** folder next to the
workbook, e.g. `K 1442 air dried.xy`, `K 1442 glycolated.xy`, … Each file is
a two-column CSV (angle, intensity).

**Intensities are normalised to counts-per-second** (`Iobs ÷ CT`) so they are
on the same basis as MudLab's CPI and XRDML imports. If you need the raw
counts instead, add `--raw`.

---

## Step 2 — Import the .xy files into MudLab

1. **Import Specimen** in MudLab.
2. Navigate to the `converted_xy` folder.
3. Select the `.xy` files (multi-select if your file chooser allows).

Each file imports as a separate specimen named after its sheet, so the
treatments (air-dried / glycolated / heated) stay clearly distinguished.

---

## Notes

- The converter identifies the 2θ and intensity columns by their header
  text (`2Th`/`Pos`/`Angle` and `Iobs`/`cts`/`Int`/`Counts`), so it tolerates
  minor header differences and the blank rows that exporters often insert.
- `.xy` files are read by MudLab's standard CSV/XY parser (also handles
  `.dat`, `.csv`, `.tab`).
- This is a deliberate, transparent workflow rather than an in-app Excel
  importer — see the reasoning above.

---

[← Back to User Manual](../index.md)
