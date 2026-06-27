# MudLab – Claude Instructions

## Project Overview
MudLab is a Python desktop application for **X-ray diffraction (XRD) analysis of disordered layered minerals** (clays, micas, mixed-layer silicates). It models stacking disorder and refines structural parameters against measured diffraction patterns.

**Current active source path:** `data/lib/python3.14/site-packages/mudlab/`

## Repository
- GitHub: Parthasarathi-Ghosh/MudLab
- Main branch: `main`
- Active working branch: `V18`

---

## Architecture
- **Bundled distribution:** The app ships its own Python runtime. Everything needed to run is inside `data/`.
  - Binaries/DLLs: `data/bin/`
  - Python stdlib + site-packages: `data/lib/python3.14/`
  - Launcher executable: `data/bin/mudlab-cmd.exe` (calls `data/lib/python3.14/.../mudlab/__main__.py`)
  - GUI launcher: `data/bin/mudlab.exe` (no console window)
- **MVC framework:** `data/lib/python3.14/site-packages/mvc/` — internal framework derived from pygtkmvc
  - `mvc.Model` — observable properties; `@Controller.observe("prop", assign=True)` triggers on change
  - `mvc.View` — wraps a GTK widget tree loaded from a Glade XML file
  - `mvc.Controller` — subscribes to model changes; wires GTK signal handlers
- **GTK3 UI:** Glade XML files in each module's `glade/` subfolder; loaded by `BaseView` subclasses
- **Key packages:** numpy, scipy, matplotlib, GTK3 via PyGObject (all from MSYS2 MinGW64)

## Key Module Layout (under `data/lib/python3.14/site-packages/mudlab/`)
```
mudlab/
  calculations/       # Core math: peak_detection.py, math_tools.py, phases.py, specimen.py, mixture.py
  atoms/              # AtomType model; atomic scattering factors table (.atl)
  phases/
    models/phase.py               # Phase, Component, Atom models
    models/atom_relations.py      # AtomRatio, AtomContents
    views.py                      # EditPhaseView, CifImportDialog
    controllers/component_controllers.py
    controllers/atom_relation_controllers.py
    glade/phase.glade, component.glade, ...
  specimen/
    models/markers.py             # Marker, ThresholdSelector, MineralScorer
    controllers/marker_controllers.py
    views/markers.py
    glade/edit_marker.glade, find_peaks.glade, ...
  mixture/
    views/edit_mixture_view.py
    views/edit_insitu_mixture_view.py
  refinement/
    methods/scipy_runs.py         # L-BFGS-B wrapper
    views/refiner_view.py
    views/glade/refine_results.glade
  generic/
    views/__init__.py             # BaseView, DialogView, ObjectListStoreView hierarchies
    views/line_views.py           # BackgroundView, SmoothDataView, ShiftDataView, etc.
    views/glade/edit_dialog.glade # Shared dialog window (1050×750 default)
    views/glade/object_store.glade
    views/glade/inline_ols.glade
    plot/plotters.py
    plot/controllers.py
    io/data_registry.py
    io/json_codec.py              # MudLabLine shim for old .pyxrd files
  data/settings.py                # App settings; uses DummyAsyncServerProvider (Pyro4 disabled)
  core.py                         # Entry point, GTK path setup for Windows
```

---

## Scientific Model

### Object hierarchy
```
Project
  ├── specimens[]        — measured XRD patterns + markers
  ├── phases[]           — crystallographic layer types
  │     └── components[] — one layer type each (G components per phase)
  │           ├── layer_atoms[]
  │           ├── interlayer_atoms[]
  │           └── atom_relations[]
  └── mixtures[]         — maps phase fractions/scales to each specimen
```

### Phase
- `d001` — basal spacing (Å); `delta_c`, `default_c`, `sigma_star`
- `G` — number of layer types; `R` — Reichweite (stacking correlation order)
- `based_on` — optional parent phase to inherit CSDS/σ* from (used for treatment variants: AD → EG, 350°C)
- Setting `based_on` clears all component `linked_with` links unconditionally to prevent stale references

### Component
- `cell_a`, `cell_b` — lateral cell dimensions (Å); `ucp_a`, `ucp_b` — refinable wrappers
- `layer_atoms`, `interlayer_atoms` — lists of `Atom` objects
- `atom_relations` — list of `AtomRatio` / `AtomContents` objects
- `linked_with` — optional link to a component in the `based_on` phase; enables per-property inherit checkboxes

### Atom
- `name`, `atom_type` (→ AtomType with Cromer-Mann coefficients), `pn`, `z`, `default_z`, `stretch_z`
- `pn` = "projected number" — atom count projected onto c-axis per unit cell (occupancy × multiplicity)
- There is **no `B_iso` on Atom**. The Debye-Waller factor lives on `AtomType` as `debye` — it is per element/ion type, loaded from `atomic scattering factors.atl`, and is not a per-atom refinable parameter.

### Atom Relations (models/atom_relations.py)
Applied reactively via MVC observers before each structure-factor calculation (`Component._apply_atom_relations()`).

**AtomRatio** — binary substitution at a shared site:
```
atom1.pn = value × sum
atom2.pn = (1 − value) × sum
```
`value` is refinable [0,1]; `sum` is fixed total site occupancy.

**AtomContents** — absolute occupancy:
```
atom.pn = amount × value
```
`amount` is user-defined [0, ∞), default 0.0; `value` is refinable. Both relation types can chain: their SUM/RATIO properties can be targeted by other relations' dropdowns.

### Mixture
- Matrix of `(fraction, scale)` per `(specimen, phase)` pair
- `auto_scales` — recomputed by linear regression each refinement step
- `auto_background` — background polynomial recomputed analytically
- Total calculated pattern: `y_calc = Σ_phases (fraction_p × scale_p × I_phase) + background`

---

## XRD Calculation Pipeline
Source: `calculations/` — `atoms.py`, `components.py`, `phases.py`, `specimen.py`, `mixture.py`

All arrays are functions of `stl = 2 sin(θ) / λ` (Å⁻¹).

```
atom positions + pn (modified by atom_relations)
  → ASF = c + Σ aᵢ exp(−bᵢ s)          Cromer-Mann (s = (stl×0.05)²)
  → f   = ASF × exp(−B_iso × s)         Debye-Waller
  → F_atom = f × pn × exp(2πi z stl)
  → F_comp = Σ F_atom                   structure factor per component
  → CSDS distribution × Q-matrix powers → phase intensity I(stl)
  → Lorentz-polarisation + goniometer corrections + Kα1/Kα2 splitting
  → × fraction × scale + background
  → Rp / Rwp residual vs. observed
```

Cromer-Mann coefficients loaded from `atomic scattering factors.atl` via `data_registry`.

---

## Refinement
Source: `refinement/methods/scipy_runs.py`, `refinement/refiner.py`

- Algorithm: **L-BFGS-B** (`scipy.optimize.fmin_l_bfgs_b`)
- `MAXFUN=500`, `MAXITER=150`, `IPRINT=-1` (suppresses Fortran stdout — avoids Windows crash)
- Runs in a background thread; GTK loop stays responsive; completion via `GLib.idle_add`
- `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1` set in `core.py`
- Results dialog (`refine_results.glade`): Best / Last / Initial buttons; Show Plot opens parameter-space window

---

## GTK UI Conventions

### View class hierarchy
```
BaseView
  ├── DialogView          ← loads edit_dialog.glade (GtkWindow, 1050×750 default, no type_hint)
  │     ├── ObjectListStoreView     ← left list + right editor, used for Edit Phase / Edit Mixture
  │     └── small tool dialogs     ← BackgroundView, SmoothDataView, AddNoiseView,
  │                                   StripPeakView, CalculatePeakPropertiesView, TrimView
  │                                   — all call set_default_size(-1, -1) to auto-size to content
  └── InlineObjectListStoreView    ← compact lists (layer/interlayer/atom relations boxes)
```

### Key glade templates
| File | Used for |
|---|---|
| `generic/views/glade/edit_dialog.glade` | All `DialogView` windows — 1050×750, no `type_hint` (gives maximize/restore on Windows) |
| `generic/views/glade/object_store.glade` | HPaned left-list + right-editor layout |
| `generic/views/glade/inline_ols.glade` | Layer atoms, interlayer atoms, atom relations inline lists |
| `generic/views/glade/lines/shift_dialog.glade` | Shift Pattern — own window, auto-sizes to content |
| `refinement/views/glade/refine_results.glade` | Refinement results — 900×700, no `type_hint` |

### Scrollbar policy — always use classic mode
```xml
<property name="vscrollbar_policy">automatic</property>
<property name="overlay_scrolling">False</property>
```
Overlay scrollbars appear on top of adjacent widgets (dropdowns, pencil buttons) and are disruptive.

### Preventing over-tall spin buttons
When a `GtkSpinButton` shares a table row with a taller widget, wrap it in `GtkAlignment` with `yscale=0`:
```xml
<object class="GtkAlignment">
  <property name="yalign">0.5</property>
  <property name="yscale">0</property>
  <child><object class="GtkSpinButton" .../></child>
</object>
```

### Component list height (object_store.glade)
`frm_objects_tv`: `vexpand=False`, `expand=False` (packing). Scrolled window: `propagate_natural_height=True`, `max_content_height=300`. Prevents the component name list from stretching when the right panel grows on selection.

### Window type hint
Omitting `type_hint` gives standard window decoration (minimize/maximize/close) on Windows; setting `type_hint=dialog` removes the minimize and maximize buttons (Close stays, window still drag-resizable).

**Intentional exception — Edit Phases / Edit Mixtures.** These three views (`EditPhaseView`, `EditMixtureView`, `EditInSituMixtureView`) set the class attribute `window_type_hint = "DIALOG"` (applied in `BaseView.__init__` via `set_type_hint`). Their glade "top" widget is a `GtkTable`/`GtkVBox` (the MVC framework wraps it in a window), so the hint is set programmatically, not in glade. This drops min/max **on purpose**: the dialogs are `transient_for` the main window, so minimizing them used to also minimize the main window. On-top behavior and the live plot updates are unaffected (transient/model signals are independent of `type_hint`). Do not "restore" maximize on these by removing the hint.

### Small tool dialogs
`BackgroundView`, `SmoothDataView`, `AddNoiseView`, `StripPeakView`, `CalculatePeakPropertiesView`, `TrimView` all inherit `edit_dialog.glade`'s 1050×750 default. Each overrides it in `__init__`:
```python
self.get_toplevel().set_default_size(-1, -1)
```
This auto-sizes to content, matching `ShiftDataView` (which uses its own glade with no fixed size).

---

## CIF Import
Source: `phases/models/phase.py`, `phases/views.py` (`CifImportDialog`), `phases/controllers/component_controllers.py`

- `Component.parse_cif_for_import()` — finds `_atom_site_label` loops with `_atom_site_fract_z`; groups atoms by (element, z) within tolerance `_Z_TOL=1e-4`; sums occupancies into `pn`
- `pn` ("projected number" / Multiplicity) = atoms projected onto c-axis per unit cell
- Dialog shows a plot (atoms as horizontal lines labelled `O ×4` etc.) and an editable table
- Threshold slider splits layer vs. interlayer atoms
- `Component.build_from_import_result()` creates `Atom` objects from confirmed assignments

---

## File Formats
- **`.mud`** — project file (JSON); loads old `.pyxrd` files via MudLabLine shim in `json_codec.py`
- **`.phs`** — phase export/import (one or more serialised Phase objects)
- **`.cmp`** — single component export
- **`.cif`** — CIF import (atoms) and export (`Component.save_as_cif()`)
- **Pattern formats:** `.rd`/`.RAW` (Bruker), `.xrdml` (PANalytical), `.chi`/`.dat`/`.txt`/`.asc` (ASCII)
- **`atomic scattering factors.atl`** — Cromer-Mann coefficients table, loaded by `data_registry`

---

## Key Decisions
- **Pyro4 removed.** Deleted in V8 — do not re-add. `mudlab/data/settings.py` uses only `DummyAsyncServerProvider`.
- **importlib.resources** everywhere instead of `pkg_resources.resource_filename`.
  Pattern: `import importlib.resources as _ir; resource_filename = lambda pkg, path: str(_ir.files(pkg).joinpath(path))`
- **MudLabLine shim:** `mudlab/generic/io/json_codec.py` remaps old `pyxrd.*` type strings on load.
- **notes/** folder at repo root — Obsidian vault with 11 concept notes (Overview, Architecture, XRD Calculation, Phase/Component Model, Atom Relations, CIF Import, Mixture Model, Refinement, Markers/Peak Detection, GTK UI Conventions, File Formats).

## Commit Message Format
Always use `HHMMddmmyyyy` using the current system time (e.g. `011920022026` = 01:19 on Feb 20 2026).

## Watch Out For
- A linter may silently revert file edits. Always run `git diff` to confirm a change stuck before committing.
- The `data/lib/python3.14/` path contains both `.py` source files and `.pyc` compiled files — edit only the `.py` files.
- `__pycache__` `.pyc` files show as untracked in `git status` constantly — ignore them, do not stage or commit them.
- When testing, always relaunch `data\bin\mudlab-cmd.exe` from scratch — Python bytecache means old code runs if the process isn't restarted.

---

## Current Status (as of V18 branch, 2026-05-15)
- App launches cleanly, no warnings
- Project files open successfully (`.mud` and legacy `.pyxrd`)
- Edit Phases dialog: works — including CIF import with pn multiplier labels in plot
- Edit Mixtures dialog: works
- Find Peaks / Match Minerals / Auto Match: works
- Refinement (L-BFGS-B): works — completes without crash, shows results dialog
- Parameter space plot popup: works, fully interactive
- All main dialogs: 1050×750, maximize/restore buttons present (no `type_hint=dialog`)
- Small tool dialogs (Shift Pattern, Remove Background, Smooth Data, Add Noise, Strip Peak, Calculate Peak Properties, Trim): auto-size to content
- Refinement log: classic scrollbar (`overlay_scrolling=False`)
- Marker Position spin boxes: compact height (wrapped in `GtkAlignment yscale=0`)
- Component name list: fixed natural height (no vexpand)
- Mouse zoom/pan on main plot: Ctrl+scroll=zoom, Shift+scroll=pan, right-click=reset
- Adaptive 2θ tick marks with minor subdivisions

---

## MudLab Rebrand (2026-03-29, V12 branch)
- Full rename from PyXRD.clays → MudLab across all source, config, and docs
- Package directory renamed: `site-packages/pyxrd/` → `site-packages/mudlab/`
- All class names updated: `PyXRDLine→MudLabLine`, `PyXRDModel→MudLabModel`, etc.
- File extension: `.pyxrd` → `.mud` (old files still load via shim)
- Executables: `pyxrd.exe/pyxrd-cmd.exe` → `mudlab.exe/mudlab-cmd.exe`
- Repository relocated: KazukiNoSuzaku/PyXRD.clays → Parthasarathi-Ghosh/MudLab

---

## V8 Cleanup (2026-03-14)
- `data/lib/python3.8/` deleted entirely (5,700+ files) — only python3.14 runtime remains
- `Pyro4`, `serpent`, `msgpack`, `ordered_set` removed from `python3.14/site-packages`
- `debug_matches.py` removed (leftover debug script)

---

## Python 3.14 Upgrade — Completed Fixes (V7 branch)

The bundled Python was upgraded from **3.8 → 3.14.3** (MSYS2 MinGW64). All fixes below are already applied.

### Infrastructure
- MSYS2 MinGW64 used for pre-built PyGObject/GTK3 + numpy/scipy/matplotlib
- New launcher in `launcher/mudlab_launcher.c` using `PyConfig` API (Python 3.12+)
- `data/bin/` DLLs replaced with 64-bit MSYS2 versions
- `mudlab.iss` and `build-installer.yml` updated for python3.14 paths

### pkg_resources → importlib.resources (21 files)
All `from pkg_resources import resource_filename` calls replaced. Affected files include:
`core.py`, `generic/io/data_registry.py`, all view files (`phases/views.py`, `project/views.py`,
`generic/views/__init__.py`, `generic/plot/controllers.py`, `mixture/views/*.py`,
`specimen/views/*.py`, `refinement/views/*.py`, `probabilities/views.py`,
`atoms/views.py`, `application/views.py`, `goniometer/views.py`)

### NumPy 2.0 breaking changes
- `np.complex_` / `np.complex` → `np.complex128` (math_tools.py, phases.py)
- `np.float_` → `np.float64` (specimen.py)
- `np.Inf` → `np.inf` (peak_detection.py — 7 occurrences)

### scipy breaking changes
- `scipy.integrate.trapz` → `trapezoid` (generic/models/lines/experimental_line.py)
- `scipy.stats.linregress()` no longer accepts 2D arrays — now called with explicit x/y columns

### matplotlib breaking changes
- `hist(..., normed=1, ...)` → `hist(..., density=True, ...)` (phases/views.py)
- `AnchoredOffsetbox.remove()` raises `NotImplementedError` — caught alongside `ValueError` (plotters.py)
- `get_renderer()`, `NavigationToolbar` signature, `Bbox.inverse_transformed` — fixed in generic/plot/controllers.py

### numpy array resize
- `.resize(shape)` → `.resize(shape, refcheck=False)` for `phase_combos` and `behav_combos`

### Python syntax fixes
- `return` in `finally` block → try/except (mvc/support/collections/weak_list.py)
- Invalid escape sequences `\D`, `\P` in docstrings (data/appdirs.py)
- Invalid escape `\s` → raw string `r"$\sigma^*$ [°]"` (phases/models/phase.py)

### Logic fixes
- `sorted()` result not assigned — two occurrences (specimen/models/markers.py lines 70, 102)
- Peak match threshold `> 3` → `>= 2` (peak_detection.py)
- `markers_to_use = self.get_selected_objects() or list(self.model.markers)` fallback (marker_controllers.py)
- Explicit `btn.connect("clicked", self.on_auto_match_clicked)` in `MatchMineralController.register_view`
- score_minerals single-peak path: removed `elif i == 0: break`; added `min_peaks_needed`; positional-accuracy scoring; `np.unique` guard on linregress

### Refinement fixes
- `NavigationToolbar(self.canvas)` — removed deprecated `window` argument
- `MAXFUN=500`, `MAXITER=150`, `IPRINT=-1` — lowered from 15000
- Root crash fix: `GLib.MainContext.default().find_source_by_id()` not thread-safe — fixed in `mvc/adapters/gtk_support/toolkit_functions.py`
- `except (IndexError, TypeError)` in `get_history_residual()` — fmin_l_bfgs_b returns plain float
- `faulthandler.enable()` added to `core.py`

### Unicode logging fix
- `SafeStreamHandler` class in `logs.py`; σ encoded to ASCII at source in `refiner.py`

### Other fixes
- `imp.load_source` → `importlib.util` (mixture/models/insitu_mixture.py)
- `inspect.getargspec` → `getfullargspec` (mvc/models/base.py, mvc/models/properties/labeled_property.py)
- Windows GTK path setup block added to `core.py`
