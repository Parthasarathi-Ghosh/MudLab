# How to Interpret Parameter Space Plots

[← Back to User Manual](../index.md)

The Parameter Space plot is a visualisation of how the residual error (how poorly the model fits the data) varies across pairs of refined parameters.

---

## Layout

With *n* refined parameters, there are *n(n−1)/2* cross-section panels arranged in a grid — one for each unique pair of parameters. For example, with 6 parameters there are 15 panels.

Each panel's X and Y axes represent one pair of parameters, labelled #1–#n with the parameter name.

---

## What the Shading Means

- The **colour intensity** (grayscale) shows the interpolated residual error across that 2D slice of parameter space — darker = higher error, lighter = lower error (or vice versa, depending on the colormap direction).
- The **contour lines** are iso-residual lines — all points on a contour line have the same residual value.

The **colorbar** on the right gives the residual scale shared across all panels.

---

## The Red Cross (+)

The red cross marks the **best solution found** — the parameter combination that gave the lowest residual error during refinement.

---

## What to Look For

| Pattern | Meaning |
|---|---|
| Smooth, concentric contours with the red cross at the centre | Well-behaved refinement — the solution is reliable |
| Elongated contours | The two parameters are **correlated** — changing one can be compensated by changing the other; the solution may not be unique |
| Messy or flat plot | Too few refinement iterations were recorded to interpolate well — consider increasing iterations |

---

## Tips

- If contours are elongated along a diagonal, the two correlated parameters should not be refined simultaneously. Fix one and refine the other.
- A very narrow, deep minimum (tight concentric contours) indicates high sensitivity to those parameters — small changes cause large residual changes.
- If the red cross sits on the edge of the plot (boundary of the parameter range), the true minimum may be outside the current range. Widen the parameter bounds and refine again.

---

[← Back to User Manual](../index.md)
