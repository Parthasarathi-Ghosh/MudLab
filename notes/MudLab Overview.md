# MudLab Overview

MudLab is a desktop application for **X-ray diffraction (XRD) analysis of disordered layered minerals** (clays, micas, mixed-layer silicates). It models stacking disorder and refines structural parameters against measured diffraction patterns.

## What it does

1. Load one or more experimental XRD patterns (specimens)
2. Build crystallographic **phases** (layer types, stacking sequences, atom positions)
3. Assemble a **mixture** — assign phases and their weight fractions to each specimen
4. Calculate a synthetic diffraction pattern and compare it to the measured one
5. **Refine** selected parameters (fractions, scales, d-spacings, atom occupancies) to minimise the residual

## Key scientific objects

| Object | Role |
|---|---|
| **Specimen** | A measured XRD pattern + metadata |
| **Phase** | One crystallographic layer type (d001, atoms, stacking) |
| **Component** | A layer type within a multi-component phase (G > 1) |
| **Mixture** | Maps phase fractions and scales to each specimen |
| **Marker** | A labelled position on the pattern (peak annotation) |

## Entry point

`data/bin/mudlab-cmd.exe` → `mudlab/__main__.py` → `mudlab/core.py`

## Source root

`data/lib/python3.14/site-packages/mudlab/`

## Related Notes

- [[Architecture]]
- [[Phase and Component Model]]
- [[Mixture Model]]
- [[XRD Diffraction Calculation]]
- [[Refinement]]
- [[Markers and Peak Detection]]
