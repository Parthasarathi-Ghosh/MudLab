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

The workflow is:

1. **Convert** the workbook to `.xy` files (one per sheet) with the script.
2. **Import** those `.xy` files into MudLab.

The rest of this page is a detailed, step-by-step guide to running the
converter, including how to set up Python and what to do when something goes
wrong.

---

## What you need

| Requirement | Notes |
|---|---|
| A Python interpreter (3.8+) | See "Step 1" — **not** the Python bundled inside MudLab (that one has no package installer). |
| The packages `pandas` and an Excel engine | `xlrd` for `.xls`, `openpyxl` for `.xlsx`. |
| The script | `scripts/excel_xrd_to_xy.py` in the MudLab source tree. |

> **Why not MudLab's own Python?** MudLab bundles a private Python runtime,
> but it is built without the network/SSL support `pip` needs, so you cannot
> install pandas into it. Use a normal Python installation as described below.

---

## Step 1 — Get a Python with pandas

Pick **one** of these. If you already use Python for data work, you almost
certainly have one of them.

### Option A — Anaconda / Miniconda (recommended for scientists)

Anaconda ships with pandas already installed. Install the Excel engines once:

```
conda install xlrd openpyxl
```

Use the **"Anaconda Prompt"** (from the Start menu) as your terminal in
Step 3.

### Option B — Python from python.org

1. Download and install Python from <https://www.python.org/downloads/>.
   On the first installer screen, tick **"Add Python to PATH"**.
2. Open **PowerShell** (see Step 2) and install the packages:

```
python -m pip install pandas xlrd openpyxl
```

If `python` is not recognised, try `py` instead of `python` throughout.

---

## Step 2 — Open a terminal

On Windows:

- Press **Start**, type **PowerShell**, press **Enter**; **or**
- open the **Anaconda Prompt** if you used Option A.

You'll type the commands in the next steps here.

Tip: you can change to the folder containing your workbook first, e.g.

```
cd "C:\Users\<you>\Downloads\XRD clay test data"
```

(The quotes matter because the path contains spaces.)

---

## Step 3 — Run the converter

The general form is:

```
python "<path to>\excel_xrd_to_xy.py"  "<path to your workbook>"
```

Always wrap paths that contain spaces in **double quotes**.

**Example** (workbook in your Downloads folder):

```
python "C:\GitHub\MudLab\scripts\excel_xrd_to_xy.py" "C:\Users\me\Downloads\XRD clay test data\A15-03498_Clay anchor scan data.xls"
```

You should see output like:

```
Converting 9 sheet(s) from A15-03498_Clay anchor scan data.xls
  K 1442 air dried             1588 pts  x=[3.0034..29.9824]  CPS (/29.925 s) -> K 1442 air dried.xy
  K 1442 glycolated            1588 pts  x=[3.0034..29.9824]  CPS (/29.925 s) -> K 1442 glycolated.xy
  ...
Output folder: C:\Users\me\Downloads\XRD clay test data\converted_xy
```

### Options

| Option | Effect |
|---|---|
| *(none)* | Intensities are normalised to **counts-per-second** (`Iobs ÷ CT`), matching MudLab's CPI/XRDML imports. |
| `--raw` | Keep the **raw counts** (no counting-time normalisation). |
| `-o FOLDER` / `--outdir FOLDER` | Write the `.xy` files to `FOLDER` instead of the default `converted_xy` folder next to the workbook. |

**Examples:**

```
python excel_xrd_to_xy.py "scan data.xlsx" -o "C:\converted"
python excel_xrd_to_xy.py "scan data.xls" --raw
```

---

## Step 4 — Import the .xy files into MudLab

1. In MudLab choose **Import Specimen**.
2. Navigate to the `converted_xy` folder (or your `-o` folder).
3. Select the `.xy` files (multi-select if your file chooser allows).

Each file imports as a separate specimen **named after its sheet**, so the
treatments (air-dried / glycolated / heated) stay clearly distinguished.

---

## What the converter does

- Reads **every sheet** of the `.xls`/`.xlsx` workbook.
- Finds the **2θ** and **intensity** columns by their header text
  (`2Th` / `Pos` / `Angle`, and `Iobs` / `cts` / `Int` / `Counts`), plus an
  optional **counting-time** column (`CT` / `time`). Blank rows that
  exporters insert are skipped automatically.
- Writes `<sheet name>.xy` — a two-column file (angle, intensity).
- **Normalises to counts-per-second** (`Iobs ÷ CT`, per data point) unless
  `--raw` is given. It does *not* divide by the angular step width — that is
  not standard for XRD, and CPI/XRDML don't do it either.

`.xy` files are read by MudLab's standard CSV/XY parser (which also handles
`.dat`, `.csv`, `.tab`).

---

## Troubleshooting

| Message / symptom | Cause and fix |
|---|---|
| `This tool needs pandas: pip install pandas xlrd openpyxl` | pandas isn't installed in the Python you ran. Install it (Step 1), or run with the Python that has it. |
| `Missing Excel engine for this file type` | The reader for your file type isn't installed: `pip install xlrd` for `.xls`, `pip install openpyxl` for `.xlsx`. |
| `'python' is not recognized…` | Python isn't on PATH. Use `py` instead of `python`, or re-run the python.org installer and tick "Add Python to PATH". |
| `File not found: …` | Check the workbook path; wrap it in double quotes if it contains spaces. |
| A sheet says `skipped (no 2-theta / intensity columns found)` | That sheet has no recognisable header. Make sure the scan table has a header row containing the 2θ and intensity column names, near the top of the sheet. |
| Intensities look ~N× too large/small vs another pattern | Mismatched normalisation. Use the default (CPS) for everything, or `--raw` for everything — don't mix. |

---

## Reference

- Script: [`scripts/excel_xrd_to_xy.py`](../../scripts/excel_xrd_to_xy.py)
- Script index: [`scripts/README.md`](../../scripts/README.md)

---

[← Back to User Manual](../index.md)
