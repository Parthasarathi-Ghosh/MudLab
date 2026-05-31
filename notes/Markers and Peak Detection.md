# Markers and Peak Detection

Source: `mudlab/specimen/models/markers.py`, `mudlab/calculations/peak_detection.py`  
Controller: `mudlab/specimen/controllers/marker_controllers.py`  
View: `mudlab/specimen/views/markers.py`  
Docs: `docs/how-to/markers.md`

## Markers

A **marker** is a labelled vertical line drawn on the XRD plot at a specific 2θ position. Each specimen has its own marker list.

### Marker properties

| Property | Meaning |
|---|---|
| `position` | 2θ angle (°) |
| `nm` | d-spacing (nm), computed from position via Bragg's law |
| `label` | Text shown on the plot |
| `visible` | Show/hide the marker line |
| `style` | Line style (solid, dashed, dotted, …) |
| `color` | Marker colour |
| `align` | Label alignment (left, right, centre) |
| `base` / `top` | Whether the line extends from the pattern base or top |
| `x_offset`, `y_offset` | Fine position adjustments for the label |
| `angle` | Label rotation angle |

Markers can **inherit** style/colour/alignment from a per-specimen default marker — useful when you want all markers on a specimen to share a style.

### Editing markers

Edit Markers dialog: select a marker in the list on the left; properties appear on the right. The eyedropper button lets you click directly on the plot to set the position.

2θ and nm are kept in sync: editing either one recalculates the other using `λ` from the goniometer.

## Find Peaks (automatic detection)

`mudlab/calculations/peak_detection.py`

Automatically locates peaks in the experimental pattern and creates markers at each peak.

**Algorithm:**
1. Smooth the pattern (configurable window)
2. Find local maxima above a threshold
3. Filter by minimum separation
4. Create a `Marker` for each detected peak

## Match Minerals

`MatchMineralController` — compares detected peaks against a library of reference mineral d-spacings (`MineralScorer`).

**Scoring:**
- Positional match: observed d-spacing vs. reference within tolerance
- Intensity correlation: linear regression of observed vs. reference intensities
- Single-peak path: positional accuracy scoring + `np.unique` guard on linregress

Results are displayed in the Match Minerals dialog ranked by score. `min_peaks_needed` prevents spurious single-peak matches.

## ThresholdSelector

Interactive model: user drags a threshold line on the pattern; peaks above the threshold are passed to Find Peaks or Match Minerals. When no markers are selected, `markers_to_use` falls back to `list(self.model.markers)` (all markers).

## Related Notes

- [[MudLab Overview]]
- [[Mixture Model]]
- [[XRD Diffraction Calculation]]
- [[GTK UI Conventions]]
