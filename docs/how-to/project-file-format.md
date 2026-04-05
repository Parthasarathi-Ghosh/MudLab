# Project File Format (`.mud`)

[← Back to User Manual](../index.md)

A `.mud` file is a **ZIP archive** containing several JSON entries. You can open it with any ZIP tool (7-Zip, Windows Explorer) to inspect or manually edit the contents. The JSON entries use a standard envelope:

```jsonc
{
    "type": "<registered class name>",
    "properties": { ... }
}
```

---

## ZIP entries

| Entry name  | Content |
|---|---|
| `version`   | Plain JSON string — the MudLab version that wrote the file (e.g. `"0.1.0"`) |
| `content`   | The root `Project` object; the four list properties (`phases`, `specimens`, `atom_types`, `mixtures`) are replaced by `"file://<name>"` references pointing to the other entries |
| `phases`    | JSON array of `Phase` objects |
| `specimens` | JSON array of `Specimen` objects |
| `atom_types`| JSON array of `AtomType` objects |
| `mixtures`  | JSON array of `Mixture` objects |

On load, the parser reads `content` first, then reads each of the four named entries and splices them back into `content["properties"]` before decoding. All cross-object references (e.g. mixture → specimen, mixture → phase) use `uuid` strings resolved through a global object pool.

---

## `content` — Project

```jsonc
{
    "type": "Project",
    "properties": {

        // --- Metadata ---
        "name":        "My project",
        "date":        "2026-04-05",
        "description": "Notes about this project",
        "author":      "J. Smith",

        // --- Plot axes ---
        "axes_xlimit":    0,        // 0 = automatic, 1 = manual
        "axes_xmin":      0.0,      // lower 2θ limit (degrees) when manual
        "axes_xmax":      45.0,     // upper 2θ limit (degrees) when manual
        "axes_xstretch":  false,    // stretch X-axis to fill window
        "axes_dspacing":  false,    // show d-spacing instead of 2θ on X-axis

        "axes_ylimit":    0,        // 0 = automatic, 1 = manual
        "axes_ymin":      0.0,      // lower intensity limit when manual
        "axes_ymax":      0.0,      // upper intensity limit when manual
        "axes_ynormalize":0,        // 0 = raw counts, 1 = single-normalised, 2 = multi-normalised
        "axes_yvisible":  true,     // show Y-axis

        // --- Layout ---
        "layout_mode": "FULL",      // "FULL" or "VIEWER"

        // --- Pattern display defaults ---
        "display_plot_offset":    0.75,   // vertical offset between patterns (fraction of max intensity)
        "display_group_by":       1,      // number of patterns to stack without offset
        "display_label_pos":      0.85,   // relative label position (fraction of pattern height)

        // --- Calculated pattern line defaults ---
        "display_calc_color":  "#0000FF",
        "display_calc_lw":     2,         // line width in points
        "display_calc_ls":     "-",       // line style: "-", "--", "-.", ":"
        "display_calc_marker": "",        // matplotlib marker symbol; "" = none

        // --- Experimental pattern line defaults ---
        "display_exp_color":   "#000000",
        "display_exp_lw":      1,
        "display_exp_ls":      "-",
        "display_exp_marker":  "",

        // --- Peak marker defaults ---
        "display_marker_angle":      0.0,     // label angle in degrees
        "display_marker_top_offset": 0.0,     // vertical offset from base
        "display_marker_align":      "left",  // "left", "center", "right"
        "display_marker_base":       0,       // base line style index
        "display_marker_top":        0,       // top line style index
        "display_marker_style":      "solid", // marker line style
        "display_marker_color":      "#000000",

        // --- The four list properties (replaced by file:// references in the ZIP) ---
        "phases":      "file://phases",
        "specimens":   "file://specimens",
        "atom_types":  "file://atom_types",
        "mixtures":    "file://mixtures"
    }
}
```

---

## `specimens` — array of Specimen

Each element in the `specimens` array describes one measured sample.

```jsonc
{
    "type": "Specimen",
    "properties": {
        "uuid": "...",
        "name":        "Bulk",
        "sample_name": "Clay 01-AD",

        // --- Pattern visibility ---
        "display_calculated":      true,
        "display_experimental":    true,
        "display_phases":          true,   // show individual phase contributions
        "display_residuals":       true,   // show Rp residual pattern
        "display_residual_scale":  1.0,
        "display_derivatives":     false,
        "display_stats_in_lbl":    true,   // show Rp/Rwp/GoF in the pattern label
        "display_vshift":          0.0,    // vertical shift (counts)
        "display_vscale":          0.0,    // vertical scale multiplier

        // --- Goniometer ---
        // Full Goniometer object embedded here (see Goniometer section below)
        "goniometer": { "type": "Goniometer", "properties": { ... } },

        // --- Patterns ---
        // ExperimentalLine: the measured diffractogram
        // CalculatedLine:   the sum of all phase contributions
        // Each line stores x/y arrays, a label, and display settings
        "experimental_pattern": { "type": "ExperimentalLine", "properties": { ... } },
        "calculated_pattern":   { "type": "CalculatedLine",   "properties": { ... } },

        // --- Exclusion ranges ---
        // List of [x_start, x_end] pairs (in °2θ) excluded from Rp calculation
        "exclusion_ranges": { "type": "MudLabLine", "properties": { ... } },

        // --- Peak markers ---
        "markers": [
            {
                "type": "Marker",
                "properties": {
                    "uuid":     "...",
                    "label":    "1.00",     // displayed label text
                    "position": 8.85,       // 2θ position in degrees
                    "visible":  true,
                    "base":     1,          // base style index
                    // inherit_* flags take display settings from the project defaults
                    "inherit_angle":      true,
                    "inherit_align":      true,
                    "inherit_color":      true,
                    "inherit_style":      true,
                    "inherit_base":       false,
                    "inherit_top":        true,
                    "inherit_top_offset": true
                }
            }
        ]
    }
}
```

### Goniometer

Embedded inside each `Specimen`. All angles are in degrees, lengths in cm.

```jsonc
{
    "type": "Goniometer",
    "properties": {
        "min_2theta":   3.0,      // scan start angle (°2θ)
        "max_2theta":   45.0,     // scan end angle (°2θ)
        "steps":        2500,     // number of data points

        // Wavelength distribution: a MudLabLine with (wavelength_nm, intensity) pairs
        // The dominant wavelength is read as the X value at max Y.
        // Default: CuKα₁ at 0.154056 nm
        "wavelength_distribution": { "type": "MudLabLine", "properties": { ... } },

        // Soller slits (axial divergence, in degrees half-angle)
        "has_soller1": true,
        "soller1":     2.3,
        "has_soller2": true,
        "soller2":     2.3,

        "radius":          24.0,   // goniometer radius
        "divergence_mode": "fixed",// "fixed" or "automatic"
        "divergence":      0.5,    // divergence slit opening (°) or sample length (cm) if automatic

        // Absorption correction
        "has_absorption_correction": false,
        "sample_length":       1.25,   // sample length (cm)
        "sample_surf_density": 20.0,   // surface density (mg/cm²)
        "absorption":          45.0,   // mass attenuation coefficient (cm²/g); user-entered

        "mcr_2theta": 0.0       // monochromator 2θ correction (28.44° for Si, 26.53° for C; 0 = disabled)
    }
}
```

---

## `phases` — array of Phase

Each element is a Phase. The structure is identical to the phase objects described in [Phase and Component File Formats](file-formats.md); refer to that document for full field descriptions and annotated examples.

Key fields:

| Field | Description |
|---|---|
| `uuid` | Unique identifier; referenced by `Mixture.phase_uuids` |
| `G` | Number of distinct layer types (components) |
| `sigma_star` | Turbostratic broadening (°) |
| `CSDS_distribution` | Coherent scattering domain size model |
| `probabilities` | Stacking disorder model (`R0G1Model`, `R0G2Model`, `R1G2Model`, …) |
| `components` | List of Component objects (full crystallographic data) |
| `based_on_uuid` | UUID of the primary (AD) phase; empty for the primary itself |
| `inherit_*` | If true, phase-level property taken from `based_on` phase at runtime |

Refinable parameters have a companion `<name>_ref_info` array:

```jsonc
"sigma_star": 3.0,
"sigma_star_ref_info": [0.0, 90.0, false]  // [min, max, is_refinable]
```

---

## `atom_types` — array of AtomType

Custom atom types defined in this project (supplements the built-in `atomic scattering factors.atl`). Each has:

| Field | Description |
|---|---|
| `uuid` | Unique identifier |
| `name` | Name used as `atom_type_name` in Component atoms |
| `atom_nr` | Atomic number (integer) |
| `charge` | Formal charge |
| `weight` | Atomic weight (amu) |
| `debye` | Debye–Waller B factor |
| `par_c`, `par_a[1-5]`, `par_b[1-5]` | Cromer–Mann scattering factor coefficients |

If `atom_types` is empty (`[]`), all atoms in the project use the built-in table.

---

## `mixtures` — array of Mixture

Each Mixture links specimens to phases and stores the optimiser state.

```jsonc
{
    "type": "Mixture",
    "properties": {
        "uuid": "...",
        "name":        "AD Mixture",
        "auto_run":    false,   // run optimiser automatically on any change
        "auto_bg":     false,   // let optimiser adjust background shifts
        "auto_scales": true,    // let optimiser adjust per-specimen scales

        // phase_matrix: 2D array of phase UUIDs
        // Rows = specimens (same order as specimen_uuids)
        // Cols = mixture phases (same order as phases list)
        // "" means that phase is not used for that specimen
        "phase_uuids": [
            ["uuid-illite-AD",    "uuid-smectite-AD"],   // specimen 0
            ["uuid-illite-AD",    "uuid-smectite-AD"]    // specimen 1
        ],

        // specimen_uuids: ordered list of specimen UUIDs in this mixture
        "specimen_uuids": ["uuid-specimen-0", "uuid-specimen-1"],

        // phases: ordered list of display names for the columns
        "phases": ["Illite AD", "Smectite AD"],

        // fractions: one value per column (phase) — weight fractions (sum to ≤ 1)
        "fractions": [0.7, 0.3],

        // fractions_mask: 1 = let optimiser vary, 0 = hold fixed
        "fractions_mask": [1, 1],

        // scales: one value per row (specimen) — absolute intensity scale
        "scales": [1.0, 1.0],

        // bgshifts: one value per row (specimen) — background offset (counts)
        "bgshifts": [0.0, 0.0],

        // Refinement settings
        "refine_method_index": 0,   // 0 = L-BFGS-B
        "refine_options": { ... },  // method-specific options dict
        "all_refine_options": { ... }
    }
}
```

---

## Backward compatibility

Files saved before the MudLab rebrand (when the application was called PyXRD.clays) use the extension `.pyxrd`. They can still be opened: the decoder transparently remaps legacy `type` strings:

- `"pyxrd.*"` → `"mudlab.*"`
- `"PyXRDLine"` → `"MudLabLine"`

No manual migration is needed.

---

[← Back to User Manual](../index.md)
