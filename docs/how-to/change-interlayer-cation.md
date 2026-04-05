# How to Change an Interlayer Cation

[← Back to User Manual](../index.md)

This guide uses the substitution of Ca²⁺ → Ba²⁺ in an R0 di-smectite as a worked example.
The same principles apply to any interlayer cation substitution.

---

## UI walkthrough: Ca → Ba in R0 Di-Smectite

### Background — how the default phase is structured

When you load **Di-Smectite Ca** from the default phase library, it adds three linked phases to your project:

| Phase name | Treatment | Component | Linked / Based on |
|---|---|---|---|
| S R0 Ca-AD | Air-dried | 2WAT | — (master) |
| S R0 Ca-EG | Ethylene glycol | 2GLY | based on AD; component linked to 2WAT |
| S R0 Ca-350 | Heated 350 °C | Heated | based on AD; component linked to 2WAT |

The EG and 350 components **inherit** layer atoms, ucp_a/b, and delta_c from the 2WAT component, so those fields are hidden in their editors. Each component has its **own** interlayer atoms and its own d001 / default_c — these are always editable independently.

---

### Step 1 — Load the default Di-Smectite Ca phase

1. Open **Edit Phases** from the main toolbar or menu.
2. Click the **+** button at the top-left of the phases list.
3. In the **Add Phase** dialog, select **"Choose a default phase:"**.
4. In the dropdown, navigate to **Smectites → Di-Smectite Ca** and select it.
5. Click **OK**.

Three phases appear in the list: *S R0 Ca-AD*, *S R0 Ca-EG*, *S R0 Ca-350*.

---

### Step 2 — Edit the AD phase (2WAT component)

This is the **master component**. Its layer atoms, ucp_a/b, and delta_c are shared by the other two treatments.

1. Double-click **S R0 Ca-AD** in the phases list to open its editor.
2. In the **Name** field at the top, change the name to **S R0 Ba-AD** (or any name you prefer).
3. Click the **Components** tab and select the single component in the list.
4. In the component editor:
   - Change **Cell length c [nm]** from **1.500** to **1.480**.
   - Change **Default c length [nm]** from **1.500** to **1.480**.
5. In the **Interlayer atoms** table, update all three rows:

   | Row | Field | Old value | New value |
   |---|---|---|---|
   | H2O (below) | Def. Z (nm) | 0.957 | **0.947** |
   | Ca | Atom name | Ca | **Ba** |
   | Ca | Def. Z (nm) | 1.077 | **1.067** |
   | Ca | Element | Ca2+ | **Ba2+** |
   | H2O (above) | Def. Z (nm) | 1.197 | **1.187** |

6. Close the component editor.

> **Why does d001 change here but not in 2GLY?** Ba²⁺ has a larger ionic radius than Ca²⁺ and a different hydration shell geometry, which makes the 2W interlayer structure slightly more compact. Literature values for Ba-smectite air-dried (2W state) are consistently around 14.8 Å compared to 15.0 Å for Ca — a shift of ~0.08° at the d001 peak, which is visible in a good XRD pattern. The glycolated state is dominated by the geometry of the glycol molecule arrangement and is insensitive to the cation.

---

### Step 3 — Edit the EG phase (2GLY component)

1. Double-click **S R0 Ca-EG** in the phases list.
2. Rename the phase to **S R0 Ba-EG**.
3. Go to the **Components** tab and select the component.
4. The **Layer atoms**, **ucp_a/b**, and **delta_c** rows are hidden — they are inherited from the 2WAT component and correct as-is.
5. In the **Interlayer atoms** table, in the Ca row:
   - Change **Atom name** to **Ba**.
   - Change **Element** to **Ba2+**.
6. Do **not** change d001 or Def. Z — the 2GLY values are identical for Ba.
7. Close the component editor.

---

### Step 4 — Edit the 350 phase (Heated component)

This is the only component where the structural parameters **must** be updated, because Ba²⁺ is too large to allow the layer to collapse to the Ca value of 9.6 Å.

1. Double-click **S R0 Ca-350** in the phases list.
2. Rename the phase to **S R0 Ba-350**.
3. Go to the **Components** tab and select the component.
4. In the **Interlayer atoms** table, in the Ca row:
   - Change **Atom name** to **Ba**.
   - Change **Element** to **Ba2+**.
   - Change **Def. Z (nm)** from **0.807** to **0.827**.
5. In the component fields above the atom tables:
   - Change **Cell length c [nm]** from **0.960** to **1.000**.
   - Change **Default c length [nm]** from **0.960** to **1.000**.
6. Close the component editor.

> **Why these values?** Ba²⁺ (ionic radius ~1.35 Å) is large enough to prevent full layer collapse on dehydroxylation. Ba-smectite heated to 350 °C stabilises at ~10.0 Å rather than the 9.6 Å seen for Ca. The new Def. Z follows the midplane rule: 0.654 + (1.000 − 0.654) / 2 = **0.827 nm**.

---

### Step 5 — Export as a new phase file

1. In the phases list, click **S R0 Ba-AD** to select it.
2. Hold **Ctrl** and click **S R0 Ba-EG** and **S R0 Ba-350** to add them to the selection.
3. Click the **Export** button (↓ icon) in the phases toolbar.
4. In the save dialog, enter a filename such as **Di-Smectite Ba** and save as **Phase file (*.PHS)**.

The three linked phases are saved together in a single .phs file. You can load them again in any project using **Import** (↑ icon) in the phases toolbar.

---

## Reference tables

### What changes automatically when you switch the Element

| Parameter | Updated automatically? |
|---|---|
| Cromer-Mann scattering coefficients (a1–5, b1–5, c) | Yes — loaded from built-in table |
| Debye-Waller B factor | Yes |
| Atomic weight (used in Composition) | Yes |
| Ionic charge | Yes |
| **Calc. Z** (read-only column) | Yes — recalculated from Def. Z whenever d001 changes |
| **pn** driven by an AtomRatio / AtomContents relation | Yes — the relation targets the Atom object, not the element |

### What must be changed manually

The interlayer cation sits at the geometric midplane of the interlayer space in all default Di-Smectite components:

```
Def. Z = lattice_d + (d001 − lattice_d) / 2
```

where `lattice_d = 0.654 nm` (z of the topmost basal oxygen, same for all components and treatments).

| Component | Ca d001 | **Ba d001** | Ca Def. Z | **Ba Def. Z** | Change needed? |
|---|---|---|---|---|---|
| 2WAT | 1.500 nm | **1.480 nm** | 1.077 nm | **1.067 nm** | Element, name, d001, default_c, Def. Z, H2O positions |
| 2GLY | 1.686 nm | **1.686 nm** | 1.172 nm | **1.172 nm** | Element + name only |
| Heated | 0.960 nm | **1.000 nm** | 0.807 nm | **0.827 nm** | Element, name, d001, default_c, Def. Z |

*pn stays at 0.4 in all components — Ba²⁺ has the same +2 charge as Ca²⁺.*

> **TODO — verify references before publishing:**
> The Ba 2W d001 ≈ 14.8 Å value needs a confirmed source. Candidates to check:
> - Bérend et al. (1995), Clays and Clay Minerals 43(3):324–336 — likely covers **monovalent** cations only (Li⁺, Na⁺, K⁺, Rb⁺, Cs⁺); may not include Ba.
> - Cases et al. (1997) — companion paper to Bérend 1995, may cover divalent cations.
> - Ferrage et al. (2005), American Mineralogist 90:1494–1507 — detailed smectite hydration modelling; check if Ba is included.
> - Newman & Brown (1987), *Chemistry of Clays and Clay Minerals* — general reference for cation hydration states.
> Once confirmed, replace this block with the correct citation(s).

### Interlayer water and glycol molecules

These are not recalculated automatically when you change the cation or d001. For the 2WAT component, d001 changes, so all interlayer positions must be updated by hand. For 2GLY, d001 is unchanged, so no adjustments are needed.

| Component | Interlayer molecules | Change needed? |
|---|---|---|
| 2WAT | H2O: 0.957 nm (below) → **0.947 nm**; 1.197 nm (above) → **1.187 nm** | **Yes** — d001 changes, so all interlayer z-positions shift |
| 2GLY | Glycol at 0.939, 1.034, 1.310, 1.405 nm; H2O at 1.121, 1.223 nm | No — d001 unchanged |
| Heated | None | — |

### What is not affected at all

| Item | Reason |
|---|---|
| Layer atoms (tetrahedral Si/Al, octahedral Al/Mg/Fe) | Independent of the interlayer cation |
| `lattice_d` | Derived from max z of layer atoms (0.654 nm); unchanged |
| `ucp_a`, `ucp_b` | Silicate framework a/b dimensions; unchanged |
| σ\*, CSDS, stacking probabilities | Phase-level parameters inherited from the AD phase |

---

[← Back to User Manual](../index.md)
