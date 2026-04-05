# Edit Phases — Complete Reference

[← Back to User Manual](../index.md)

This page covers everything you can do in the **Edit Phases** dialogue: what each field means, its unit, how to edit it, and how the values affect the calculated diffraction pattern.

---

## Overview of the dialogue

Edit Phases is a two-panel window:

- **Left panel** — a list of all phases in the project. Buttons below the list add, remove, import, and export phases.
- **Right panel** — the editor for the selected phase. It is divided into a top section (phase-level parameters) and a notebook with three tabs:
  - **CSDS Distribution** — coherent scattering domain size (number-of-layers distribution)
  - **Probabilities & weight fractions** — stacking disorder model and layer-type fractions
  - **Components** — the layer-type crystallographic data

---

## Phases

A **phase** represents one crystallographic layer type or one mixed-layered sequence. Every phase has exactly one set of stacking parameters (R, G) and one CSDS distribution. You add multiple phases to a project, then assign them to specimens via **Edit Mixtures**.

### Managing phases

| Action | How |
|---|---|
| Add a new phase | Click **+** below the phase list. A dialogue asks for name and number of components (G). |
| Delete a phase | Select it and click **−**. This is irreversible; phases in use by a mixture will no longer calculate. |
| Import from a .phs file | Click the import (←) button. A .phs file may contain multiple phase variants (e.g. AD, EG, 350). |
| Export to a .phs file | Select one or more phases and click the export (→) button. |
| Duplicate a phase | There is no duplicate button; export and re-import. |

### Phase-level fields

#### Name & colour

| UI element | Meaning | Notes |
|---|---|---|
| **Name** (text entry) | The label shown in the phase list and plot legend | Free text |
| **Colour** (colour button) | Line colour of this phase's contribution in the plot | Click the swatch to open a colour picker |
| **Inherit colour** (checkbox) | Take colour from the "Based on phase" instead | Only enabled when "Based on phase" is set |

#### Based on phase

A drop-down that links this phase to another phase of the **same G and R** in the project. Used for treatment variants: you create a primary phase (AD), then create secondary phases (EG, 350) that inherit CSDS, σ*, colour, and/or atom positions from the AD phase, changing only d001 and interlayer atoms.

- The dropdown only shows phases with the same G and R and that are not already downstream of this one (no circular references).
- Setting "Based on phase" enables the three **Inherit** checkboxes.

#### Nr. of components (read-only)

Shows the current value of **G** (the number of distinct layer types in this phase). It equals the number of entries in the Components list. To change G you must add or remove components — there is no direct G field to type into.

#### Reichweite (read-only)

Shows **R** (the stacking order / range of correlations). It is derived from the probability model type — you change it by selecting a different model type in the Probabilities tab. R = 0 means random stacking; R = 1 means nearest-neighbour Markov; R = 2 and R = 3 are higher-order.

#### σ* [°] — sigma star

| Detail | Value |
|---|---|
| **UI label** | σ* [°] |
| **Meaning** | Orientation disorder parameter; accounts for turbostratic stacking (random rotation of layers around c-axis) |
| **Unit** | degrees |
| **Range** | 0–90° |
| **Default** | 3.0° |
| **Refinable** | Yes |
| **Inherit checkbox** | "Inherit σ*" — takes value from "Based on phase" |

In the calculation σ* broadens each peak by a Gaussian with standard deviation proportional to σ* and to sin θ. Increasing σ* broadens all basal reflections, with higher-order peaks broadened more strongly. A value of 0 means perfectly oriented crystallites.

**Widget:** `ScaleEntry` (slider + spin button, 0–90°, 5 decimal places).

---

## CSDS Distribution tab

**CSDS** = Coherent Scattering Domain Size. It is the number of layers that scatter coherently; physically, it is the stacking height of a crystallite expressed as a layer count rather than a length. The distribution describes the spread of crystallite sizes in the sample.

### Type selector

A dropdown to switch between two distribution models:

| Type | Description |
|---|---|
| **Log-normal CSDS distr. (Drits et al. 1997)** *(default)* | Log-normal distribution; only **Average CSDS** is editable; the shape parameters (α, β) are fixed at the empirically derived values from Drits 1997 |
| **Generic log-normal CSDS distr. (Eberl et al. 1990)** | Same log-normal form but all four shape parameters are freely editable and refinable |

### Fields (Drits model — default)

| UI label | Meaning | Unit | Default | Refinable |
|---|---|---|---|---|
| **Average CSDS** | Mean number of layers in the stacking sequence ⟨T⟩ | layers (integer) | 10 | Yes |

The minimum is 1, maximum is 200. The corresponding coherent scattering length is `Average CSDS × d001`.

The distribution is sampled from 1 up to `LOG_NORMAL_MAX_CSDS_FACTOR × Average CSDS` (default factor = 10, so up to 100 layers for a mean of 10). A small preview plot in the tab shows the resulting distribution.

**Inherit CSDS checkbox** (in the tab header): tick to take the full distribution from the "Based on phase".

### Fields (Generic log-normal model)

The same **Average CSDS** plus four shape parameters:

| UI label | Meaning | Default | Refinable |
|---|---|---|---|
| **α scale factor** | Scales the α parameter of the log-normal distribution | 0.9485 | Yes |
| **α offset factor** | Shifts the α parameter | −0.0017 | Yes |
| **β² scale factor** | Scales the β² parameter | 0.1032 | Yes |
| **β² offset factor** | Shifts the β² parameter | 0.0034 | Yes |

The parameters are combined as: `α = α_scale × log(⟨T⟩) + α_offset` and `β² = β_scale × log(⟨T⟩) + β_offset`. These control the shape (width and skewness) of the log-normal distribution.

---

## Probabilities & weight fractions tab

This tab is only shown when **G > 1** (mixed-layered phases). For a pure phase (G = 1) there is only one layer type, so no stacking parameters are needed and the tab is hidden.

### What the tab contains

- A stacking model type selector (implicitly: the model type was chosen when the phase was created by setting G and R).
- Editable probability parameters (Wᵢ, Pᵢⱼ) depending on R and G.
- Layer-type weight fractions Fᵢ derived from the Wᵢ.

### Stacking model types and their parameters

The model type is selected when adding a new phase. You cannot change G or R after creation without recreating the phase.

| Model | G | R | Parameters |
|---|---|---|---|
| R0G2Model | 2 | 0 | **F1** — fraction of layer type 1; F2 = 1 − F1 |
| R1G2Model | 2 | 1 | **W1** — weight fraction of layer 1; **P11** — probability that layer 1 is followed by layer 1 |
| R2G2Model | 2 | 2 | W1, P11, P111 |
| R3G2Model | 2 | 3 | W1, P11, P111, P1111 |
| R0G3Model | 3 | 0 | F1, F2 (F3 = 1 − F1 − F2) |
| R1G3Model | 3 | 1 | W1, W2, P11, P12, P21, P22 (subject to sum constraints) |

**F** values are weight fractions (probability of encountering a given layer type, irrespective of context).  
**P** values are conditional transition probabilities: P11 = probability of layer type 1 being followed by layer type 1.

The displayed fields vary by model. Each parameter has a refinement info pair `[min, max, is_refinable]` shown alongside it. All probability parameters are refinable.

---

## Components tab

This tab lists the **components** (layer types) that make up the phase. For a pure phase (G = 1) there is exactly one component. For a mixed-layered phase (G = 2, 3, …) there is one component per layer type.

**Adding and removing components is not supported through the tab buttons** — the buttons are hidden. The number of components is fixed at the G value chosen when the phase was created.

Clicking a component in the list opens its editor in the right panel. The component editor is a table with the following sections.

---

## Component editor

### Name

Free-text label for this layer type. Used in the component list and in exported .cmp files.

### Linked with

A drop-down that links this component to a component of the **same position** in the "Based on phase". When linked, any field with its corresponding **Inherit** checkbox ticked will take its value from the linked component at runtime instead of from its own stored value.

- The dropdown is only populated when the phase has a "Based on phase" set.
- Linking is used for treatment variants: the EG and 350 components link to the AD component so they share the silicate layer structure (atoms, cell dimensions) but have different d001 and interlayer atoms.

---

## Cell dimensions

These three parameters define the c-axis geometry of the layer.

### Cell length c [nm] — d001

| Detail | Value |
|---|---|
| **UI label** | Cell length c [nm] |
| **Internal name** | `d001` |
| **Meaning** | Basal spacing — the full c-axis repeat distance including the interlayer space |
| **Unit** | nm |
| **Range** | 0–5 nm |
| **Default** | 1.0 nm |
| **Refinable** | Yes |
| **Widget** | Slider + spin button (ScaleEntry) |
| **Inherit checkbox** | Tick to take value from linked component |

This is the most important structural parameter. It controls Bragg peak positions directly (`2θₙ = 2 arcsin(nλ / 2d001)`). Changing it also stretches interlayer atom positions (see Interlayer atoms section).

Physically meaningful values for common clay minerals:

| Mineral | d001 (nm) |
|---|---|
| Kaolinite | 0.716 |
| Illite / muscovite | 0.995–1.004 |
| Smectite, 1-water layer (Ca) | ~1.25 |
| Smectite, 2-water layers (Ca) | ~1.50 |
| Smectite, glycolated | ~1.686 |
| Chlorite | ~1.42 |
| Vermiculite (2-water) | ~1.43 |

A new component defaults to 1.0 nm, which is physically meaningless until set correctly.

### Default length c [nm] — default_c

| Detail | Value |
|---|---|
| **UI label** | Default length c [nm] |
| **Internal name** | `default_c` |
| **Meaning** | Reference basal spacing at which the interlayer atom z-positions were originally defined |
| **Unit** | nm |
| **Range** | 0–5 nm |
| **Default** | 1.0 nm |
| **Refinable** | No |
| **Widget** | Slider + spin button (ScaleEntry) |
| **Inherit checkbox** | Tick to take value from linked component |

When you first set up a component, set `default_c = d001`. If you later change d001 (e.g. during a swelling series), the interlayer atoms stretch proportionally between `lattice_d` and `d001` relative to `default_c`. If `default_c` and `d001` are equal no stretching occurs — atom positions are taken literally from `default_z`.

### Δc spacing [nm] — delta_c

| Detail | Value |
|---|---|
| **UI label** | Δc spacing [nm] |
| **Internal name** | `delta_c` |
| **Meaning** | Layer-to-layer c-spacing disorder; introduces a Gaussian spread of basal spacings, broadening all peaks |
| **Unit** | nm |
| **Range** | 0–0.05 nm |
| **Default** | 0.0 nm |
| **Refinable** | Yes |
| **Widget** | Slider + spin button (ScaleEntry) |
| **Inherit checkbox** | Tick to take value from linked component |

δc enters the phase difference factor as a damping term: `PF(stl) = exp(2πi × stl × (d001 × i − π × δc × stl))`. Larger δc broadens higher-order basal reflections more strongly than lower-order ones.

---

## Cell lengths a and b — Unit Cell Properties

The a and b lateral cell dimensions are not simple float fields. They are **Unit Cell Properties** (UCP) — objects that can either hold a fixed value or compute their value from a formula driven by the occupancy (`pn`) of an atom.

Each is displayed as a two-row widget:

**Row 1 — current value:**
```
[value entry]
```

**Row 2 — formula (when enabled):**
```
[Enabled checkbox]   [factor entry]  x  [atom dropdown]  +  [constant entry]
```

### Unit Cell Property fields

| UI element | Meaning | Unit | Default |
|---|---|---|---|
| **Value** (entry, row 1) | Current cell length; directly editable when the formula is disabled | nm | 0.0 |
| **Enabled** (checkbox, row 2) | When ticked, the value is computed as `factor × atom.pn + constant` and the value entry becomes read-only | — | off |
| **Factor** (entry, row 2) | Multiplier applied to the atom's occupancy in the formula | nm / atoms | 1.0 |
| **Atom** (dropdown, row 2) | The atom (from layer or interlayer list) whose `pn` (occupancy) drives the formula | — | none |
| **Constant** (entry, row 2) | Additive offset in the formula | nm | 0.0 |

**Inherit checkboxes** for `ucp_a` and `ucp_b` appear in the component header and work the same as for `d001`.

**Cell length a [nm]** — the a-axis repeat distance of the unit cell. For clay minerals: `a = 0.57735 × b` (hexagonal approximation, so often formula-driven off `cell_b`).

**Cell length b [nm]** — the b-axis repeat distance. For clay minerals, b varies with octahedral composition: Fe-rich compositions have larger b than Al-rich. A typical formula: `b = 0.9 + 0.0043 × Fe_pn`.

The volume used in the absolute intensity scale calculation is `cell_a × cell_b × d001`. Setting `ucp_a = ucp_b = 0` (the default on new components) causes a floor value of `1×10⁻²⁵` to be used for volume, which makes the calculated intensity astronomically large — always set realistic values for a and b before calculating.

---

## Layer atoms

The **Layer atoms** list contains the atoms that form the silicate layer framework (tetrahedral and octahedral sheets). These atoms do **not** move when d001 changes — their z-positions are fixed relative to the silicate lattice.

### Editing the list

| Action | How |
|---|---|
| Add an atom | Click the **+** button below the list |
| Delete an atom | Select a row and click the **−** button |
| Import atoms from .lyr file | Click the ← (Import layer) toolbar button |
| Export selected atoms to .lyr file | Select rows, click → (Export layer) toolbar button |
| Edit a field inline | Double-click the cell (or single-click in an editable column) |

### Columns

| Column | Internal name | Unit | Description |
|---|---|---|---|
| **Atom name** | `name` | — | Free text label (e.g. "Al1", "Si2", "O"). No effect on calculation — for identification only. |
| **Def. Z (nm)** | `default_z` | nm | Default fractional position of the atom along the c-axis. Z = 0 is the bottom oxygen plane of the layer; Z increases toward the interlayer. For a layer with d001 = 0.716 nm, Z = 0.716 would be the very top of the next layer. |
| **Calc. Z (nm)** | `z` (read-only) | nm | The actual z position used in the structure factor calculation. For layer atoms, this equals `default_z` unless `stretch_z` is true (see below). Displayed for reference — not editable. |
| **#** | `pn` | atoms per half unit cell | Number of atoms of this type per half unit cell projected onto the c-axis. Non-integer values represent partial occupancies (e.g. Fe/Al substitution). Also called "multiplicity" or "occupancy". |
| **Element** | `atom_type` | — | Drop-down selecting the ion type from the project's element library. Determines the X-ray scattering factor, charge, and weight. |

> **Note on `pn`:** In the structure factor formula, `pn` is the weight of this atom's contribution. A dioctahedral clay with 4 Si and 4 Al per unit cell uses `pn = 4.0` for each (or `pn = 2.0` per half cell). Partial occupancy (e.g. `pn = 0.5` Fe alongside `pn = 3.5` Al) represents a substitutional solid solution.

---

## Interlayer atoms

The **Interlayer atoms** list is structurally identical to the layer atoms list and uses the same columns. The key difference is:

- Interlayer atoms represent exchangeable cations (K⁺, Na⁺, Ca²⁺, Mg²⁺) and water molecules (H₂O) that occupy the space between silicate layers.
- They have `stretch_z = True` by default, meaning their **Calc. Z (nm)** is **not** `default_z`. Instead, it is recomputed each time d001 changes using:

```
lattice_d = max(layer atom z positions)   (height of the silicate framework)
z_factor  = (d001 − lattice_d) / (default_c − lattice_d)
calc_z    = lattice_d + (default_z − lattice_d) × z_factor
```

So when you increase d001 (e.g. swelling), interlayer atoms move upward proportionally while the silicate layer framework stays fixed.

**Setting up interlayer atoms:**
1. First set `default_c = d001` for the reference state (e.g. the AD spacing).
2. Enter the interlayer atom positions as `default_z` values appropriate for that reference spacing.
3. When you change d001 (for EG or 350 variants), `calc_z` adjusts automatically; you do not need to re-enter atom positions.

### Common interlayer entries

| Ion / molecule | Element name | Typical pn | Notes |
|---|---|---|---|
| K⁺ | K1+ | 1.5–2.0 | Illite interlayer |
| Na⁺ | Na1+ | ~1.0 | Smectite interlayer |
| Ca²⁺ | Ca2+ | 0.3–0.5 | Smectite (Ca-saturation) |
| H₂O (1 layer) | H2O | 3.5–4.0 | Low-charge smectite |
| H₂O (2 layers) | H2O | 3.5 per plane × 2 planes | 2-water-layer smectite |
| Ethylene glycol | Glycol | ~3.2 per plane × 2 planes | Glycolated smectite |
| Mg²⁺ | Mg2+ | 0.3–0.5 | Saponite / hectorite |

The atom types H2O (atom_nr = 301) and Glycol (atom_nr = 302) are special compound entries in the built-in scattering factor table.

---

## Atom relations

**Atom relations** enforce constraints between atom occupancies (`pn`) inside a component. They are listed in the **Atom relations** panel at the bottom-right of the component editor.

Use them when you need to keep total occupancy on a site fixed while changing the substitution ratio, or when you want a single slider to control multiple atoms simultaneously.

### Managing relations

| Action | How |
|---|---|
| Add an AtomRatio | Click **+** in the Atom relations list |
| Add an AtomContents | Click the type selector dropdown first, then **+** |
| Delete a relation | Select a relation and click **−** |
| Edit a relation | Select it — its editor opens in the right panel of the Atom relations section |

Two relation types are available:

---

### AtomRatio

**Purpose:** Maintain a fixed total site occupancy while freely varying the ratio of two atoms. Changing the **Ratio** adjusts both `pn` values simultaneously so they always sum to **Sum**.

**Example:** octahedral Fe/Al substitution in illite. Total octahedral occupancy = 4.0. Ratio = Fe/(Fe + Al).

| UI label | Meaning | Unit | Notes |
|---|---|---|---|
| **Name** | Label for this relation | — | Free text (e.g. "OctFe") |
| **Enabled** (checkbox) | When unticked the relation is suspended and atoms keep their last pn values | — | |
| **Substituting atom** (dropdown) | The atom whose pn = Ratio × Sum | — | Typically the minority species (Fe, Mg, …) |
| **Original atom** (dropdown) | The atom whose pn = (1 − Ratio) × Sum | — | Typically the majority species (Al) |
| **Ratio** (entry) | Fraction of the substituting atom relative to the total: `0 ≤ Ratio ≤ 1` | dimensionless | Refinable |
| **Sum** (entry) | Total site occupancy: `pn_atom1 + pn_atom2` | atoms per half unit cell | |

When you change **Ratio**, both `pn` values are updated immediately and the calculated pattern updates. Ratio is refinable.

The dropdown lists for **Substituting atom** and **Original atom** include all layer and interlayer atoms of this component, plus the `SUM` and `RATIO` properties of any other `AtomRatio` relations — allowing chained substitutions (e.g. Al → Fe + Mg, with a second ratio controlling Fe/Mg).

---

### AtomContents

**Purpose:** Control the occupancy of one or more atoms with a single **Value** parameter, where each atom's `pn` is set to `Value × amount` (a per-atom multiplier).

**Example:** K interlayer content. One relation with Value = 1.5 and one atom (K, amount = 1.0) sets K pn = 1.5.

| UI label | Meaning | Unit | Notes |
|---|---|---|---|
| **Name** | Label for this relation | — | Free text (e.g. "K Content") |
| **Enabled** (checkbox) | Suspend the relation | — | |
| **Value** (entry) | The controlling value; each atom's pn = Value × its amount | varies | Refinable |
| **Atom contents list** | Table of (atom, amount) pairs that this relation drives | — | Add rows with **+**; each row has an atom dropdown and an amount entry |

Each row in the atom contents list sets `atom.pn = Value × amount`. Using amount = 1 means the atom's pn directly equals Value.

---

## Elements (Atom Types)

**Elements** are the ion definitions that back the **Element** column in the atom lists. They contain all the X-ray scattering parameters for one ionic species.

Elements are managed in a **separate** Edit Atom Types dialogue (accessible via the main application menu), not from Edit Phases. The Edit Phases atom lists reference the elements by name.

### What an element contains

| Field | Meaning | Unit |
|---|---|---|
| **Name** | Ion name (e.g. "Al1.5+", "Fe2+", "H2O") | — |
| **Atom Nr** | Atomic number (e.g. 13 for Al, 26 for Fe). Values > 300 indicate compound types (H2O = 301, Glycol = 302). | — |
| **Charge** | Formal charge of the ion | elementary charge units |
| **Weight** | Atomic weight | amu |
| **Debye** | Debye–Waller temperature factor B | Å² |
| **c** | Constant term in Cromer–Mann scattering factor formula | electrons |
| **a1–a5, b1–b5** | Gaussian expansion coefficients of the Cromer–Mann formula | electrons (aᵢ), Å² (bᵢ) |

The **Cromer–Mann** formula computes the atomic scattering factor as:

```
f(s) = c + Σᵢ aᵢ × exp(−bᵢ × s²)

where s = (sin θ / λ)² = stl²
```

The built-in library (`atomic scattering factors.atl`) contains 218 entries from Waasmaier & Kirfel (1995), covering all common clay-mineral ions including fractional oxidation states (Al1.5+, Fe1.5+, Mg1+) and compound species (H2O, Glycol). Additional elements can be defined per-project in Edit Atom Types.

### How elements are resolved

When a project file is loaded, each atom's `atom_type_name` string is matched against the project's atom type list, then against the built-in table. If no match is found the atom has no scattering contribution (its structure factor is zero).

---

## Inherit checkboxes — summary

Inherit checkboxes appear throughout the phase and component editor. They are only active when a "based on" (phase level) or "linked with" (component level) relationship is set.

| Level | Checkbox | What it inherits |
|---|---|---|
| Phase | Inherit colour | Display colour from "Based on phase" |
| Phase | Inherit σ* | σ* value from "Based on phase" |
| Phase | Inherit CSDS (tab header) | Entire CSDS distribution from "Based on phase" |
| Component | Inherit cell length a | ucp_a object (value, formula) from linked component |
| Component | Inherit cell length b | ucp_b object (value, formula) from linked component |
| Component | Inherit cell length c | d001 value from linked component |
| Component | Inherit default length c | default_c value from linked component |
| Component | Inherit Δc spacing | delta_c value from linked component |
| Component | Inherit layer atoms | Entire layer atom list from linked component |
| Component | Inherit interlayer atoms | Entire interlayer atom list from linked component |
| Component | Inherit atom relations | Entire atom relations list from linked component |

When an inherit checkbox is ticked:
- The corresponding input widget is **hidden** (not just greyed out).
- The field's value comes from the parent phase/component at calculation time.
- The stored value in the file is ignored at runtime but still saved (allowing you to un-inherit without losing your work).

---

## Refinable parameters — summary

The following parameters from Edit Phases can be selected in the Refinement dialogue:

| Parameter | Where set | Unit |
|---|---|---|
| σ* | Phase level | ° |
| Average CSDS | CSDS Distribution tab | layers |
| Stacking probabilities (Wᵢ, Pᵢⱼ, Fᵢ) | Probabilities tab | dimensionless |
| Cell length c (d001) | Component — cell dimensions | nm |
| Δc spacing (delta_c) | Component — cell dimensions | nm |
| Cell length a (ucp_a value) | Component — unit cell property (when formula disabled) | nm |
| Cell length b (ucp_b value) | Component — unit cell property (when formula disabled) | nm |
| AtomRatio value | Component — atom relations | dimensionless |
| AtomContents value | Component — atom relations | varies |

Each refinable parameter has a `_ref_info` triplet `[minimum, maximum, is_refinable]` that you edit from the Refinement dialogue's parameter table.

---

[← Back to User Manual](../index.md)
