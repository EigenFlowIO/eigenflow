# PCSCS visualization parity map

Eigenflow treats PCSCS as a canonical special case. The visualization surface therefore preserves the interpretive work performed by PCSCS plots while generalizing the underlying objects from cosine-threshold component sifting to arbitrary Eigenflow metrics, filtrations, operators, analyses, and layer×control comparisons.

| PCSCS surface | Eigenflow equivalent | Generalization |
|---|---|---|
| `plot_layer_analysis` | `component_trajectory` + `percolation_dashboard` | Component count, smoothed trend, critical/convergence annotations plus generalized graph-growth observables |
| `plot_merge_events` | `merge_event_plot` / `merge_events` | Works from retained graph-filtration lineage and can be combined with factor/probe metadata |
| `plot_dendrogram` | `dendrogram_view` | Single-linkage hierarchy derived from the exact relational matrix; supports arbitrary similarity or distance metrics with documented axis semantics |
| `plot_combined_layers` | `combined_layer_dynamics` + `layer_control_heatmap` | Multi-site trajectories and full layer×control fields for any scalar structural observable |
| `plot_eigenvalue_spectrum` | `static_spectrum` | Operator-aware static spectrum with Laplacian annotations |
| `plot_spectral_flow` | `spectral_flow` / `eigenflow_plot` | Generalized across Eigenflow spectral trajectories and explicitly paired with eigenspace-stability diagnostics |
| `plot_spectral_properties` | `spectral_properties_dashboard` | Algebraic connectivity, spectral entropy, effective rank, energy, localization and related operator-dependent summaries |
| similarity/class partition helpers | `relational_matrix_heatmap`, `component_membership_raster`, `factor_alignment_trajectory`, `factor_connectivity` | Makes semantic alignment with controlled probe factors a first-class visualization family |

PCSCS parity is a floor rather than the complete Eigenflow visualization objective. Eigenflow additionally exposes probe-design, relational-geometry, percolation, eigenspace, bridge/core, robustness, cross-result, and integrated interpretation views because those objects are part of the broader experiment model.
