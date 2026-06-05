# Major Oxide Composition

[← Back to User Manual](../index.md)

> **Printing to PDF:** Open this page in your browser and use **File → Print → Save as PDF**.

This page explains how MudLab computes the major oxide weight-percent composition of each specimen from the structural parameters of the phases in a mixture.

---

## Where to find it

In the **Edit Mixtures** dialog, click the **Composition** button. A table appears showing the weight-percent of each major oxide for every specimen in the mixture. The table can be exported as a CSV file.

---

## What is being computed

MudLab derives a **theoretical chemical composition** from the atom occupancies defined in the phase models. It converts element masses to oxide masses and expresses the result as weight percent, normalised to 100%.

This is the composition that a clay mineral **would have** if its structural model were exactly correct — it is a cross-check against measured geochemical analyses, not an independent measurement.

---

## Computation steps

### Step 1 — Oxide conversion table

Source: `mudlab/data/composition_conversion.csv`

A lookup table maps each element (by atomic number) to its conventional oxide form and an element→oxide mass conversion factor:

| Element | Atomic nr | Oxide | Conversion factor |
|---|---|---|---|
| Si | 14 | SiO₂ | 2.1392 |
| Al | 13 | Al₂O₃ | 1.8895 |
| Fe | 26 | Fe₂O₃ | 1.4297 |
| Ca | 20 | CaO | 1.3992 |
| Mg | 12 | MgO | 1.6582 |
| Na | 11 | Na₂O | 1.3480 |
| K  | 19 | K₂O  | 1.2046 |

Only elements listed in this table contribute to the output. All other elements (e.g. Ti, Mn, H, O) are excluded from the calculation and the remaining oxides are renormalised to 100%.

The conversion factor converts the mass of the pure element to the mass of its oxide:

```
mass(oxide) = mass(element) × conversion_factor
```

For example, the factor for SiO₂ is the ratio of the molar mass of SiO₂ (60.08 g/mol) to that of Si (28.09 g/mol) = 2.1392.

---

### Step 2 — Weight accumulation

Source: `mudlab/mixture/models/mixture.py` → `get_composition_matrix()`

For each specimen, the code iterates over every phase and component in the mixture:

```
for each phase p:
    for each component k within phase p:

        component_fraction = mW[k] × phase_fraction[p]

        for each atom in layer_atoms + interlayer_atoms:
            if atom element is in the conversion table:
                raw_oxide_weight += pn × atomic_weight × component_fraction × oxide_factor
```

The four terms in the accumulation are:

| Term | Source | Meaning |
|---|---|---|
| `pn` | Atom model | Occupancy — atoms per unit cell projected onto the c-axis |
| `atomic_weight` | AtomType model | Atomic mass of the element (g/mol) |
| `component_fraction` | `mW[k] × phase_fraction[p]` | Weight fraction of this component across the whole specimen |
| `oxide_factor` | Conversion table | Converts element mass to oxide mass |

**`component_fraction`** is the product of two fractions:
- `phase_fraction[p]` — weight fraction of phase p in the specimen (set in Edit Mixtures)
- `mW[k]` — weight fraction of component k within that phase (set in the Probabilities tab of Edit Phases)

For a single-component phase (G = 1), `mW[0] = 1.0` and `component_fraction = phase_fraction`.

---

### Step 3 — Normalise to 100 %

After all atoms across all phases and components have been accumulated:

```
oxide_wt% = raw_oxide_weight / sum(all raw oxide weights) × 100
```

Each oxide's weight is expressed as a percentage of the total oxide mass, summing to 100 %.

---

## Limitations

- **Only 7 elements** are included by default (Si, Al, Fe, Ca, Mg, Na, K). Elements outside this list (Ti, Mn, H, O, etc.) are silently ignored and the result is renormalised. This means the output represents a **partial composition** if significant amounts of unlisted elements are present.
- **Fe is always expressed as Fe₂O₃** regardless of the actual oxidation state. If you have Fe²⁺ (FeO) in the structure, the result will be incorrect unless you adjust the conversion factor.
- The computation uses the **current phase fractions** from the mixture matrix — run **Optimize** first to ensure fractions are up to date before reading the composition.
- `pn` values modified by **Atom Relations** (AtomRatio / AtomContents) are used as-is at the time of the calculation, so the composition reflects the current relation values, including any that were set during refinement.

---

## Extending the conversion table

To add more elements, edit `mudlab/data/composition_conversion.csv`. Each row has three fields:

```
atomic_number, oxide_name, conversion_factor
```

The conversion factor is:

```
factor = molar_mass(oxide) / molar_mass(element) × (atoms of element per formula unit)
```

For example, TiO₂: molar mass 79.87, Ti molar mass 47.87, one Ti per formula unit → factor = 79.87 / 47.87 = 1.6685.

---

## Related source files

| Role | File |
|---|---|
| Computation | `mudlab/mixture/models/mixture.py` → `get_composition_matrix()` |
| UI display and CSV export | `mudlab/mixture/controllers/edit_mixture_controller.py` → `on_composition_clicked()` |
| Conversion table | `mudlab/data/composition_conversion.csv` |
| AtomType (atomic weight) | `mudlab/atoms/models.py` |

---

[← Back to User Manual](../index.md)
