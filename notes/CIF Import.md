# CIF Import

Source: `mudlab/phases/models/phase.py` (`Component.parse_cif_for_import`, `Component.build_from_import_result`)  
View: `mudlab/phases/views.py` (`CifImportDialog`)  
Controller: `mudlab/phases/controllers/component_controllers.py` (`ComponentsController._import_from_cif`)

CIF (Crystallographic Information File) import lets you populate a component's atom list from a `.cif` file instead of entering atoms manually.

## Trigger

In Edit Phases → Components tab → click **Import** → select a `.cif` file.

## Two-step workflow

### Step 1 — Parse

`Component.parse_cif_for_import()` reads the CIF and finds every `_atom_site_label` loop that contains `_atom_site_fract_z`. It groups atoms into **blocks** (one block per crystallographic data block in the CIF).

Atoms with `_atom_site_symmetry_multiplicity` in a P1 cell will have `pn` summed from repeated sites at the same (element, z) position (tolerance `_Z_TOL = 1e-4`).

**pn (Multiplicity)** — "projected number" = number of atoms projected onto the c-axis per unit cell. For P1 symmetry this equals the sum of occupancies across symmetry-equivalent sites.

### Step 2 — Dialog (`CifImportDialog`)

For each CIF block, a dialog opens showing:

- **Plot** — atoms plotted as horizontal lines at their z-position (Å). Labels show element and multiplicity, e.g. `O ×4`.
- **Table** — editable rows: Name, Atom type (element), z (Å), pn (Multiplicity), Assignment (Layer / Interlayer / Skip)

The **threshold slider** sets the z-value that splits layer atoms (below) from interlayer atoms (above). Atoms assigned "Skip" are excluded.

The **Atom type column** offers a combo to map each atom to an existing `AtomType` in the project (for ionic variants, e.g. Fe²⁺ vs Fe³⁺).

### Step 3 — Build

`Component.build_from_import_result()` creates `Atom` objects from the confirmed assignments and appends them to the component's `layer_atoms` or `interlayer_atoms` list.

## Replacement vs. append

- If components are **selected** in the list before importing, the import **replaces** those components (same-count rule).
- If nothing is selected, new components are **appended**.

## Related Notes

- [[Phase and Component Model]]
- [[Atom Relations]]
- [[GTK UI Conventions]]
