# Anatomy of the MudLab Plot

This page describes the visual components that appear on the main data plot in MudLab.

---

## Overall Layout

The plot area displays one or more **specimens** stacked vertically. When multiple specimens are loaded, they are offset from each other so their patterns do not overlap. Each specimen occupies its own vertical band, which can optionally be split between the pattern area (upper 65%) and a statistics area (lower 35%) when residuals or derivatives are enabled.

---

## Single vs. Multiple Specimen Display

The specimen list on the left side of the window supports both single and multiple selection.

### Single Specimen Selected
Click a single specimen name in the list. Only that specimen's pattern is shown on the plot. All pattern-preparation tools (Smooth, Shift, Strip Peak, Peak Properties, etc.) are available because they operate on a single specimen.

### Multiple Specimens Selected
Hold **Ctrl** and click additional specimens, or hold **Shift** to select a range. All selected specimens are displayed together, stacked vertically with offsets. Pattern-preparation tools that require a single specimen are disabled in this mode.

---

## Specimen Label

Each specimen's name is displayed as a text label to the **left** of the plot area, aligned vertically with that specimen's pattern. The label position can be adjusted in the project settings.

---

## Experimental Pattern

The experimental (measured) XRD pattern is drawn as a line plot when **Display Experimental** is enabled for the specimen. The line colour, width, and style are set in the specimen's experimental pattern properties.

### Tool Previews on the Experimental Pattern

When certain tools are active, temporary overlay lines appear on top of the experimental pattern:

| Tool | Overlay | Colour | Description |
|------|---------|--------|-------------|
| **Smooth** | Smooth preview line | Red (`#cc0000`) | Shows the smoothed version of the pattern. The original pattern is hidden unless "Show Original" is checked. |
| **Add Noise** | Noise preview line | Purple (`#660099`) | Shows the pattern with the specified noise fraction applied. |
| **Shift Pattern** | Shift preview line + Reference line | Pattern colour + Purple (`#660099`) | The preview line shows the pattern shifted by the current shift value. A thin vertical reference line marks the target peak position. |
| **Remove Background** | Background line | Purple (`#660099`) | Shows the background level (flat line or loaded pattern) that will be subtracted. |
| **Strip Peak** | Stripped segment line | Purple (`#660099`) | Shows the replacement segment (linear interpolation + noise) between the start and end positions. |
| **Peak Properties** | Filled area + FWHM line | Purple fill (`#660099`, 40% opacity) + Dark line (`#330033`) | The shaded area shows the integrated peak area above the background baseline. A horizontal line marks the full width at half maximum (FWHM). |

---

## Calculated Pattern

When **Display Calculated** is enabled and a mixture has been set up, the calculated (modelled) pattern is drawn. Its line colour, width, and style are set independently from the experimental pattern.

### Individual Phase Lines

When **Display Phases** is enabled, individual phase contribution lines are drawn beneath the total calculated pattern. Each phase line uses the **display colour** of the corresponding Phase object, making it easy to identify which phase contributes to which part of the diffraction pattern.

---

## Markers

Markers are vertical lines at specific 2-theta positions, used to label peaks. Each marker has:

- A **vertical line** whose base can be anchored to the x-axis, the experimental pattern, the calculated pattern, the minimum of both, or the maximum of both.
- A **text label** above the line showing the peak identification (e.g., d-spacing, mineral name).

Markers are created by the peak detection tool or added manually.

---

## Mineral Preview Sticks

When browsing the mineral match results, **preview stick patterns** appear as vertical magenta lines (`#FF00FF`). Each stick represents a reference peak for the candidate mineral, positioned at the corresponding 2-theta value with height proportional to relative intensity (scaled 0-100%).

---

## Exclusion Ranges

Exclusion ranges are regions of the pattern that are excluded from refinement. They appear as **hatched rectangular areas** spanning the full height of the specimen's plot band, bounded by vertical lines on the left and right edges.

---

## Residual Pattern (Statistics Area)

When **Display Residuals** is enabled and a calculated pattern exists, the lower 35% of the specimen's vertical band shows the **residual pattern** (difference between experimental and calculated). The residual is plotted centred on its own zero line, so positive and negative deviations are visible. A user-adjustable scale factor controls the vertical magnification.

### Derivative Patterns

When **Display Derivatives** is enabled, derivative patterns of the experimental, calculated, and residual are drawn in the same statistics area (at 65% opacity), useful for comparing peak shapes and positions.

---

## Mixture Legend (Upper-Right Corner)

When one or more mixtures are defined, a **mixture legend** appears in the upper-right corner of the plot. It is structured as follows:

### Title Row
The mixture name (e.g., "Mix 1"), followed by transparent placeholder boxes for alignment.

### Phase Rows
Each row represents one **phase slot** in the mixture and displays:

1. **Text label** — the phase name and its weight fraction as a percentage (e.g., `Illite:  45.0`).
2. **Coloured boxes** — one box per **specimen** in the mixture. Each box is filled with the **display colour** of the Phase object assigned to that specimen-phase cell in the mixture matrix.

For example, if a mixture has 2 specimens and 3 phases, the legend shows 3 phase rows, each with up to 2 coloured boxes. A box is omitted if no phase is assigned in that cell (`None`).

The coloured boxes let you visually match each phase's contribution line on the plot to its entry in the legend, and see at a glance which phase objects are assigned across specimens.

---

## Mouse Interaction

### Zooming

| Action | Effect |
|--------|--------|
| **Scroll wheel** | Zoom in/out on the x-axis, centred on the cursor position |
| **Ctrl + Scroll** | Zoom in/out on the y-axis, centred on the cursor position |

Zooming is clamped so you cannot zoom out past the full extent of the data.

### Panning

| Action | Effect |
|--------|--------|
| **Shift + Scroll** | Pan left/right along the x-axis (10% of visible range per scroll step) |
| **Left / Right arrow keys** | Pan left/right along the x-axis |

Panning is clamped so the view cannot scroll beyond the data range.

### Resetting the View

| Action | Effect |
|--------|--------|
| **Right-click** on the plot | Reset both x and y axes to the full (home) view |

---

## Crosshair Cursor

The crosshair is a dashed vertical line that follows the mouse pointer across the plot. It is toggled on and off using the **Crosshair** toolbar button.

When the crosshair is enabled:
- A thin dashed vertical line (`#555555`) tracks the cursor's x-position across the plot.
- **Left-click and drag** highlights a region of all visible patterns between the start and end x-positions with an orange overlay (`#FF6600`, 45% opacity). Releasing the mouse button clears the highlight. This is useful for visually isolating a 2-theta range of interest.
- While the drag is in progress, the status bar switches from the point readout to a **range readout** showing the absolute width of the highlighted interval:

  ```
  Δ 2θ= 2.50 °    Δ d= 0.08 nm
  ```

  In multi-specimen mode, the Δd value is followed by an asterisk (`Δ d= 0.08* nm`), same convention as the point readout — the Δd is computed from the first specimen in the selection order. The range display turns on as soon as the drag starts and reverts to the normal point readout the moment the mouse button is released.

---

## Status Bar

The status bar is located at the bottom of the plot area and displays live information as the mouse moves over the plot. Its content depends on whether a single specimen or multiple specimens are selected.

### Single Specimen Mode

When one specimen is selected, the status bar shows:

```
2θ= 12.34 °    d= 0.72 nm    Ie= 1234    Ic=  987
```

| Field | Meaning |
|-------|---------|
| **2θ** | The 2-theta angle at the cursor position (degrees) |
| **d** | The d-spacing converted from the cursor's 2-theta using the selected specimen's goniometer wavelength (nm) |
| **I_e** | The experimental pattern intensity at the cursor position |
| **I_c** | The calculated pattern intensity at the cursor position (shown only when a calculated pattern is displayed in FULL layout mode) |

### Multiple Specimen Mode

When multiple specimens are selected, the status bar shows:

```
2θ= 12.34 °    d= 0.72* nm
```

| Field | Meaning |
|-------|---------|
| **2θ** | The 2-theta angle at the cursor position (degrees) |
| **d\*** | The d-spacing, followed by an asterisk (**\***). The **\*** indicates that the d-value is computed from the **first** specimen in the current selection (since different specimens may have different goniometer wavelengths, only one can be shown). |

Intensity values (I_e, I_c) are not displayed in multi-specimen mode because multiple overlapping patterns make a single intensity reading ambiguous.

### Changing Which Specimen's d-spacing is Shown

In multi-specimen mode, the d-value always comes from the **first specimen in the selection order**. To change which specimen's goniometer is used for the d-spacing calculation, change the selection order:

1. Click on the specimen you want to use for d-spacing first.
2. Then **Ctrl+click** the remaining specimens.

The first-clicked specimen becomes the first in the selection list, and its goniometer wavelength is used for the d-spacing conversion displayed in the status bar.

---

## Axis Labels

- **X-axis**: 2-theta angle in degrees, with adaptive major and minor tick marks.
- **Y-axis**: Intensity (counts or normalised, depending on project settings).
