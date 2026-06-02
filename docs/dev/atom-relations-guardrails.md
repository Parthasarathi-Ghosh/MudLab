# Atom Relations — UI Guardrails

Developer reference for the validation and guardrail layer added to the Atom Relations UI (V18, June 2026).

---

## What was added and where

### 1. AtomRatio Value clamp to [0, 1] — inline list

**File:** `mudlab/phases/controllers/atom_relation_controllers.py`  
**Class:** `EditAtomRelationsController`  
**Method:** `on_item_cell_edited` (new override)

When the user edits the **Value** cell in the Atom Relations list:
- If the row is an `AtomRatio`, the entered value is clamped to `[0.0, 1.0]`.
- A `logger.warning` is emitted naming the relation and the clamped value.
- `AtomContents` rows are left unclamped — their value is a molecule count (e.g. H₂O = 3.5), not a fraction.

### 2. Out-of-range Value shown in red — inline list

**File:** `mudlab/phases/controllers/atom_relation_controllers.py`  
**Class:** `EditAtomRelationsController`  
**Method:** `_reset_treeview` → `data_renderer` closure

The `data_renderer` for the Value column now sets `foreground='#cc0000'` (red) when:
- The row object is an `AtomRatio`, AND
- The current value is outside `[0.0, 1.0]`.

This gives immediate visual feedback before the clamp fires on edit.

### 3. Auto-suggest Sum in the AtomRatio dialog

**File:** `mudlab/phases/controllers/atom_relation_controllers.py`  
**Functions:** `_auto_suggest_sum(controller)` (module-level helper)  
**Triggered by:** `AtomComboMixin.custom_handler` → `on_changed` closure, only when the controller has `_auto_suggest_on_change = True` (set on `EditAtomRatioController`).

When either atom dropdown in the AtomRatio dialog changes:
- If both `atom1` and `atom2` target `.pn` properties (not chained SUM/RATIO channels), AND
- Both atoms have `pn > 0` (non-zero starting occupancy):
- `sum` is auto-set to `atom1.pn + atom2.pn`.

The user can still override sum manually after. The sentinel `_auto_suggest_on_change` prevents this from firing in `EditUnitCellPropertyController`, which reuses the same mixin.

### 4. Loewenstein warning in the AtomRatio dialog

**Files:**
- `mudlab/phases/glade/ratio.glade` — added `GtkLabel id="ratio_loewenstein_warning"` at row 6, spanning both columns, `visible=False` by default. The table `n_rows` was bumped from 6 → 7.
- `mudlab/phases/controllers/atom_relation_controllers.py` — `_check_loewenstein(controller)` helper + `EditAtomRatioController.register_adapters` wires it to the `ratio_value` entry's `changed` signal; also called from the combo `on_changed`.

**Logic:** The label is shown (amber markup text) when ALL of:
- `atom1.atom_type.name.startswith('Al')` (substituting = Al)
- `atom2.atom_type.name.startswith('Si')` (original = Si)
- Both target `.pn` properties
- `value > 0.5`

Loewenstein's rule states no two adjacent tetrahedral sites can both be Al, so Al/Si ≤ 1, meaning the maximum fraction of Al substitution is 0.5. The check is heuristic (based on atom type name prefix) and will miss cases where atom types have non-standard names.

### 5. Red `#` (pn) cell in the atom table

**File:** `mudlab/phases/controllers/layer_controllers.py`  
**Class:** `EditLayerController`  
**Method:** `_setup_treeview`

The `#` (pn) column previously used `add_text_col` with `create_float_data_func()`. It now uses a custom `pn_data_func` that:
- Renders pn as a float string (same format as before).
- Sets `foreground='#cc0000'` (red) when `pn < 0.0`.
- Clears the foreground property otherwise.

This catches the consequence of an out-of-range AtomRatio value immediately in the atom list, even if the user did not interact with the Atom Relations panel during that session.

### 6. Model-level [0, 1] clamp in `AtomRatio.refine_value` — protects refinement

**File:** `mudlab/phases/models/atom_relations.py`  
**Class:** `AtomRatio`

Overrides `AtomRelation.refine_value.setter` to clamp to `[0.0, 1.0]`:

```python
@AtomRelation.refine_value.setter
def refine_value(self, value):
    self.value = max(0.0, min(1.0, float(value)))
```

This is the only guardrail that fires **during refinement**. When L-BFGS-B sets a parameter value via `RefinableWrapper.value.setter → AtomRelation.refine_value`, this clamp intercepts it before the value reaches the model — even if the user has not set `value_min`/`value_max` bounds in the refinement dialog.

**Why AtomRatio only:** `AtomContents.refine_value` is left unclamped. Its value is a count (H₂O = 3.5), not a mole fraction, and must be free above 1.

**Interaction with L-BFGS-B bounds:** If the user also sets `value_min=0.0, value_max=1.0` in the refinement dialog, both the L-BFGS-B bounds (passed to scipy) AND this setter enforce the constraint — double protection. If no bounds are set (defaults = None), only this setter guards the model.

### 7. Warning log in `AtomRatio.apply_relation`

**File:** `mudlab/phases/models/atom_relations.py`  
**Class:** `AtomRatio`  
**Method:** `apply_relation`

Added `import logging` and a module-level `logger`. Before applying, if `value` is outside `[0, 1]`, a `logger.warning` is emitted. This covers the case where value is set programmatically (e.g. driven by another relation or loaded from a file), not via the UI.

---

## 7. Charge balance indicator — Components tab

**Approach inspired by:** pymatgen's `Structure.charge` = `sum(site.species.charge × occupancy for site in structure)`. MudLab's `AtomType.charge` (from the ATL file) is the direct equivalent of pymatgen's `Species.oxi_state` — each ion already carries its formal charge.

**Files changed:**
- `mudlab/phases/models/component.py` — `compute_charge_balance()` (new method)
- `mudlab/phases/glade/component.glade` — `component_charge_balance` GtkLabel at row 14 (full width); `n_rows` 14→15
- `mudlab/phases/controllers/component_controllers.py` — `update_charge_balance()` method; called from `register_adapters()` and `@Controller.observe("data_changed", signal=True)`

**Formula:**
```python
layer_charge     = sum(atom.pn * atom.atom_type.charge for atom in layer_atoms)
interlayer_charge = sum(atom.pn * atom.atom_type.charge for atom in interlayer_atoms)
net              = layer_charge + interlayer_charge   # ≈ 0 for charge-neutral model
```

**Display:**
- Balanced (`|net| ≤ 0.05`): `Charge balance: Layer: −0.66 | Interlayer: +0.66 | Net: 0.00 ✓`  (small grey text)
- Imbalanced: amber `⚠ Charge imbalance: Layer: −0.40 | Interlayer: +0.80 | Net: +0.40`

**Threshold:** `_CHARGE_BALANCE_THRESHOLD = 0.05` per unit cell (class attribute on `EditComponentController`, easy to adjust).

**Data availability:** `AtomType.charge` is populated from the ATL file for all standard ions. Atoms with `atom_type = None` are silently skipped. If no atom types are set (e.g. new empty component), the label shows `—`.

**Pymatgen reference:** The key insight borrowed from pymatgen is that charge is a property of the ion species, not of the atom placement. MudLab already stores this in `AtomType.charge` — no new field needed. The charge balance formula is identical to pymatgen's `Structure.charge` property.

---

## Extension points for future guardrails

### Interlayer sum vs layer charge cross-check
The charge balance indicator shows the net imbalance but does not yet flag the specific mis-configuration (e.g. Ca.pn too low for the octahedral substitution level). A more targeted check could:
1. Compute `expected_interlayer_charge = -layer_charge` (what the interlayer must compensate)
2. Compare with actual interlayer charge
3. Suggest the correct interlayer sum = `|layer_charge| / cation_valence`

This would require knowing which interlayer atoms are charge-compensating cations vs structural atoms (H₂O, F⁻). A heuristic: atoms with `atom_type.charge > 0` in `interlayer_atoms` are cations.

### Amber `pn > expected_max` in atom table
To colour a cell amber when pn exceeds the site maximum, the atom table would need to know the expected max for each atom. Options:
- Store `max_pn` on `Atom` as a persistent property (set by the user or inferred from the driving AtomRatio's `sum`).
- After `_apply_atom_relations`, for each driving AtomRatio, check `atom.pn > ratio.sum` and emit a separate `atoms_out_of_range` signal the view can consume.

### Interlayer charge balance guardrail
See the next section in the doc (layer charge computation discussion). The key challenge is that MudLab has no concept of ion valence attached to AtomType — the charge of each ion type is external crystallographic knowledge, not stored in the model.

---

## 8. Post-refinement validation report (read-only)

**File:** `mudlab/refinement/controllers/refiner_controller.py`  
**Class:** `RefinerController`  
**Methods:** `_build_validation_report()` (new) + `populate_log()` (extended)

After the optimizer completes and `apply_best_solution()` has been called, the refinement results log already shows the parameter table and residuals. A new "Post-refinement Validation" section is now appended to that same log — **read-only, values are never changed**.

**When it runs:** inside `populate_log()`, which is called from `thread_completed` in `RefinementController._launch_refine_thread()`, on the GTK main thread, after the best solution is already applied.

**What it checks (on every component in every phase in the mixture):**

| Check | Pass | Warn |
|---|---|---|
| AtomRatio value in [0, 1] | ✓ printed | ⚠ printed |
| Loewenstein (Si→Al value ≤ 0.5) | ✓ printed | ⚠ printed |
| Any atom pn < 0 | — | ⚠ printed |
| Charge balance \|net\| ≤ 0.05 | ✓ printed | ⚠ printed |

**Output format in the log:**
```
==========================================================
  Post-refinement Validation  (read-only)
==========================================================

  WARNINGS:
  ⚠  [Beidellite / Component 1]  Relation 'Si-Al(tet)': value=0.5123 exceeds 0.5 — Loewenstein's rule violated.
  ⚠  [Montmorillonite / Component 1]  Charge balance: Layer=-0.80  Interlayer=+0.40  Net=-0.40  ⚠ imbalanced

  Passed checks:
     [Beidellite / Component 1]  Relation 'Si-Al(tet)': value=0.2500  ✓  in [0, 1]
     [Beidellite / Component 1]  Charge balance: Layer=-0.80  Interlayer=+0.80  Net=0.000  ✓

  2 warning(s) above — values were NOT changed by this check.
==========================================================
```

**Thresholds (class attributes, easy to adjust):**
- `_CHARGE_BALANCE_THRESHOLD = 0.05` — net charge per unit cell
- `_LOEWENSTEIN_THRESHOLD = 0.5` — max Al mole fraction at tetrahedral site

**Why read-only:** The optimizer has already converged. Changing values post-hoc would invalidate the residual and misrepresent what the model actually refined. Warnings are for the user to act on manually (tighten bounds and re-refine, or revisit the structural setup).

---

## Test checklist

After any change to these guardrails, verify:
- [ ] AtomRatio value > 1 in inline list: clamped to 1.0, value cell turns red during entry then clears after clamp.
- [ ] AtomRatio value < 0: clamped to 0.0.
- [ ] AtomContents value (e.g. H₂O = 3.5): not clamped, remains > 1 freely.
- [ ] AtomRatio dialog: select Al_tet (atom1) + Si (atom2) → Sum auto-fills.
- [ ] AtomRatio dialog: type value > 0.5 with Si→Al pair → Loewenstein warning appears; clear to ≤ 0.5 → warning hides.
- [ ] Atom table: set AtomRatio value to 1.1 (before clamp is active) → pn of atom2 goes negative → `#` cell turns red.
- [ ] Atom table: fix value → pn goes positive → red clears.
- [ ] Run refinement with a Loewenstein-violating value → post-refinement log shows ⚠ warning.
- [ ] Run refinement with correct charge balance → post-refinement log shows ✓ for all checks.
- [ ] Run refinement with charge imbalance → post-refinement log shows ⚠ imbalanced.
- [ ] Confirm values in the model are unchanged after validation log is shown.
- [ ] Component with correct Ca²⁺ + layer substitution → charge balance label shows "✓".
- [ ] Remove Ca from interlayer → net imbalance > 0.05 → label turns amber.
- [ ] Change atom type of an interlayer atom → label updates immediately.
