# File Formats

Source: `mudlab/generic/io/`, `mudlab/generic/io/json_codec.py`  
Docs: `docs/how-to/file-formats.md`, `docs/how-to/project-file-format.md`

## Project file — `.mud`

JSON-based archive. Loaded and saved by the main application window.

Old files saved as `.pyxrd` still open via the **MudLabLine shim** in `json_codec.py`, which remaps type strings:

```python
"pyxrd.PyXRDLine" → "mudlab.MudLabLine"
"PyXRD.*"         → "MudLab.*"
```

### Structure

```
project.mud  (JSON)
  ├── specimens[]
  │     ├── experimental pattern (2θ, intensity)
  │     └── markers[]
  ├── phases[]
  │     └── components[]
  │           ├── layer_atoms[]
  │           ├── interlayer_atoms[]
  │           └── atom_relations[]
  └── mixtures[]
```

## Phase file — `.phs`

Exported/imported from the Edit Phases dialog. Contains one or more serialised `Phase` objects. Used to transfer phases between projects or share treatment variants (AD/EG/350).

## Component file — `.cmp`

Single-component export. Contains a serialised `Component` object including all atoms and relations.

## CIF file — `.cif`

Standard Crystallographic Information File. Imported via the CIF import dialog to populate atom lists. See [[CIF Import]].

Exported from the Components dialog: `Component.save_as_cif()`.

## Pattern data formats

Experimental XRD patterns loaded from:
- `.rd` / `.RAW` — Siemens/Bruker binary
- `.xrdml` — PANalytical XML
- `.chi`, `.dat`, `.txt` — various ASCII column formats
- `.asc` — ASCII

Loaded by `mudlab/generic/io/data_registry.py` using a registry of format parsers.

## Atomic scattering factors table — `.atl`

`atomic scattering factors.atl` — shipped with MudLab, loaded by `data_registry`. Contains Cromer-Mann coefficients (a₁–a₄, b₁–b₄, c) for each element and ionic species. Used in [[XRD Diffraction Calculation]].

## importlib.resources

All bundled data files (glade, atl, icons) are located using:

```python
import importlib.resources as _ir
resource_filename = lambda pkg, path: str(_ir.files(pkg).joinpath(path))
```

This replaced `pkg_resources.resource_filename` across 21 files during the Python 3.14 upgrade.

## Related Notes

- [[MudLab Overview]]
- [[CIF Import]]
- [[XRD Diffraction Calculation]]
- [[Architecture]]
