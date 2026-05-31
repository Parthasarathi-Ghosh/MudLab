# Atom Relations

Source: `mudlab/phases/models/atom_relations.py`  
Controller: `mudlab/phases/controllers/atom_relation_controllers.py`  
Docs: `docs/how-to/edit-phases.md` → Atom relations section, `docs/how-to/diffraction-calculation.md` → Step 1

Atom relations are rules that **dynamically set `pn` (occupancy)** on one or more atoms before each structure-factor calculation. They live in the **Atom relations** box on the Components tab of the Edit Phases dialog.

## Why they exist

In real minerals, cation sites are often partly or fully occupied by different elements. Instead of fixing `pn` manually, atom relations let you express occupancy as a **refinable relationship** — e.g. "Fe and Al share a site; refine the Fe/(Fe+Al) ratio".

## How pn flows into XRD

```
AtomRelation.apply_relation()
  → atom.pn updated
      → Component.data_object (snapshot)
          → F_atom = f × pn × exp(2πi z stl)
              → Structure factor → Intensity
```

Triggered reactively via MVC observers whenever `value` changes (including during [[Refinement]]).

## AtomRatio — binary substitution

```python
atom1.pn = value × sum
atom2.pn = (1 − value) × sum
```

- `sum` — total site occupancy (fixed by user, e.g. 4.0 for octahedral sheet)
- `value` — the refinable ratio, e.g. Fe/(Fe+Al); range [0, 1]

**Dropdowns in the UI:**
- Atom 1 / Atom 2 — any layer or interlayer atom in this component
- Linked to property — SUM or RATIO of another relation (chain occupancies)

**Example:** Fe/Al octahedral substitution — 4 sites total:
```
AtomRatio: Fe ↔ Al, sum=4.0, value=0.3
→ Fe.pn = 1.2,  Al.pn = 2.8
```

## AtomContents — absolute occupancy

```python
atom.pn = amount × value
```

- `amount` — user-defined multiplier, range [0, ∞), default 0.0
- `value` — refinable scale; no enforced bounds

Used when an atom's absolute occupancy depends on a refinable quantity rather than a complementary partner.

**Dropdown:** targets SUM or RATIO properties of other relations, enabling chained expressions.

## Creating relations

In the Atom relations box:
1. Select type from the combo (Ratio / Contents)
2. Click **Add** — a new row appears
3. Click the **pencil icon** to open the relation editor and set atoms + parameters

## Related Notes

- [[Phase and Component Model]]
- [[XRD Diffraction Calculation]]
- [[Refinement]]
