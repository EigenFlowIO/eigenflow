# Eigenflow

Eigenflow is a PyTorch-first post hoc neural-network interpretability toolkit for controlled experiments on the **relational organization of probe populations** across network depth and control scale.

The methodological pipeline is:

`probe design → representation extraction → relational metric → graph filtration → structural/spectral observables → human inference about latent feature organization`

Eigenflow does not assume that a structural observable is itself a semantic explanation. Probe design supplies the experimental contrasts; Eigenflow supplies reproducible population-level measurements.

## Core object

For probe inputs \(x_i\) and an internal representation site \(\ell\), the model produces vectors \(z_i^{(\ell)}\). A metric induces a pairwise relation \(S^{(\ell)}\), and a filtration generates graphs \(G_{\ell,p}\) across control parameter \(p\). Analyses return observables \(Q(\ell,p)\).

## Quick start

```python
import torch
import eigenflow as ef

model = torch.nn.Sequential(
    torch.nn.Linear(4, 8),
    torch.nn.ReLU(),
    torch.nn.Linear(8, 2),
)

inputs = [torch.randn(4) for _ in range(32)]
metadata = [{"class": "A" if i < 16 else "B"} for i in range(32)]
probes = ef.ProbePopulation.from_items(inputs, metadata=metadata)

experiment = ef.Experiment(
    model=model,
    probes=probes,
    metric=ef.metrics.CosineSimilarity(),
    filtration=ef.filtrations.EdgeDensityFiltration(start=0.0, stop=0.5, steps=40),
    analyses=["components", "percolation", "spectra", "factor_alignment"],
)

result = experiment.run()
print(result.summary())
```

By default, the generic PyTorch extractor captures leaf modules that produce tensor outputs. Explicit module names can be supplied through `ExtractionConfig(sites=[...])`.

## Probe design

`ProbePopulation` preserves stable IDs and metadata and provides balancing, stratification, factorial cell selection, and matched contrast helpers. Metadata factors can be compared with graph partitions through NMI/ARI and class-conditioned structural measurements.

## Metrics

Built-ins include cosine similarity, Euclidean and squared Euclidean distance, Manhattan distance, correlation distance, dot-product similarity, Mahalanobis distance, RBF kernels, polynomial kernels, and callable custom metrics.

## Filtrations

Built-ins include native similarity/distance thresholding, edge-density filtration, k-nearest-neighbor filtration, and mutual-kNN filtration. Edge density is a first-class control coordinate for comparisons across metrics.

## Structural analysis

The initial v1 architecture includes connected components, PCSCS-compatible sifting, giant and second components, susceptibility, cluster-size distributions, bridge edges, k-cores, communities, adjacency/Laplacian/normalized-Laplacian/random-walk/modularity operators, eigenspectra, spectral gaps, entropy, energy, effective rank, IPR/localization, and eigenspace correspondence diagnostics.

## PCSCS

PCSCS remains a canonical special case:

```python
result = ef.presets.pcscs(model, probes)
```

This configures flattened activations, cosine similarity, threshold filtration, PCSCS connected-component analysis, and spectral diagnostics across captured representation sites.

## Scientific interpretation

Eigenflow measures structural consequences of learned representations. A controlled probe experiment can support inferences such as whether a representation is organized more strongly by class than background, where a distinction becomes coherent through network depth, or which samples bridge otherwise distinct groups. The software intentionally keeps those empirical observations separate from stronger semantic or causal claims.

## Persistent project state

The repository includes `project_state/`, containing the canonical project state, state-management protocol, and execution manifest used to build this initial repository.
