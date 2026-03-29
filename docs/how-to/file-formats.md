# Phase and Component File Formats

[← Back to User Manual](../index.md)

Both `.phs` (phase) and `.cmp` (component) files are **ZIP archives** containing one or more JSON entries. You can open them with any ZIP tool (e.g., 7-Zip, Windows Explorer) to inspect or manually edit the JSON. Comments in the examples below (lines starting with `//`) are added for explanation and are **not** part of the actual JSON.

---

## Component File (`.cmp`)

A component file contains a single ZIP entry named after the component's UUID. It encodes the full crystallographic description of one layer type: basal spacing, unit cell parameters, atom positions, and occupancy constraints.

### Example — Kaolinite.cmp

Kaolinite is a 1:1 di-octahedral clay with no interlayer. It has no atom relations (fixed stoichiometry).

```jsonc
{
    "type": "Component",
    "properties": {
        "uuid": "5cbe111a07e711e28873782bcbaf1941",   // unique ID for cross-referencing
        "name": "Kaolinite",

        // d001: basal spacing in nm (layer repeat distance, ~0.716 nm for kaolinite)
        // d001_ref_info: [min, max, refineable] — refinement bounds and flag
        "d001_ref_info": [0.71, 0.73, false],
        "d001": 0.716,
        "default_c": 0.716,        // initial c used when no delta_c is applied

        // delta_c: perturbation to c; usually 0.0 for ideal stacking
        "delta_c_ref_info": [0.0, 0.05, false],
        "delta_c": 0.0,

        // ucp_a, ucp_b: lateral unit cell parameters a and b (in nm)
        // Stored as UnitCellProperty objects that can be fixed or formula-driven
        "ucp_a": {
            "type": "UnitCellProperty",
            "properties": {
                "uuid": "5cbe0abc07e711e28873782bcbaf1941",
                "value": 0.5162,       // current value in nm
                "factor": 0.57735,     // formula: value = factor * prop + constant
                "constant": 0.0,
                "prop": [              // [uuid, attribute] — links to ucp_b of this component
                    "5cbe111a07e711e28873782bcbaf1941", "cell_b"
                ],
                "enabled": true        // formula is active; ucp_a tracks ucp_b
            }
        },
        "ucp_b": {
            "type": "UnitCellProperty",
            "properties": {
                "uuid": "5cbe20ce07e711e28873782bcbaf1941",
                "value": 0.894,        // b = 0.894 nm (fixed, no formula)
                "factor": 1.0,
                "constant": 0.0,
                "prop": null,
                "enabled": false       // formula disabled; value is used directly
            }
        },

        // inherit_* flags: if true, this component takes the value from its linked_with parent
        "inherit_d001": false,
        "inherit_ucp_b": false,
        "inherit_ucp_a": false,
        "inherit_default_c": false,
        "inherit_delta_c": false,
        "inherit_layer_atoms": false,
        "inherit_interlayer_atoms": false,
        "inherit_atom_relations": false,

        // atom_relations: occupancy constraints (none for kaolinite — stoichiometry is fixed)
        "atom_relations": [],

        // layer_atoms: atoms in the silicate layer (tetrahedral + octahedral sheets)
        // default_z: fractional position along c within the layer (0 = bottom oxygen plane)
        // pn: number of atoms per half unit cell
        // atom_type_name: key into the atomic scattering factors table
        "layer_atoms": [
            {"type": "Atom", "properties": {"name": "Al1",  "default_z": 0.3378, "pn": 2.0, "atom_type_name": "Al1.5+"}},
            {"type": "Atom", "properties": {"name": "Al2",  "default_z": 0.3363, "pn": 2.0, "atom_type_name": "Al1.5+"}},
            {"type": "Atom", "properties": {"name": "Si1",  "default_z": 0.065,  "pn": 2.0, "atom_type_name": "Si2+"}},
            {"type": "Atom", "properties": {"name": "Si2",  "default_z": 0.0653, "pn": 2.0, "atom_type_name": "Si2+"}},
            {"type": "Atom", "properties": {"name": "O",    "default_z": 0.2268, "pn": 2.0, "atom_type_name": "O1-"}},
            {"type": "Atom", "properties": {"name": "O",    "default_z": 0.2272, "pn": 2.0, "atom_type_name": "O1-"}},
            {"type": "Atom", "properties": {"name": "O",    "default_z": 0.0,    "pn": 2.0, "atom_type_name": "O1-"}},
            {"type": "Atom", "properties": {"name": "O",    "default_z": 0.0177, "pn": 2.0, "atom_type_name": "O1-"}},
            {"type": "Atom", "properties": {"name": "O",    "default_z": 0.0023, "pn": 2.0, "atom_type_name": "O1-"}},
            {"type": "Atom", "properties": {"name": "OH",   "default_z": 0.2304, "pn": 2.0, "atom_type_name": "OH1-"}},
            {"type": "Atom", "properties": {"name": "OH",   "default_z": 0.433,  "pn": 2.0, "atom_type_name": "OH1-"}},
            {"type": "Atom", "properties": {"name": "OH",   "default_z": 0.4351, "pn": 2.0, "atom_type_name": "OH1-"}},
            {"type": "Atom", "properties": {"name": "OH",   "default_z": 0.4361, "pn": 2.0, "atom_type_name": "OH1-"}}
        ],

        // interlayer_atoms: atoms occupying the space between layers
        // Kaolinite has no interlayer cations or water molecules
        "interlayer_atoms": []
    }
}
```

---

### Example — Illite.cmp

Illite is a 2:1 di-octahedral clay with a potassium interlayer. It has two atom relations that constrain the Fe/Al octahedral ratio and the K interlayer content.

```jsonc
{
    "type": "Component",
    "properties": {
        "uuid": "878298324e9e11e2b238150ae229a525",
        "name": "Illite",

        "d001_ref_info": [0.995, 1.004, false],
        "d001": 0.998,                 // ~1 nm basal spacing for illite
        "default_c": 0.998,
        "delta_c": 0.0,

        // ucp_a is formula-driven: a = 0.57735 * b (hexagonal approximation)
        "ucp_a": {
            "type": "UnitCellProperty",
            "properties": {
                "value": 0.5209,
                "factor": 0.57735,
                "constant": 0.0,
                "prop": ["878298324e9e11e2b238150ae229a525", "cell_b"],
                "enabled": true
            }
        },
        // ucp_b is also formula-driven: b = 0.0043 * Fe_pn + 0.9
        // This links the b parameter to the octahedral iron content
        "ucp_b": {
            "type": "UnitCellProperty",
            "properties": {
                "value": 0.90215,
                "factor": 0.0043,
                "constant": 0.9,
                "prop": ["878057a24e9e11e2b238150ae229a525", "pn"],  // Fe atom
                "enabled": true
            }
        },

        "atom_relations": [
            {
                // AtomRatio: maintains Fe/(Fe+Al) = value/sum = 0.125/4 = 0.03125
                // Changing the ratio automatically adjusts both Fe and Al pn values
                "type": "AtomRatio",
                "properties": {
                    "name": "OctFe",
                    "value": 0.125,          // Fe pn
                    "value_ref_info": [0.0, 1.0, false],
                    "sum": 4.0,              // Fe + Al total = 4 per unit cell
                    "atom1": ["878057a24e9e11e2b238150ae229a525", "pn"],  // Fe
                    "atom2": ["87822ee24e9e11e2b238150ae229a525", "pn"]   // Al
                }
            },
            {
                // AtomContents: a single controllable parameter that sets
                // the occupancy of one or more atoms simultaneously
                "type": "AtomContents",
                "properties": {
                    "name": "K Content",
                    "value": 1.5,            // K atoms per unit cell
                    "value_ref_info": [0.5, 2.0, false],
                    "atom_contents": [
                        ["9166fa7316564dfd843f9d1e712bb212", "pn", 1.0]  // K atom, multiplier 1
                    ]
                }
            }
        ],

        // layer_atoms: 2:1 layer (two Si tetrahedra + one Al/Fe octahedra sheet)
        // Positions progress from top O-plane (z=0.66) down to bottom O-plane (z=0)
        "layer_atoms": [
            {"type": "Atom", "properties": {"name": "O",  "default_z": 0.66,   "pn": 6.0, "atom_type_name": "O1-"}},
            {"type": "Atom", "properties": {"name": "Si", "default_z": 0.602,  "pn": 4.0, "atom_type_name": "Si2+"}},
            {"type": "Atom", "properties": {"name": "O",  "default_z": 0.4365, "pn": 4.0, "atom_type_name": "O1-"}},
            {"type": "Atom", "properties": {"name": "OH", "default_z": 0.4365, "pn": 2.0, "atom_type_name": "OH1-"}},
            {"type": "Atom", "properties": {"name": "Fe", "default_z": 0.33,   "pn": 0.5, "atom_type_name": "Fe1.5+"}},
            {"type": "Atom", "properties": {"name": "Al", "default_z": 0.33,   "pn": 3.5, "atom_type_name": "Al1.5+"}},
            {"type": "Atom", "properties": {"name": "OH", "default_z": 0.2235, "pn": 2.0, "atom_type_name": "OH1-"}},
            {"type": "Atom", "properties": {"name": "O",  "default_z": 0.2235, "pn": 4.0, "atom_type_name": "O1-"}},
            {"type": "Atom", "properties": {"name": "Si", "default_z": 0.058,  "pn": 4.0, "atom_type_name": "Si2+"}},
            {"type": "Atom", "properties": {"name": "O",  "default_z": 0.0,    "pn": 6.0, "atom_type_name": "O1-"}}
        ],

        // interlayer_atoms: K sits between two 2:1 layers
        "interlayer_atoms": [
            {"type": "Atom", "properties": {"name": "K", "default_z": 0.829, "pn": 1.5, "atom_type_name": "K1+"}}
        ]
    }
}
```

---

## Phase File (`.phs`)

A phase file is a ZIP archive containing one or more JSON entries. Each entry corresponds to one named phase (e.g., one treatment variant). The ZIP entry name follows the pattern `<index>###<uuid>`.

### Example — Illite.phs (pure phase)

A pure phase file contains a single ZIP entry. The phase has G=1 (one component type) and uses the R0G1Model (no stacking disorder).

```jsonc
{
    "type": "Phase",
    "properties": {
        "uuid": "...",
        "name": "Illite",
        "G": 1,                         // number of distinct layer types
        "display_color": "#AACC00",

        // inherit_* phase-level flags: if true, value is taken from based_on phase
        "inherit_CSDS_distribution": false,
        "inherit_display_color": false,
        "inherit_sigma_star": false,

        // sigma_star: peak broadening due to turbostratic disorder (degrees)
        "sigma_star": 3.0,
        "sigma_star_ref_info": [0.0, 90.0, false],

        // CSDS_distribution: coherent scattering domain size (number of layers)
        "CSDS_distribution": {
            "type": "DritsCSDSDistribution",
            "properties": {
                "average": 10,                    // mean number of layers
                "average_ref_info": [1.0, 200.0, false]
            }
        },

        // probabilities: stacking model
        // R0G1Model = random stacking with 1 layer type (pure phase, no disorder)
        "probabilities": {
            "type": "R0G1Model",
            "properties": {
                "uuid": "..."
                // No stacking parameters needed for a single layer type
            }
        },

        // components: the layer type definitions (full component data, not a .cmp reference)
        // For a pure phase there is one component (the Illite layer)
        "components": [
            {
                // ... full Component JSON as shown in Illite.cmp above ...
            }
        ],

        "based_on_uuid": ""             // empty: this is the primary (AD) phase
    }
}
```

---

### Example — IS R0 Ca.phs (expandable interstratified phase)

An IS R0 phase file contains **three ZIP entries** — one per treatment variant (Ca-AD, Ca-EG, Ca-350). Each entry is a separate Phase JSON object. The AD phase is standalone; the EG and 350 phases reference the AD phase via `based_on_uuid` and use `inherit_*` flags to share properties.

#### Entry 0 — IS R0 Ca-AD (air-dried)

```jsonc
{
    "type": "Phase",
    "properties": {
        "uuid": "92276e6531f84cf081781d0984370de8",
        "name": "IS R0 Ca-AD",
        "G": 2,                         // 2 layer types: Illite + Smectite

        "inherit_CSDS_distribution": false,
        "inherit_display_color": false,
        "inherit_sigma_star": false,
        "sigma_star": 3.0,

        "CSDS_distribution": {
            "type": "DritsCSDSDistribution",
            "properties": {"average": 10}
        },

        // R0G2Model: random (Reichweite 0) stacking of 2 layer types
        // F1: fraction of layer type 1 (Illite)
        "probabilities": {
            "type": "R0G2Model",
            "properties": {
                "F1": 0.8,              // 80% Illite layers by default
                "F1_ref_info": [0.0, 1.0, false],
                "inherit_F1": false
            }
        },

        // Two components: Illite (d001=0.998 nm) and Di-Smectite 2WAT (d001=1.5 nm)
        "components": [
            {
                "type": "Component",
                "properties": {
                    "name": "Illite",
                    "d001": 0.998,
                    "linked_with": null,        // AD components have no parent link
                    // ... full atom lists as in Illite.cmp ...
                }
            },
            {
                "type": "Component",
                "properties": {
                    "name": "Di-Smectite 2wat",
                    "d001": 1.5,               // 2-water-layer smectite spacing
                    "linked_with": null,
                    // interlayer contains Ca2+ and two H2O planes:
                    "interlayer_atoms": [
                        {"type": "Atom", "properties": {"name": "H2O", "default_z": 1.197, "pn": 3.5, "atom_type_name": "H2O"}},
                        {"type": "Atom", "properties": {"name": "Ca",  "default_z": 1.077, "pn": 0.4, "atom_type_name": "Ca2+"}},
                        {"type": "Atom", "properties": {"name": "H2O", "default_z": 0.957, "pn": 3.5, "atom_type_name": "H2O"}}
                    ]
                }
            }
        ],

        "based_on_uuid": ""             // this is the primary (AD) phase
    }
}
```

#### Entry 1 — IS R0 Ca-EG (ethylene-glycol solvated)

```jsonc
{
    "type": "Phase",
    "properties": {
        "uuid": "961b4912a1364e0a8622f3a6b6952826",
        "name": "IS R0 Ca-EG",
        "G": 2,

        // These three properties are inherited from the AD phase
        "inherit_CSDS_distribution": true,
        "inherit_display_color": true,
        "inherit_sigma_star": true,

        "sigma_star": 3.0,              // value stored but overridden at runtime by AD

        // probabilities is also inherited (inherit_probabilities flag set during generation)
        "probabilities": {
            "type": "R0G2Model",
            "properties": {"F1": 0.8}
        },

        "components": [
            {
                "type": "Component",
                "properties": {
                    "name": "Illite",
                    "d001": 0.998,
                    // linked_with points to the Illite component of the AD phase
                    // At runtime: ucp_a, ucp_b, delta_c, layer_atoms come from AD's Illite
                    "inherit_ucp_a": true,
                    "inherit_ucp_b": true,
                    "inherit_delta_c": true,
                    "inherit_layer_atoms": true,
                    "linked_with": { /* full AD Illite component snapshot */ }
                }
            },
            {
                "type": "Component",
                "properties": {
                    "name": "Di-Smectite 2gly",
                    "d001": 1.686,          // glycolated spacing (~1.7 nm for 2-glycol layers)
                    // linked_with points to Di-Smectite 2wat from the AD phase
                    // layer atoms (silicate sheet) are shared; only d001 and interlayer change
                    "inherit_ucp_a": true,
                    "inherit_ucp_b": true,
                    "inherit_delta_c": true,
                    "inherit_layer_atoms": true,
                    "linked_with": { /* full AD Smectite component snapshot */ }
                }
            }
        ],

        // based_on_uuid references the AD phase — phase-level inherited properties
        // (color, sigma_star, CSDS) are taken from there at runtime
        "based_on_uuid": "92276e6531f84cf081781d0984370de8"
    }
}
```

#### Entry 2 — IS R0 Ca-350 (heated to 350 °C)

The structure is identical to the EG phase, except:

- `"name": "IS R0 Ca-350"`
- Smectite component uses Di-Smectite Heated with `"d001": 0.96` (collapsed interlayer)
- `based_on_uuid` is the same AD phase UUID

---

## Field Reference Summary

### Component fields

| Field | Type | Description |
|---|---|---|
| `uuid` | string | Unique identifier; used by `prop` and `linked_with` cross-references |
| `d001` | float (nm) | Basal spacing — the layer repeat distance |
| `default_c` | float (nm) | c used for initial positioning (normally equals d001) |
| `delta_c` | float (nm) | Perturbation added to c; used for non-ideal stacking |
| `ucp_a`, `ucp_b` | UnitCellProperty | Lateral cell parameters; may be formula-linked to another property |
| `layer_atoms` | list | Atoms in the silicate 1:1 or 2:1 layer |
| `interlayer_atoms` | list | Cations and water molecules in the interlayer |
| `atom_relations` | list | Occupancy constraints (AtomRatio or AtomContents) |
| `inherit_*` | bool | If true, value is taken from `linked_with` component at runtime |

### Atom fields

| Field | Description |
|---|---|
| `default_z` | Fractional z position in the layer (0 = bottom O-plane) |
| `pn` | Atoms per half unit cell (occupancy) |
| `atom_type_name` | Key into `atomic scattering factors.atl` for X-ray scattering |
| `stretch_z` | If true, z rescales proportionally when d001 changes |

### Phase fields

| Field | Description |
|---|---|
| `G` | Number of distinct layer types |
| `sigma_star` | Peak broadening from turbostratic disorder (°) |
| `CSDS_distribution` | Coherent scattering domain size (layer count distribution) |
| `probabilities` | Stacking disorder model (R0G1, R0G2, R1G2, …) |
| `based_on_uuid` | UUID of the AD (primary) phase; empty for the primary itself |
| `inherit_*` | Phase-level: if true, color/sigma*/CSDS comes from `based_on` at runtime |

### Stacking probability model types

| Type | Meaning |
|---|---|
| `R0G1Model` | Single layer type, no disorder |
| `R0G2Model` | Two layer types, random (Reichweite 0); parameter F1 = fraction of layer 1 |
| `R1G2Model` | Two layer types, Markov (Reichweite 1); parameters W1, P11 |
| `R2G2Model` | Two layer types, Reichweite 2 |
| `R3G2Model` | Two layer types, Reichweite 3 |
| `R0G3Model` | Three layer types, random |
| `R1G3Model` | Three layer types, Markov |

---

[← Back to User Manual](../index.md)
