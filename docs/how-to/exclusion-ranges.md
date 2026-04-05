# Exclusion Ranges

[← Back to User Manual](../index.md)

Exclusion ranges let you mark one or more 2θ intervals in an experimental pattern that should be ignored when evaluating the fit quality. They have no effect on the calculated pattern itself — only on the statistics that measure how well the calculation matches the experiment.

---

## What exclusion ranges do (and do not do)

| Affected | Not affected |
|---|---|
| Rp, Rwp, GoF residuals — computed only on non-excluded points | The calculated XRD pattern — always computed over the full 2θ range |
| Point count shown in statistics labels | Phase parameters, peak shapes, structure factors |
| The visual display — excluded regions are drawn as hatched overlays on the plot | Peak detection — `auto_add_peaks` searches the full pattern; peaks inside excluded regions can still be found |

**Why this matters:** If a region of the experimental pattern contains a non-clay peak (e.g. quartz, calcite) or a detector artefact that the model is not intended to reproduce, excluding it prevents that mismatch from inflating the Rwp, without changing what is being modelled.

---

## Where to find exclusion ranges in the UI

Open **Edit Pattern** for the specimen (double-click the specimen name in the specimen list, or use the toolbar button). In the dialog, select the **Exclusions** tab. The tab contains:

- A table with two editable columns: **From [°2θ]** and **To [°2θ]**
- **+** button — adds a new row
- **−** button — removes the selected row(s); the button is enabled only when at least one row is selected
- **Import** button — loads ranges from a `.EXC` file, replacing all current ranges (a confirmation dialog is shown first)
- **Export** button — saves the current ranges to a `.EXC` file

---

## Adding a range

1. Go to the **Exclusions** tab in Edit Pattern.
2. Click **+**. A new row appears with both values set to **0**.
3. Click the value in the **From [°2θ]** column and type the start of the range.
4. Click the value in the **To [°2θ]** column and type the end of the range.
5. Press Enter or click elsewhere to confirm.

The hatched overlay on the plot updates immediately.

---

## Removing a range

1. Click a row in the table to select it. Hold **Ctrl** or **Shift** to select multiple rows.
2. Click **−**. The selected rows are deleted and the plot updates immediately.

---

## Multiple non-consecutive ranges

**Yes — any number of separate ranges can be defined for a single specimen.** Each row in the table is an independent interval. They do not need to be contiguous or in any particular order; the selector logic sorts them before applying.

Example: a specimen with a strong quartz peak at ~26.6 ° and a calcite peak at ~29.4 ° could have two separate ranges:

| From [°2θ] | To [°2θ] |
|---|---|
| 25.5 | 27.5 |
| 28.5 | 30.5 |

Each range is applied independently. A data point is excluded if it falls inside **any** of the defined ranges.

---

## Import / Export (.EXC files)

Exclusion ranges can be saved to and loaded from plain-text `.EXC` files (ASCII CSV, one row per range). This allows reuse across specimens or projects.

- **Import** replaces all existing ranges for the specimen. A confirmation dialog is shown before the current ranges are overwritten.
- **Export** writes the current ranges to a `.EXC` file with the specimen name and sample name as a header line.

Ranges are also saved automatically inside the `.mud` project file as part of normal **File → Save Project**.

---

## How the selector works (technical detail)

Each exclusion range `(x0, x1)` contributes a mask `(2θ < x0) | (2θ > x1)`. All masks are combined with AND, so a point must clear every range to be included. The result is a boolean array of the same length as the 2θ axis, passed to the Rp/Rwp/GoF functions in `specimen/models/statistics.py`.

---

## Relevant source files

| Component | File |
|---|---|
| Model property | `mudlab/specimen/models/base.py` — `exclusion_ranges`, `get_exclusion_selector()` |
| UI controller | `mudlab/specimen/controllers/specimen_controllers.py` — `setup_exclusion_ranges_tree_view()`, `on_add_exclusion_range_clicked()`, `on_del_exclusion_ranges_clicked()` |
| Statistics | `mudlab/specimen/models/statistics.py` — `update_statistics()` |
| Plot rendering | `mudlab/generic/plot/plotters.py` — `plot_hatches()` |
| File parser | `mudlab/file_parsers/exc_parsers/__init__.py` — `EXCParser` |
| Visual settings | `mudlab/data/settings.py` — `EXCLUSION_FOREG`, `EXCLUSION_LINES` |

---

[← Back to User Manual](../index.md)
