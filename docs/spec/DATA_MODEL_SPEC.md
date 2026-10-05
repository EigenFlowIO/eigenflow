# Eigenflow data-model specification

This specification describes the current in-memory object chain and persistence behavior.

## Object chain

The principal objects are:

```text
ProbePopulation
    ↓
RepresentationCollection
    ↓
RelationalMatrix
    ↓
GraphFiltration
    ↓
GraphSnapshot
    ↓
AnalysisResult
    ↓
LayerResult
    ↓
ExperimentResult
```

The same probe ordering must remain invariant through the chain.

## Probe identity and ordering

A `ProbePopulation` contains ordered `ProbeSample` objects.

```python
ProbeSample(
    input=<model-compatible object>,
    id=<unique string>,
    metadata=<mapping>,
)
```

IDs must be unique.

The order of `ProbePopulation.samples` defines the row order used during extraction. That order becomes the order of:

- representation rows;
- relational-matrix rows and columns;
- graph nodes;
- component label arrays;
- spectral node coordinates.

Do not reorder a downstream matrix without reordering probe IDs and all dependent objects consistently.

## Representation

A `Representation` corresponds to one captured site.

Conceptually:

```text
values       N × D numeric matrix
site         module/site identifier
probe_ids    ordered IDs, length N
raw_shape    captured tensor shape metadata
reducer      reducer name
```

`D` may differ by site.

Raw activation shape can be multidimensional, but the reducer returns one vector per probe.

## RepresentationCollection

A `RepresentationCollection` maps site names to `Representation` objects and preserves the population IDs.

Different sites may have different feature dimensions but must contain the same probes in the same order.

## RelationalMatrix

```python
RelationalMatrix(
    values: N × N array,
    kind: "similarity" | "distance",
    metric: str,
    probe_ids: list[str],
    metadata: dict,
)
```

The matrix must be square.

`kind` is semantically important. Threshold filtrations use it to determine whether larger or smaller raw values represent stronger relations.

A relational matrix is not assumed to be a neural-network parameter object. It is a derived measurement of the population representation.

## GraphSnapshot

```python
GraphSnapshot(
    parameter: float,
    adjacency: scipy.sparse.csr_matrix,
    edge_density: float,
    native_parameter: float | int | None,
    metadata: dict,
)
```

`parameter` is the filtration's exposed control coordinate.

`native_parameter` records the corresponding native threshold or k value when useful.

The adjacency matrix uses probe order as node order.

## GraphFiltration

```python
GraphFiltration(
    snapshots: list[GraphSnapshot],
    relational_matrix: RelationalMatrix,
    name: str,
    monotone: bool = True,
)
```

Convenience properties:

```python
filtration.parameters
filtration.edge_densities
```

A monotone flag indicates the intended graph-growth property. It should not be interpreted as a formal proof that all arbitrary custom filtrations satisfy nestedness.

## AnalysisResult

```python
AnalysisResult(
    name: str,
    observables: dict,
    records: list[dict],
    metadata: dict,
)
```

The payload shape is analysis dependent.

Use `observables` for named aggregate or trajectory objects and `records` for control-step records.

Examples:

`components.observables["component_count"]` is a list.

`spectra.observables["trajectory"]` is a `SpectralTrajectory`.

`factor_alignment.records` contains factor-specific NMI/ARI dictionaries at each control step.

## Spectral objects

### SpectralSnapshot

```text
parameter
eigenvalues
eigenvectors or None
operator
observables
```

### SpectralTrajectory

```text
snapshots
operator
parameters
```

The in-memory representation may contain eigenvectors.

## LayerResult

```python
LayerResult(
    site: str,
    metric: str,
    filtration: str,
    analyses: dict[str, AnalysisResult],
    relational_metadata: dict = {},
    artifacts: LayerArtifacts | None = None,
)
```

One `LayerResult` represents one captured population representation after all configured analyses.

`relational_metadata` currently includes metric diagnostics, representation shape, and reducer name.

## ExperimentResult

```python
ExperimentResult(
    layers: dict[str, LayerResult],
    provenance: dict,
    metadata: dict = {},
    artifacts: ExperimentArtifacts | None = None,
)
```

`layers` is keyed by captured site.

`summary()` returns a compact mapping of site → metric, filtration, and analysis names.

## Provenance

The experiment currently records runtime/model/configuration provenance produced by `collect_provenance`.

Treat provenance as part of the experimental method. A scientifically comparable result requires more than an array of observables; it requires knowing which model, probe population, representation reducer, metric, filtration, sites, and analyses produced those observables.


## Runtime visualization artifacts

The current in-memory result model retains non-persistent runtime objects so visualization can operate on the exact measured objects rather than reconstructing them from summaries.

`LayerResult.artifacts` is a `LayerArtifacts` object containing:

```text
representation       reduced Representation for the site
relational_matrix    exact RelationalMatrix used by the filtration
filtration           exact GraphFiltration and GraphSnapshot objects
```

`ExperimentResult.artifacts` is an `ExperimentArtifacts` object containing the original `ProbePopulation`.

These objects support factor-ordered relational matrices, graph snapshots, component lineage views, dendrograms, and probe-aware diagnostics. They are runtime references to objects already produced during execution; retaining them does not imply a second extraction or analysis pass.

They are deliberately omitted by `ExperimentResult.save()`. Therefore a loaded or externally reconstructed `result.json` does not contain enough information to regenerate every runtime visualization. The saved JSON remains a report-like persistence surface; the heavy runtime analysis artifacts remain in memory unless a future explicit artifact-persistence format is introduced.

## Current persistence format

Call:

```python
result.save("results/run_01")
```

The current implementation writes:

```text
results/run_01/
└── result.json
```

Serialization recursively converts:

- NumPy arrays → lists;
- NumPy integer/float scalars → Python scalars;
- dataclass-like objects → dictionaries;
- tuples/lists → JSON arrays;
- dictionaries → JSON objects.

The serializer deliberately omits fields named `eigenvectors`.

This means the saved JSON is a human-inspectable result representation, not a lossless round-trip serialization of every in-memory object.

## No current reconstruction API

The current alpha release does not implement:

```python
ExperimentResult.load(...)
```

and does not write NPZ sidecar files.

An external reader should therefore treat `result.json` as a versioned report-like serialization rather than assume that loading it recreates the exact original Python object graph.

## Example serialized shape

A simplified saved result resembles:

```json
{
  "provenance": {
    "model": "Sequential",
    "metric": "cosine",
    "filtration": "edge_density"
  },
  "metadata": {
    "probe_population": "demo",
    "probe_count": 32
  },
  "layers": {
    "0": {
      "site": "0",
      "metric": "cosine",
      "filtration": "edge_density",
      "analyses": {
        "components": {
          "name": "components",
          "observables": {
            "component_count": [32, 20, 8, 2, 1]
          },
          "records": [],
          "metadata": {}
        }
      },
      "relational_metadata": {}
    }
  }
}
```

Actual output contains the complete configured records and provenance, so files can be substantially larger.

## Schema and compatibility policy

The package is currently `1.0.0a1`. The serialized JSON does not yet carry a dedicated persisted schema-version field independent of package provenance.

Until a stable persistence version is introduced:

- store the package version with archived experiment results;
- do not assume future releases will reconstruct current JSON automatically;
- use saved JSON for audit, inspection, and external analysis with explicit version handling;
- preserve the original experiment configuration when reproducibility matters.

A future lossless persistence layer should introduce an explicit schema version and migration policy rather than silently changing current JSON meaning.
