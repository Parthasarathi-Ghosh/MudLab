# XRD Diffraction Calculation

Source: `mudlab/calculations/` — `atoms.py`, `components.py`, `phases.py`, `specimen.py`, `mixture.py`

Docs: `docs/how-to/diffraction-calculation.md`

## Reciprocal space coordinate

All arrays are functions of:

```
stl = 2 sin(θ) / λ     (Å⁻¹)
```

## Pipeline

```
Atom positions + pn
  → Atomic scattering factor (Cromer-Mann)
  → Debye-Waller correction
  → Structure factor F(stl) per component
      → CSDS distribution (N-layer domain sizes)
      → Q-matrix (stacking probability powers)
      → Phase intensity I(stl)
          → Lorentz-polarisation factor
          → Goniometer corrections (divergence slit, etc.)
          → Wavelength splitting (Kα1/Kα2/Kβ)
          → Specimen intensity
              → × phase fraction × scale + background
              → Total calculated pattern
                  → Rp / Rwp residual vs. observed
```

## Step 1 — Atomic scattering factor

```
s     = (stl × 0.05)²
ASF   = c + Σ aᵢ exp(−bᵢ s)        ← Cromer-Mann (4-term)
f     = ASF × exp(−B_iso × s)       ← Debye-Waller
F_atom = f × pn × exp(2πi × z × stl)
```

`pn` = atom count (occupancy projected onto c-axis). Modified live by [[Atom Relations]].
`z` = fractional z-position (Å).
`B_iso` = isotropic displacement parameter.
Cromer-Mann coefficients are loaded from `atomic scattering factors.atl`.

## Step 2 — Component structure factor

```
F_comp(stl) = Σ_atoms F_atom(stl)
```

Summed separately for layer atoms and interlayer atoms. The data bridge is `component.data_object` — a lightweight frozen snapshot passed to the calculation layer.

## Step 3 — CSDS and stacking

The **coherent scattering domain size (CSDS)** distribution gives a probability P(N) for a crystallite to contain N layers. The **Q-matrix** encodes layer-stacking probabilities (R-order model). Phase intensity integrates over all domain sizes.

## Step 4 — Goniometer corrections

Applied per specimen via goniometer settings: divergence slit, axial divergence, flat-specimen correction, preferred orientation, Lorentz-polarisation. Configured in the Goniometer dialog.

## Step 5 — Mixture

Each phase contributes `fraction × scale × I_phase(stl)`. The background polynomial is added. This total is compared to the observed pattern. See [[Mixture Model]].

## Residual metrics

```
Rp  = Σ|y_obs − y_calc| / Σ y_obs
Rwp = sqrt( Σ w(y_obs − y_calc)² / Σ w·y_obs² )
GoF = Rwp / Rexp
```

Minimised by L-BFGS-B. See [[Refinement]].

## Related Notes

- [[Atom Relations]]
- [[Phase and Component Model]]
- [[Mixture Model]]
- [[Refinement]]
- [[Architecture]]
