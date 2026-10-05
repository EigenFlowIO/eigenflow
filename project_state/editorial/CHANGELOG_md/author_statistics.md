# Computational statistics professor with a background in computational research design draft — `CHANGELOG.md`

Prioritize identification, measurement assumptions, sensitivity, finite-sample behavior, alternative explanations, convergence of evidence, and calibrated interpretation.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## 1.0.0a1 — initial alpha

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: 

## Added

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: - PyTorch-first population activation extraction using `nn.Module` forward hooks. - Stable probe IDs and metadata-aware `ProbePopulation`. - Probe balancing, stratification, factorial selection, and matched contrasts. - Reducers for flattening, global average/max pooling, token selection, and token averaging. - Pairwise cosine, Euclidean, squared Euclidean, Manhattan, correlation, dot-product, Mahalanobis, RBF, polynomial, and callable metrics. - Metric preprocessing pipelines with centering, standardization, and L2 normalization. - Threshold, edge-density, epsilon-style, kNN, mutual-kNN, and weighted-threshold filtrations. - Connected-component and PCSCS-style analysis. - Giant-component, s

## Changed

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: - PCSCS is represented as a canonical special case within the broader Eigenflow architecture rather than the general package architecture. - Documentation now frames interpretation as an inverse experimental inference from controlled structural evidence to hypotheses about latent feature organization.

## Known limitations

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: - `ExperimentResult.save()` currently writes JSON only; there is no public `load()` method. - Eigenvectors are omitted from saved JSON. - `ExtractionConfig.retain_raw` exists but raw activation persistence is not currently implemented. - No persistent execution cache is implemented. - Default capture uses leaf modules; Eigenflow does not automatically determine which sites are semantically best for an arbitrary model. - Large full spectral sweeps can be computationally expensive. - The current package is PyTorch-first; other neural-network frameworks are not yet supported. - Percolation-style transition statistics are descriptive and do not establish statistical-physics criticality or univer

## Scientific interpretation

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: Results are conditional on the probe population, representation sites, reducer, metric, filtration, control range, graph operator, and analysis. Changes to any of these can affect the meaning and comparability of outputs. When upgrading between alpha releases, rerun important experiments or explicitly verify that the relevant measurement semantics have not changed.
