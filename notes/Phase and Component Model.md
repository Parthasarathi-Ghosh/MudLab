# Phase and Component Model

Source: `mudlab/phases/models/`  
Docs: `docs/how-to/edit-phases.md`

## Phase

A **phase** is one crystallographic entity — a pure layer type or a mixed-layer sequence.

| Property | Meaning |
|---|---|
| `d001` | Basal spacing (Å) — the repeat unit along c |
| `delta_c` | Expansion correction (Å) |
| `default_c` | Default total layer thickness |
| `sigma_star` | Turbostratic disorder (°) |
| `G` | Number of layer types (components) |
| `R` | Reichweite — stacking correlation order |
| `based_on` | Optional parent phase to inherit CSDS/σ* from |

**based_on** is used for treatment variants: one primary phase (AD) defines the full structure; secondary phases (EG, 350°C) inherit CSDS, σ*, and colour and only change d001 and interlayer atoms.

### Stacking model (probabilities)

Probabilities tab: weight fractions of each component and layer-transition probabilities (Q-matrix). The R/G combination determines which probability parameters are shown.

### CSDS Distribution

Coherent Scattering Domain Size — the number-of-layers distribution in a crystallite. Log-normal or custom. Used directly in the intensity calculation. See [[XRD Diffraction Calculation]].

## Component

Each phase has G ≥ 1 components. A component is one distinct **layer type** with its own crystallographic data.

| Property | Meaning |
|---|---|
| `cell_a`, `cell_b` | Lateral unit cell dimensions (Å) |
| `ucp_a`, `ucp_b` | Unit cell property objects (refinable wrappers) |
| `layer_atoms` | Atoms inside the silicate layer |
| `interlayer_atoms` | Atoms in the interlayer space |
| `atom_relations` | [[Atom Relations]] modifying atom pn values |
| `linked_with` | Optional link to a component in the `based_on` phase |

### Linked with

When `phase.based_on` is set, each component can be **Linked with** a component in the parent phase. Linking enables per-property inherit checkboxes (`inherit_layer_atoms`, `inherit_interlayer_atoms`, `inherit_atom_relations`, `inherit_ucp_a`, `inherit_ucp_b`, `inherit_d001`, etc.).

## Atom model

Each atom (layer or interlayer) has:

| Property | Meaning |
|---|---|
| `name` | User label (e.g. `Fe1`) |
| `atom_type` | Reference to an `AtomType` (element + scattering params) |
| `pn` | Occupancy / multiplicity (atoms projected on c-axis per unit cell) |
| `z` | Fractional z-coordinate (Å) |
| `B_iso` | Isotropic displacement parameter (Å²) |
| `default_z` | Z-position without offset |

`pn` may be controlled by [[Atom Relations]] rather than set directly.

## CIF import

Atoms can be bulk-imported from a CIF file via the CIF import dialog. See [[CIF Import]].

## Related Notes

- [[Atom Relations]]
- [[CIF Import]]
- [[XRD Diffraction Calculation]]
- [[Mixture Model]]
- [[GTK UI Conventions]]
