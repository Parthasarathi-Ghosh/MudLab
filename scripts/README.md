# MudLab utility scripts

Standalone helper scripts that sit alongside MudLab but are **not** part of
the application. Run them with any Python that has the listed requirements.

| Script | Purpose |
|---|---|
| [`excel_xrd_to_xy.py`](excel_xrd_to_xy.py) | Convert XRD scans pasted into an Excel workbook (one scan per sheet) into MudLab-importable `.xy` files. |

---

## excel_xrd_to_xy.py

XRD data are sometimes delivered as an Excel workbook with one scan per
sheet — e.g. a PANalytical HighScore / X'Pert export pasted into columns
`No. | Pos. [°2Th.] | Iobs [cts] | CT [s]`. MudLab has no Excel reader (and
there's no reliable way to recognise every format that might be pasted into
a spreadsheet), so this tool converts each sheet into a two-column `.xy`
file that **Import Specimen** reads directly.

**What it does**
- Reads every sheet of an `.xls` or `.xlsx` workbook.
- Finds the 2θ and intensity columns by their header text, plus an optional
  counting-time column.
- Writes `<sheet name>.xy` (angle, intensity) — each imports as one,
  distinctly-named specimen.
- Normalises intensity to **counts-per-second** (`Iobs / CT`) when a
  counting-time column is present — matching MudLab's CPI and XRDML import
  convention. Pass `--raw` to keep raw counts.

**Requirements**
```
pip install pandas
pip install xlrd        # for old-style .xls workbooks
pip install openpyxl    # for .xlsx workbooks
```
(pandas picks the engine automatically; install the one matching your files.)

**Usage**
```
python excel_xrd_to_xy.py "scan data.xls"
python excel_xrd_to_xy.py "scan data.xlsx" -o out_folder
python excel_xrd_to_xy.py "scan data.xls" --raw
```
By default the `.xy` files are written to a `converted_xy` folder next to
the workbook. Then in MudLab: **Import Specimen → select the `.xy` files**.

**Full step-by-step guide** (setting up Python, installing the packages,
running on Windows, options, and troubleshooting):
[docs/how-to/import-excel-xrd.md](../docs/how-to/import-excel-xrd.md).

Run `python excel_xrd_to_xy.py -h` for the built-in option help.
