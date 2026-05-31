# Architecture

## Runtime layout

MudLab ships a **self-contained Python runtime** — no system Python required.

```
data/
  bin/
    mudlab.exe          ← GUI launcher (no console)
    mudlab-cmd.exe      ← Console launcher
    *.dll               ← GTK3 + NumPy/SciPy DLLs (MSYS2 MinGW64)
  lib/python3.14/
    site-packages/
      mudlab/           ← Application source
      mvc/              ← Internal MVC framework
      gi/               ← PyGObject (GTK3 bindings)
      numpy/ scipy/ matplotlib/
```

Python 3.14 (MSYS2 MinGW64). Upgraded from 3.8 in V7.

## MVC framework

`site-packages/mvc/` — an internal framework derived from **pygtkmvc**.

- `mvc.Model` — observable properties; notifies controllers on change
- `mvc.View` — wraps a GTK widget tree loaded from a Glade XML file
- `mvc.Controller` — subscribes to model changes; wires GTK signal handlers

The framework uses `@Controller.observe("prop_name", assign=True)` decorators to react to property changes. This is the mechanism behind [[Atom Relations]] and live plot updates.

## Module layout

```
mudlab/
  calculations/     ← Core math (peaks, phases, specimen, mixture)
  phases/           ← Phase + Component models, views, controllers
  specimen/         ← Specimen, Marker models, views, controllers
  mixture/          ← Mixture model, Edit Mixture dialog
  atoms/            ← AtomType model and scattering factor table
  refinement/       ← L-BFGS-B refiner, results dialog
  generic/
    views/          ← BaseView, DialogView, glade templates
    plot/           ← Matplotlib canvas, plotters
    io/             ← JSON codec, data registry, file loaders
  data/settings.py  ← App-wide settings (DummyAsyncServerProvider)
  core.py           ← Startup, GTK path setup, faulthandler
```

## GTK UI

Every dialog is defined by a **Glade XML file** (`*.glade`) loaded by a `BaseView` subclass. See [[GTK UI Conventions]].

## Key dependencies

| Library | Use |
|---|---|
| GTK3 / PyGObject | All UI |
| Matplotlib (GTK3Cairo backend) | XRD plot canvas |
| NumPy / SciPy | Array math, peak finding, L-BFGS-B |
| importlib.resources | Locating bundled data files |

`pkg_resources` was replaced by `importlib.resources` across all 21 view files during the Python 3.14 upgrade.

## Related Notes

- [[MudLab Overview]]
- [[GTK UI Conventions]]
- [[XRD Diffraction Calculation]]
- [[Refinement]]
