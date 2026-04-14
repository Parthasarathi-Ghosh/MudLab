# How to do a Refinement

Refinement adjusts selected phase/mixture parameters to minimise the residual (Rwp) between the calculated and experimental patterns. Open the dialogue via **Refine** on the mixture toolbar.

## Workflow

1. Reduce Rwp manually first (fractions, scale, background) — refinement is most effective when the starting point is already close.
2. In the refinement dialogue, tick the **Refine** checkbox next to each parameter you want to vary. Start small: one or two parameters at a time.
3. Set sensible `min` / `max` bounds for each refined parameter, or use the helper buttons below.
4. Pick a refinement method (L-BFGS-B is the default) and click **Refine**.
5. When the run finishes, accept or reject the new values in the results dialogue.

## Helper buttons

### Restrict values

Auto-sets the bounds of every parameter currently marked **Refine** to ±20% of its present value:

- `value_min = value × 0.8`
- `value_max = value × 1.2`

It's a one-click way to tighten the search range around the current values before running the refiner, instead of editing each parameter's min/max by hand. Use it once you're reasonably confident the current values are in the right neighbourhood — it keeps the optimiser from wandering into unphysical territory and speeds convergence.

Source: [refinement.py:143-153](../../data/lib/python3.14/site-packages/mudlab/refinement/refinement.py#L143-L153).

### Randomize

Replaces the current value of every parameter marked **Refine** with a uniformly random draw from its existing `[value_min, value_max]` interval:

- `value = uniform(value_min, value_max)`

Use it to escape a local minimum: if a refinement run has converged but Rwp is still poor, click **Randomize** to perturb the starting point and re-run. Because it samples within the bounds you've already set, it respects whatever physical range you've defined — so set the min/max first (e.g. via **Restrict values**) before randomising.

Note: the in-code docstring claims Randomize also runs an optimisation afterwards, but the current implementation only reassigns values — you still need to click **Refine** to start the optimiser.

Source: [refinement.py:155-166](../../data/lib/python3.14/site-packages/mudlab/refinement/refinement.py#L155-L166).
