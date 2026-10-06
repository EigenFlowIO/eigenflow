
## Unreleased - complex-spectrum semantics

- preserve complex eigenpairs for nonsymmetric operators instead of truncating imaginary components;
- add `SpectralAnalysis(..., complex=...)` with `auto`, `preserve`, `modulus`, `real`, `phase`, `imag`, and `error`;
- add tolerance-aware complex detection and operator spectral expectations;
- make eigenspace overlap and IPR complex-safe;
- add matched complex spectral trajectories and `complex_spectrum_plot`;
- add policy-aware spectral comparison and explicit projection-specific gap semantics;
- persist complex eigenvalues and complex spectral eigenvectors losslessly;
- surface complex/incompatibility status in result summaries.

# Changelog

All notable user-visible changes to Eigenflow should be recorded here.

The project is currently at **1.0.0a1**, an alpha release. Public interfaces and persistence behavior may still change before a stable 1.0 release.

## Unreleased

### Added

- Structured graph/operator compatibility validation via `OperatorCompatibilityError`.
- Explicit `signed_laplacian` and `signed_normalized_laplacian` operators using absolute weighted degree.
- Structured eigenspace incompatibility records when consecutive operator matrices live in different ambient spaces.

### Changed

- Ordinary `normalized_laplacian` and `random_walk` operators now reject negative weighted graphs before numerical normalization instead of permitting NaN/Inf propagation.
- `SpectralAnalysis`, `EigenspaceAnalysis`, and `LocalizationAnalysis` preserve mathematically incompatible snapshots as explicit result records rather than surfacing opaque downstream linear-algebra failures.
- Non-backtracking eigenspace trajectories now report `changing_ambient_space` when filtration snapshots have different directed-edge dimensions.

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
- Comprehensive visualization ontology and public visualization suite covering probe design, relational geometry, PCSCS-compatible component trajectories and dendrograms, percolation dashboards, graph snapshots, static spectra, spectral flow, spectral-property and eigenspace views, factor alignment, layer × control maps, robustness comparisons, and integrated interpretation dashboards.
- In-memory runtime result artifacts retaining probes, reduced representations, relational matrices, and graph filtrations for faithful visualization while keeping JSON persistence unchanged.
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

## Development instrumentation phase

- Added first-class experiment specifications and compatibility validation for controlled cross-model/checkpoint comparisons.
- Added versioned `ProbeSuite`, `ExperimentSeries`, `StructuralDiff`, `LongitudinalResult`, `SiteAlignment`, `BehavioralRecord`, and `DevelopmentReport` abstractions.
- Added portable experiment-series persistence with result subdirectories and compressed numeric-array sidecars.
- Added retention/forgetting summaries, PEFT-targeting diagnostics, transparent checkpoint selection, and training-data diagnostics.
- Added checkpoint, longitudinal-surface, layer×checkpoint, structural-diff, architecture-comparison, retention, and development-dashboard visualizations.
- Added runnable architecture-comparison and fine-tuning/checkpoint examples plus a Colab launcher.
- Added development-instrumentation, architecture-development, fine-tuning/post-training, and longitudinal-interpretation documentation.
