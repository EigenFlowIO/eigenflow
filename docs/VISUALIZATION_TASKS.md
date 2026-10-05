# Visualization implementation backlog

Status: **complete**

> Historical implementation backlog. The post-implementation human-facing reconciliation is tracked separately in [`HUMAN_FACING_REVISION_TASKS.md`](HUMAN_FACING_REVISION_TASKS.md).

## viz_task_001 — Inventory PCSCS visualization semantics

**Status:** complete

**Priority:** critical

**Objective:** Document the exact semantic purpose, inputs, outputs, and annotations of every PCSCS visualization so Eigenflow can preserve or supersede them intentionally.

**Acceptance criteria:**

- Includes plot_layer_analysis, plot_merge_events, plot_dendrogram, plot_combined_layers, plot_eigenvalue_spectrum, plot_spectral_flow, and plot_spectral_properties.
- Records which PCSCS statistics each plot exposes: component count, smoothed count, critical threshold, convergence threshold, merge events, layer comparison, spectra, spectral flow, and spectral properties.
- Identifies any PCSCS view that has no current Eigenflow equivalent.

## viz_task_002 — Implement connected-component trajectory plot

**Status:** complete

**Priority:** critical

**Objective:** Add an Eigenflow visualization for component count over control scale with PCSCS-compatible annotations.

**Acceptance criteria:**

- Plots raw connected-component count over filtration parameter.
- Supports optional smoothed trajectory when PCSCS-style derivative analysis is available.
- Marks critical parameter and convergence parameter when present.
- Works for both native threshold and edge-density filtrations.
- Accepts LayerResult / AnalysisResult without re-running the experiment.

## viz_task_003 — Implement merge-event visualization

**Status:** complete

**Priority:** critical

**Objective:** Visualize discrete component-merger events across the filtration and expose which groups/probes participate.

**Acceptance criteria:**

- Shows merge parameter/control value.
- Represents source components and resulting merged component.
- Supports probe IDs and optional factor/class labels.
- Can be generated from existing component/PCSCS analysis output or a dedicated merge-event record.

## viz_task_004 — Implement dendrogram / hierarchical merge view

**Status:** complete

**Priority:** critical

**Objective:** Provide a dendrogram-like hierarchy showing how probes or connected groups merge as relational thresholds are relaxed.

**Acceptance criteria:**

- Branch height corresponds to a documented filtration/native-threshold quantity.
- Leaf labels can show probe IDs and optionally metadata factors.
- Tie handling is deterministic and documented.
- The visualization makes no unsupported claim that the graph filtration is equivalent to standard agglomerative clustering.
- Works with PCSCS-compatible cosine-threshold experiments.

## viz_task_005 — Implement combined-layer component dynamics view

**Status:** complete

**Priority:** high

**Objective:** Generalize PCSCS combined-layer plots so component dynamics can be compared across representation sites.

**Acceptance criteria:**

- Displays component-count trajectories for multiple sites on comparable axes.
- Can mark per-layer critical and convergence parameters.
- Supports matched edge density for cross-layer/cross-metric comparisons.
- Provides clear labeling when native thresholds are not directly comparable.

## viz_task_006 — Implement static eigenvalue spectrum view

**Status:** complete

**Priority:** high

**Objective:** Add a dedicated static-spectrum visualization for one graph snapshot, distinct from spectral flow.

**Acceptance criteria:**

- Plots the selected operator spectrum at one control value.
- Displays operator name and control/native parameter.
- Supports Laplacian zero-mode/component interpretation where applicable.
- Optionally highlights algebraic connectivity and requested spectral gaps.

## viz_task_007 — Expand spectral-flow visualization

**Status:** complete

**Priority:** high

**Objective:** Ensure Eigenflow spectral-flow plots cover the full PCSCS spectral-flow use case and generalized operator analysis.

**Acceptance criteria:**

- Plots multiple eigenvalue branches across control scale.
- Supports mode-count limits and operator labeling.
- Handles eigenvalue ordering carefully and points readers to eigenspace analysis near crossings/degeneracy.
- Works with multiple graph operators where spectra are available.

## viz_task_008 — Implement spectral-properties dashboard

**Status:** complete

**Priority:** high

**Objective:** Create a consolidated spectral-properties view analogous to PCSCS spectral-properties plotting but generalized to Eigenflow observables.

**Acceptance criteria:**

- Includes algebraic connectivity when defined.
- Includes one or more spectral-gap summaries.
- Includes spectral entropy/effective rank and localization/IPR where available.
- Can overlay or annotate PCSCS critical/convergence/transition parameters.
- Uses separate axes/panels only where units or scales differ.

## viz_task_009 — Add graph-snapshot structural view

**Status:** complete

**Priority:** medium

**Objective:** Retain the generalized Eigenflow graph snapshot view and make it a documented complement to PCSCS parity plots.

**Acceptance criteria:**

- Colors or groups nodes by selected probe metadata when requested.
- Highlights bridges/cores/communities when requested.
- Displays control parameter and site.
- Clearly treats layout as visualization rather than a learned embedding.

## viz_task_010 — Add factor-alignment and class-structure visualizations

**Status:** complete

**Priority:** medium

**Objective:** Visualize semantic alignment diagnostics across control scale for controlled probe factors.

**Acceptance criteria:**

- Plots NMI and/or ARI by factor over control parameter.
- Plots within-factor versus external density where class_structure is used.
- Supports multiple sites or one-site detail views.
- Documentation states that alignment is evidence conditioned on the probe design, not proof of unique encoding.

## viz_task_011 — Add eigenspace stability visualizations

**Status:** complete

**Priority:** medium

**Objective:** Visualize principal angles and overlap matrices so spectral correspondence is not inferred from eigenvalue ordering alone.

**Acceptance criteria:**

- Principal-angle trajectory plot exists.
- Eigenspace-overlap heatmap exists.
- Examples include a crossing/near-degeneracy interpretation.

## viz_task_012 — Define canonical visualization API

**Status:** complete

**Priority:** critical

**Objective:** Unify PCSCS-compatible and generalized Eigenflow visualizations behind documented public functions.

**Acceptance criteria:**

- Names, signatures, accepted result objects, defaults, return types, and failure behavior are specified.
- Every visualization consumes existing result objects where possible instead of re-running analyses.
- PCSCS compatibility aliases or migration examples are documented.
- API_SPEC.md and visualization package exports agree exactly.

## viz_task_013 — Regenerate complete Colab demonstration

**Status:** complete

**Priority:** critical

**Objective:** Replace the incomplete spectral-demo bundle with a complete visualization demonstration using the actual Eigenflow public visualization API.

**Acceptance criteria:**

- Runs from a clean Google Colab session against a pinned Eigenflow commit.
- Generates every canonical visualization type, including component-count trajectory, merge events, dendrogram, combined-layer view, static spectrum, spectral flow, and spectral-properties view.
- Generates generalized Eigenflow views for factor alignment, graph snapshots, eigenspace stability, and layer×control summaries.
- Produces numerical outputs and metadata required to reproduce every figure.

## viz_task_014 — Package visualization artifact bundle

**Status:** complete

**Priority:** high

**Objective:** Create a reproducible ZIP containing the script, figures, data tables, result JSON, configuration, environment metadata, and checksums.

**Acceptance criteria:**

- Figure manifest maps every image to generating function, input result object, site, control parameter, and interpretation purpose.
- README in the ZIP explains each image type and what question it answers.
- SHA-256 manifest covers all generated artifacts.
- Bundle is generated by the Colab script itself.

## viz_task_015 — Integrate generated visuals into repository documentation

**Status:** complete

**Priority:** high

**Objective:** Add selected real generated images and their code/output examples to the Eigenflow human-facing surface.

**Acceptance criteria:**

- README contains a compact visual orientation without becoming image-heavy.
- A dedicated visualization/example guide contains all canonical figure types.
- Each figure is accompanied by code, description of axes/encoding, intended use, interpretation example, alternatives, and unsupported claims.
- PCSCS compatibility docs explicitly map old plot functions to new Eigenflow equivalents.

## viz_task_016 — Add visualization regression tests

**Status:** complete

**Priority:** high

**Objective:** Prevent future loss of visualization surface and ensure plotting functions continue to accept real result objects.

**Acceptance criteria:**

- Smoke tests generate every public visualization without exception.
- Tests verify required annotations/axes/data-series presence.
- At least one PCSCS-compatible fixture exercises dendrogram/component/merge views.
- Tests avoid brittle pixel-perfect comparison unless a stable image-regression harness is intentionally adopted.

## viz_task_017 — Validate visualization interpretation surface

**Status:** complete

**Priority:** high

**Objective:** Run the antagonistic author/editor process on visualization documentation so figure interpretation is technically correct and epistemically bounded.

**Acceptance criteria:**

- Every figure type has indication, construction, reading instructions, interpretation, alternatives, and claim boundary.
- Software editor confirms exact implementation fidelity.
- Research/statistics review confirms that plots are not treated as semantic proof.
- PCSCS parity claims are checked against the PCSCS visualization inventory.
