# Academic author for a computational interpretability journal draft — `docs/spec/DATA_MODEL_SPEC.md`

Prioritize formal definitions, conceptual precision, epistemic scope, scholarly claim discipline, and the relation between measurements and latent-feature hypotheses.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## Object chain

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The principal objects are: The same probe ordering must remain invariant through the chain.

## Probe identity and ordering

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: A `ProbePopulation` contains ordered `ProbeSample` objects. IDs must be unique. The order of `ProbePopulation.samples` defines the row order used during extraction. That order becomes the order of: - representation rows; - relational-matrix rows and columns; - graph nodes; - component label arrays; - spectral node coordinates. Do not reorder a downstream matrix without reordering probe IDs and all dependent objects consistently.

## Representation

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: A `Representation` corresponds to one captured site. Conceptually: `D` may differ by site. Raw activation shape can be multidimensional, but the reducer returns one vector per probe.

## RepresentationCollection

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: A `RepresentationCollection` maps site names to `Representation` objects and preserves the population IDs. Different sites may have different feature dimensions but must contain the same probes in the same order.

## RelationalMatrix

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The matrix must be square. `kind` is semantically important. Threshold filtrations use it to determine whether larger or smaller raw values represent stronger relations. A relational matrix is not assumed to be a neural-network parameter object. It is a derived measurement of the population representation.

## GraphSnapshot

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: `parameter` is the filtration's exposed control coordinate. `native_parameter` records the corresponding native threshold or k value when useful. The adjacency matrix uses probe order as node order.

## GraphFiltration

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Convenience properties: A monotone flag indicates the intended graph-growth property. It should not be interpreted as a formal proof that all arbitrary custom filtrations satisfy nestedness.

## AnalysisResult

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The payload shape is analysis dependent. Use `observables` for named aggregate or trajectory objects and `records` for control-step records. Examples: `components.observables["component_count"]` is a list. `spectra.observables["trajectory"]` is a `SpectralTrajectory`. `factor_alignment.records` contains factor-specific NMI/ARI dictionaries at each control step.

## Spectral objects

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## SpectralSnapshot

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## SpectralTrajectory

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The in-memory representation may contain eigenvectors.

## LayerResult

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: One `LayerResult` represents one captured population representation after all configured analyses. `relational_metadata` currently includes metric diagnostics, representation shape, and reducer name.

## ExperimentResult

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: `layers` is keyed by captured site. `summary()` returns a compact mapping of site → metric, filtration, and analysis names.

## Provenance

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The experiment currently records runtime/model/configuration provenance produced by `collect_provenance`. Treat provenance as part of the experimental method. A scientifically comparable result requires more than an array of observables; it requires knowing which model, probe population, representation reducer, metric, filtration, sites, and analyses produced those observables.

## Current persistence format

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Call: The current implementation writes: Serialization recursively converts: - NumPy arrays → lists; - NumPy integer/float scalars → Python scalars; - dataclass-like objects → dictionaries; - tuples/lists → JSON arrays; - dictionaries → JSON objects. The serializer deliberately omits fields named `eigenvectors`. This means the saved JSON is a human-inspectable result representation, not a lossless round-trip serialization of every in-memory object.

## No current reconstruction API

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The current alpha release does not implement: and does not write NPZ sidecar files. An external reader should therefore treat `result.json` as a versioned report-like serialization rather than assume that loading it recreates the exact original Python object graph.

## Example serialized shape

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: A simplified saved result resembles: Actual output contains the complete configured records and provenance, so files can be substantially larger.

## Schema and compatibility policy

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The package is currently `1.0.0a1`. The serialized JSON does not yet carry a dedicated persisted schema-version field independent of package provenance. Until a stable persistence version is introduced: - store the package version with archived experiment results; - do not assume future releases will reconstruct current JSON automatically; - use saved JSON for audit, inspection, and external analysis with explicit version handling; - preserve the original experiment configuration when reproducibility matters. A future lossless persistence layer should introduce an explicit schema version and migration policy rather than silently changing current JSON meaning.
