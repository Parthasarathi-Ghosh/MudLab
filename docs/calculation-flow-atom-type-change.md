# Calculation Flow: Atom Type Change

Describes what happens — from UI event to diffraction intensity — when a user
picks a new element from the **Element** dropdown in
*Edit Phases → Component → Layer/Interlayer Atoms*.

---

## Signal chain

```
[UI] on_atom_type_edited()
       atom.atom_type = new_atom_type          # LabeledProperty, signal_name="data_changed"
         │
         ▼
[Component] _on_data_model_changed()           # component observes every atom via observe_model()
       ├─ _apply_atom_relations()              # re-applies ratio constraints between atoms
       └─ _update_ucp_values()                 # refreshes cell-a / cell-b unit cell properties
       └─ component.data_changed.emit()
         │
         ▼
[Phase] notify_data_changed()                  # phase observes each component
       └─ phase.data_changed.emit()
          (if based_on: probabilities.update() first)
         │
         ▼
[Mixture] notify_data_changed()                # mixture observes each phase
       └─ needs_update.emit()
  notify_needs_update()
       └─ mixture.update()
            ├─ auto_run=True  → optimize()     # L-BFGS-B re-optimises fractions/scales/bgshifts
            └─ auto_run=False → apply_current_data_object()   # recalculate with current solution
         │
         ▼
[calculations/specimen.py] calculate_phase_intensities(specimen)
       └─ per phase: get_intensity(range_theta, range_stl, soller1, soller2, mcr_2theta, phase)
            ├─ _phase_intensity_cache lookup   # key includes atom_type params — cache miss on change
            └─ _get_diffracted_intensity(phase)
                 └─ get_structure_factors(range_stl, G, phase.components)
                      └─ per component: get_factors(range_stl, component)
         │
         ▼
[calculations/components.py] get_factors()
       └─ per atom (layer then interlayer):
            atom.z = atom.default_z            # set z for layer atoms
            if interlayer: atom.z = calculate_z(...)   # stretch z for interlayer atoms
            sf_tot += get_structure_factor(range_stl, atom)
         │
         ▼
[calculations/atoms.py] get_structure_factor()
       └─ get_atomic_scattering_factor(angstrom_range, atom.atom_type)
            ASF = [Σ aᵢ · exp(−bᵢ · s²) + c] · exp(−B · s²)
       SF = ASF · pn · exp(2πi · z · stl)
```

No manual trigger is needed. The `data_changed` signal propagates automatically
through the MVC observer chain every time `atom.atom_type` is assigned.

---

## Layer atoms vs Interlayer atoms

Both pass through the same `get_structure_factor` call. The only difference is
how the z coordinate is determined before that call.

| | Layer atoms | Interlayer atoms |
|---|---|---|
| **z** | `atom.z = atom.default_z` — unchanged, exactly as the user set it | `atom.z = calculate_z(default_z, lattice_d, z_factor)` — position is stretched between `lattice_d` and `default_c` |
| **stretch_values flag** | `False` | `True` (set on insertion) |

---

## Variable reference

### Atom-level quantities

**`atom.default_z`** (nm)
: The user-specified z position of the atom within the unit cell, measured from
the bottom of the layer along the c-axis. Displayed and edited as *Def. Z (nm)*
in the component dialog. For layer atoms this is the final position used in the
structure factor. For interlayer atoms it is the *reference* position at the
default (unswollen) basal spacing.

**`atom.z`** (nm)
: The effective z position used in the structure factor calculation.
Recomputed by `get_factors` on every calculation pass — never stored
permanently. For layer atoms `z = default_z`. For interlayer atoms `z` is
stretched by `z_factor` (see below).

**`atom.pn`** (dimensionless)
: Occupancy / multiplicity of the atom site. Scales the structure factor
linearly; used to represent partial occupancies or multiple atoms at
equivalent positions.

---

### Component-level quantities

**`component.lattice_d`** (nm)
: The actual repeat distance of the layer part of the unit cell — determined as
`max(atom.default_z)` over all layer atoms. Represents the thickness of the
rigid layer stack (tetrahedral + octahedral sheets), excluding the interlayer
space.

**`component.default_c`** (nm)
: The default (reference) total basal spacing of the component. Equal to
`d001` when no swelling or stretching is active. Serves as the denominator
reference for scaling interlayer atom positions.

**`component.d001`** (nm)
: The *current* basal spacing — the c-axis repeat distance of the component
during a given calculation. May differ from `default_c` when the interlayer is
expanded (swollen). All interlayer atom positions are linearly interpolated
between `lattice_d` and `d001` using `z_factor`.

**`z_factor`** (dimensionless, computed inside `get_factors`)
: Scaling factor that maps interlayer atom positions from the reference spacing
(`default_c`) to the current spacing (`d001`):

```
z_factor = (d001 − lattice_d) / (default_c − lattice_d)
```

When `d001 = default_c`, `z_factor = 1.0` and positions are unchanged.
When the layer is swollen (`d001 > default_c`), `z_factor > 1` and interlayer
atoms are pushed further from `lattice_d`.

The effective z of an interlayer atom is then:

```
z = lattice_d + z_factor × (default_z − lattice_d)
```

---

### AtomType scattering parameters

All four parameters come from the `AtomType` model and are stored in the
project's atom-type library (imported from standard crystallographic tables,
typically Cromer–Mann coefficients).

**`atom_type.par_a`** (array of 5 floats, electrons)
: Gaussian pre-exponential coefficients `[a₁, a₂, a₃, a₄, a₅]` in the
Cromer–Mann expansion of the atomic scattering factor:

```
ASF(s) = Σᵢ aᵢ · exp(−bᵢ · s²)  +  c
```

where `s = (2 sin θ / λ)²` in Å⁻² units. Each `aᵢ` is the amplitude of one
Gaussian lobe. Larger values indicate more electrons and stronger scattering.

**`atom_type.par_b`** (array of 5 floats, Å²)
: Gaussian width coefficients `[b₁, b₂, b₃, b₄, b₅]` in the Cromer–Mann
expansion. Each `bᵢ` controls how quickly the corresponding lobe falls off
with scattering angle. Heavier atoms tend to have at least one very broad
lobe (large `b`) representing core electrons.

**`atom_type.par_c`** (float, electrons)
: Constant offset `c` in the Cromer–Mann expansion. Represents a non-zero
asymptotic limit of the scattering factor at high angles. Usually small but
non-negligible for accurate peak intensities.

The full ASF before the Debye–Waller factor is:

```
ASF₀(s) = Σᵢ₌₁⁵ aᵢ · exp(−bᵢ · s²)  +  c
```

**`atom_type.debye`** (Å², also called the *B-factor* or *Debye–Waller factor*)
: Isotropic displacement parameter `B`. Accounts for thermal vibration and
static disorder of the atom around its mean position. Applied as an overall
multiplicative envelope to the ASF:

```
ASF(s) = ASF₀(s) · exp(−B · s²)
```

A larger `B` causes the scattering factor to decay faster with angle, reducing
high-angle peak intensities. `B = 8π² <u²>` where `<u²>` is the mean-squared
atomic displacement.

---

## Full structure factor formula

```
SF(stl) = ASF(s) · pn · exp(2πi · z · stl)
```

where:
- `stl = 2 sin θ / λ`  (1/nm units, passed as `range_stl`)
- `s = (stl × 0.05)²`  (converts to 1/Å² units for Cromer–Mann evaluation)
- `ASF(s)` encodes *what* the atom is (element + displacement)
- `pn` encodes *how many* atoms are at this site
- `exp(2πi · z · stl)` encodes *where* the atom sits along c

The imaginary exponential is the phase factor: atoms at different z produce
interference that creates the characteristic peak positions of the mineral.

---

## Atom Relations: constraining occupancies

`AtomRelation` objects live in `component.atom_relations` and enforce algebraic
constraints on atom occupancies (`pn`) every time any atom or relation in the
component changes. There are two concrete types.

---

### `AtomRatio` — binary substitution

Links **two atoms** so their occupancies always share a fixed total (`sum`),
split by `value`:

```
atom1.pn = value       × sum
atom2.pn = (1 − value) × sum
```

**Example** — Fe²⁺ substituting for Al³⁺ in an octahedral sheet:

```
sum   = 4.0   (total octahedral site occupancy)
value = 0.3   (30 % Fe, 70 % Al)
→  Fe.pn = 0.3 × 4 = 1.2
→  Al.pn = 0.7 × 4 = 2.8
```

`value` is **refinable** — the L-BFGS-B optimiser can vary it while `sum`
stays fixed.

---

### `AtomContents` — proportional scaling of many atoms

Holds a list of `(atom, prop, amount)` entries. All atoms are scaled by one
number `value`:

```
atom.pn = amount × value   for each entry
```

**Example** — interlayer water molecules at varying hydration:

```
value     = 0.8   (hydration level)
H₂O_entry: amount=1.0  →  H₂O.pn = 0.8
OH_entry:   amount=0.5  →  OH.pn  = 0.4
```

---

### Chained `AtomRatio` — multi-element substitution

`AtomRatio` can point its `sum` target at **another** `AtomRatio` via the
special `__internal_sum__` setter, enabling three-way (or higher) substitution:

```
AtomRatioFeAndMgForAl
  atom1 = Al,  atom2 → feeds __internal_sum__ of AtomRatioMgForFe
  value = 0.4  (60 % Al, 40 % combined Fe+Mg)

AtomRatioMgForFe  (its sum is driven by the above)
  atom1 = Mg,  atom2 = Fe
  value = 0.5  (50/50 split of the Fe+Mg total)

Result (sum = 4):
  Al.pn  = 0.6 × 4 = 2.4
  Mg.pn  = 0.5 × (0.4 × 4) = 0.8
  Fe.pn  = 0.5 × (0.4 × 4) = 0.8
```

When the first ratio updates it calls `AtomRatioMgForFe.__internal_sum__ = new_value`
directly, triggering `apply_relation()` on the chained ratio immediately —
no signal needed.

---

### When relations are re-applied

`Component._apply_atom_relations()` is called from `_on_data_model_changed`
whenever **any** observed model in the component fires `data_changed`:

| Trigger | Reason |
|---|---|
| `atom.atom_type` changed | Scattering factor changed; pn constraints must be current |
| `atom.pn` edited manually | May conflict with a relation — re-applying enforces it |
| `atom_ratio.value` changed | Core constraint parameter changed |
| `atom_ratio.sum` changed | Total occupancy changed |
| `atom_ratio.enabled` toggled | Relation switches on or off |
| Atom added / removed | New atom may be target of a relation |
| AtomRelation added / removed | Constraint set changed |

---

### Silent writes and the `driven_by_other` flag

`apply_relation` writes to `atom.pn` inside `data_changed.ignore()` so the
write does not re-trigger `_on_data_model_changed` and loop:

```python
# AtomRatio.apply_relation  (atom_relations.py:368)
with atom.data_changed.ignore():
    setattr(atom, prop, value * self.sum)
    atom._set_driven_flag_for_prop(prop)
```

After all relations have been applied, the outer `data_changed.hold_and_emit()`
in `_apply_atom_relations` fires **one** `component.data_changed`, which
propagates up to the calculation chain.

When an atom's `pn` is owned by a relation, `_set_driven_flag_for_prop` marks
that relation's `driven_by_other = True`. This:

1. **Blocks independent refinement** — `is_refinable` returns `False` when
   `driven_by_other` is set, preventing the optimiser from treating a driven
   value as a free parameter.
2. **Prevents reset loops** — at the start of every `_apply_atom_relations`
   call all flags are cleared, then re-set by whichever relation applies.

---

### Constraint → calculation flow

```
user edits atom_ratio.value
  │
  ▼
atom_ratio.data_changed
  └─ Component._on_data_model_changed()
       └─ _apply_atom_relations()
            ├─ clear all driven_by_other flags
            ├─ AtomRatio.apply_relation()
            │    atom1.pn = value × sum      (silent — data_changed suppressed)
            │    atom2.pn = (1−value) × sum  (silent — data_changed suppressed)
            └─ component.data_changed.emit()
                 └─ Phase → Mixture.needs_update
                      └─ calculate_phase_intensities()
                           └─ get_factors() reads the updated atom.pn
                                └─ get_structure_factor()
                                     SF = ASF · pn · exp(2πi · z · stl)
```

Changing `pn` directly scales the diffracted intensity from that atom site —
it appears linearly in the structure factor formula.
