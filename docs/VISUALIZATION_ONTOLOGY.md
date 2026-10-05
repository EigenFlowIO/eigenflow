# Eigenflow visualization ontology

Status: **current project phase**

Eigenflow's visualization system is designed from the package's experimental and epistemic objectives rather than from the list of statistics currently implemented.

## Governing purpose

Eigenflow supports controlled post hoc inference about latent feature organization by measuring population-level relational structure across network depth and control scale.

A visualization is therefore justified only if it helps the analyst answer a consequential question in that inferential chain.

## Visualization tiers

### Primary evidential views

Expose measured relational or structural evidence directly and support substantive experimental inference.

### Diagnostic views

Explain anomalies, pivotal probes, local graph roles, or measurement behavior. They are not the primary semantic evidence.

### Summary/report views

Synthesize multiple validated evidential views for comparison, interpretation, and communication.

## Canonical view schema

Every public visualization must specify:

- the analyst question it answers;
- source data/result objects;
- required analysis dependencies;
- visual encoding;
- permitted inference;
- common misinterpretation;
- upstream dependencies;
- tier and implementation priority.

## view_001 — Probe design / factor structure view

**Tier:** primary evidential

**Question:** Does the probe population actually distinguish the experimental hypotheses?

**Source objects:** ProbePopulation.metadata, ProbePopulation.design

**Required analysis:** none

**Encoding:** factor-count bars, factorial contingency heatmap, missing-cell indicators, optional sample gallery

**Permitted inference:** Assess balance, coverage, factorial completeness, and obvious confounding in the probe design.

**Common misinterpretation:** Treating balanced counts as proof that all nuisance variables are controlled.

**Dependencies:** probe metadata

**Priority:** critical

## view_002 — Factor-ordered relational matrix

**Tier:** primary evidential

**Question:** What pairwise relational geometry exists before graph thresholding, and how does it align with known factors?

**Source objects:** RelationalMatrix.values, RelationalMatrix.probe_ids, ProbePopulation.metadata

**Required analysis:** metric only

**Encoding:** heatmap ordered or annotated by experimental factors

**Permitted inference:** Identify broad block structure, gradients, outliers, and factor-consistent relational organization under the chosen metric.

**Common misinterpretation:** Treating visible blocks as metric-independent latent classes.

**Dependencies:** representation reducer, metric

**Priority:** critical

## view_003 — Connected-component trajectory

**Tier:** primary evidential

**Question:** How does fragmentation collapse as the control parameter changes?

**Source objects:** ComponentsAnalysis, PCSCSAnalysis

**Required analysis:** components or pcscs

**Encoding:** component count vs control parameter; optional smoothed curve; critical and convergence annotations

**Permitted inference:** Locate regimes of rapid merger, persistence, and global convergence.

**Common misinterpretation:** Equating the maximal derivative with a physical critical point or semantic transition without supporting evidence.

**Dependencies:** filtration

**Priority:** critical

## view_004 — Component membership raster

**Tier:** primary evidential

**Question:** Which probes remain grouped together across control scale?

**Source objects:** ComponentsAnalysis.records, ProbePopulation.metadata

**Required analysis:** components

**Encoding:** probe × control matrix colored by component identity, optionally ordered by factor

**Permitted inference:** Assess persistence, group stability, and which probes change membership relationships across scale.

**Common misinterpretation:** Interpreting component color identity as stable semantic labels when components merge and labels may be arbitrary.

**Dependencies:** components

**Priority:** critical

## view_005 — Merge-event plot

**Tier:** primary evidential

**Question:** Which groups merge, at what control values, and through which relations?

**Source objects:** component lineage / merge records, BridgeAnalysis, GraphFiltration

**Required analysis:** components plus merge-event derivation

**Encoding:** event timeline/tree with source and resulting components

**Permitted inference:** Identify discrete merger events and candidate bridge relations driving larger-scale consolidation.

**Common misinterpretation:** Assuming one merge event corresponds to one semantic feature transition.

**Dependencies:** component lineage

**Priority:** critical

## view_006 — Dendrogram / merge hierarchy

**Tier:** primary evidential

**Question:** What hierarchical order of relational consolidation is induced by the filtration?

**Source objects:** threshold/merge events, probe IDs, metadata

**Required analysis:** merge hierarchy derivation

**Encoding:** hierarchical tree with branch height tied to filtration/native threshold quantity

**Permitted inference:** Visualize persistent relational groupings and their merge order.

**Common misinterpretation:** Treating the graph filtration as identical to standard agglomerative clustering or treating branch heights as metric-independent semantic distances.

**Dependencies:** monotone merge hierarchy

**Priority:** critical

## view_007 — Percolation / structural-transition dashboard

**Tier:** summary/report

**Question:** How does graph structure move from local fragmentation to mesoscale and macroscopic connectivity?

**Source objects:** ComponentsAnalysis, PercolationAnalysis, TransitionsAnalysis

**Required analysis:** components, percolation, transitions

**Encoding:** aligned component count, giant component, second component, susceptibility, transition markers

**Permitted inference:** Characterize graph-growth regimes and compare multiple transition indicators.

**Common misinterpretation:** Calling finite-sample transition markers universal phase transitions.

**Dependencies:** filtration

**Priority:** critical

## view_008 — Graph snapshot with semantic annotation

**Tier:** diagnostic

**Question:** What does one selected graph state look like, and which probes/edges are structurally important?

**Source objects:** GraphSnapshot, ProbePopulation.metadata, BridgesAnalysis, KCoreAnalysis, CommunitiesAnalysis

**Required analysis:** optional bridges/kcore/communities

**Encoding:** node-link layout colored by factor/community/core with highlighted bridges

**Permitted inference:** Inspect local structural roles and identify probes worth qualitative examination.

**Common misinterpretation:** Reading force-directed node position as a learned embedding or metric geometry.

**Dependencies:** graph snapshot

**Priority:** high

## view_009 — Static eigenvalue spectrum

**Tier:** primary evidential

**Question:** What operator-scale structure exists at a selected graph state?

**Source objects:** SpectralSnapshot

**Required analysis:** spectra

**Encoding:** eigenvalue index/value plot with operator and control annotations

**Permitted inference:** Inspect zero modes, algebraic connectivity, spectral gaps, spectral concentration, and operator-specific structure.

**Common misinterpretation:** Assigning semantic meaning to isolated eigenvalues without probe/factor context.

**Dependencies:** graph operator

**Priority:** high

## view_010 — Spectral flow

**Tier:** primary evidential

**Question:** How do operator eigenvalues change across the filtration?

**Source objects:** SpectralTrajectory

**Required analysis:** spectra

**Encoding:** multiple eigenvalue branches vs control parameter

**Permitted inference:** Identify persistent spectral regimes, crossings, gap openings/closures, and scale-dependent operator structure.

**Common misinterpretation:** Assuming sorted eigenvalue index identifies the same eigenmode across crossings or degeneracy.

**Dependencies:** spectra

**Priority:** critical

## view_011 — Spectral-properties dashboard

**Tier:** summary/report

**Question:** How do key spectral observables jointly characterize structural organization across control scale?

**Source objects:** SpectralTrajectory, TransitionsAnalysis

**Required analysis:** spectra

**Encoding:** aligned algebraic connectivity, selected gaps, entropy/effective rank, energy, localization/IPR, transition annotations

**Permitted inference:** Compare complementary spectral summaries and align them with structural transition regimes.

**Common misinterpretation:** Treating all spectral statistics as interchangeable measures of one latent property.

**Dependencies:** spectra

**Priority:** critical

## view_012 — Eigenspace stability view

**Tier:** primary evidential

**Question:** Are low-dimensional structural modes stable across adjacent control values?

**Source objects:** EigenspaceAnalysis.records

**Required analysis:** eigenspaces

**Encoding:** principal-angle trajectories and overlap heatmaps

**Permitted inference:** Assess subspace continuity through eigenvalue crossings or near-degeneracy.

**Common misinterpretation:** Treating an individual basis vector as stable when only the subspace is identified.

**Dependencies:** eigenspaces

**Priority:** high

## view_013 — Factor-alignment trajectory

**Tier:** primary evidential

**Question:** How strongly does emergent graph structure align with controlled semantic factors across scale?

**Source objects:** FactorAlignmentAnalysis.records

**Required analysis:** factor_alignment

**Encoding:** NMI/ARI vs control parameter for one or more factors

**Permitted inference:** Compare which recorded factors best explain emergent component partitions under the current design.

**Common misinterpretation:** Treating high alignment as proof of unique semantic encoding or causality.

**Dependencies:** probe metadata, components

**Priority:** critical

## view_014 — Factor internal-vs-external connectivity

**Tier:** primary evidential

**Question:** Are probes within a factor level more densely connected than they are to other levels?

**Source objects:** ClassStructureAnalysis.records

**Required analysis:** class_structure

**Encoding:** internal and external edge-density trajectories by factor level

**Permitted inference:** Assess relational coherence and mixing of controlled groups.

**Common misinterpretation:** Interpreting group separation as universally desirable or as sufficient evidence of a causal feature.

**Dependencies:** probe metadata, filtration

**Priority:** high

## view_015 — Layer × control heatmap

**Tier:** primary evidential

**Question:** Where in network depth and relational scale does a structural observable change?

**Source objects:** ExperimentResult.layers, scalar AnalysisResult observable

**Required analysis:** any scalar trajectory

**Encoding:** site/layer × control heatmap

**Permitted inference:** Locate depth-dependent emergence, strengthening, weakening, or movement of structural regimes.

**Common misinterpretation:** Treating non-equivalent sites across architectures as metrically interchangeable.

**Dependencies:** multiple sites

**Priority:** critical

## view_016 — Combined-layer dynamics

**Tier:** primary evidential

**Question:** How do the same structural trajectories compare across representation sites?

**Source objects:** ExperimentResult.layers

**Required analysis:** components/percolation/spectra/factor alignment

**Encoding:** multi-layer overlays or aligned small multiples

**Permitted inference:** Compare persistence, transition location, and structural strength through depth.

**Common misinterpretation:** Comparing native metric thresholds across layers or metrics when scales are not commensurable.

**Dependencies:** multiple sites

**Priority:** critical

## view_017 — Bridge/core/outlier diagnostic

**Tier:** diagnostic

**Question:** Which individual probes disproportionately influence structural connectivity or spectral organization?

**Source objects:** BridgesAnalysis, KCoreAnalysis, LocalizationAnalysis, SpectralSnapshot.eigenvectors

**Required analysis:** bridges/kcore/localization/spectra

**Encoding:** probe ranking, probe trajectory, highlighted graph nodes, optional image/contact sheet

**Permitted inference:** Identify structurally pivotal or atypical probes for qualitative inspection.

**Common misinterpretation:** Assuming an influential probe is mislabeled or semantically ambiguous without inspecting it.

**Dependencies:** probe IDs

**Priority:** high

## view_018 — Measurement robustness comparison

**Tier:** primary evidential

**Question:** Does the substantive interpretation survive reasonable changes in metric, reducer, filtration, or probe sample?

**Source objects:** multiple ExperimentResult objects

**Required analysis:** comparison layer

**Encoding:** matched-control overlays, robustness matrices, difference heatmaps, resampling intervals

**Permitted inference:** Assess dependence of conclusions on analysis choices and finite-sample variation.

**Common misinterpretation:** Treating numerical non-identity as failure when the substantive structural conclusion is stable.

**Dependencies:** comparable repeated experiments

**Priority:** critical

## view_019 — Cross-model / cross-condition comparison

**Tier:** summary/report

**Question:** How does representational organization differ between models, checkpoints, or interventions?

**Source objects:** multiple ExperimentResult objects

**Required analysis:** comparison layer

**Encoding:** difference heatmaps, aligned trajectories, model × layer summaries

**Permitted inference:** Compare structural consequences of training state, architecture, or intervention under matched probe designs.

**Common misinterpretation:** Attributing differences to architecture/training when probe preprocessing or site alignment also changed.

**Dependencies:** matched experiment specifications

**Priority:** medium

## view_020 — Integrated experimental-interpretation dashboard

**Tier:** summary/report

**Question:** What combined visual evidence bears directly on the experiment's feature-interpretation hypothesis?

**Source objects:** ExperimentResult, ProbePopulation.metadata, selected analyses

**Required analysis:** multiple

**Encoding:** curated panel combining factor alignment, structural transition, layer×control, selected graph, and robustness evidence

**Permitted inference:** Synthesize complementary evidence into a bounded experimental conclusion.

**Common misinterpretation:** Treating the dashboard as an automated explanation rather than a structured evidence display.

**Dependencies:** primary evidential views

**Priority:** critical

## Implemented public mapping

The ontology is implemented through the following public visualization surface. A single function may support more than one ontology question, and dashboards intentionally synthesize multiple primary views.

| Ontology view | Public implementation |
| --- | --- |
| Probe design / factor structure | `probe_design_view` |
| Factor-ordered relational matrix | `relational_matrix_heatmap` |
| Connected-component trajectory | `component_trajectory` |
| Component membership raster | `component_membership_raster` |
| Merge-event view | `merge_events`, `merge_event_plot` |
| Dendrogram / merge hierarchy | `dendrogram_view` |
| Percolation / structural transition | `percolation_dashboard` |
| Graph snapshot | `graph_snapshot` |
| Static eigenvalue spectrum | `static_spectrum` |
| Spectral flow | `spectral_flow`, compatibility alias `eigenflow_plot` |
| Spectral-properties dashboard | `spectral_properties_dashboard` |
| Eigenspace stability | `eigenspace_stability`, `eigenspace_overlap_heatmap` |
| Factor alignment | `factor_alignment_trajectory` |
| Factor internal/external connectivity | `factor_connectivity` |
| Layer × control field | `layer_control_heatmap` |
| Combined-layer dynamics | `combined_layer_dynamics` |
| Bridge/core/outlier diagnostics | `bridge_probe_frequency`, `graph_snapshot`, `localization_trajectory` |
| Measurement robustness | `robustness_comparison` |
| Cross-result comparison | `cross_result_summary` |
| Integrated interpretation | `interpretation_dashboard` |

The implementation mapping does not change the epistemic status of a view. In particular, graph layouts and probe-level diagnostics remain diagnostic even when they are visually prominent, and dashboards remain summaries of underlying evidence rather than automated semantic explanations.
