# Simulating Isomorphous Substitutions Using Atom Relations

[← Back to User Manual](../index.md)

> **Printing to PDF:** Open this page in your browser and use **File → Print → Save as PDF**.

This page explains how to use the **Atom Relations** feature in Edit Phases to simulate the full range of isomorphous (ionic) substitutions that occur in clay minerals and phyllosilicates.

---

## Background

Isomorphous substitution means one ion replaces another at a crystallographic site without changing the basic layer structure. In MudLab, the structural atom parameters `pn` (site occupancy × multiplicity) must always reflect the current substitution state. Rather than editing `pn` values by hand, **Atom Relations** let you parameterise a substitution with a single refinable value and have MudLab maintain all constraints automatically.

Two relation types are available:

| Type | Formula | Use for |
|---|---|---|
| **AtomRatio** | `atom1.pn = value × sum`; `atom2.pn = (1−value) × sum` | Binary substitution at one site |
| **AtomContents** | `atom.pn = amount × value` for each listed atom | Absolute occupancy control; master driver for coupled substitutions |

Relations can be **chained**: the target of one relation can be another relation's `value` (RATIO) or `sum` (SUM), allowing coupled multi-site substitutions to be driven by a single parameter.

---

## Prerequisites

Before adding any Atom Relation:

1. **Both atoms must already exist** in the layer or interlayer atom list.
2. Set their initial `pn` values consistently — the relation will overwrite them on first apply, but a sensible starting value avoids confusion.
3. Place them at the correct crystallographic `z` position. Substituting ions at the same site share the same `z` (or very close to it).

---

## Reference: All Substitution Types

The table below lists every substitution class found in natural clay minerals. Worked examples for each follow in the sections below.

| # | Site | Original ion | Substituting ion | Charge effect | Occurs in |
|---|---|---|---|---|---|
| 1 | Tetrahedral | Si⁴⁺ | Al³⁺ | −1 per event | Beidellite, illite, mica |
| 2 | Octahedral (dioctahedral) | Al³⁺ | Mg²⁺ | −1 per event | Montmorillonite, smectite |
| 3 | Octahedral (dioctahedral) | Al³⁺ | Fe³⁺ | 0 (isovalent) | Nontronite, kaolinite |
| 4 | Octahedral (dioctahedral) | Al³⁺ | Fe²⁺ | −1 per event | Some smectites, illites |
| 5 | Octahedral (trioctahedral) | Mg²⁺ | Fe²⁺ | 0 (isovalent) | Chlorite, talc, biotite |
| 6 | Octahedral (trioctahedral) | Mg²⁺ | Fe³⁺ | +1 per event | Some chlorites |
| 7 | Tetrahedral + Octahedral | Si⁴⁺ + Mg²⁺ | Al³⁺ + Al³⁺ | 0 (coupled) | Chlorite, mica (Tschermak) |
| 8 | Octahedral | Al³⁺ | Cr³⁺ | 0 (isovalent) | Synthetic kaolinite |
| 9 | Octahedral | Al³⁺ | Ni²⁺/Zn²⁺/Cu²⁺ | −1 per event | Transition-metal-rich clays |
| 10 | Interlayer | K⁺ | Na⁺ / Ca²⁺ / Mg²⁺ | depends | Smectite, illite |
| 11 | Octahedral (two sub-groups) | Al³⁺ | Mg²⁺ + Fe²⁺ | −1 per event | Smectite (chained) |
| 12 | Hydroxyl | OH⁻ | F⁻ | 0 (isovalent) | Micas, some smectites |

---

## Worked Examples

### 1 — Tetrahedral Si → Al (beidellite, illite, mica)

**Science:** Al³⁺ enters the tetrahedral sheet, replacing Si⁴⁺. Each substitution creates one unit of negative layer charge, compensated by interlayer cations. This is the dominant charge source in beidellite and illite.

**Relation type:** `AtomRatio`

**Atoms required in layer_atoms:**

| Atom | Element | z (Å) | initial pn |
|---|---|---|---|
| Si | Si | ~1.12 | 4 |
| Al_tet | Al | ~1.12 (same site) | 0 |

**Setup:**

| Field | Value |
|---|---|
| Name | `Si-Al(tet)` |
| Sum | `4` — four tetrahedral sites per O₁₀(OH)₂ in a 2:1 clay |
| Atom 1 (substituting) | `Al_tet · pn` |
| Atom 2 (original) | `Si · pn` |
| Value | substitution fraction, e.g. `0.25` |

**Result at value = 0.25:**
```
Al_tet.pn = 0.25 × 4 = 1.0    →  1 Al per formula unit
Si.pn     = 0.75 × 4 = 3.0    →  3 Si per formula unit
```
Formula unit: Si₃Al₁O₁₀

**Refinement bounds:** `[0.0, 0.5]` — Loewenstein's rule limits Al/Si to ≤ 1, so at most half of the 4 tetrahedral sites can carry Al.

---

### 2 — Octahedral Al → Mg (montmorillonite)

**Science:** Mg²⁺ replaces Al³⁺ in the dioctahedral sheet. This is the primary source of negative layer charge in montmorillonite. The two occupied octahedral sites per O₁₀(OH)₂ together carry the substitution.

**Relation type:** `AtomRatio`

**Atoms required in layer_atoms (dioctahedral, 2 occupied sites):**

| Atom | Element | z (Å) | initial pn |
|---|---|---|---|
| Al_oct | Al | ~2.40 | 2 |
| Mg_oct | Mg | ~2.40 | 0 |

**Setup:**

| Field | Value |
|---|---|
| Name | `Al-Mg(oct)` |
| Sum | `2` — two occupied octahedral sites |
| Atom 1 (substituting) | `Mg_oct · pn` |
| Atom 2 (original) | `Al_oct · pn` |
| Value | substitution fraction, e.g. `0.165` |

**Result at value = 0.165:**
```
Mg_oct.pn = 0.165 × 2 = 0.33    →  0.33 Mg per formula unit
Al_oct.pn = 0.835 × 2 = 1.67    →  1.67 Al per formula unit
```
Layer charge per O₁₀(OH)₂: −0.33

---

### 3 — Octahedral Al → Fe³⁺ (nontronite, Fe-kaolinite)

**Science:** Fe³⁺ is isovalent with Al³⁺, so substitution generates **no layer charge**. The diffraction signature changes because Fe has a very different atomic scattering factor. Nontronite is the Fe³⁺-dominant end-member; kaolinite can incorporate up to ~30 mol% Fe³⁺ hydrothermally.

**Relation type:** `AtomRatio`

**Atoms required in layer_atoms:**

| Atom | Element | z (Å) | initial pn |
|---|---|---|---|
| Al_oct | Al | ~2.40 | 2 |
| Fe3_oct | Fe | ~2.40 | 0 |

**Setup:**

| Field | Value |
|---|---|
| Name | `Al-Fe3(oct)` |
| Sum | `2` |
| Atom 1 (substituting) | `Fe3_oct · pn` |
| Atom 2 (original) | `Al_oct · pn` |
| Value | Fe³⁺ fraction, e.g. `0.5` |

**Result at value = 0.5:**
```
Fe3_oct.pn = 1.0    →  Al₁Fe₁ (half-substituted)
Al_oct.pn  = 1.0
```
No layer charge change. Use with a separate tetrahedral Si→Al relation if charge is needed (as in nontronite).

---

### 4 — Octahedral Al → Fe²⁺ (charge-generating)

**Science:** Fe²⁺ is divalent, so each substitution creates one unit of negative charge — the same sense as the Al→Mg substitution but with a heavier scatterer.

Setup is identical to Example 3, but use `Fe` atom type set to **Fe²⁺** (ferrous) in the AtomType selection. Charge effect: −1 per substitution event, same formula as Example 2.

---

### 5 — Trioctahedral Mg → Fe²⁺ (chlorite, talc, biotite)

**Science:** In trioctahedral phases all three octahedral sites are occupied (pn = 6 per full unit cell, or 3 per O₁₀(OH)₂ half cell). Mg²⁺ and Fe²⁺ are isovalent — the substitution is charge-neutral and creates a complete solid solution (clinochlore → chamosite).

**Relation type:** `AtomRatio`

**Atoms required (trioctahedral, 3 occupied sites per O₁₀(OH)₂):**

| Atom | Element | z (Å) | initial pn |
|---|---|---|---|
| Mg_oct | Mg | ~2.40 | 3 |
| Fe2_oct | Fe | ~2.40 | 0 |

**Setup:**

| Field | Value |
|---|---|
| Name | `Mg-Fe2(oct)` |
| Sum | `3` — three trioctahedral sites |
| Atom 1 (substituting) | `Fe2_oct · pn` |
| Atom 2 (original) | `Mg_oct · pn` |
| Value | Fe²⁺ fraction, e.g. `0.33` |

**Result at value = 0.33:**
```
Fe2_oct.pn = 0.33 × 3 = 1.0
Mg_oct.pn  = 0.67 × 3 = 2.0
```
Formula: (Mg₂Fe₁)Si₄O₁₀(OH)₂ — intermediate clinochlore/chamosite.

---

### 6 — Isovalent octahedral substitution: Al → Cr³⁺

Same setup as Example 3 (Al → Fe³⁺) but `Fe3_oct` replaced by a `Cr` atom. No layer charge generated. Observed in synthetic kaolinites made under hydrothermal conditions.

---

### 7 — Interlayer cation substitution: K → Na or Ca

**Science:** In smectites the interlayer cation is exchangeable. Swapping between monovalent (Na⁺, K⁺) and divalent (Ca²⁺, Mg²⁺) species changes basal spacing and hydration state significantly. In models that explicitly include an interlayer atom, this can be parameterised.

**Relation type:** `AtomRatio`

**Atoms required in interlayer_atoms:**

| Atom | Element | z (Å) | initial pn | stretch_z |
|---|---|---|---|---|
| K_il | K | ~d001/2 | 1 | True |
| Na_il | Na | ~d001/2 | 0 | True |

**Setup (K ↔ Na, one interlayer site):**

| Field | Value |
|---|---|
| Name | `K-Na(interlayer)` |
| Sum | `1` — one interlayer cation site |
| Atom 1 (substituting) | `Na_il · pn` |
| Atom 2 (original) | `K_il · pn` |
| Value | Na fraction, e.g. `0.0` (pure K) → `1.0` (pure Na) |

> **Note for divalent cations:** Ca²⁺ or Mg²⁺ compensate two units of charge each. If your layer charge per O₁₀(OH)₂ is 0.33, a Ca²⁺ interlayer would have `pn = 0.165` (half the K equivalent). Adjust `sum` accordingly.

---

### 8 — Hydroxyl → Fluorine substitution

**Science:** F⁻ replaces OH⁻ at the hydroxyl position in the octahedral sheet. Both are monovalent anions of similar ionic radius — no charge is generated. F-substitution increases thermal stability. Occurs in micas, some smectites, and chlorites.

**Atoms required in layer_atoms (or interlayer_atoms for brucite-like sheets):**

| Atom | Element | z (Å) | initial pn |
|---|---|---|---|
| OH_layer | OH | ~0.0 or top of sheet | 2 |
| F_layer | F | same z | 0 |

> **AtomType:** You need an `OH` type and an `F` type already defined in the AtomTypes table. The scattering factors differ — this substitution changes the calculated intensity near low-angle reflections.

**Setup:**

| Field | Value |
|---|---|
| Name | `OH-F` |
| Sum | `2` — two hydroxyl sites per O₁₀(OH)₂ |
| Atom 1 (substituting) | `F_layer · pn` |
| Atom 2 (original) | `OH_layer · pn` |
| Value | F fraction, e.g. `0.0` (pure hydroxyl) |

---

### 9 — Al replaced simultaneously by Mg and Fe²⁺ (chained substitution)

**Science:** In some smectites, both Mg²⁺ and Fe²⁺ replace Al³⁺ in the octahedral sheet. The total substitution is one parameter; the Mg/Fe split is a second, independent parameter. Both can be refined.

This uses **two chained AtomRatio relations**:
- `AtomRatio_MgFe_for_Al` — controls how much of the octahedral Al is replaced (total divalent content)
- `AtomRatio_Mg_for_Fe` — controls the Mg/Fe split within the divalent fraction; its **sum is driven** by the first relation's output via the SUM channel

**Atoms required:**

| Atom | Element | z (Å) | initial pn |
|---|---|---|---|
| Al_oct | Al | ~2.40 | 2 |
| Mg_oct | Mg | ~2.40 | 0 |
| Fe2_oct | Fe | ~2.40 | 0 |

**Relation 1 — `AtomRatio_MgFe_for_Al`:**

| Field | Value |
|---|---|
| Name | `(Mg+Fe)-Al(oct)` |
| Sum | `2` |
| Atom 1 | `AtomRatio_Mg_for_Fe · SUM` ← targets the second relation's sum |
| Atom 2 | `Al_oct · pn` |
| Value | total divalent fraction, e.g. `0.4` |

**Relation 2 — `AtomRatio_Mg_for_Fe`:**

| Field | Value |
|---|---|
| Name | `Mg-Fe(oct)` |
| Sum | driven by Relation 1 (do not edit manually) |
| Atom 1 | `Mg_oct · pn` |
| Atom 2 | `Fe2_oct · pn` |
| Value | Mg fraction within divalent group, e.g. `0.6` |

**Result at value₁ = 0.4, value₂ = 0.6:**
```
Al_oct.pn  = (1 − 0.4) × 2 = 1.2
(Mg + Fe) total = 0.4 × 2 = 0.8     (passed to Relation 2 as its sum)
  Mg_oct.pn  = 0.6 × 0.8 = 0.48
  Fe2_oct.pn = 0.4 × 0.8 = 0.32
```

**Refinement:** Relation 1's `value` and Relation 2's `value` are both independently refinable. Relation 2's `sum` is not refinable (driven by Relation 1). Relation 2's `driven_by_other` flag is NOT set (sum-driving does not lock the value), so both values appear in the refinement parameter list.

---

### 10 — Tschermak coupled substitution (simultaneous tetrahedral + octahedral)

**Science:** The Tschermak substitution couples a tetrahedral and an octahedral exchange so that overall charge balance is maintained:

```
Mg²⁺ (octahedral) + Si⁴⁺ (tetrahedral)  →  Al³⁺ (octahedral) + Al³⁺ (tetrahedral)
```

Both changes must move by the same amount `x` (one Tschermak unit = one ion swapped at each site simultaneously). This is important in chlorites and micas where pure Tschermak exchange is the dominant solid-solution vector.

This uses **one `AtomContents` master** driving the `value` of **two `AtomRatio` slaves**.

**Atoms required:**

| Sheet | Atom | Element | z (Å) | initial pn |
|---|---|---|---|---|
| Layer (tet) | Si | Si | ~1.12 | 4 |
| Layer (tet) | Al_tet | Al | ~1.12 | 0 |
| Layer (oct) | Mg_oct | Mg | ~2.40 | 3 |
| Layer (oct) | Al_oct | Al | ~2.40 | 0 |

**Relation 1 — `AtomRatio_tet` (slave):**

| Field | Value |
|---|---|
| Name | `Si-Al(tet) [Tschermak]` |
| Sum | `4` |
| Atom 1 | `Al_tet · pn` |
| Atom 2 | `Si · pn` |
| Value | `0` initially — will be driven by master |

**Relation 2 — `AtomRatio_oct` (slave):**

| Field | Value |
|---|---|
| Name | `Mg-Al(oct) [Tschermak]` |
| Sum | `3` |
| Atom 1 | `Al_oct · pn` |
| Atom 2 | `Mg_oct · pn` |
| Value | `0` initially — will be driven by master |

**Relation 3 — `AtomContents_Tschermak` (master, refinable):**

| Field | Value |
|---|---|
| Name | `Tschermak` |
| Value | `x` — the Tschermak substitution fraction |
| Atom contents | `(AtomRatio_tet · RATIO, amount = 1.0)` |
| | `(AtomRatio_oct · RATIO, amount = 1.0)` |

The master sets both slaves' `value` to `x × 1.0 = x`. Each slave then applies its own sum:

**Result at x = 0.25:**
```
Tetrahedral:  Al_tet.pn = 0.25 × 4 = 1.0;  Si.pn = 0.75 × 4 = 3.0
Octahedral:   Al_oct.pn = 0.25 × 3 = 0.75; Mg_oct.pn = 0.75 × 3 = 2.25
```
Net charge change: −1 (tet) + 1 (oct) = **0** — Tschermak is charge-neutral.

**Refinement:** Only the master `AtomContents` value is refinable. The two slave `AtomRatio` values carry `driven_by_other = True` and are excluded from the refinement parameter list automatically.

> **Order in the atom relations list matters for value-driven chains.** The master must appear **before** both slaves so that when `_apply_atom_relations` iterates, the slaves' `value` is already updated before their `apply_relation()` runs.

---

## Summary: Choosing the Right Setup

| Substitution | Relation type | Notes |
|---|---|---|
| Single binary, one site | `AtomRatio` | Standard case |
| Isovalent (no charge change) | `AtomRatio` | Same setup; charge balance automatic |
| Two species replacing one (Mg+Fe for Al) | Two `AtomRatio`, chained via SUM | Second relation's sum is driven |
| Simultaneous two-site (Tschermak) | One `AtomContents` + two `AtomRatio`, chained via RATIO | Master drives both slaves' value |
| Absolute occupancy control | `AtomContents` | Used when site is not binary |

---

## Related source files

| Role | File |
|---|---|
| Relation models | `mudlab/phases/models/atom_relations.py` |
| Apply loop | `mudlab/phases/models/component.py` → `_apply_atom_relations()` |
| UI controllers | `mudlab/phases/controllers/atom_relation_controllers.py` |

---

[← Back to User Manual](../index.md)
