# MudLab User Manual (2026)

MudLab is a software for modelling 1-dimensional X-ray diffraction patterns of clay minerals.
It can model patterns for both pure and mixed-layered clays, as well as their mixtures.

> **Printing to PDF:** Open this page in your browser and use **File → Print → Save as PDF**.

---

## Tools Overview

MudLab provides three sets of tools:

### 1. Pattern Preparation
Tools for preparing experimental patterns for modelling:
- Setting goniometer parameters
- Baseline adjustment
- Correction of 2θ shift using references
- Smoothening noisy patterns

### 2. Phase Identification
Exploratory tools for phase identification:
- Peak detection and labelling
- Search-match peaks using a reference database for clay and non-clay minerals

### 3. Modelling
Tools for modelling patterns for individual clay phases and their mixtures:
- Adjusting parameters of standard phases
- Creating new phases
- Defining participating phases in a mixture
- Determining relative proportions of phases present in a mixture
- Determining ideal major oxide composition based on clay phases
- Refining phase parameters against experimental patterns from various treatments (e.g., air dried, glycolated)

---

## Sample Walkthrough

### Step 1 — Create a new project
**File → New Project.** Change the project name, type, and other properties as needed.

### Step 2 — Import specimens
**Data → Import.** Set specimen properties such as name and goniometer parameters.
Specimen names will be listed on the left; their patterns will be displayed in the plot.
Repeat for each specimen.

### Step 3 — Pre-process specimens
Select a specimen, then apply tools such as **Smooth**, **Shift**, etc., as required.

### Step 4 (optional) — Identify peaks and minerals
Use the **Marker** tool to detect peaks, match minerals from the reference database, and label the peaks.

### Step 5 — Load and edit phases
Use **Edit Phases** to load the supplied standard phases.
On first use, standard phases need to be generated once.
Edit structural parameters for each component, as well as additional parameters for interstratified phases.

> **Note:** Edit Phases manages phases only. A phase is not used for modelling unless it is included in a mixture.
> Once a phase is added to a mixture, any parameter change in Edit Phases dynamically updates the pattern plot.

### Step 6 — Create a mixture
Use **Edit Mixtures** to create a new mixture.
Add columns (specimens) and rows (phases) using the buttons in the right and bottom margins.
Select the specimen to model in each column and the participating phase in each row.
Add more columns and rows as necessary.

### Step 7 — Optimise phase proportions
Click the **Optimize** button to determine the relative proportions of phases in each specimen.
The calculated pattern plot updates dynamically, and phase proportions and residuals are updated in the plot labels.

> **Notes:**
> 1. Individual phase parameters are not changed by optimisation.
> 2. "Optimize" only calculates the relative proportions of tick-marked phases.
> 3. For manual adjustment, remove the tick against the phase name and click "Optimize" again.
>    Phase parameters can also be adjusted manually by opening Edit Phases alongside.
> 4. It is good practice to reduce residuals (Rwp) by making manual adjustments before attempting refinement.

### Step 8 — View composition
Click the **Composition** button to display the major oxide composition of the mixture computed from the phase parameters.

### Step 9 — Refine phase parameters
Click **Refine** to open the refinement dialogue. Select up to two parameters from the list and click **Refine** to run the process.
If successful, refinement results will be displayed. Accepting the new values updates the calculated pattern plot and labels.

> **Notes:**
> 1. If Rwp is not low enough, refinement of phase parameters may be considered.
> 2. Refinement is computationally intensive. Complexity increases with the number of parameters, value ranges, algorithm choice, and number of iterations.
> 3. To speed up refinement: restrict parameter value ranges, change the algorithm, or reduce the number of iterations.

### Step 10 — Save and export
**File → Save Project.** Export the graph, refinement results, etc., as needed.

---

## How Things Work

Detailed explanations of MudLab's tools and outputs:

- [How MudLab calculates a diffraction pattern](how-to/diffraction-calculation.md)
- [Phase and component file formats](how-to/file-formats.md)
- [How default phases are generated](how-to/default-phases.md)
- [How to interpret Parameter Space Plots](how-to/parameter-space-plots.md)
- [How to correct for Goniometer shift](how-to/goniometer-shift.md)
- How to perform Baseline adjustment *(coming soon)*
- How to use the Search-Match tool *(coming soon)*
- How to set up a Refinement *(coming soon)*
