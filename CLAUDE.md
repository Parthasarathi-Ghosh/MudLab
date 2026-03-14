# PyXRD – Claude Instructions

## Project Overview
PyXRD is a Python application for X-ray diffraction analysis of disordered layered minerals.

**Current active source path:** `data/lib/python3.14/site-packages/pyxrd/`

## Repository
- GitHub: KazukiNoSuzaku/PyXRD (fork: KazukiNoSuzaku/PyXRD.clays)
- Main branch: `main`
- Active working branch: `V8`

## Architecture
- **Bundled distribution:** The app ships its own Python runtime. Everything needed to run is inside `data/`.
  - Binaries/DLLs: `data/bin/`
  - Python stdlib + site-packages: `data/lib/python3.14/`
  - Launcher executable: `data/bin/pyxrd-cmd.exe` (calls `data/lib/python3.14/.../pyxrd/__main__.py`)
- **MVC framework:** `data/lib/python3.14/site-packages/mvc/` — internal framework derived from pygtkmvc
- **GTK3 UI:** Glade XML files in each module's `glade/` subfolder; loaded by `BaseView` subclasses
- **Key packages:** numpy, scipy, matplotlib, GTK3 via PyGObject (all from MSYS2 MinGW64)

## Key Module Layout (under `data/lib/python3.14/site-packages/pyxrd/`)
```
pyxrd/
  calculations/       # Core math: peak_detection.py, math_tools.py, phases.py, specimen.py, mixture.py
  specimen/
    models/markers.py      # Marker, ThresholdSelector, MineralScorer models
    controllers/marker_controllers.py  # EditMarkerController, MarkersController, MatchMineralController, ThresholdController
    views/markers.py       # EditMarkerView, DetectPeaksView, MatchMineralsView
  phases/
    models/phase.py
    views.py
  mixture/
    views/edit_mixture_view.py
    views/edit_insitu_mixture_view.py
  generic/
    plot/plotters.py       # Matplotlib rendering (AnchoredOffsetbox, etc.)
    plot/controllers.py
    io/data_registry.py
  data/settings.py         # App settings; uses DummyAsyncServerProvider (Pyro4 disabled)
  core.py                  # Entry point, GTK path setup for Windows
```

## Key Decisions
- **Pyro4 removed.** The Pyro4 package, serpent, msgpack, and ordered_set were deleted from
  `site-packages` in V8 — they are not needed. `pyxrd/data/settings.py` uses only
  `DummyAsyncServerProvider`. Do not re-add Pyro4 unless explicitly asked.
- **importlib.resources** is used everywhere instead of `pkg_resources.resource_filename`.
  Pattern: `import importlib.resources as _ir; resource_filename = lambda pkg, path: str(_ir.files(pkg).joinpath(path))`

## Commit Message Format
Always use `HHMMddmmyyyy` using the current system time (e.g. `011920022026` = 01:19 on Feb 20 2026).

## Watch Out For
- A linter may silently revert file edits. Always run `git diff` to confirm a change stuck before committing.
- The `data/lib/python3.14/` path contains both `.py` source files and `.pyc` compiled files — edit only the `.py` files.
- `__pycache__` `.pyc` files show as untracked in `git status` constantly — ignore them, do not stage or commit them.
- When testing, always relaunch `data\bin\pyxrd-cmd.exe` from scratch — Python bytecache means old code runs if the process isn't restarted.

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
- New launcher in `launcher/pyxrd_launcher.c` using `PyConfig` API (Python 3.12+)
- `data/bin/` DLLs replaced with 64-bit MSYS2 versions
- `pyxrd.iss` and `build-installer.yml` updated for python3.14 paths

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
- `scipy.stats.linregress()` no longer accepts 2D arrays — now called with explicit x/y columns:
  `stats.linregress(p_matches[:, 0], p_matches[:, 1])` (peak_detection.py)

### matplotlib breaking changes
- `hist(..., normed=1, ...)` → `hist(..., density=True, ...)` (phases/views.py)
- `AnchoredOffsetbox.remove()` raises `NotImplementedError` — caught alongside `ValueError` (plotters.py)
- `get_renderer()`, `NavigationToolbar` signature, `Bbox.inverse_transformed` — fixed in generic/plot/controllers.py

### numpy array resize
- `.resize(shape)` → `.resize(shape, refcheck=False)` for `phase_combos` and `behav_combos`
  (mixture/views/edit_mixture_view.py, mixture/views/edit_insitu_mixture_view.py)

### Python syntax fixes
- `return` in `finally` block → try/except (mvc/support/collections/weak_list.py)
- Invalid escape sequences `\D`, `\P` in docstrings (data/appdirs.py — Win10+ paths only now)
- Invalid escape `\s` in math_text string → raw string `r"$\sigma^*$ [°]"` (phases/models/phase.py)

### Logic fixes
- `sorted()` result not assigned — two occurrences (specimen/models/markers.py lines 70, 102)
- Peak match threshold `> 3` → `>= 2` (peak_detection.py) — was too strict, ignoring valid matches
- `markers_to_use = self.get_selected_objects() or list(self.model.markers)` — fallback when no markers selected (marker_controllers.py)
- Explicit `btn.connect("clicked", self.on_auto_match_clicked)` in `MatchMineralController.register_view` — fallback for glade signal wiring (marker_controllers.py)
- score_minerals single-peak path: removed `elif i == 0: break` that skipped all minerals; added `min_peaks_needed`; added positional-accuracy scoring for single match; added `np.unique` guard on intensity linregress (peak_detection.py)

### Refinement fixes
- `NavigationToolbar(self.canvas)` — removed deprecated `window` argument (refinement/views/refiner_view.py)
- `MAXFUN = 500`, `MAXITER = 150`, `IPRINT = -1` — lowered from 15000; L-BFGS-B with nested `optimize_mixture()` is extremely expensive; IPRINT=-1 suppresses Fortran stdout writes that can crash on Windows (refinement/methods/scipy_runs.py)
- Root crash fix: `GLib.MainContext.default().find_source_by_id()` is not thread-safe — was called from the refinement background thread via MVC signal chain (`apply_solution` → property setter → `visuals_changed` signal → `__notify_observer__` → `add_idle_call`). Fixed in `mvc/adapters/gtk_support/toolkit_functions.py`: call `GLib.idle_add()` (thread-safe) always, but only call `find_source_by_id()` from the main thread. Added `None` guard to `remove_source()`.
- `except (IndexError, TypeError)` in `get_history_residual()` — fmin_l_bfgs_b returns a plain float residual; Python 3 raises `TypeError` (not `IndexError`) when indexing a float (refinement/refiner.py)
- `faulthandler.enable()` added to `core.py` — prints C-level stack trace on native crashes
- `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1` env vars set in `core.py` before numpy import

### Unicode logging fix
- `SafeStreamHandler` class in `logs.py` — encodes each log message through the stream's codec with `errors='replace'` before writing; `reconfigure()` does not work on Windows console streams
- σ encoded to ASCII at source in `refiner.py` log message (`encode('ascii', errors='replace')`)

### Other fixes
- `imp.load_source` → `importlib.util` (mixture/models/insitu_mixture.py)
- `inspect.getargspec` → `getfullargspec` (mvc/models/base.py, mvc/models/properties/labeled_property.py)
- Windows GTK path setup block added to `core.py` (`os.add_dll_directory`, `GI_TYPELIB_PATH`, `GDK_PIXBUF` paths)

---

## Current Status (as of 2026-03-14, V8 branch)
- App launches cleanly, no warnings
- Project files open successfully
- Edit Phases dialog: works
- Edit Mixtures dialog: works
- Find Peaks: works
- Match Minerals / Auto Match: works (single and multiple peak selections)
- Refinement (L-BFGS-B): works — completes without crash and shows results dialog
- Codebase cleaned: python3.8 tree removed, Pyro4 and unused packages deleted
