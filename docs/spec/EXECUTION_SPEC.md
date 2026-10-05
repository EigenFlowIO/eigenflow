# Eigenflow execution specification

This document describes what the current implementation actually computes and distinguishes that behavior from future caching or optimization architecture.

## Current execution path

`Experiment.run()` performs the following sequence.

```text
resolve metric
resolve filtration
resolve analyses
        ↓
PyTorchExtractor.extract(probes)
        ↓
RepresentationCollection
        ↓
for each representation site:
    metric.pairwise(representation)
        ↓
    filtration.build(relational_matrix)
        ↓
    run every configured analysis
        ↓
    construct LayerResult
        ↓
collect provenance
        ↓
ExperimentResult
```

The neural network is executed once per extraction pass over the probe population, in batches.

The metric and filtration are then recomputed independently for each captured representation site.

The resulting `LayerResult` retains the reduced representation, relational matrix, and graph filtration as non-persistent runtime artifacts. The `ExperimentResult` retains the probe population. This adds no extra analytical recomputation; it preserves already-created objects for faithful visualization and diagnostics. `ExperimentResult.save()` omits these runtime artifacts.

Visualization is downstream of `Experiment.run()`. Calling a plotting function on an in-memory result does not execute the neural network, recompute the metric, or rebuild the filtration. A plotting call can still perform view-specific derivations from retained objects (for example, a merge hierarchy or graph layout), but those derivations are presentation/inspection work rather than a new model-analysis run.

## Dependency graph

The conceptual dependency graph is:

```text
model + probes + extraction config
                ↓
        representations by site
                ↓
              metric
                ↓
       relational matrix
                ↓
            filtration
                ↓
        graph snapshots
         /      |      \
components  percolation  operator
                         ↓
                       spectra
```

Factor analyses additionally depend on probe metadata.

Transition analysis currently recomputes several component/percolation-derived quantities from the filtration rather than consuming previous analysis results.

## Reuse within a run

Within one site:

- the metric is computed once;
- the filtration is built once;
- every analysis receives the same `AnalysisContext` containing that filtration.

Analyses can therefore share the graph-family object.

However, the current implementation does **not** memoize shared derived quantities such as component labels across analyses. If `components`, `percolation`, and `transitions` each need related graph statistics, they may compute them separately.

## No persistent execution cache

The current repository does not implement a `cache=` argument on `Experiment`, content-addressed cache keys, or persistent reuse across runs.

The dependency graph in this document describes semantic dependencies and potential reuse opportunities. It is not a claim that all nodes are currently cached.

This distinction matters for both performance expectations and reproducibility.

## Configuration invalidation

Even without an implemented cache, dependency reasoning determines what would need recomputation.

Changing only the requested **visualization** should not require rerunning the model if the required result object is already in memory.

Changing the **analysis list** while keeping a retained filtration could in principle reuse representations, metric, and graph snapshots, but the current top-level `Experiment.run()` recomputes the full path.

Changing the **filtration** invalidates graph snapshots and all graph-dependent analyses but not the underlying relational matrix in principle.

Changing the **metric** invalidates the relational matrix, filtration, and all downstream graph/operator analyses but not the extracted representations in principle.

Changing the **reducer** or **capture sites** invalidates the affected representations and everything downstream.

Changing the **probe population**, input preprocessing, or model/checkpoint invalidates the whole scientific object.

These rules should guide future caching work.

## Model execution behavior

The extractor:

1. selects explicit sites or named leaf modules;
2. registers forward hooks;
3. records the model's existing training state;
4. switches the model to evaluation mode;
5. runs batches under `torch.no_grad()`;
6. captures tensor outputs;
7. removes hooks;
8. restores the previous training state.

If a captured module returns:

- a tensor: it is reduced directly;
- a tuple/list: the first tensor element is used;
- a dict: the first tensor value is used;
- no tensor: that module contributes no representation.

## Batching and collation

`ExtractionConfig.batch_size` controls probe batching.

If every probe input is already a tensor, the default batching operation is:

```python
torch.stack(xs)
```

Non-tensor inputs require `collate_fn`.

The collated batch is moved to the configured device only if the collated object is itself a tensor. Complex model input signatures may therefore require a custom wrapper or collate strategy.

## Representation reduction

The reducer runs inside each forward hook and returns one row per batch item.

Captured reduced batches are moved to CPU and concatenated after extraction.

Downstream metric and graph computation currently operate through NumPy/SciPy/scikit-learn/NetworkX rather than remaining on the model's accelerator device.

## Computational scaling

Let:

- \(N\) = number of probes;
- \(D_\ell\) = representation dimension at site \(\ell\);
- \(L\) = number of captured sites;
- \(P\) = number of filtration snapshots.

Pairwise metrics generally require at least \(O(N^2)\) relational storage and often \(O(N^2D_\ell)\) work.

Materialized graph analysis scales with both \(N\) and \(P\).

Full dense eigendecomposition can scale approximately as \(O(N^3)\) per snapshot for node-space operators.

For large probe populations:

- reduce the number of sites;
- use a lower-dimensional reducer when scientifically defensible;
- reduce filtration steps during exploration;
- use explicit `SpectralAnalysis(k=...)` for partial spectra;
- avoid non-backtracking full spectra on large dense graphs;
- reserve full-resolution runs for the configurations that matter scientifically.

## Spectral solver behavior

`solve_spectrum` uses dense eigendecomposition when:

- matrix size is at most 128;
- `k is None`;
- or `k >= n - 1`.

For larger matrices with finite `k`, it uses sparse `eigsh` for symmetric matrices under the current implementation.

Non-symmetric operator handling uses dense `numpy.linalg.eig` in the dense path. The current sparse `eigsh` path is designed for symmetric matrices; configure spectral work accordingly.

## Failure behavior

The current `Experiment.run()` is not transactional.

If extraction or one analysis raises an exception, no partial `ExperimentResult` is returned by the top-level call.

Common validation failures include:

- empty probe population;
- duplicate probe IDs;
- unknown explicit module site;
- non-tensor inputs without `collate_fn`;
- unsupported metric/filtration/analysis keyword;
- reducer incompatible with tensor dimensionality.

## Worked recomputation cases

### Change only cosine to Euclidean

Scientifically unchanged:

- model;
- probes;
- captured site definitions;
- reducer.

Must change:

- relational matrix;
- filtration graph states;
- all downstream graph and spectral outputs.

A future cache could reuse extracted representations. Current `Experiment.run()` will extract again.

### Change only edge-density resolution

Representations and relational matrices are conceptually reusable.

Graph snapshots and downstream analyses change.

Current top-level execution recomputes everything.

### Add `bridges` to an otherwise identical run

Conceptually, existing representations, relational matrix, and graph filtration could be reused.

Current top-level execution reruns extraction and upstream construction.

### Change flatten to global-average pooling

The representation matrix changes, so the metric and every downstream object are no longer comparable as if only a plotting choice changed.

This is a new measurement configuration.

## Future optimization boundary

Caching, parallel execution, incremental graph updates, and warm-start eigensolvers can be added behind the current semantic boundaries without changing what an experiment means.

Any such implementation must preserve:

- probe ordering;
- deterministic configuration identity where possible;
- metric orientation;
- filtration parameters;
- analysis configuration;
- provenance sufficient to determine whether reuse is valid.
