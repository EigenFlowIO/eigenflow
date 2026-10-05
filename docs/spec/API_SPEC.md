# Eigenflow v1 API specification

This document describes the public behavior implemented in the current repository (`1.0.0a1`). It is a reference document. For methodological guidance, begin with the conceptual documentation.

## Top-level exports

```python
import eigenflow as ef
```

The package exports:

```python
ef.Experiment
ef.ExperimentResult
ef.LayerResult
ef.ProbePopulation
ef.ProbeSample
ef.ExtractionConfig
ef.PyTorchExtractor

ef.metrics
ef.filtrations
ef.analyses
ef.operators
ef.spectra
ef.percolation
ef.transitions
ef.visualization
ef.presets
```

## `Experiment`

```python
@dataclass
class Experiment:
    model: object
    probes: ProbePopulation
    metric: object = "cosine"
    filtration: object = "edge_density"
    analyses: list = ["components", "percolation", "spectra"]
    extraction: ExtractionConfig = ExtractionConfig()
    device: object = None
    collate_fn: object = None
```

Run:

```python
result = experiment.run()
```

### `model`

Expected to be a PyTorch `nn.Module`. Eigenflow relies on `named_modules()`, forward hooks, `.eval()`, `.train()`, and ordinary PyTorch forward execution.

### `probes`

A `ProbePopulation`.

### `metric`

Either:

- a metric keyword;
- a `Metric` instance;
- an object exposing `.pairwise(...)`.

Supported keywords:

```text
cosine
euclidean
squared_euclidean
manhattan
correlation
dot_product
mahalanobis
rbf
polynomial
```

### `filtration`

Either a `Filtration` instance or supported keyword:

```text
threshold
edge_density
knn
mutual_knn
weighted_threshold
```

`"epsilon"` is represented by the `EpsilonFiltration` class but is not currently registered as a string alias in `resolve_filtration`.

### `analyses`

A list containing analysis keywords or `Analysis` instances.

Supported keywords:

```text
components
pcscs
percolation
spectra
eigenspaces
bridges
kcore
communities
factor_alignment
class_structure
transitions
localization
```

Keywords instantiate default configurations. Use explicit analysis objects for non-default parameters.

### `device`

Device passed to the `PyTorchExtractor`. If omitted, the extractor uses the device of the first model parameter when available, otherwise CPU.

### `collate_fn`

Optional callable used to combine non-tensor probe inputs into a model batch. If probe inputs are tensors and no `collate_fn` is supplied, Eigenflow uses `torch.stack`.

## Probe population

### `ProbeSample`

```python
ProbeSample(
    input,
    id: str,
    metadata: Mapping[str, Any] = {},
)
```

### `ProbePopulation`

```python
ProbePopulation(
    samples: list[ProbeSample],
    name: str = "probe_population",
    design: dict = {},
)
```

Probe IDs must be unique and a population may not be empty.

### `ProbePopulation.from_items`

```python
ProbePopulation.from_items(
    inputs,
    metadata=None,
    ids=None,
    name="probe_population",
)
```

If IDs are omitted, stable IDs of the form `probe_000000` are generated for the constructed population.

### Properties

```python
probes.ids
probes.metadata
probes.inputs
probes.values("class")
```

### `subset`

```python
subset = probes.subset(indices, name=None)
```

### `balance`

```python
balanced = probes.balance(
    factor="class",
    n_per_group=None,
    seed=0,
)
```

If `n_per_group` is omitted, the smallest observed group size is used.

### `stratify`

```python
cells = probes.stratify(
    by=["class", "background"],
)
```

Returns a dictionary from factor-value tuples to sample indices.

### `factorial`

```python
factorial = probes.factorial(
    factors=["class", "background"],
    n_per_cell=None,
    seed=0,
)
```

This samples existing cells. It does not synthesize missing factor combinations.

### `match`

```python
matched = probes.match(
    treatment={"background": "snow"},
    control={"background": "grass"},
    on=["class"],
)
```

Returns matched treatment/control samples for available keys.

## Extraction

### `ExtractionConfig`

```python
ExtractionConfig(
    sites="all",
    reducer="flatten",
    batch_size=32,
    retain_raw=False,
    leaf_modules_only=True,
)
```

`retain_raw` is present in the configuration but the current extractor does not persist raw activation tensors in the returned `Representation` objects. Do not rely on this field as an implemented raw-activation cache.

### Site selection

`sites="all"` with `leaf_modules_only=True` selects named leaf modules.

Explicit site selection:

```python
ExtractionConfig(
    sites=["features.4", "features.9"],
)
```

Explicit names are validated against `model.named_modules()`.

### `PyTorchExtractor`

```python
extractor = ef.PyTorchExtractor(
    model,
    config=None,
    device=None,
)
```

List all named module sites:

```python
extractor.available_sites()
```

Extract:

```python
representations = extractor.extract(
    probes,
    collate_fn=None,
)
```

During extraction the model is placed in evaluation mode and the forward pass runs under `torch.no_grad()`. The previous training/eval state is restored afterward.

For tuple/list or dict module outputs, the extractor captures the first tensor value it finds. Modules producing no tensor output are skipped.

## Reducers

Import from `eigenflow.extraction`.

```python
from eigenflow.extraction import (
    Flatten,
    GlobalAveragePool,
    GlobalMaxPool,
    SelectToken,
    MeanTokens,
)
```

Accepted reducer keywords:

```text
flatten
global_average
global_max
mean_tokens
```

`SelectToken` must currently be passed as an object:

```python
ExtractionConfig(
    reducer=SelectToken(index=0),
)
```

A callable can also be used. It receives the captured tensor and must return a tensor whose first dimension is batch.

## Representations

A representation contains the reduced population matrix, site name, probe IDs, raw output shape metadata, and reducer name.

The downstream metric layer expects rows to correspond exactly to probe order.

## Metrics

### Metric protocol

Subclass `Metric` and implement:

```python
class MyMetric(Metric):
    name = "my_metric"
    kind = "similarity"  # or "distance"

    def pairwise_values(self, X):
        ...
```

The base `.pairwise(...)` method constructs a `RelationalMatrix`.

### Built-ins

```python
ef.metrics.CosineSimilarity()
ef.metrics.EuclideanDistance()
ef.metrics.SquaredEuclideanDistance()
ef.metrics.ManhattanDistance()
ef.metrics.CorrelationDistance()
ef.metrics.DotProductSimilarity()
ef.metrics.MahalanobisDistance(regularization=1e-6)
ef.metrics.RBFKernel(gamma=None)
ef.metrics.PolynomialKernel(degree=3, gamma=None, coef0=1)
ef.metrics.CallableMetric(fn, name="callable", kind="similarity")
```

### Metric pipeline

```python
from eigenflow.metrics import (
    MetricPipeline,
    Center,
    Standardize,
    L2Normalize,
)

metric = MetricPipeline(
    transforms=[Center(), L2Normalize()],
    metric="cosine",
)
```

Transforms are applied to the representation matrix before the final metric.

### Metric diagnostics

```python
ef.metrics.metric_diagnostics(relational_matrix)
```

Experiment execution stores metric diagnostics in each `LayerResult.relational_metadata`.

## Filtrations

### Threshold

```python
ef.filtrations.ThresholdFiltration(
    values=None,
    steps=100,
)
```

For similarities, larger relations enter first as threshold decreases. For distances, orientation is reversed as necessary.

### Edge density

```python
ef.filtrations.EdgeDensityFiltration(
    densities=None,
    start=0.0,
    stop=1.0,
    steps=100,
)
```

The control parameter is requested edge density. Ties may cause multiple pairwise values to share the same native threshold, but the implementation selects a fixed number of ranked pairs.

### Epsilon

```python
ef.filtrations.EpsilonFiltration(
    values=None,
    steps=100,
)
```

This currently inherits threshold behavior and relies on a distance metric for epsilon-style semantics.

### k-nearest neighbors

```python
ef.filtrations.KNNFiltration(
    k_values=range(1, 11),
    mutual=False,
)

ef.filtrations.MutualKNNFiltration(
    k_values=range(1, 11),
)
```

The ordinary kNN graph symmetrizes directed neighbor choices by logical OR. Mutual kNN requires reciprocal neighbor selection.

### Weighted threshold

```python
ef.filtrations.WeightedThresholdFiltration(
    values=None,
    steps=100,
)
```

Retained similarity values become edge weights. For distance matrices, retained distances are converted to positive affinities relative to the maximum retained distance at that snapshot.

## Graph operators

Resolve by string:

```python
from eigenflow.operators import resolve_operator

operator = resolve_operator("normalized_laplacian")
```

Supported names:

```text
adjacency
laplacian
normalized_laplacian
random_walk
modularity
nonbacktracking
```

Operators are primarily configured through explicit spectral/eigenspace analysis objects.

## Analyses

### `ComponentsAnalysis`

Records component count, largest-component size, edge density, parameter, and node labels at every snapshot.

### `PCSCSAnalysis`

Extends components with:

```text
critical_parameter
component_derivative
convergence_parameter
```

### `PercolationAnalysis`

Observables:

```text
giant_component_fraction
second_component_fraction
susceptibility
susceptibility_peak_parameter
```

### `SpectralAnalysis`

```python
from eigenflow.analyses import SpectralAnalysis

SpectralAnalysis(
    operator="normalized_laplacian",
    k=None,
    vectors=True,
)
```

Returns a `SpectralTrajectory`.

### `EigenspaceAnalysis`

```python
EigenspaceAnalysis(
    operator="normalized_laplacian",
    dimensions=3,
)
```

Records overlap matrices and principal angles between consecutive low-dimensional eigenspaces.

### `BridgesAnalysis`

Records bridge edges per snapshot.

### `KCoreAnalysis`

```python
KCoreAnalysis(k=2)
```

Records surviving node indices and population fraction.

### `CommunitiesAnalysis`

Records community partitions returned by the graph community routine.

### `FactorAlignmentAnalysis`

```python
FactorAlignmentAnalysis(
    factors=None,
)
```

If factors are omitted, all metadata keys observed in the probe population are considered. Complete factors are compared with component labels using NMI and ARI.

### `ClassStructureAnalysis`

```python
ClassStructureAnalysis(
    factor="class",
)
```

Reports internal and external edge density per factor level.

### `TransitionsAnalysis`

Produces component-derivative, susceptibility-peak, and second-component-peak candidates and a simple consensus.

### `LocalizationAnalysis`

Available under keyword `"localization"`. Consult the implementation when using this experimental analysis; its API is not yet as stable as the major analysis classes above.

## Results

### `ExperimentResult`

```python
result.layers
result.provenance
result.metadata
result.summary()
result.save(path)
```

`result[site]` is equivalent to `result.layers[site]`.

### `LayerResult`

```python
layer.site
layer.metric
layer.filtration
layer.analyses
layer.relational_metadata
```

### `AnalysisResult`

```python
analysis.name
analysis.observables
analysis.records
analysis.metadata
```

## Persistence

```python
result.save("results/run_01")
```

The current implementation creates the directory and writes:

```text
results/run_01/result.json
```

NumPy arrays are converted to lists, NumPy scalar values are converted to Python scalars, and dataclass-like results are recursively converted. Spectral eigenvectors are deliberately omitted from JSON serialization.

There is **no current `ExperimentResult.load()` API** and no NPZ sidecar written by `save()`.

## Visualization

All public plotting functions return a Matplotlib `Figure`; `merge_events(...)` is the non-plotting helper that returns derived merge-event records. Plotting functions consume existing results and do not rerun the model or analysis pipeline. Functions that need the relational matrix, graph filtration, or original probes require an in-memory result from the current process because those runtime artifacts are intentionally omitted from `result.json`.

When a function accepts `probes=None`, it may use the probe population retained on an in-memory `ExperimentResult`; a standalone `LayerResult` does not itself contain the experiment-level probe population. The visualization guide documents which views are primary evidential views, diagnostics, or summary/report views.

Core compatibility helpers:

```python
from eigenflow.visualization import (
    observable_curve,
    layer_control_heatmap,
    eigenflow_plot,
)
```

Canonical structural views:

```python
probe_design_view(result_or_probes, factors=None, ax=None)
relational_matrix_heatmap(layer_result, probes=None, factor=None, ax=None)
component_trajectory(layer_result, analysis=None, smooth=True, ax=None)
component_membership_raster(layer_result, probes=None, factor=None, ax=None)
merge_events(layer_result)
merge_event_plot(layer_result, ax=None)
dendrogram_view(layer_result, probes=None, factor=None, ax=None)
graph_snapshot(layer_result, index=None, parameter=None, probes=None, factor=None,
               highlight_bridges=False, kcore=None, ax=None, seed=0)
combined_layer_dynamics(result, analysis="components", observable="component_count",
                        x="parameter", ax=None)
```

Spectral/eigenspace views:

```python
static_spectrum(layer_result, index=None, parameter=None, ax=None, highlight_gap=True)
spectral_flow(layer_result, ax=None, max_modes=12)
spectral_properties_dashboard(layer_result, fig=None)
localization_trajectory(layer_result, mode=0, ax=None)
eigenspace_stability(layer_result, ax=None)
eigenspace_overlap_heatmap(layer_result, index=-1, ax=None)
```

Semantic/diagnostic views:

```python
factor_alignment_trajectory(layer_result, factors=None, metric="nmi", ax=None)
factor_connectivity(layer_result, classes=None, ax=None)
bridge_probe_frequency(layer_result, probes=None, top_n=15, ax=None)
```

Comparison/report views:

```python
robustness_comparison(results, labels=None, site=None, analysis="factor_alignment",
                      factor="class", metric="nmi", ax=None)
cross_result_summary(results, labels=None, analysis="percolation",
                     observable="susceptibility_peak_parameter", ax=None)
percolation_dashboard(layer_result, fig=None)
interpretation_dashboard(layer_result, factor="class", fig=None)
```

`eigenflow_plot(...)` is a compatibility alias for the generalized spectral-flow view. The visualization guide documents the analyst question, evidential tier, interpretation boundary, and worked output for every canonical view.

## Presets

### PCSCS

```python
ef.presets.pcscs(
    model,
    probes,
    sites="all",
    thresholds=None,
    steps=100,
    device=None,
    collate_fn=None,
)
```

Uses flattening, cosine similarity, threshold filtration, `pcscs`, and `spectra`.

### Full

```python
ef.presets.full(model, probes, **kwargs)
```

Defaults analyses to components, percolation, spectra, eigenspaces, factor alignment, class structure, bridges, k-core, and communities.

## Current non-features

The v1 alpha interface does not currently provide:

- an `operators=` parameter on `Experiment`;
- a `cache=` parameter or persistent content-addressed execution cache;
- `ExperimentResult.load()`;
- raw-activation persistence despite the existing `retain_raw` configuration field;
- automatic semantic selection of "meaningful" layers for arbitrary architectures.

These are intentionally stated here so reference documentation does not promise behavior absent from the current implementation.
