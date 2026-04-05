# Troubleshooting

[← Back to User Manual](../index.md)

> **Printing to PDF:** Open this page in your browser and use **File → Print → Save as PDF**.

---

## How the scale per specimen is determined

### Initial value

When a new specimen column is added to a mixture, the scale is initialised to **1.0**. When a project is loaded from file, the previously saved scale value is restored.

### What scale physically represents

`scale` is a single multiplier applied to the entire calculated pattern for that specimen:

```
I_calc(θ) = scale × Σₚ wₚ × Iₚ(θ) × C(θ)  +  Δbg × C(θ)
```

It absorbs everything that makes the absolute intensity of the measured pattern differ from the sum of calculated phase intensities — detector efficiency, beam intensity, sample mass on the holder, and any residual mismatch not captured by `abs_scale` inside each phase. It is **one value per specimen**, shared equally by all phases in that specimen.

### Whether the optimiser adjusts it — the `auto_scales` flag

The behaviour is controlled by the **Auto Scales** checkbox in Edit Mixtures:

| Setting | Effect |
|---|---|
| Auto Scales ON (default) | Scale is a free variable; the optimiser adjusts it together with fractions and background. |
| Auto Scales OFF | Scale is held fixed at whatever value is currently shown in the mixture table. |

When Auto Scales is ON, scale is included in the L-BFGS-B solution vector with a lower bound of **1×10⁻³** and no upper bound.

### How the optimiser adjusts scale

The solution vector packed for optimisation is:

```
x = [ w₁, …, wₘ,   scale₁, scale₂, …,   Δbg₁, Δbg₂, … ]
```

All three groups are varied simultaneously to minimise the residual (Rwp by default). After convergence, fractions are renormalised to sum to 1, and scale is multiplied by the same normalisation factor to compensate:

```python
fractions = fractions / sum(fractions)   # normalise to 1
scales    = scales * sum_frac            # absorb the magnitude
```

This means **fractions are relative** (they always sum to 1) and **scale carries the absolute intensity level**. The two are coupled — the optimiser can trade off between them, but their product is what determines the final pattern height.

### The lower-bound floor

The hard lower bound on scale is **1×10⁻³**. If the calculated phase intensities are so large that even this minimum scale cannot bring them down to match the observed pattern, the optimiser is stuck at the floor and the fit is meaningless. This is the most common cause of the scale collapsing to a very small value — see the next section.

---

## Optimiser sets the scale to a very small value

**Symptom:** After clicking **Optimize**, the scale for one or more specimens drops to an extremely small value (0.001 or near it) and the calculated pattern does not match the observed pattern.

### Background

The optimiser controls three variables per specimen: phase **fractions** (wₚ), an overall intensity **scale**, and a **background offset** (Δbg). The total calculated intensity is:

```
I_calc(θ) = scale × Σₚ wₚ × Iₚ(θ) × C(θ)  +  Δbg × C(θ)
```

The lower bound on `scale` is **1×10⁻³** (hard floor set in the optimiser). The scale is driven toward this floor when the calculated phase intensities are **orders of magnitude larger than the observed pattern**.

Each phase's intensity already incorporates an `abs_scale` factor:

```
abs_scale = mean_d001 / (CSDS_real_mean × mean_volume² × mean_density)
```

Because `scale` is **per specimen** — it applies equally to every phase in that specimen — a single phase with a grossly inflated `abs_scale` drags the scale down and suppresses all other phases along with it.

---

### Cause 1 — Cell parameters not set (most common)

**What happens:** The component volume is `cell_a × cell_b × d001`. To prevent division by zero, MudLab clamps the minimum volume to 1×10⁻²⁵. If `ucp_a` or `ucp_b` has not been set (e.g., a newly created empty phase), the volume collapses to this floor, giving:

```
abs_scale ∝ 1 / volume²  →  1 / (1e-25)²  =  1e50
```

Even at `scale = 1e-3` the calculated intensity is still astronomically large and the fit is broken.

#### What are ucp_a and ucp_b?

`ucp_a` and `ucp_b` (**Unit Cell Properties**) are the lateral dimensions of the clay layer's unit cell along the **a** and **b** axes (in nm). Together with `d001` (the c-axis basal spacing) they define the layer volume used in the absolute scale calculation:

```
volume = cell_a × cell_b × d001
```

Each `UnitCellProperty` works in one of two modes:

- **Fixed** (`enabled = False`): the `value` field is used directly as the cell dimension. This is the normal case — a number entered in Edit Phases.
- **Formula-driven** (`enabled = True`): the value is computed from the occupancy of a chosen atom in the layer using a linear formula:

  ```
  value = factor × atom_occupancy + constant
  ```

  This is used when the cell dimension depends on the mineral's composition — for example, the b-axis length of illite varies linearly with iron content (Drits formula: `b = 0.3321 × Fe + 0.895` nm). When the iron occupancy is changed in the atom list, `ucp_b` updates automatically.

Both `ucp_a` and `ucp_b` default to `value = 0.0` on a newly created component. Until they are explicitly set, the volume product is zero, the 1×10⁻²⁵ floor applies, and `abs_scale` becomes astronomically large.

**Fix:** Open **Edit Phases**, select the affected phase, and verify that `ucp_a`, `ucp_b`, and `d001` are set to physically reasonable values for the mineral (e.g., `ucp_a ≈ 0.518 nm`, `ucp_b ≈ 0.900 nm` for a dioctahedral clay). Use the standard phases supplied with MudLab as a reference.

---

### Cause 2 — One badly-parameterised phase in a multi-phase mixture

**What happens:** The scale is shared across all phases in a specimen. If even one phase has a large `abs_scale` (due to Cause 1 or any other incorrect parameter), the optimiser drives the common scale to its minimum, simultaneously suppressing all correctly-parameterised phases. The residual increases and the fit is meaningless.

**Fix:** Identify the offending phase by temporarily removing phases from the mixture one at a time and re-running Optimize after each removal. When the scale recovers to a normal value, the last removed phase is the problem. Correct its parameters in Edit Phases.

---

### Cause 3 — Very small average CSDS

**What happens:** `abs_scale` is inversely proportional to `CSDS_real_mean`. A very small average CSDS (e.g., 1–2 layers) gives a `CSDS_real_mean ≈ 1`, making `abs_scale` much larger than it would be for a physically realistic value (e.g., CSDS = 10 gives an `abs_scale` ~10× smaller). On its own this is rarely catastrophic, but it compounds with other causes.

**Fix:** Check the **Average CSDS** value in Edit Phases. A physically reasonable starting value for most clay minerals is 8–15 layers. Values below 3 should be scrutinised.

---

### Cause 4 — All atom occupancies set to zero

**What happens:** The component weight is the sum of all atom weights. If all atom occupancies (`pn`) are zero, `comp.weight = 0`, which makes `mean_density = 0` and therefore `mean_mass = 0`. MudLab handles this edge case by returning `abs_scale = 0`, meaning the phase produces **zero intensity** regardless of scale or fraction. The phase is effectively invisible; scale becomes meaningless for it.

**Symptom distinction:** Unlike Causes 1–3, the scale does not necessarily collapse to the minimum — instead the affected phase simply contributes nothing to the pattern, and the residual will be high if that phase was expected to be present.

**Fix:** Open Edit Phases → select the component → inspect the atom list. Ensure every atom has a non-zero occupancy value (`pn > 0`).

---

### Cause 5 — RawPatternPhase mixed with calculated phases

**What happens:** A RawPatternPhase is normalised internally to a maximum of 1. Calculated phases produce intensities in the range ~0.01–0.1. If a calculated phase with incorrect parameters (Cause 1 or 2) is also in the mixture, the scale may be driven down in an attempt to suppress the inflated calculated phase, distorting the contribution of the RawPatternPhase.

**Fix:** Resolve any parameter issues in the calculated phases first (see Causes 1–3), then re-run Optimize.

---

### Quick diagnostic checklist

Before running Optimize, verify for every phase in the mixture:

1. `ucp_a` and `ucp_b` are set to non-zero values.
2. `d001` is set to a physically reasonable value for the mineral.
3. Average CSDS is ≥ 3 (preferably 8–15 for a starting point).
4. At least one atom in each component has a non-zero occupancy (`pn > 0`).
5. No phase in the mixture is a leftover empty placeholder.

---

[← Back to User Manual](../index.md)
