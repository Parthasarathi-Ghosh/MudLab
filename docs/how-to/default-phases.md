# How Default Phases Are Generated

[← Back to User Manual](../index.md)

## Overview

When you open **Edit Phases** for the first time, MudLab prompts you to generate the default phase library. Clicking **Generate Phases** runs a background script that assembles ~100 ready-to-use phase files and saves them to your user data folder. This page explains what is generated, where it goes, and how the internal structure works.

---

## What Triggers Generation

The **Generate Phases** button in the Add Phase dialog calls `mudlab/scripts/generate_default_phases.py`. A progress bar tracks completion. Once finished, the phase library is immediately available in the drop-down list and does not need to be regenerated unless you delete the folder.

---

## Where the Files Are Saved

Generated files are written to:

```
C:\Users\<username>\AppData\Local\MudLab\default phases\
```

This folder is created automatically, including all subfolders. The files are plain JSON (`.phs` extension) and can be opened in a text editor if needed.

The component templates used as input are shipped with MudLab and are read-only:

```
<MudLab install>\data\lib\python3.14\site-packages\mudlab\data\default components\
```

---

## Input: Default Components

Component files (`.cmp`) define the crystallographic building blocks — atom positions, scattering factors, and unit cell parameters — for a single layer type. MudLab ships with the following:

| Component | Code | Description |
|---|---|---|
| Kaolinite | `K` | Di-octahedral 1:1 layer |
| Illite | `I` | Di-octahedral 2:1 layer, K-interlayer |
| Chlorite | `C` | Tri-octahedral 2:1+1 layer |
| Serpentine | `Se` | Tri-octahedral 1:1 layer |
| Talc | `T` | Tri-octahedral 2:1 layer, no interlayer |
| Margarite | `Ma` | Di-octahedral brittle mica |
| Paragonite | `Pa` | Di-octahedral Na-mica |
| Leucophyllite | `L` | Di-octahedral Li-mica |
| Di-Smectite Ca 2WAT | `dS2w` | Di-oct. smectite, Ca-saturated, 2-water-layer (air-dried) |
| Di-Smectite Ca 1WAT | `dS1w` | Di-oct. smectite, Ca-saturated, 1-water-layer |
| Di-Smectite Ca Dehydr | `dS0w` | Di-oct. smectite, Ca-saturated, dehydrated |
| Di-Smectite Ca 2GLY | `dS2g` | Di-oct. smectite, Ca-saturated, glycolated |
| Di-Smectite Ca 1GLY | `dS1g` | Di-oct. smectite, Ca-saturated, 1-glycol-layer |
| Di-Smectite Ca Heated | `dSht` | Di-oct. smectite, Ca-saturated, heated (350 °C) |
| Tri-Smectite Ca * | `tS*` | As above but tri-octahedral |
| Di-Vermiculite Ca * | `dV*` | Di-oct. vermiculite variants (2WAT, 1WAT, Dehydr, 2GLY, 1GLY, Heated) |

---

## Output: Generated Phase Library

Phases are saved in subfolders by mineral family. Each phase file (`.phs`) contains one or more named phases (treatment variants).

### Pure Phases

Single-component, R0 (no disorder):

```
default phases/
  Kaolinite.phs
  Illite.phs
  Chlorite.phs
  Serpentine.phs
  Talc.phs
  Margarite.phs
  Leucophyllite.phs
  Paragonite.phs
```

### Expandable Phases

Expandable phases (smectite, vermiculite, and their interstratifications) are generated across a range of **R-order** values (stacking disorder regime) and three **treatment variants**:

| Suffix | Treatment | Component used |
|---|---|---|
| `Ca-AD` | Air-dried | 2WAT hydration state |
| `Ca-EG` | Ethylene-glycol solvated | 2GLY or 1GLY state |
| `Ca-350` | Heated to 350 °C | Heated / dehydrated state |

The folder structure groups phases by mineral series and interstratification type:

```
default phases/
  Smectites/
    Di-Smectite Ca.phs          (R0 only, 3 treatments)
    SS/
      Di-SS R0 Ca.phs           (2-component smectite, R0)
      Di-SS R1 Ca.phs
      Di-SS R2 Ca.phs
      Di-SS R3 Ca.phs
    SSS/
      Di-SSS R0 Ca.phs          (3-component smectite, R0–R2)
      ...
    Tri-Smectite Ca.phs
    SS/  (Tri variants)
    SSS/ (Tri variants)

  Vermiculites/
    Di-Vermiculite Ca.phs       (R0 only)
    VV/   (R0–R3)
    VVV/  (R0–R2)

  Kaolinite-Smectites/
    KS/   (R0–R3)
    KSS/  (R0–R2)
    KSSS/ (R0–R1)

  Illite-Smectites/
    IS/   (R0–R3)
    ISS/  (R0–R2)
    ISSS/ (R0–R1)

  Chlorite-Smectites/
    CS/   (R0–R3, Chlorite + Tri-Smectite)
    CSS/  (R0–R2)
    CSSS/ (R0–R1)

  Talc-Smectites/
    TS/   (R0–R3)
    TSS/  (R0–R2)
    TSSS/ (R0–R1)

  Illite-Chlorite-Smectites/
    ICS/  (R0–R2, AD and EG only)
    ICSS/ (R0–R1)
    ICSSS/(R0 only)

  Kaolinite-Chlorite-Smectites/
    KCS/  (R0–R2, AD and EG only)
    KCSS/ (R0–R1)
    KCSSS/(R0 only)
```

**Naming convention:** `XY R<n> Ca-<treatment>.phs` where `XY` is the phase series abbreviation and `n` is the R-order (0–3).

---

## Internal Structure: Phase and Component Inheritance

### Treatment Variants and `based_on`

Within each `.phs` file the EG and 350 phases are declared as **based on** the AD phase. This means they inherit:

- Display colour
- σ\* (peak broadening parameter)
- CSDS distribution (coherent scattering domain size)
- Stacking probabilities

Any change you make to these properties on the AD phase automatically propagates to the EG and 350 variants. You can override any inherited property on a variant individually by un-checking its inherit flag in Edit Phases.

### Component Linking and `linked_with`

In interstratified phases the EG/heated components are **linked** to their AD counterparts for structural parameters:

- Unit cell parameters a and b
- δc (c-axis distortion)
- Layer atom positions

This keeps the layer geometry consistent across treatments. For example, the glycolated smectite component shares its silicate sheet geometry with the 2WAT component; only the interlayer (d001) changes between treatments.

---

## How the Script Works

The generation runs as a two-stage threaded pipeline:

1. **Phase worker thread** — reads each phase description, loads the required `.cmp` component files, resolves `based_on` and `linked_with` cross-references, and constructs `Phase` objects in memory.

2. **IO worker thread** — receives completed `Phase` objects from the phase worker, creates the necessary subfolders, and serialises each phase to a `.phs` JSON file.

Both threads run concurrently so file I/O overlaps with object construction. The progress bar in the dialog reflects how many phase descriptions have been dispatched from the phase worker queue.

---

## Re-generating Phases

If you need to regenerate (e.g. after deleting the folder or after a MudLab update):

1. Open **Edit Phases**.
2. Click **Add Phase** (the `+` button).
3. In the Add Phase dialog, click **Generate Phases**.
4. Wait for the progress bar to reach 100 %.

> **Note:** Regeneration overwrites any existing `.phs` files in the default phases folder. If you have made structural edits to a default phase and want to keep them, copy the relevant `.phs` file to a different location first.

---

## Relevant Source Files

| Component | File |
|---|---|
| Generation script | `mudlab/scripts/generate_default_phases.py` |
| Trigger (button handler) | `mudlab/phases/controllers/add_phase_controller.py` — `on_btn_generate_phases_clicked()` |
| Component templates | `mudlab/data/default components/` (shipped, read-only) |
| Output folder | `AppData\Local\MudLab\default phases\` (user-writable) |
| Folder paths | `mudlab/data/settings.py` — `DEFAULT_COMPONENTS`, `DEFAULT_PHASES` |

---

[← Back to User Manual](../index.md)
