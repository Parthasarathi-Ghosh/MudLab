# Markers: Peak Detection and Mineral Identification

[← Back to User Manual](../index.md)

Markers are vertical annotations on a specimen's diffraction pattern. They record peak positions (as d-spacings in nm and as °2θ), carry a text label that appears on the plot, and can optionally display a connector line from the pattern profile up to the label. Markers are saved as part of the `.mud` project file and can also be exported and reused across specimens.

---

## Opening Edit Markers

Click the **Marker** toolbar button, or select a specimen and choose the corresponding menu item. The **Edit Markers** dialog opens.

The dialog has two areas:
- **Left — the marker list**: every marker for the selected specimen. Two columns are shown:
  - A toggle (✓/—) to set the marker **visible** or hidden on the plot.
  - The marker **label**, as it appears in the label text box.
- **Right — the edit panel**: properties of the marker selected in the list.

Buttons above the list:

| Button | Action |
|---|---|
| **+** | Add a new blank marker at position 0 |
| **−** | Delete the selected marker (irreversible) |
| **Import** | Load markers from a `.MRK` file, appending to the current list |
| **Export** | Save the selected markers to a `.MRK` file |
| **Find Peaks** | Auto-detect peaks and create markers (see below) |
| **Match Minerals** | Open the mineral matching dialog (see below) |

---

## Marker Properties

Selecting a marker in the list shows its properties on the right.

### Label

Free-text string displayed on the plot at the marker position. After running **Append Labels** in the Match Minerals dialog, the mineral abbreviation is appended to this field (e.g., `0.720, Sm`). The label field shows the current full text and can be edited directly at any time.

### Position

The marker's 2θ position in two equivalent units:

- **°2θ spin** — set directly in degrees.
- **nm spin** — set as a d-spacing; the goniometer converts it to °2θ automatically.
- **Eye-dropper button** — click it, then click a point on the main plot. The dialog hides while you click, then reappears with the position updated.

### Visible

Checkbox. Unchecked markers are hidden on the plot but retained in the project.

### Line and Label Style

The six style options below each have a **default** checkbox. When checked, the value is inherited from the project-level display settings; when unchecked you can set a per-marker value.

| Property | Options | Notes |
|---|---|---|
| **Label Angle** | Any angle (degrees) | 0° = vertical text; 90° = horizontal text |
| **Label alignment** | Left / Centered / Right | Alignment of the label text relative to the marker position |
| **Line style** | None / Solid / Dash / Dotted / Dash-Dotted / Display at Y-offset | "None" shows only the text label without a connector line; "Display at Y-offset" draws the line at a fixed y position rather than from the base point |
| **Line base** | X-axis / Experimental profile / Calculated profile / Lowest of both / Highest of both | Where the bottom of the connector line is anchored |
| **Line top** | Relative to base / Top of plot | "Relative to base" stops the line at **Offset from base** above the anchor; "Top of plot" extends the line to the top of the figure |
| **Offset from base** | Float (°2θ units) | How far above the base point the line extends when Line top is "Relative to base" |
| **Colour** | Colour picker | The colour of both the connector line and the label text |

### X Offset and Y Offset

Additional fine-grained position adjustments for the label text, in °2θ units. These shift the label without moving the underlying peak position.

---

## Finding Peaks Automatically

Click **Find Peaks** in the Edit Markers toolbar.

If the specimen already has markers, a confirmation dialog asks whether to clear them. Choose **Yes** to start fresh, or **No** to keep existing markers and add new ones alongside them.

### Auto Detect Peaks dialog

| Control | Description |
|---|---|
| **Pattern** | Which profile to analyse — Experimental or Calculated |
| **Algorithm** | Detection method — see below |
| **Maximum** | Upper limit of the histogram parameter range (0–1, as a fraction of the maximum intensity) |
| **Steps** | Number of parameter values to evaluate when building the histogram |
| **# of peaks** | Target number of peaks — the algorithm selects the parameter value that produces this many peaks |
| **Selected threshold / Min. prominence** | The exact parameter value corresponding to the chosen peak count; can also be edited directly for fine-tuning |
| **Min. distance (°2θ)** | *(Prominence only)* Minimum separation between two detected peaks in °2θ; prevents two markers being placed on the same broad peak |

### Algorithms

Two peak detection algorithms are available:

#### Prominence (scipy) — default

Uses `scipy.signal.find_peaks` with a minimum **prominence** filter. Prominence measures how much a peak stands out above its surrounding baseline — a peak that is merely a shoulder on a larger peak has low prominence even if it has high absolute intensity. This makes the method robust for XRD patterns where peaks sit on broad humps or strong backgrounds.

The histogram shows **# of peaks vs. minimum prominence**. Higher minimum prominence → fewer, more isolated peaks.

The **Min. distance** parameter enforces a minimum °2θ gap between any two accepted peaks, preventing the algorithm from placing multiple markers on the flanks of a single broad reflection.

#### Threshold (classic)

The original algorithm. Detects peaks by looking for a local maximum that drops by at least a threshold fraction of the maximum intensity on both sides. The histogram shows **# of peaks vs. threshold value**.

### Choosing the number of peaks

The recommended workflow is:

1. Enter the approximate number of peaks you expect in the **# of peaks** spinner. The parameter value (prominence or threshold) is set automatically by looking up the histogram curve.
2. The blue draggable vertical line on the histogram moves to the corresponding position. Drag it left or right to fine-tune if needed — the **# of peaks** spinner updates as you drag.
3. Inspect the histogram shape: the ideal parameter value is usually at the kink or step where the curve flattens, beyond the noise-driven linear increase.
4. Click **OK** to confirm.

Markers are inserted at each detected peak position. Their labels are set to the d-spacing in nm (e.g., `0.720`). Duplicate positions (peaks already in the list) are skipped.

---

## Match Minerals

Click **Match Minerals** (or select one or more markers first and then click it). The Edit Markers dialog hides and the Match Minerals dialog opens.

The dialog has two panels side-by-side:

- **Matched minerals (left)** — minerals selected for labelling. Three columns: Name, Abbreviation, Score.
- **All minerals (right)** — the full reference database (alphabetical). Two columns: Name, Abbreviation.

### Scoring

Score is calculated by comparing each mineral's reference d-spacings against the marker positions. A tolerance of 1% of the reference d-spacing is used. Each matching peak contributes to the score based on positional accuracy and relative intensity. A score of 0 means no marker position matched any reference peak for that mineral.

### Workflow

1. **Auto Match** — MudLab searches the full mineral database and populates the left panel with the best-scoring minerals automatically. The mineral with the highest score is pre-selected.

2. **Manual add** — Select any row in the right panel and click **← (left arrow)** to move it to the left panel. Its score is computed against the current markers.

3. **Manual remove** — Select a row in the left panel and click **→ (right arrow)** to remove it.

4. **Specimen range checkbox** — When ticked, reference peaks outside the specimen's 2θ range are filtered out before scoring and before the mineral preview is drawn on the plot. This prevents high scores driven by peaks you cannot observe.

5. **Preview** — Clicking any row in either panel draws that mineral's reference peaks as short vertical lines on the main plot, so you can visually inspect the match before committing.

6. **Append Labels** — Select one or more rows in the left panel (Ctrl/Shift-click for multiple) and click **Append Labels**. The mineral abbreviation is appended to the label of each marker whose position matches a reference peak of that mineral (e.g., a marker labelled `0.720` becomes `0.720, Sm`).

   The updated label is immediately visible in the Edit Markers label text box and can be edited further at any time.

   > **Note:** The button is enabled only when at least one selected match has a score > 0. A manually-added mineral with no matching peaks has score 0 and would silently do nothing, so the button is disabled in that case.

7. Close the dialog with the window close button. Edit Markers reappears.

---

## Import and Export (.MRK files)

Markers can be saved to and loaded from `.MRK` files (plain-text CSV). This allows you to:
- Reuse a peak list across multiple specimens in the same or different projects.
- Keep reference peak lists for common mineral assemblages.

**Export** saves only the selected markers (select rows in the list before clicking Export). If nothing is selected, nothing is saved.

**Import** appends the markers from the file to the current specimen. Existing markers are not removed. Duplicate positions are not checked — importing the same file twice adds duplicates.

Markers are also stored inside the `.mud` project file when you do **File → Save Project**.

---

## How Markers Appear on the Plot

For each visible marker within the displayed 2θ range:

- A **connector line** (if Line style is not "None") is drawn from the base point up to the top position. The line inherits the marker's colour and line style.
- A **text label** is drawn at the top of the line. The text is the marker's **Label** field. The label is rotated (default: 90°, i.e., vertical), aligned, and coloured according to the marker's properties.

---

## Relevant Source Files

| Component | File |
|---|---|
| Marker model | `mudlab/specimen/models/markers.py` — `Marker`, `ThresholdSelector`, `MineralScorer` |
| Controllers | `mudlab/specimen/controllers/marker_controllers.py` — `EditMarkerController`, `MarkersController`, `MatchMineralController`, `ThresholdController` |
| Views | `mudlab/specimen/views/markers.py` — `EditMarkerView`, `EditMarkersView`, `MatchMineralsView`, `DetectPeaksView` |
| Plot rendering | `mudlab/generic/plot/plotters.py` — `plot_marker_text()`, `plot_marker_line()`, `plot_markers()` |
| Peak detection | `mudlab/calculations/peak_detection.py` — `peakdetect()`, `scipy_peakdetect()`, `score_minerals()` |
| Line histogram methods | `mudlab/generic/models/lines/mudlab_line.py` — `calculate_npeaks_for()`, `get_best_threshold()`, `calculate_npeaks_for_scipy()`, `get_best_prominence()` |
| Specimen methods | `mudlab/specimen/models/base.py` — `auto_add_peaks()`, `clear_markers()` |
| Mineral database | `mudlab/data/mineral_references.csv` |
| Display defaults | `mudlab/data/settings.py` — `MARKER_*` constants |

---

[← Back to User Manual](../index.md)
