# Eigenflow v1 Public API Specification

## Core experiment

`Experiment(model, probes, extraction, metric, filtration, analyses, operators=None, device=None, cache=True)` is the top-level declarative object. `run()` returns an `ExperimentResult`.

The architecture-aware boundary is `PyTorchExtractor`; downstream components consume `RepresentationCollection` objects and have no dependency on model type.

## Core protocols

- `Reducer.reduce(tensor) -> Tensor`: converts a module output into one feature vector per batch element.
- `Metric.pairwise(X) -> RelationalMatrix`: computes a symmetric pairwise relation and declares whether larger values mean greater similarity or distance.
- `Filtration.build(RelationalMatrix) -> GraphFiltration`: creates an ordered parameterized graph family.
- `GraphOperator.matrix(GraphSnapshot) -> sparse matrix`: derives an operator from a graph.
- `Analysis.run(AnalysisContext) -> AnalysisResult`: computes structural observables.

## Probe population

`ProbePopulation` stores ordered inputs, stable IDs, and metadata. Construction utilities include balancing, stratification, factorial cell selection, and matched contrasts.

## Extraction

`ExtractionConfig` defines module selection, reducer, batch handling, raw-activation retention, and device. Generic PyTorch extraction uses `named_modules()` and forward hooks. Default selection is leaf modules with tensor outputs; callers may choose explicit module names or predicates.

## Results

`ExperimentResult` contains provenance, representations, per-layer metric/filtration results, analyses, and comparison-ready observables. It supports JSON metadata export plus NPZ payload export via `save()`.

## Built-in analysis keywords

`components`, `pcscs`, `percolation`, `spectra`, `eigenspaces`, `localization`, `factor_alignment`, `class_structure`, `bridges`, `kcore`, `communities`, `transitions`.

String keywords are conveniences. Each maps to a typed `Analysis` implementation and can be replaced by an explicit configured object.
