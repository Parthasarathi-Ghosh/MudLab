# Handoff → MudLab2: probability-model invalid-matrix crash (Bug B) + affected models

Direction: **upstream (MudLab / GTK) → downstream (MudLab2 / Qt).**
This is the return note for "Bug B" in `HANDOFF-from-mudlab2.md`. Bug B is now
fixed upstream; this note records the root cause, the exact models affected
(measured), the upstream fix, and what MudLab2 should verify on its side.

## Summary

Editing or refining the stacking **probabilities** of an R≥1, multi-parameter
phase crashed upstream when the parameter values produced an **invalid junction
matrix**. It looked R1G3-specific but is a general invalid-matrix path — R1G3 was
just the first model tested that lands there often.

Downstream note from the original handoff said the MudLab2 calc "returns zeros
for an invalid matrix", so the port should not crash. Please still **verify the
guard covers every affected model below** (especially R2G3/R3G2, which are
invalid almost everywhere) and **check for the same `validate()` threshold typo**.

## Root cause (upstream)

When a probability model is invalid, `Phase.data_object` (`phases/models/phase.py`)
nulls the whole calc block — including `sigma_star = None` (also `CSDS`, `W`, `P`,
`components`). But `get_intensity` (`calculations/phases.py`) computed the
Lorentz-polarisation factor with `phase.sigma_star` **before** the `valid_probs`
guard:

```
intensity = get_diffracted_intensity(...)      # correctly returns zeros if invalid
if phase.apply_lpf:                            # <-- runs even when invalid
    result = intensity * get_lorentz_polarisation_factor(range_theta,
                 phase.sigma_star, ...)        # phase.sigma_star is None
```

`get_lorentz_polarisation_factor → get_T` (`calculations/goniometer.py`) then did
`float(max(sigma_star, 1e-18))` with `sigma_star=None` →
`TypeError: '>' not supported between instances of 'float' and 'NoneType'`.

## Affected models (measured)

Invalid fraction of the independent-parameter box `(0,1)^k` (uniform random,
N=2000; a set is "invalid" when `not (all(P_valid) and all(W_valid))`):

| Model | independent params (k) | invalid % | affected |
|---|---|---|---|
| R0G2 / R0G3 / R0G4 (all R0) | 1–3 | **0.0%** | no |
| R1G2 | 2 | **0.0%** | no |
| R1G3 | 6 | **76.2%** | **yes** |
| R1G4 | 12 | **85.5%** | **yes** |
| R2G2 | 4 | **23.4%** | **yes** |
| R2G3 | 6 | **100.0%** | **yes** |
| R3G2 | 2 | **100.0%** | **yes** |

Reading this:
- **Never affected:** every R0 model, and **R1G2** — their parameter box is
  entirely valid, so they can never reach the invalid path.
- **Affected:** R1G3, R1G4, R2G2, R2G3, R3G2.
- **R2G3 and R3G2 are the worst (100%):** only the fitted point is valid, so
  *any* edit away from it lands in an invalid matrix. A stored/fitted project
  still loads and calculates fine; the crash is strictly on **editing/refining**.

## Upstream fix (MudLab — applied & committed)

1. `calculations/phases.py`, `get_intensity`: guard the LP factor on validity —
   `if phase.apply_lpf and phase.valid_probs:` — so an invalid matrix yields a
   zero pattern instead of dereferencing the nulled `sigma_star`.
2. `probabilities/models/base_models.py`, `validate()`: fixed a latent Py2→3
   sign-typo — the sum-to-one / row-stochastic thresholds were `1e4` / `1e6`
   (never fired; only the value-in-[0,1] checks were live) → corrected to
   `1e-4` / `1e-6`.

Verified headless (R1 G3 / R2 G2 / R2 G3 / R3 G2 test projects): 0 crashes over
random probability edits; invalid sets correctly blank; valid baselines
unchanged; R0 / R1G2 unaffected.

## For MudLab2 — please verify

1. **Guard coverage:** confirm the port's invalid-matrix guard returns zeros
   *before* any use of `sigma_star` / `CSDS` / `W` / `P` (whatever your
   `Phase.data_object` equivalent nulls). Test **R2G3 and R3G2** specifically —
   they are invalid on essentially every edit, so they exercise the guard hardest.
2. **validate() thresholds:** if you ported `validate()`, make sure it is not the
   same `1e4` / `1e6` typo (should be `1e-4` / `1e-6`); otherwise validity
   detection silently passes non-row-stochastic matrices.
3. **Optional UX:** because R1G4 / R2G3 / R3G2 are almost entirely invalid, a
   blanked pattern on nearly every edit is confusing. Consider an explicit
   "invalid probability model" indicator (and/or constrained editable ranges)
   rather than a silent zero pattern.
