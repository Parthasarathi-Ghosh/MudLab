# Oxide Composition

Source: `mudlab/mixture/models/mixture.py` → `get_composition_matrix()`  
Controller: `mudlab/mixture/controllers/edit_mixture_controller.py` → `on_composition_clicked()`  
Conversion table: `mudlab/data/composition_conversion.csv`  
Docs: `docs/how-to/composition.md`

Triggered by the **Composition** button in Edit Mixtures. Produces a table of major oxide weight percentages for each specimen, derived from the structural atom data of the phases.

## Conversion table (7 elements)

| Element | Oxide | Factor |
|---|---|---|
| Si (14) | SiO₂ | 2.1392 |
| Al (13) | Al₂O₃ | 1.8895 |
| Fe (26) | Fe₂O₃ | 1.4297 |
| Ca (20) | CaO | 1.3992 |
| Mg (12) | MgO | 1.6582 |
| Na (11) | Na₂O | 1.3480 |
| K (19) | K₂O | 1.2046 |

Only these elements contribute. Others are silently excluded and the result is renormalised to 100%.

## Formula

For each atom in every component of every phase:

```
raw_oxide_weight += pn × atomic_weight × component_fraction × oxide_factor
```

where `component_fraction = mW[k] × phase_fraction[p]`.

Then normalised:

```
oxide_wt% = raw_oxide_weight / Σ(all raw weights) × 100
```

## Key caveats

- Fe is always expressed as Fe₂O₃ regardless of oxidation state
- Uses current `pn` values — [[Atom Relations]] values at the time of the call are used
- Uses current phase fractions — run Optimize before reading composition
- Extend by adding rows to `composition_conversion.csv` (format: `atomic_nr, oxide_name, factor`)

## Related Notes

- [[Mixture Model]]
- [[Phase and Component Model]]
- [[Atom Relations]]
