# MudLab

**X-ray Diffraction Analysis for Disordered Layered Minerals**

MudLab is a Windows desktop application for modelling and fitting
X-ray diffraction (XRD) patterns of disordered clay minerals and other
layered structures. It combines an interactive GTK3 graphical interface
with a powerful numerical back-end (NumPy, SciPy, Matplotlib) to let you
build structural phase models, detect peaks, identify minerals, and refine
parameters against measured data — all without writing a single line of code.

---

## Installation

### Recommended — Installer

1. Go to the [Releases page](https://github.com/KazukiNoSuzaku/MudLab/releases)
2. Download `MudLab-<version>-Setup.exe`
3. Run the installer and follow the on-screen steps

> No administrator rights required. No Python installation needed.
> Everything is self-contained.

Launch **MudLab** from the Start Menu or Desktop shortcut.

### Portable — No Install

1. Download `MudLab-<version>-Portable.zip`
2. Extract anywhere (a USB drive, a project folder, etc.)
3. Run `mudlab.exe` inside the extracted folder

---

## System Requirements

| | |
|---|---|
| **OS** | Windows 10 or later (64-bit) |
| **Disk space** | ~300 MB |
| **RAM** | 4 GB recommended |
| **Internet** | Not required after installation |

---

## Features

### Project & Specimen Management
- Organise your work into **projects** containing one or more specimens
- Import measured XRD patterns from a wide range of formats:
  `.RAW` (Bruker), `.BRML`, `.CPI`, `.RD`, `.UDF`, `.CSV`
- Visualise experimental and calculated patterns side by side on an
  interactive Matplotlib plot

### Phase Modelling
- Build **multi-component phase models** with full control over:
  - Unit cell parameters
  - Atom positions and scattering factors
  - Coherent scattering domain size (CSDS) distributions
  - Layer stacking probabilities (R0, R1, R2, R3 models)
- Define **mixtures** of phases and optimise their weight fractions

### Peak Detection & Mineral Identification
- Automatic **peak detection** with adjustable threshold
- **Match Minerals** dialog: score and rank peaks against a reference
  mineral database
- Append matched mineral abbreviations as plot annotations
- Preview mineral diffraction lines overlaid on your pattern

### Refinement
Six optimisation algorithms available:

| Algorithm | Best for |
|---|---|
| L-BFGS-B | Fast gradient-based refinement |
| DEAP CMA-ES | Robust global search |
| DEAP PSO + CMA | Hybrid swarm + covariance |
| DEAP PSO | Particle swarm optimisation |
| Custom Brute | Grid search |
| Basin Hopping | Escaping local minima |

Residual metrics, convergence history, and best/last solution recall
are all shown in a dedicated refinement dialog.

### Goniometer Configuration
- Configure your diffractometer geometry (wavelength, radius, etc.)
- Supports multiple wavelength distributions

---

## Getting Started

1. **Open or create a project** — `File > New` or `File > Open`
2. **Add a specimen** — click the `+` button in the specimen panel and
   load your measured `.RAW` / `.CSV` / etc. file
3. **Add phases** — open `Edit > Phases`, add a phase, and configure
   its components and layer parameters
4. **Create a mixture** — open `Edit > Mixtures`, assign phases and
   their fractions
5. **Find peaks** — in the specimen panel click `Find Peaks` to
   auto-detect peak positions
6. **Match minerals** — click `Match Minerals`, run Auto Match, select
   the best candidates, and click `Append Labels`
7. **Refine** — open the refinement dialog, select parameters to
   optimise, choose an algorithm, and click `Refine`

---

## File Formats

| Format | Extension | Notes |
|---|---|---|
| MudLab project | `.mud` | Native JSON-based format |
| Bruker RAW | `.RAW` | v1, v2, v3 |
| Bruker BRML | `.brml` | ZIP-based XML |
| Sietronics CPI | `.cpi` | |
| Philips RD | `.rd` | |
| Philips UDF | `.udf` | |
| CSV | `.csv` | Two-column 2θ / intensity |

---

## Uninstalling

Go to **Settings > Apps** (or the classic Control Panel) and remove
**MudLab** — same as any other Windows application.

The portable version leaves no traces: simply delete the extracted folder.

---

## Building from Source

The application ships its own Python 3.14 runtime (MSYS2 MinGW64).
To rebuild the launcher executable you need MSYS2 with the MinGW64
toolchain installed.

```bash
# From the repo root inside an MSYS2 MinGW64 shell:
bash launcher/build.sh
cp launcher/mudlab.exe     data/bin/
cp launcher/mudlab-cmd.exe data/bin/
```

To build the Windows installer, install [Inno Setup 6](https://jrsoftware.org/isinfo.php) and run:

```
iscc mudlab.iss
```

Output: `dist/MudLab-<version>-Setup.exe`

---

## Licence

BSD 2-Clause — see **Help > About** inside the application.

---

## Acknowledgements

MudLab is a substantially rewritten and extended fork of
[PyXRD](https://github.com/mathijs-dumon/PyXRD) by Mathijs Dumon.

---

## Links

- [Releases](https://github.com/KazukiNoSuzaku/MudLab/releases)
- [Issue tracker](https://github.com/KazukiNoSuzaku/MudLab/issues)
