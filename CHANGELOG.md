# Changelog

All notable user-visible changes to Eigenflow should be recorded here.

The project is currently at **1.0.0a1**, an alpha release. Public interfaces and persistence behavior may still change before a stable 1.0 release.

## 1.0.0a1 — 2026-10-04 — initial alpha

### Added

- PyTorch-first population activation extraction using `nn.Module` forward hooks.
- Stable probe IDs and metadata-aware `ProbePopulation`.
- Probe balancing, stratification, factorial selection, and matched contrasts.
- Reducers for flattening, global average/max pooling, token selection, and token averaging.
- Pairwise cosine, Euclidean, squared Euclidean, Manhattan, correlation, dot-product, Mahalanobis, RBF, polynomial, and callable metrics.
- Metric preprocessing pipelines with centering, standardization, and L2 normalization.
- Threshold, edge-density, epsilon-style, kNN, mutual-kNN, and weighted-threshold filtrations.
- Connected-component and PCSCS-style analysis.
- Giant-component, second-component, and susceptibility percolation observables.
- Adjacency, Laplacian, normalized-Laplacian, random-walk, modularity, and non-backtracking graph operators.
- Spectral trajectories, algebraic connectivity, spectral gaps, entropy, effective rank, energy, and IPR.
- Eigenspace overlap and principal-angle tracking across control scale.
- Bridge, k-core, community, factor-alignment, class-structure, localization, and transition analyses.
- Basic layer/control and spectral visualization utilities.
- PCSCS and full-analysis presets.
- JSON result export.
- Persistent project-state and documentation-development workflow.

### Changed

- PCSCS is represented as a canonical special case within the broader Eigenflow architecture rather than the general package architecture.
- Documentation now frames interpretation as an inverse experimental inference from controlled structural evidence to hypotheses about latent feature organization.

### Known limitations

- `ExperimentResult.save()` currently writes JSON only; there is no public `load()` method.
- Eigenvectors are omitted from saved JSON.
- `ExtractionConfig.retain_raw` exists but raw activation persistence is not currently implemented.
- No persistent execution cache is implemented.
- Default capture uses leaf modules; Eigenflow does not automatically determine which sites are semantically best for an arbitrary model.
- Large full spectral sweeps can be computationally expensive.
- The current package is PyTorch-first; other neural-network frameworks are not yet supported.
- Percolation-style transition statistics are descriptive and do not establish statistical-physics criticality or universality.

### Scientific interpretation

Results are conditional on the probe population, representation sites, reducer, metric, filtration, control range, graph operator, and analysis. Changes to any of these can affect the meaning and comparability of outputs.

When upgrading between alpha releases, rerun important experiments or explicitly verify that the relevant measurement semantics have not changed.
