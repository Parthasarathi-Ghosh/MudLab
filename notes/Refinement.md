# Refinement

Source: `mudlab/refinement/`  
Docs: `docs/how-to/refinement.md`, `docs/how-to/parameter-space-plots.md`

Refinement minimises the weighted residual **Rwp** between the observed and calculated XRD patterns by adjusting selected parameters using **L-BFGS-B** (limited-memory Broyden–Fletcher–Goldfarb–Shanno with box constraints).

## Refinable parameters

Any model property marked `refinable=True` can be added to the refinement:
- Phase fractions and absolute scales (in [[Mixture Model]])
- Background polynomial coefficients
- d001, delta_c (layer spacing)
- Atom `pn`, `z`, `B_iso`
- `value` in [[Atom Relations]] (AtomRatio / AtomContents)
- CSDS distribution parameters
- σ* (turbostratic disorder)

## Algorithm

```
L-BFGS-B (scipy.optimize.fmin_l_bfgs_b)
  MAXFUN = 500   ← max function evaluations
  MAXITER = 150  ← max iterations
  IPRINT = -1    ← suppress Fortran stdout (avoid crash on Windows)
```

Each function evaluation:
1. Updates parameter values in the model
2. Calls `mixture.optimize_mixture()` (recomputes fractions/scales if auto enabled)
3. Computes the full calculated pattern via [[XRD Diffraction Calculation]]
4. Returns Rwp as the objective

## Residual metrics

```
Rp  = Σ|y_obs − y_calc| / Σ y_obs
Rwp = sqrt( Σ w(y_obs − y_calc)² / Σ w·y_obs² )
GoF = Rwp / Rexp          (goodness of fit; target ≈ 1)
```

## Results dialog

Shows initial / best / last residual and GoF. Buttons:
- **Best** — apply the best solution found
- **Last** — apply the last iteration
- **Initial** — revert to pre-refinement parameters
- **Show Plot** — opens the parameter-space plot window

## Parameter space plot

`mudlab/refinement/views/refiner_view.py` — interactive Matplotlib window (1000×800) showing how the objective varies across the parameter space. Useful for diagnosing local minima.

## Threading

The refinement runs in a background thread. The GTK main loop stays responsive. Completion is signalled back via `GLib.idle_add`. Thread safety: `GLib.MainContext.default().find_source_by_id()` is not called from the worker thread.

## Environment variables set at startup

```
OPENBLAS_NUM_THREADS=1
OMP_NUM_THREADS=1
MKL_NUM_THREADS=1
```

Prevents nested thread-pool over-subscription from NumPy/SciPy.

## Related Notes

- [[Mixture Model]]
- [[XRD Diffraction Calculation]]
- [[Atom Relations]]
- [[Phase and Component Model]]
- [[Architecture]]
