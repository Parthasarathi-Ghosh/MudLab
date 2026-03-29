# How to Correct for Goniometer Shift

[← Back to User Manual](../index.md)

## Overview

The **Shift Pattern** tool corrects systematic 2θ errors in experimental XRD patterns. These errors arise from instrument misalignment or sample displacement from the diffractometer centre — they cause all peaks to appear at slightly wrong 2θ positions.

The dialogue is opened from the specimen toolbar via the **Shift Pattern** button.

> **Warning — No Undo**
> Shifting permanently overwrites the stored 2θ axis (`data_x`) of the specimen. There is no undo. Save the project before applying if you may want to recover the original.

---

## Dialog Controls

| Control | Description |
|---|---|
| **Position** | Reference material drop-down — selects the known d-spacing used to locate the target peak, or **Manual** to enter the shift value directly |
| **Value** | The shift amount in °2θ; auto-filled when a reference material is selected, or entered manually for the Manual option |
| **Cancel** | Closes the dialog; any value showing in the spinbutton is discarded, no change is made to the data |
| **Apply** | Applies the current shift value to the pattern and keeps the dialog open for further corrections; enables the Done button |
| **Done** | Closes the dialog; enabled only after at least one Apply has been performed |

Pressing **Escape** or clicking the window close button behaves like **Cancel**.

---

## Reference Materials

When a reference material is selected, the expected 2θ position of its strongest peak is calculated from the known d-spacing using Bragg's law. The dialogue automatically scans a ±0.5 ° window around that position and finds the actual peak maximum, then pre-fills **Value** with the difference.

| Position | Material | d-spacing (nm) |
|---|---|---|
| Manual | — | — |
| Quartz | SiO₂ | 0.42574 |
| Silicon | Si | 0.31355 |
| Zincite | ZnO | 0.24759 |
| Corundum | Al₂O₃ | 0.2085 |
| Goethite | FeO(OH) | 0.4183 |
| Gibbsite | Al(OH)₃ | 0.48486 |

When a reference material is selected, two visual aids appear on the plot:

- **Reference line** — a thin purple vertical line at the expected 2θ position of the reference peak. It is fixed; it does not move as the shift value changes.
- **Preview pattern** — a dashed ghost of the experimental pattern, shifted by the current **Value**. As the spinner is adjusted, the preview shifts live so the user can see how a peak aligns with the reference line before committing.

Both appear together when **Value** is non-zero and a reference material is selected. Both disappear after Apply (shift value resets to 0) and reappear as soon as the spinner is adjusted again. Neither appears in Manual mode.

---

## Correction Method

The currently active correction method is **Displacement** (set in `mudlab/data/settings.py` via `PATTERN_SHIFT_TYPE`).

### Displacement correction (default)

Accounts for a sample physically offset from the diffractometer centre. A constant linear offset would be incorrect — the error is 2θ-dependent. The correction applied to every data point is:

```
displacement = 0.5 × R × shift_value / cos(θ_ref)
correction(2θ) = 2 × displacement × cos(2θ / 2) / R
data_x = data_x − correction(2θ)
```

where `R` is the goniometer radius and `θ_ref` is the theta angle of the reference peak. This produces a larger correction at low 2θ and a smaller one at high 2θ.

### Linear correction (alternative)

Subtracts the shift value uniformly from all 2θ positions:

```
data_x = data_x − shift_value
```

All markers on the specimen are also shifted by the same amount. This mode is appropriate for a pure zero-point angular error. Switch by setting `PATTERN_SHIFT_TYPE = "Linear"` in `mudlab/data/settings.py`.

---

## Typical Workflows

### Workflow A — Single specimen with a known reference material

Use this when the specimen itself contains a reference phase (e.g., a Quartz internal standard).

1. Open the **Shift Pattern** dialogue for the specimen.
2. Select the matching reference material from the **Position** drop-down.
3. The **Value** spinbutton is auto-filled with the detected shift.
4. If the auto-detected peak is incorrect (noisy data, overlapping peaks), adjust **Value** manually using the spinbutton.
5. Click **Apply**. The correction is applied to the pattern.
6. If satisfied, click **Done** to close.

### Workflow B — Determine instrument shift from a standard, apply to other specimens

Use this when you measure a pure standard material separately to characterise the instrument offset, then apply the same correction to other specimens.

1. Import the standard material pattern as a specimen.
2. Open **Shift Pattern**, select the matching reference material, verify or adjust the auto-detected **Value**, and click **Apply**. Note the shift value used.
3. Click **Done** to close.
4. Switch to each specimen that needs correcting.
5. Open **Shift Pattern**, select **Manual** from the **Position** drop-down.
6. Enter the shift value noted in step 2 into the **Value** spinbutton.
7. Click **Apply**, then **Done**.

### Workflow C — Iterative correction

Because the dialog stays open after Apply, you can apply corrections in steps:

1. Apply a coarse correction (large Value).
2. Inspect the plot to see whether the peak now aligns with the reference line.
3. Adjust Value and click Apply again with a fine correction.
4. Repeat until satisfied, then click **Done**.

---

## Auto-Detection Limitations

The auto-detection finds the highest data point within ±0.5 ° of the expected reference peak. It may give a wrong result if:

- The reference peak is obscured by a nearby stronger peak from the sample.
- The data in that region is very noisy.
- The pattern has not yet been smoothed and the true maximum is split across several adjacent points.

In these cases, adjust **Value** manually with the spinbutton before clicking **Apply**.

---

## Relevant Source Files

| Component | File |
|---|---|
| Auto-detect + apply logic | `mudlab/generic/models/lines/experimental_line.py` — `setup_shift_variables()`, `shift_data()` |
| Controller | `mudlab/generic/controllers/line_controllers.py` — `ShiftDataController` |
| View | `mudlab/generic/views/line_views.py` — `ShiftDataView` |
| Dialog frame (buttons) | `mudlab/generic/views/glade/lines/shift_dialog.glade` |
| Content layout | `mudlab/generic/views/glade/lines/shifting.glade` |
| Reference line on plot | `mudlab/generic/plot/plotters.py` |
| Reference positions + shift type | `mudlab/data/settings.py` — `PATTERN_SHIFT_POSITIONS`, `PATTERN_SHIFT_TYPE` |
| Bragg conversion | `mudlab/calculations/goniometer.py` — `get_2t_from_nm()`, `get_t_from_nm()` |

---

[← Back to User Manual](../index.md)
