# How MudLab Calculates a Diffraction Pattern

[← Back to User Manual](../index.md)

> **Printing to PDF:** Open this page in your browser and use **File → Print → Save as PDF**.

This page describes the full mathematical pipeline that MudLab uses to compute a calculated XRD pattern from a set of phases and goniometer settings. It is intended for users who want to understand what the software is doing during refinement, how instrument parameters affect the result, or how to interpret the goodness-of-fit statistics.

---

## Pipeline Overview

```
Phase parameters (d001, atoms, stacking probabilities, CSDS)
  └─ Atomic scattering factors
  └─ Component structure factors
  └─ CSDS distribution
  └─ Absolute scale
  └─ Q-matrix powers (domain-size-weighted stacking correlations)
  └─ Phase intensity  I(θ)
        └─ Lorentz-polarisation factor
        └─ Machine & sample corrections
        └─ Wavelength distribution (Kα2, Kβ)
        └─ Specimen-level corrected intensity
              └─ Multiply by phase fractions and scale
              └─ Add background offset
              └─ Total calculated pattern
                    └─ Compare to observed → residual (Rp, Rwp, …)
                          └─ L-BFGS-B optimise fractions / scales / background
```

All calculation is done in the **reciprocal space coordinate**:

```
stl = 2 sin(θ) / λ          (units: Å⁻¹)
```

where θ is the Bragg angle and λ the primary X-ray wavelength. Every intensity array is a function of `stl`, computed on the same grid as the measured pattern.

---

## Step 1 — Atomic Scattering Factors

Source: `mudlab/calculations/atoms.py` and `mudlab/calculations/components.py`

For each atom in a component (both layer and interlayer atoms), the **atomic scattering factor** is:

```
s = (stl × 0.05)²         (converts to (sin θ / λ)² in Å²)

ASF(s) = c + Σᵢ aᵢ exp(−bᵢ s)       (Cromer-Mann parametrisation)

f(s) = ASF(s) × exp(−B_iso × s)      (Debye-Waller thermal correction)
```

Parameters `a`, `b`, `c` (4 terms each) are taken from the `atomic scattering factors.atl` table shipped with MudLab, keyed by `atom_type_name`. `B_iso` is the isotropic displacement factor.

The **atomic contribution to the structure factor** then includes the phase shift from the atom's fractional z-position within the layer:

```
F_atom(stl) = f(stl) × pn × exp(2π i × z × stl)
```

where `pn` is the atom count (occupancy) and `z` is the z-coordinate in Å.

---

## Step 2 — Component Structure Factors

Source: `mudlab/calculations/components.py`

For each component (layer type), all atoms are summed:

```
SF(stl) = Σ_atoms  F_atom(stl)
```

The **phase difference factor** accounts for the spacing between layers and any c-axis distortion:

```
PF(stl) = exp( 2π i × stl × (d001 × i − π × δc × stl) )
```

where:
- `d001` — basal spacing of this component (nm)
- `δc` — c-axis distortion parameter (broadens individual peaks)
- The `δc` term introduces a Gaussian-like broadening that grows quadratically in reciprocal space

### How d001 is determined

`d001` is the **basal spacing** of the component — the c-axis repeat distance of the clay layer including its interlayer space (nm). It is the most important structural parameter: it controls peak positions via Bragg's law and is what you adjust when fitting swelling or collapsing behaviour.

Three companion c-axis parameters work together:

| Parameter | UI label | Meaning | Default |
|---|---|---|---|
| `d001` | **Cell length c [nm]** | Current basal spacing (the value you set or refine) | 1.0 nm |
| `default_c` | **Default length c [nm]** | Reference spacing at which interlayer atom z-positions were originally defined | same as `d001` at load time |
| `delta_c` (δc) | **Δc spacing [nm]** | Layer-to-layer spacing disorder; broadens peaks | 0.0 nm |
| `lattice_d` | *(not shown)* | Height of the silicate lattice alone (no interlayer); auto-computed as the maximum layer-atom z | — |

**How `d001` is set:**

1. **Directly by the user** — in Edit Phases, open a component and edit the **Cell length c [nm]** field. It is a combined slider and spin button with a range of 0–5 nm. The default on a new component is 1.0 nm (physically meaningless until set correctly).
2. **Inherited from a linked component** — if the inherit checkbox next to **Cell length c** is ticked and the component is linked to another via `linked_with`, `d001` tracks the linked component's value. Used in mixed-layer phases to keep component spacings consistent across treatment variants.
3. **Refined** — `d001` (Cell length c) is a refinable parameter and can be selected in the Refinement dialogue to be adjusted automatically against the observed pattern.

**How interlayer atoms respond to a change in `d001`:**

Interlayer atoms (water molecules, exchangeable cations) carry a `stretch_values = True` flag. Their z-position is not fixed — it is recomputed each time `d001` changes using a linear stretch between the silicate framework height (`lattice_d`) and the full basal spacing:

```
z_factor = (d001 − lattice_d) / (default_c − lattice_d)
atom.z   = lattice_d + z_factor × (atom.default_z − lattice_d)
```

`default_c` is the denominator reference: it records the spacing at which the interlayer positions were originally defined in the file. Layer atoms (the silicate framework) keep fixed z-positions and are not stretched.

**Consequence for the absolute scale:**

The unit cell volume used in `abs_scale` is `cell_a × cell_b × d001`. Changing `d001` therefore also shifts the absolute intensity of the phase — a larger basal spacing gives a smaller `abs_scale` and lower peak heights, all else being equal.

---

## Step 3 — CSDS Distribution

Source: `mudlab/calculations/CSDS.py`

The **coherent scattering domain size** (CSDS) distribution `q(T)` describes the probability of finding a crystallite with exactly `T` layers. MudLab uses a **log-normal** distribution:

```
a = α_scale × ln(⟨T⟩) + α_offset
b = √( β_scale × ln(⟨T⟩) + β_offset )

q(T) = exp( −(ln T − a)² / (2b²) ) / (√(2π) |b| T)     (T = 1, 2, …, T_max)
```

The parameters `α_scale`, `α_offset`, `β_scale`, `β_offset` are fixed for the Drits distribution (the default). The only user-controllable parameter is the **average domain size** `⟨T⟩` (in layers), shown in Edit Phases as "Average CSDS".

The arithmetic mean used for intensity normalisation:

```
⟨T⟩_arith = Σ T × q(T)
```

Larger `⟨T⟩` → sharper peaks (more coherently scattering layers per domain).

---

## Step 4 — Absolute Scale Factor

Source: `mudlab/calculations/phases.py`

The absolute scale converts intensity to a physically meaningful unit. It is computed from the composition-weighted mean properties:

```
⟨V⟩     = Σᵢ Wᵢ × Vᵢ         (mean component volume)
⟨d001⟩  = Σᵢ Wᵢ × d001ᵢ      (mean basal spacing)
⟨ρ⟩     = Σᵢ Wᵢ × mᵢ / Vᵢ    (mean layer mass density)

abs_scale = ⟨d001⟩ / (⟨T⟩_arith × ⟨V⟩² × ⟨ρ⟩)
```

where `Wᵢ` is the weight fraction of component `i` (diagonal of the **W matrix**).

---

## Step 5 — Q-Matrix Powers (Stacking Correlations)

Source: `mudlab/calculations/phases.py`

This is the core of the disordered-stacking calculation. The **Q matrix** combines the phase factor and the stacking probability matrix **P**:

```
Q(stl) = PF(stl) ⊗ P        (element-wise product, shape: rank × rank)
```

where `rank = G^R` for an R-order model with G component types. **P** encodes stacking sequences:

| Model | Rank | Parameters |
|---|---|---|
| R0G1 | 1 | none (single layer type) |
| R0G2 | 2 | F₁ (fraction of layer 1) |
| R1G2 | 2 | W₁, P₁₁ (weight and self-transition) |
| R2G2 | 4 | W₁, P₁₁, P₁₁₁, P₂₁₁ |
| R3G2 | 8 | W₁ and six junction probabilities |
| R0G3 | 3 | F₁, F₂ |
| R1G3 | 3 | W₁, W₂, P₁₁, P₁₂, P₂₁, P₂₂ |

The matrix power **Q^n** accumulates the correlations introduced by n successive layers. MudLab computes all powers up to `T_max`:

```
Q^1, Q^2, …, Q^(T_max)
```

using iterative matrix multiplication (`einsum('ijk,ikl->ijl', ...)`).

---

## Step 6 — Phase Intensity Assembly

Source: `mudlab/calculations/phases.py`

The intensity is assembled by summing contributions over all domain sizes, weighted by the CSDS distribution. The key quantity is the **progression factor**:

```
P_prog(n) = Σ_{m > n} (m − n) × q(m)
```

This counts the average number of inter-layer correlations contributed by domains larger than `n`.

The domain-size-weighted correlation sum is:

```
Ω = 2 Σ_{n=T_min}^{T_max}  P_prog(n) × Q^(n−1)
```

The total intensity matrix is then:

```
M = (⟨T⟩_arith × 𝐈 + Ω)     (𝐈 = identity matrix)
```

where the identity term is the single-layer (incoherent) contribution.

Finally, combining with the structure factor matrix **F** and weight matrix **W**:

```
I(stl) = abs_scale × Re{ Tr[ F(stl) × W × M(stl) ] }
```

where:
- **F** is the outer product of structure factors: `F[i,j] = SF_i × SF_j*`
- `Tr[...]` sums the diagonal (interference of each layer with itself and others)
- `Re{...}` takes the real part (imaginary parts cancel by symmetry)

**Physical interpretation:**
The trace sums over all layer-pair interference contributions. For R0 (fully disordered) phases, off-diagonal terms average to zero and only the diagonal (single-layer scattering) survives. For ordered sequences (higher R), off-diagonal terms add constructive/destructive interference, sharpening or splitting peaks.

---

## Step 7 — Lorentz-Polarisation Factor

Source: `mudlab/calculations/specimen.py`

The **Lorentz-polarisation factor (LPF)** accounts for:
1. The **angular acceptance** of the diffractometer (Soller slits, angular divergence)
2. The **polarisation state** of the X-rays (modified by the monochromator)

```
S      = √( (σ₁/2)² + (σ₂/2)² )     (combined Soller slit divergence in radians)
Q      = S / (√8 × sin θ × σ*)        (normalised divergence ratio)

T(θ)   = erf(Q) × √(2π) / (2σ* × S)  −  2 sin θ × (1 − exp(−Q²)) / S²

pol    = cos²(2θ_mcr)                  (monochromator polarisation factor)

LPF(θ) = T(θ) × (1 + pol × cos² 2θ) / sin θ
```

where:
- `σ₁`, `σ₂` — Soller slit openings (degrees, one on each side of the sample)
- `σ*` — angular divergence parameter of the phase (degrees; set in Edit Phases)
- `2θ_mcr` — monochromator Bragg angle (degrees; set in Edit Goniometer)

Increasing `σ*` broadens peaks; `σ*=0` gives the sharpest possible peak for the given CSDS.

---

## Step 8 — Machine and Sample Corrections

Source: `mudlab/calculations/specimen.py`

A correction factor `C(θ)` is multiplied into the intensity at each angle.

### Absorption correction

```
μ* = μ × ρ_s × 10⁻³           (effective absorption coefficient)
C_abs(θ) = 1 − exp(−2μ* / sin θ)
```

where `μ` is the mass absorption coefficient (cm²/g) and `ρ_s` is the sample surface density (mg/cm²). At low angles (small sin θ), absorption removes more intensity; the correction factor is smaller than 1.

### Fixed divergence slits

```
L_Rta = L_sample / (R × tan(φ))
C_fix(θ) = min( sin θ × L_Rta,  1 )
```

where `L_sample` is the sample length, `R` the goniometer radius, and `φ` the divergence slit angle. At low angles, only part of the beam hits the sample; this factor < 1 corrects for that.

### Automatic divergence slits (ADS)

```
C_ADS(θ) = sin θ
```

ADS maintain constant sample illumination by opening with angle. The `sin θ` factor converts the measured pattern back to what fixed slits would give, allowing direct comparison.

---

## Step 9 — Wavelength Distribution

Source: `mudlab/calculations/specimen.py`

Real X-ray sources emit a primary line (Kα₁) plus secondary lines (Kα₂, Kβ). For each secondary wavelength λ₂ with intensity fraction f:

1. Compute the 2θ shift for λ₂: the same d-spacing now diffracts at a different angle
2. Interpolate the phase intensity onto the shifted grid
3. Add `f × I_shifted` to the total

This accounts for the **Kα₂ doublet** visible as a shoulder on the high-angle side of peaks at 2θ > ~50°.

---

## Step 10 — Mixture Combination

Source: `mudlab/calculations/mixture.py`

For a specimen containing multiple phases, the total pattern is:

```
I_calc(θ) = scale × Σₚ  wₚ × Iₚ(θ) × C(θ)  +  Δbg × C(θ)
```

where:
- `wₚ` — weight fraction of phase p (sums to 1 over all phases)
- `Iₚ(θ)` — corrected intensity of phase p
- `scale` — overall intensity scale factor (accounts for mass of sample, detector efficiency, etc.)
- `Δbg` — background offset (a flat additive background)
- `C(θ)` — machine/sample correction (same for all phases in one specimen)

The three optimisable quantities per specimen are `scale`, `Δbg`, and the set of `wₚ`.

---

## Step 11 — Residuals and Goodness-of-Fit

Source: `mudlab/calculations/statistics.py`

Four residual metrics are available:

### Rp (Pattern R-factor)
```
Rp = 100 × Σ|Iobs − Icalc| / Σ|Iobs|
```
Simple unweighted difference. Sensitive to high-intensity peaks.

### Rwp (Weighted Pattern R-factor)
```
Rwp = 100 × √( Σ wᵢ(Iobs,ᵢ − Icalc,ᵢ)² / Σ wᵢ Iobs,ᵢ² )
     wᵢ = 1 / Iobs,ᵢ   (Poisson counting statistics)
```
Statistically rigorous; the preferred metric for reporting. Values below ~10% are good; below ~5% are excellent.

### Rpder (Derivative R-factor)
```
Rpder = Rp( d/dx smooth(Iobs),  d/dx smooth(Icalc) )
```
Computed on the smoothed derivatives. Sensitive to **peak positions and shapes** rather than absolute intensities; useful for diagnosing peak shift problems.

### Rphase (Phase-weighted R-factor)
```
Rphase = 100 × √( Σ wₚ × (Iobs − Icalc)² / Iobs² / Σ wₚ )
```
Weights residual by the phase fractions `wₚ`. Highlights how well the dominant phase(s) are fitted.

---

## Step 12 — Optimisation

Source: `mudlab/calculations/mixture.py` and `mudlab/refinement/methods/scipy_runs.py`

When the **Optimise** button is pressed (mixture-level), MudLab runs **L-BFGS-B** (limited-memory Broyden-Fletcher-Goldfarb-Shanno with box constraints) to minimise the selected residual.

The optimisation variables are packed into a single vector:

```
x = [ w₁, w₂, …, wₘ,   scale₁, scale₂, …,   Δbg₁, Δbg₂, … ]
```

**Bounds:**
- Phase fractions: [0, 1]
- Scale: [10⁻³, ∞)
- Background offset: [0, ∞)

Fractions are renormalised at each iteration so they sum to 1 (minus any fixed phases). Phase intensities `Iₚ(θ)` are pre-computed and cached before optimisation starts; only the linear combination coefficients are varied. This makes each objective evaluation fast (a matrix multiply rather than a full recalculation).

---

## Caching and Recalculation

Phase intensities are cached with a key that includes every parameter that affects the pattern: atom positions, scattering factors, probability matrices, CSDS parameters, goniometer geometry, and the reciprocal-space grid. If any parameter changes (e.g. during full structure refinement), the cache is invalidated and the pattern is recalculated from scratch.

---

## Low-angle intensity — what controls the pattern below the first basal peak

At the lowest 2θ, five factors multiply together to shape the calculated intensity. Several of them diverge or go to zero as θ → 0, and they largely oppose each other. The net shape at the low-angle end is therefore dominated by **goniometer geometry**, not by the crystal structure of the phases.

### The 2θ grid — no intensity below `min_2theta`

The calculation grid starts at:

```
θ_first = (min_2theta / 2) + δθ / 2        δθ = (max_2theta − min_2theta) / 2 / steps
```

The first point is offset inward by half a step from `min_2theta` (default 3°). No intensity is computed below this value. If the measured pattern starts lower than `min_2theta`, the goniometer setting must be adjusted accordingly.

### Atomic scattering factors — largest at low angle

The Cromer-Mann form factor peaks at `stl = 0` (2θ = 0) and decreases monotonically. At very low 2θ, `stl ≈ 0` and `f ≈ Z` (the atomic number), so the raw diffracted intensity from the crystallite is at its maximum. This pushes low-angle intensity **up**.

### Lorentz-polarisation factor — diverges as 1/sin θ

```
LPF(θ) ∝ T(θ) / sin θ
```

Both `T(θ)` and the explicit `1/sin θ` term grow strongly as θ → 0, amplifying low-angle peaks significantly. This also pushes intensity **up**.

### Machine corrections — the dominant suppressing force

These corrections push low-angle intensity **down** and largely cancel the two factors above:

**Fixed divergence slits:**

```
C_fix(θ) = min( sin θ × L_sample / (R × tan φ),  1 )
```

At low angles `sin θ` is small, so only a fraction of the beam falls on the sample. This is the strongest low-angle suppression factor.

**Automatic divergence slits (ADS):**

```
C_ADS(θ) = sin θ
```

The `sin θ` factor converts the ADS-measured pattern to the fixed-slit equivalent. Same suppressing effect at low angles.

**Absorption correction:**

```
C_abs(θ) = 1 − exp(−2μ* / sin θ)
```

For thick or absorbing samples, this removes additional low-angle intensity.

### The first basal peak — lowest structural feature

The `d001` term in the phase difference factor places constructive interference at:

```
2θ_n = 2 arcsin( n λ / 2 d001 )        (Bragg's law, n = 1, 2, 3, …)
```

The n = 1 peak is the **lowest 2θ feature of crystallographic origin**. For common clay minerals with Cu Kα₁ (λ = 0.154056 nm):

| Mineral / state | d001 (nm) | 001 peak (2θ) |
|---|---|---|
| Kaolinite | 0.72 | ~12.3° |
| Illite | 1.00 | ~8.8° |
| Smectite, air-dried | 1.25–1.55 | ~5.7–7.1° |
| Smectite, glycolated | 1.70 | ~5.2° |

Below the first basal peak, the calculated intensity is flat background (`Δbg`) shaped only by the machine correction geometry.

### Net result

The low-angle tail below the first 001 peak is controlled almost entirely by the goniometer settings (slit mode, divergence angle, sample length, radius, absorption), not by the phase crystal structure. Getting this region right requires correct goniometer parameters, not phase parameter adjustments.

---

## Relevant Source Files

| Step | File |
|---|---|
| Atomic scattering factors | `mudlab/calculations/atoms.py` |
| Component structure factors | `mudlab/calculations/components.py` |
| CSDS distribution | `mudlab/calculations/CSDS.py` |
| Phase intensity assembly | `mudlab/calculations/phases.py` |
| LPF, corrections, wavelength | `mudlab/calculations/specimen.py` |
| Mixture combination | `mudlab/calculations/mixture.py` |
| Residual metrics | `mudlab/calculations/statistics.py` |
| Goniometer model | `mudlab/goniometer/models.py` |
| Data containers | `mudlab/calculations/data_objects.py` |
| L-BFGS-B wrapper | `mudlab/refinement/methods/scipy_runs.py` |

---

[← Back to User Manual](../index.md)
