# Handoff: two upstream bugs found while testing the MudLab2 (Qt) port

Context: MudLab2 is the in-progress Qt port of this app. While testing 3-component
(Illite / Smectite / Kaolinite) phases, two bugs were traced back to THIS upstream
app. Bug A is fixed + has an automatic regression test; Bug B still needs the
running app to pin the exact crash line.

Environment note: use this app's OWN Python for headless tests —
`data\bin\python.exe` (its numpy / GTK / mudlab match). A plain system Python will
fail on the bundled numpy.

Test data (the user's real files, read-only — never copy into the repo):
`C:\Users\pxgho\Downloads\MudLab Test\new\` — `416 r1.mud` (+ `.bak`), the four
`ISK *.phs`, and the `.cmp` components.

---

## Bug A — DONE (fix applied + tested): cell_a unit-cell derivation nulled on import

**Symptom.** Import a glycol / heated **Di-Smectite** component into an empty
component slot; the component's `cell_a` loses its `cell_b` derivation
(`ucp_a.prop` becomes `null`), so `cell_a = 0` -> `volume ~= 0` -> the phase
produces a **zero / near-zero diffraction pattern** (a "weird" modelled pattern).
Only affects components whose `cell_a` derives from their own `cell_b` that get
re-uuid'd on import (the air-dry Di-Smectite in the same project stays correct).

**Root cause.**
1. `Component.load_components` calls `ObjectPool.change_all_uuids()`; the imported
   component's uuid collides with the same default-library component already in the
   project, so `ObjectPool.add_object` (`mvc/models/object_pool.py`) reassigns the
   colliding uuid — its own comment says *"will break refs"*.
2. That orphans the `cell_a <- cell_b` **self-reference** (`[own_uuid, 'cell_b']`);
   the `cell_b <- atom.pn` reference survives because the atom's uuid is untouched.
3. `UnitCellProperty.resolve_json_references` can't resolve the orphaned uuid and
   **nulls the derivation** -> `cell_a` recomputes to `factor*0 + constant = 0`.

**Fix applied** (uncommitted — please review & commit):
`mudlab/phases/models/unit_cell_prop.py`, `resolve_json_references` — when the
stored `prop` uuid does not resolve **and** the referenced attribute exists on the
UCP's own `component`, recover the source from `self.component` (an intra-component
derivation like `cell_a <- cell_b` is a self-reference) instead of dropping it.

**Automatic test** (added): `tests/test_ucp_cell_a.py`. Run:
```
data\bin\python.exe tests\test_ucp_cell_a.py
```
Verified: PASS with the fix (`cell_a=0.51962`), FAIL without it (`cell_a=0.00000`).

**To finish Bug A:**
1. Review the diff in `unit_cell_prop.py`; run the test above (expect PASS).
2. Optional but recommended — a full end-to-end check in the running GUI: import a
   Di-Smectite EG (2GLY) or Heated component into an empty slot, confirm `cell_a` is
   ~0.52 (not 0) and the phase's modelled pattern is non-zero.
3. Consider whether `ObjectPool.add_object`'s silent uuid reassignment ("will break
   refs") deserves a broader fix; the UCP-level fix already stops the observed data
   loss.
4. Commit + cut the next release.

Downstream (MudLab2) is NOT affected (its loader keeps the stored value and its
import remaps uuids consistently), so no equivalent port is needed — noted on that
side.

---

## Bug B — DONE (fixed): R1G3 probability change/refine errors

**RESOLVED.** Root cause was neither candidate below (both were disproven by
headless reproduction: `Gtk.Table.attach` tolerates the float positions on this
build, and `validate()` never fires so it's latent only). The real crash:

- When a probability model is INVALID, `Phase.data_object` nulls the whole
  block — including `sigma_star = None` (phase.py). But `get_intensity`
  (`calculations/phases.py`) computed the Lorentz-polarisation factor with
  `phase.sigma_star` **before** the `valid_probs` guard, so `get_T`
  (`calculations/goniometer.py`) did `max(None, 1e-18)` → `TypeError`. R1G3 lands
  in the invalid region ~75% of the time (R0G3: 0%), so editing/refining it
  crashes almost always while R0G3 never does.

**Fix applied — ONE change:**
`calculations/phases.py`, `get_intensity` — guard the LP factor on
`phase.valid_probs` (`if phase.apply_lpf and phase.valid_probs:`). An invalid
matrix now yields a zero pattern instead of crashing (matches the MudLab2
port's behaviour). Safe for RawPatternPhase (it sets `apply_lpf=False`, so the
`and` short-circuits before touching `valid_probs`).

**Do NOT touch `validate()`'s thresholds.** The second candidate below (change
`1e4`/`1e6` → `1e-4`/`1e-6`) was tried and **reverted after audit**: it blanks
legitimately FITTED R2G3/R3G2 projects. Those matrices are in-range ([0,1]) but
their row sums deviate from 1 by up to ~1.0 in the checked representation, so the
row-stochastic check is *misapplied* for R≥2 models, not merely mis-thresholded.
The crash never needed it — R1G3 invalidity is always out-of-[0,1], already
caught by the live value-in-[0,1] check.

**Verified headless** (all R0-R3 / G2-G3 test projects): 12/12 fitted projects
render non-blank (no false invalidation); R1G3/R2G3/R3G2 = 0 crashes over 50
out-of-range edits each (auto_run cascade included); R0 / R1G2 unaffected.

### Original investigation notes (candidates — kept for reference)

**Symptom.** For a 3-component **R1** phase (R1G3), changing or refining the
stacking **probability** values errors; the R0 (R0G3) version of the same phase
works. Optimize works for both.

**Why R1 is fragile (measured):** ~75% of the R1G3 6-parameter box `(0,1)^6`
produces an INVALID junction matrix, versus 0% for R0G3's 2 F-parameters — so
editing/refining R1G3 lands in invalid territory most of the time.

**Candidates found by inspection (need the actual traceback to confirm):**
- `mudlab/probabilities/models/base_models.py`, `validate()` — the sum-to-one /
  row-stochastic checks use thresholds `1e4` / `1e6` where they should be `1e-4` /
  `1e-6` (a Py2->3-era sign typo; those checks never fire). Latent; may not be the
  crash but should be fixed.
- `mudlab/probabilities/views.py` (~lines 107/108/125 and `num_rows`) —
  `i / num_columns` is float division in Python 3 (was integer division in
  Python 2); Gtk table attach positions must be ints. A prime crash site when the
  6-input R1G3 panel is built.

**To do:** run the app, load a project with an R1G3 phase (e.g. build one, or use
`416 r1.mud` -> Mix2's `ISK ... R1` phases), then change a probability value and
refine; capture the traceback and fix the exact line. (The MudLab2 port already
guards this path — its calc returns zeros for an invalid matrix — so the port is
robust; this is an upstream-only fix.)
