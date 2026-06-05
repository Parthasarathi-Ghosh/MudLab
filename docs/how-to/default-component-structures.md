# Default Component Structures

[← Back to User Manual](../index.md)

> **Printing to PDF:** Open this page in your browser and use **File → Print → Save as PDF**.

Typographic cross-section diagrams for every default component shipped with MudLab.
All `pn` and `z` values are taken directly from the component files.
`lattice_d` = maximum `Def. Z` of the layer atoms (computed at runtime).

---

## How to read the diagrams

```
z = d001 ══════  d001  (full basal spacing = c*)
  ·  atom   pn = X     interlayer atoms  (stretch_z = True)
z = ld   ══════  lattice_d  (top of rigid T-O-T or T-O layer)
  │  atom   pn = X     layer atoms  (stretch_z = False)
z = 0    ══════  z = 0
```

- **pn** = projected number = site occupancy × multiplicity per unit cell (MudLab full unit cell = 2 × O₁₀(OH)₂)
- `·` = interlayer region (atoms scale with d001)
- `│` = rigid T-O-T (or T-O) layer

---

## A — 2:1 Dioctahedral family

The T-O-T layer is common to all members of this family. It is shown in full once (Di-Smectite Dehydrated) and abbreviated in subsequent diagrams.

### A1 — Di-Smectite, Dehydrated  *(collapsed interlayer)*

```
                     ← bottom of adjacent T-O-T layer
z = 0.998 nm ══════════════════════════  d001
             ·
             ·  Ca²⁺   pn = 0.40        [Ca content = 0.40]
z = 0.826 nm ·  ───────────────────────  (collapsed interlayer, no H₂O)
             │
z = 0.654 nm ══════════════════════════  lattice_d  (top of T-O-T)
             │  O (basal)    pn = 6.0   ← upper surface
             │  ───────────────────────  UPPER TETRAHEDRAL SHEET
             │  Si           pn = 4.0     Si₄O₁₀ framework
z = 0.597 nm │  ───────────────────────
             │  O (apical)   pn = 4.0  ┐ tet / oct boundary
z = 0.433 nm │  OH (inner)   pn = 2.0  ┘
             │  ───────────────────────  OCTAHEDRAL SHEET  (dioctahedral)
             │  Al           pn = 3.5     Al : Fe = 7 : 1
z = 0.327 nm │  Fe           pn = 0.5     AtomRatio OctFe value=0.125, sum=4.0
             │  ───────────────────────
             │  OH (inner)   pn = 2.0  ┐ oct / tet boundary
z = 0.221 nm │  O (apical)   pn = 4.0  ┘
             │  ───────────────────────  LOWER TETRAHEDRAL SHEET
             │  Si           pn = 4.0     Si₄O₁₀ framework
z = 0.057 nm │  ───────────────────────
             │  O (basal)    pn = 6.0   ← lower surface
z = 0.000 nm ══════════════════════════  z = 0
                     ← top of adjacent T-O-T layer below

  Layer charge: Ca.pn × 2 = 0.40 × 2 = 0.80 / unit cell
```

---

### A2 — Di-Smectite, Ca 1-water layer  *(1WAT)*

T-O-T layer: identical to A1. Interlayer only:

```
z = 1.250 nm ══════════════════════════  d001
             ·  H₂O    pn = 3.5         [H₂O content = 3.5]
z = 1.070 nm ·  Ca²⁺   pn = 0.40        [Ca content = 0.40]  charge = 0.80/uc
z = 0.900 nm ·  (single H₂O plane — 1WAT geometry)
z = 0.654 nm ══════════════════════════  lattice_d
```

---

### A3 — Di-Smectite, Ca 2-water layer  *(2WAT)*

T-O-T layer: identical to A1. Interlayer:

```
z = 1.500 nm ══════════════════════════  d001
             ·  H₂O    pn = 3.5         [H₂O content = 3.5]
z = 1.197 nm ·  ─────────────────────── upper water plane
             ·  Ca²⁺   pn = 0.40        [Ca content = 0.40]  charge = 0.80/uc
z = 1.077 nm ·  ─────────────────────── interlayer cation
             ·  H₂O    pn = 3.5         lower water plane
z = 0.957 nm ·  ───────────────────────
z = 0.654 nm ══════════════════════════  lattice_d
```

---

### A4 — Di-Smectite, Ca 1-glycol layer  *(1GLY)*

T-O-T layer: identical to A1. Interlayer (glycol replaces H₂O):

```
z = 1.290 nm ══════════════════════════  d001
             ·  Glycol  pn = 2.0         [Glycol content = 2.0]
z = 1.017 nm ·  ─────────────────────── upper glycol plane
             ·  Ca²⁺   pn = 0.40         charge = 0.80/uc
z = 0.972 nm ·  ─────────────────────── interlayer cation
             ·  Glycol  pn = 2.0         lower glycol plane
z = 0.927 nm ·  ───────────────────────
z = 0.654 nm ══════════════════════════  lattice_d
```

---

### A5 — Di-Smectite, Ca 2-glycol layer  *(2GLY)*

T-O-T layer: identical to A1. Interlayer (two glycol bilayers + residual H₂O):

```
z = 1.686 nm ══════════════════════════  d001
             ·  Glycol  pn = 1.7        ┐ [Glycol content = 1.7]
z = 1.405 nm ·  Glycol  pn = 1.7        │ upper glycol bilayer
z = 1.310 nm ·  ─────────────────────── ┘
             ·  H₂O    pn = 1.2          [Water content = 1.2]
z = 1.223 nm ·  ─────────────────────── upper water plane
             ·  Ca²⁺   pn = 0.40         charge = 0.80/uc
z = 1.172 nm ·  ─────────────────────── interlayer cation
             ·  H₂O    pn = 1.2          lower water plane
z = 1.121 nm ·  ─────────────────────── ┐
             ·  Glycol  pn = 1.7         │ lower glycol bilayer
z = 1.034 nm ·  Glycol  pn = 1.7        ┘
z = 0.939 nm ·  ───────────────────────
z = 0.654 nm ══════════════════════════  lattice_d
```

---

### A6 — Di-Vermiculite, Ca 2-water layer  *(higher layer charge)*

T-O-T layer: same octahedral Al:Fe = 7:1 as Di-Smectite. Interlayer differs in Ca pn:

```
z = 1.450 nm ══════════════════════════  d001
             ·  H₂O    pn = 3.5         [H₂O content = 3.5]
z = 1.197 nm ·  ─────────────────────── upper water plane
             ·  Ca²⁺   pn = 0.70        [Ca content = 0.70]  charge = 1.40/uc
z = 1.077 nm ·  ─────────────────────── (higher charge than smectite)
             ·  H₂O    pn = 3.5         lower water plane
z = 0.957 nm ·  ───────────────────────
z = 0.654 nm ══════════════════════════  lattice_d  (same T-O-T as A1)
```

---

### A7 — Di-Vermiculite, Ca 1-glycol layer  *(1GLY)*

```
z = 1.290 nm ══════════════════════════  d001
             ·  Glycol  pn = 2.0
z = 1.017 nm ·  Ca²⁺   pn = 0.70        charge = 1.40/uc
z = 0.972 nm ·  Glycol  pn = 2.0
z = 0.927 nm ·  ───────────────────────
z = 0.654 nm ══════════════════════════  lattice_d
```

---

### A8 — Illite  *(fixed K⁺, no water)*

T-O-T layer: Al:Fe = 7:1 (same as Di-Smectite). Interlayer: fixed K⁺, no swelling.

```
z = 0.998 nm ══════════════════════════  d001
             ·
             ·  K⁺     pn = 1.50        [K Content = 1.50]  charge = 1.50/uc
z = 0.829 nm ·  ─────────────────────── (non-exchangeable — fixed in ditrigonal cavity)
             │
z = 0.660 nm ══════════════════════════  lattice_d
             │  O (basal)    pn = 6.0
             │  ───────────────────────  UPPER TETRAHEDRAL SHEET
z = 0.602 nm │  Si           pn = 4.0
             │  O/OH (apical/inner)  pn = 4.0 / 2.0
z = 0.437 nm │  ───────────────────────  OCTAHEDRAL SHEET  (dioctahedral)
             │  Al           pn = 3.5     Al : Fe = 7 : 1
z = 0.330 nm │  Fe           pn = 0.5     OctFe value=0.125, sum=4.0
             │  OH/O (inner/apical)  pn = 2.0 / 4.0
z = 0.224 nm │  ───────────────────────  LOWER TETRAHEDRAL SHEET
z = 0.058 nm │  Si           pn = 4.0
             │  O (basal)    pn = 6.0
z = 0.000 nm ══════════════════════════  z = 0
```

---

### A9 — Muscovite  *(K⁺ mica, low Fe)*

T-O-T same geometry as Illite. Octahedral has less Fe:

```
z = 1.002 nm ══════════════════════════  d001
             ·  K⁺     pn = 1.50        charge = 1.50/uc  (non-exchangeable)
z = 0.831 nm ·  ───────────────────────
z = 0.660 nm ══════════════════════════  lattice_d
             │         [same T-O-T structure as Illite, except:]
             │  OCTAHEDRAL:  Al pn=3.8  +  Fe pn=0.2    Al : Fe = 19 : 1
             │               OctFe value=0.050, sum=4.0  (purer aluminium)
z = 0.000 nm ══════════════════════════  z = 0
```

---

### A10 — Paragonite  *(Na⁺ mica)*

Octahedral: Al:Fe = 7:1. Interlayer: Na⁺ replaces K⁺, higher charge.

```
z = 0.960 nm ══════════════════════════  d001
             ·  Na⁺    pn = 2.00        charge = 2.00/uc  (full mica charge)
z = 0.810 nm ·  ─────────────────────── (Na⁺ is smaller than K⁺ → slightly smaller d001)
z = 0.660 nm ══════════════════════════  lattice_d
             │         [same T-O-T as Illite]
             │  OCTAHEDRAL:  Al pn=3.5  +  Fe pn=0.5    Al : Fe = 7 : 1
z = 0.000 nm ══════════════════════════  z = 0
```

---

### A11 — Margarite  *(Ca²⁺ brittle mica, very high charge)*

Octahedral: Al:Fe = 7:1. Interlayer: Ca²⁺, charge = 4.0/uc (highest of all defaults).

```
z = 0.956 nm ══════════════════════════  d001
             ·  Ca²⁺   pn = 2.00        charge = 2.00 × 2 = 4.00/uc  ← brittle mica
z = 0.808 nm ·  ─────────────────────── (Ca²⁺ is non-exchangeable at this charge level)
z = 0.660 nm ══════════════════════════  lattice_d
             │         [same T-O-T as Illite]
             │  OCTAHEDRAL:  Al pn=3.5  +  Fe pn=0.5    Al : Fe = 7 : 1
z = 0.000 nm ══════════════════════════  z = 0
```

---

### A12 — Leucophyllite  *(K⁺ mica variant)*

Same as Illite/Muscovite in structure. Octahedral: Al:Fe = 7:1.

```
z = 0.986 nm ══════════════════════════  d001
             ·  K⁺     pn = 1.50        charge = 1.50/uc
z = 0.823 nm ·  ───────────────────────
z = 0.660 nm ══════════════════════════  lattice_d
             │         [same T-O-T as Illite]
             │  OCTAHEDRAL:  Al pn=3.5  +  Fe pn=0.5    Al : Fe = 7 : 1
z = 0.000 nm ══════════════════════════  z = 0
```

---

## B — 2:1 Trioctahedral family

Three octahedral sites occupied (pn = 6 per unit cell). Octahedral cations are Mg²⁺ and Fe²⁺.

### B1 — Tri-Smectite, Ca 2-water layer  *(2WAT)*

```
z = 1.500 nm ══════════════════════════  d001
             ·  H₂O    pn = 3.5         [H₂O content = 3.5]
z = 1.197 nm ·  ─────────────────────── upper water plane
             ·  Ca²⁺   pn = 0.40        [Ca content = 0.40]  charge = 0.80/uc
z = 1.077 nm ·  ─────────────────────── interlayer cation
             ·  H₂O    pn = 3.5         lower water plane
z = 0.957 nm ·  ───────────────────────
             │
z = 0.602 nm ══════════════════════════  lattice_d  (slightly thinner than dioctahedral)
             │  O (basal)    pn = 6.0
             │  ───────────────────────  UPPER TETRAHEDRAL SHEET
z = 0.597 nm │  Si           pn = 4.0
             │  O/OH (apical/inner)  pn = 4.0 / 2.0
z = 0.433 nm │  ───────────────────────  OCTAHEDRAL SHEET  (trioctahedral, 3 sites)
             │  Mg           pn = 5.0     Mg : Fe = 5 : 1
z = 0.327 nm │  Fe           pn = 1.0     OctFe value=0.167, sum=6.0
             │  OH/O (inner/apical)  pn = 2.0 / 4.0
z = 0.221 nm │  ───────────────────────  LOWER TETRAHEDRAL SHEET
z = 0.052 nm │  Si           pn = 4.0
             │  O (basal)    pn = 6.0
z = 0.000 nm ══════════════════════════  z = 0
```

---

### B2 — Tri-Smectite, Ca 1-glycol layer  *(1GLY)*

T-O-T layer: identical to B1. Interlayer:

```
z = 1.290 nm ══════════════════════════  d001
             ·  Glycol  pn = 2.0
z = 1.017 nm ·  Ca²⁺   pn = 0.40         charge = 0.80/uc
z = 0.972 nm ·  Glycol  pn = 2.0
z = 0.927 nm ·  ───────────────────────
z = 0.602 nm ══════════════════════════  lattice_d
```

---

### B3 — Talc  *(trioctahedral, no interlayer, charge-neutral)*

Symmetric 2:1 structure. Layer atoms listed by symmetry-distinct sites (two entries per sheet).
Mg is split into two equivalent positions. No interlayer — talc has zero layer charge.

```
z = 0.940 nm ══════════════════════════  d001
             │  (no interlayer — charge-neutral, van der Waals gap only)
             │  interlayer thickness: 0.940 − 0.652 = 0.288 nm
             │
z = 0.652 nm ══════════════════════════  lattice_d
             │  O (basal)    pn = 2+2+2 = 6.0   (3 symmetry sites)
             │  ───────────────────────  UPPER TETRAHEDRAL SHEET
z = 0.598 nm │  Si × 2      pn = 2+2 = 4.0
             │  O (apical)   pn = 4.0
z = 0.436 nm │  OH (inner)   pn = 2.0
             │  ───────────────────────  OCTAHEDRAL SHEET  (trioctahedral)
             │  Mg × 2      pn = 3+3 = 6.0    (pure Mg, no Fe substitution here)
z = 0.326 nm │  ───────────────────────  (charge-neutral, no Fe default)
             │  OH (inner)   pn = 2.0
z = 0.221 nm │  O (apical)   pn = 4.0
             │  ───────────────────────  LOWER TETRAHEDRAL SHEET
z = 0.055 nm │  Si × 2      pn = 2+2 = 4.0
             │  O (basal)    pn = 2+2+2 = 6.0
z = 0.000 nm ══════════════════════════  z = 0
```

---

## C — 1:1 Dioctahedral

One tetrahedral sheet + one octahedral sheet. No second tetrahedral sheet.
Outer surface = exposed OH groups (hydrophilic).

### C1 — Kaolinite  *(1:1 dioctahedral, no interlayer)*

```
z = 0.716 nm ══════════════════════════  d001
             │  (no interlayer — zero layer charge, van der Waals gap)
             │  gap: 0.716 − 0.436 = 0.280 nm
             │
z = 0.436 nm ══════════════════════════  lattice_d
             │  OH (surface)  pn = 2+2+2 = 6.0  ← exposed hydroxyl surface (3 sites)
z = 0.433 nm │  ───────────────────────  OCTAHEDRAL SHEET  (dioctahedral, 2 sites)
             │  Al × 2       pn = 2+2 = 4.0      (no substitution in default)
z = 0.337 nm │  ───────────────────────
             │  OH (inner)   pn = 2.0   ┐ tet / oct boundary
z = 0.230 nm │  O (apical)   pn = 2+2 = 4.0  ┘
             │  ───────────────────────  TETRAHEDRAL SHEET
z = 0.065 nm │  Si × 2      pn = 2+2 = 4.0
             │  O (basal)    pn = 2+2+2 = 6.0  (3 symmetry sites)
z = 0.000 nm ══════════════════════════  z = 0
                     ← top of adjacent T-O layer below
```

---

## D — 1:1 Trioctahedral

### D1 — Serpentine  *(1:1 trioctahedral, no interlayer)*

Three octahedral sites (pn = 6). Outer surface = OH groups. No interlayer.

```
z = 0.726 nm ══════════════════════════  d001
             │  (no interlayer — charge-neutral)
             │  gap: 0.726 − 0.432 = 0.294 nm
             │
z = 0.432 nm ══════════════════════════  lattice_d
             │  OH (surface)  pn = 6.0   ← exposed hydroxyl surface (outer)
             │  ───────────────────────  OCTAHEDRAL SHEET  (trioctahedral, 3 sites)
             │  Mg           pn = 5.0     Mg : Fe = 5 : 1
z = 0.331 nm │  Fe           pn = 1.0     OctFe value=0.167, sum=6.0
             │  ───────────────────────
             │  OH (inner)   pn = 2.0   ┐ tet / oct boundary
z = 0.227 nm │  O (apical)   pn = 4.0   ┘
             │  ───────────────────────  TETRAHEDRAL SHEET
z = 0.058 nm │  Si           pn = 4.0
             │  O (basal)    pn = 6.0
z = 0.000 nm ══════════════════════════  z = 0
```

---

## E — Chlorite  *(2:1 + brucite hydroxide interlayer sheet)*

Chlorite is unique: the "interlayer" is not exchangeable ions but a **fixed brucite-like hydroxide sheet** — a second octahedral layer sandwiched between two T-O-T layers. Both the 2:1 layer octahedral sheet and the brucite sheet have the same Mg:Fe composition.

```
z = 1.420 nm ══════════════════════════  d001
             ·
             ·  OH (brucite top)   pn = 6.0  ← top surface of brucite sheet
z = 1.134 nm ·  ─────────────────────────────  BRUCITE-LIKE HYDROXIDE SHEET
             ·  Mg               pn = 5.25   Mg : Fe = 7 : 1  (structural, not exchangeable)
z = 1.032 nm ·  Fe               pn = 0.75   TriOctFe OH sheet value=0.125, sum=6.0
             ·  ─────────────────────────────
             ·  OH (brucite bot)  pn = 6.0  ← bottom surface of brucite sheet
z = 0.930 nm ·  ───────────────────────
             │
z = 0.654 nm ══════════════════════════  lattice_d  (top of 2:1 layer)
             │  O (basal)    pn = 6.0
             │  ───────────────────────  UPPER TETRAHEDRAL SHEET  (trioctahedral Si)
z = 0.602 nm │  Si           pn = 4.0     (DiSi pn=0, TriSi pn=4 → fully trioctahedral)
             │  O/OH (apical/inner)  pn = 4.0 / 2.0
z = 0.433 nm │  ───────────────────────  OCTAHEDRAL SHEET  (2:1 layer, trioctahedral)
             │  Mg           pn = 5.25    Mg : Fe = 7 : 1
z = 0.327 nm │  Fe           pn = 0.75    TriOctFe Si sheet value=0.125, sum=6.0
             │  OH/O (inner/apical)  pn = 2.0 / 4.0
z = 0.221 nm │  ───────────────────────  LOWER TETRAHEDRAL SHEET
z = 0.057 nm │  Si           pn = 4.0     (TriSi pn=4, DiSi pn=0)
             │  O (basal)    pn = 6.0
z = 0.000 nm ══════════════════════════  z = 0
                     ← top of adjacent T-O-T layer below
```

> **Charge balance in Chlorite:** The 2:1 layer carries negative charge (from any tetrahedral or octahedral substitution); the brucite sheet carries positive charge (from Al substituting Mg). In the default model both are pure Mg+Fe with no Al — net charge ≈ 0. Add Al via AtomRatio to activate the charge-balance mechanism.

---

## Summary table

| Component | Type | d001 (nm) | lattice_d (nm) | Interlayer | Layer charge /uc |
|---|---|---|---|---|---|
| Di-Smectite Dehydr | 2:1 dioctahedral | 0.998 | 0.654 | Ca²⁺ (collapsed) | 0.80 |
| Di-Smectite 1WAT | 2:1 dioctahedral | 1.250 | 0.654 | Ca²⁺ + H₂O | 0.80 |
| Di-Smectite 2WAT | 2:1 dioctahedral | 1.500 | 0.654 | Ca²⁺ + 2×H₂O | 0.80 |
| Di-Smectite 1GLY | 2:1 dioctahedral | 1.290 | 0.654 | Ca²⁺ + Glycol | 0.80 |
| Di-Smectite 2GLY | 2:1 dioctahedral | 1.686 | 0.654 | Ca²⁺ + 2×Glycol + H₂O | 0.80 |
| Di-Vermiculite 2WAT | 2:1 dioctahedral | 1.450 | 0.654 | Ca²⁺ + 2×H₂O | **1.40** |
| Di-Vermiculite 1GLY | 2:1 dioctahedral | 1.290 | 0.654 | Ca²⁺ + Glycol | **1.40** |
| Illite | 2:1 dioctahedral | 0.998 | 0.660 | K⁺ (fixed) | 1.50 |
| Muscovite | 2:1 dioctahedral | 1.002 | 0.660 | K⁺ (fixed) | 1.50 |
| Paragonite | 2:1 dioctahedral | 0.960 | 0.660 | Na⁺ (fixed) | 2.00 |
| Margarite | 2:1 dioctahedral | 0.956 | 0.660 | Ca²⁺ (fixed) | **4.00** |
| Leucophyllite | 2:1 dioctahedral | 0.986 | 0.660 | K⁺ (fixed) | 1.50 |
| Tri-Smectite 2WAT | 2:1 trioctahedral | 1.500 | 0.602 | Ca²⁺ + 2×H₂O | 0.80 |
| Tri-Smectite 1GLY | 2:1 trioctahedral | 1.290 | 0.602 | Ca²⁺ + Glycol | 0.80 |
| Talc | 2:1 trioctahedral | 0.940 | 0.652 | none | 0 |
| Kaolinite | 1:1 dioctahedral | 0.716 | 0.436 | none | 0 |
| Serpentine | 1:1 trioctahedral | 0.726 | 0.432 | none | 0 |
| Chlorite | 2:1 + brucite sheet | 1.420 | 0.654 | OH sheet (structural) | ≈ 0 |

---

[← Back to User Manual](../index.md)
