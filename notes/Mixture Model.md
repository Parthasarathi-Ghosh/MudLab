# Mixture Model

Source: `mudlab/mixture/models/`  
View: `mudlab/mixture/views/edit_mixture_view.py`, `edit_insitu_mixture_view.py`  
Docs: `docs/how-to/` (refinement, diffraction-calculation)

A **mixture** is the bridge between [[Phase and Component Model|phases]] and [[Markers and Peak Detection|specimens]]. It defines which phases contribute to each specimen and at what weight fractions and scales.

## Structure

```
Mixture
  ├── specimens[]      ← measured XRD patterns
  ├── phases[]         ← crystallographic phases
  └── matrix[s][p]     ← fraction and scale per (specimen, phase) pair
```

Each cell in the matrix has:
- **Fraction** — weight fraction of this phase in this specimen (0–1); constrained to sum to 1 across phases
- **Scale** — absolute intensity scale factor (refinable)
- **Background shift** — per-specimen constant background offset

## Auto-scale and auto-background

Checkboxes in the Edit Mixture dialog:
- **Auto scales** — scales are recomputed by linear regression at each refinement step
- **Auto background** — background shifts are recomputed analytically

Both reduce the number of free parameters during [[Refinement]].

## In-situ mixture

`EditInSituMixtureView` / `InSituMixture` — a variant where a single phase evolves over a series of specimens (e.g. a heating experiment). The fraction and scale vary continuously across the series; special interpolation controls are shown.

## Calculated vs. observed

The mixture produces the **total calculated pattern**:

```
y_calc(stl) = Σ_phases  fraction_p × scale_p × I_phase(stl)  +  background
```

This is compared to `y_obs` from the specimen to compute Rp / Rwp. See [[XRD Diffraction Calculation]].

## Edit Mixture dialog

- Rows: phases
- Columns: specimens
- Each cell: fraction input + scale input
- Buttons: Refine (launches [[Refinement]]), auto-scale checkbox, background checkbox

The dialog opens from the main window's mixture list.

## Related Notes

- [[MudLab Overview]]
- [[Phase and Component Model]]
- [[XRD Diffraction Calculation]]
- [[Refinement]]
- [[Markers and Peak Detection]]
- [[Oxide Composition]]
