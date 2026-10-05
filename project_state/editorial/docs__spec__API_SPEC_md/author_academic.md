# Academic author for a computational interpretability journal draft — `docs/spec/API_SPEC.md`

Prioritize formal definitions, conceptual precision, epistemic scope, scholarly claim discipline, and the relation between measurements and latent-feature hypotheses.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## Top-level exports

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The package exports:

## `Experiment`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Run:

## `model`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Expected to be a PyTorch `nn.Module`. Eigenflow relies on `named_modules()`, forward hooks, `.eval()`, `.train()`, and ordinary PyTorch forward execution.

## `probes`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: A `ProbePopulation`.

## `metric`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Either: - a metric keyword; - a `Metric` instance; - an object exposing `.pairwise(...)`. Supported keywords:

## `filtration`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Either a `Filtration` instance or supported keyword: `"epsilon"` is represented by the `EpsilonFiltration` class but is not currently registered as a string alias in `resolve_filtration`.

## `analyses`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: A list containing analysis keywords or `Analysis` instances. Supported keywords: Keywords instantiate default configurations. Use explicit analysis objects for non-default parameters.

## `device`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Device passed to the `PyTorchExtractor`. If omitted, the extractor uses the device of the first model parameter when available, otherwise CPU.

## `collate_fn`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Optional callable used to combine non-tensor probe inputs into a model batch. If probe inputs are tensors and no `collate_fn` is supplied, Eigenflow uses `torch.stack`.

## Probe population

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## `ProbeSample`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## `ProbePopulation`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Probe IDs must be unique and a population may not be empty.

## `ProbePopulation.from_items`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: If IDs are omitted, stable IDs of the form `probe_000000` are generated for the constructed population.

## Properties

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## `subset`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## `balance`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: If `n_per_group` is omitted, the smallest observed group size is used.

## `stratify`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Returns a dictionary from factor-value tuples to sample indices.

## `factorial`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: This samples existing cells. It does not synthesize missing factor combinations.

## `match`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Returns matched treatment/control samples for available keys.

## Extraction

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## `ExtractionConfig`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: `retain_raw` is present in the configuration but the current extractor does not persist raw activation tensors in the returned `Representation` objects. Do not rely on this field as an implemented raw-activation cache.

## Site selection

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: `sites="all"` with `leaf_modules_only=True` selects named leaf modules. Explicit site selection: Explicit names are validated against `model.named_modules()`.

## `PyTorchExtractor`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: List all named module sites: Extract: During extraction the model is placed in evaluation mode and the forward pass runs under `torch.no_grad()`. The previous training/eval state is restored afterward. For tuple/list or dict module outputs, the extractor captures the first tensor value it finds. Modules producing no tensor output are skipped.

## Reducers

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Import from `eigenflow.extraction`. Accepted reducer keywords: `SelectToken` must currently be passed as an object: A callable can also be used. It receives the captured tensor and must return a tensor whose first dimension is batch.

## Representations

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: A representation contains the reduced population matrix, site name, probe IDs, raw output shape metadata, and reducer name. The downstream metric layer expects rows to correspond exactly to probe order.

## Metrics

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## Metric protocol

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Subclass `Metric` and implement: The base `.pairwise(...)` method constructs a `RelationalMatrix`.

## Built-ins

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## Metric pipeline

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Transforms are applied to the representation matrix before the final metric.

## Metric diagnostics

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Experiment execution stores metric diagnostics in each `LayerResult.relational_metadata`.

## Filtrations

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## Threshold

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: For similarities, larger relations enter first as threshold decreases. For distances, orientation is reversed as necessary.

## Edge density

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The control parameter is requested edge density. Ties may cause multiple pairwise values to share the same native threshold, but the implementation selects a fixed number of ranked pairs.

## Epsilon

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: This currently inherits threshold behavior and relies on a distance metric for epsilon-style semantics.

## k-nearest neighbors

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The ordinary kNN graph symmetrizes directed neighbor choices by logical OR. Mutual kNN requires reciprocal neighbor selection.

## Weighted threshold

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Retained similarity values become edge weights. For distance matrices, retained distances are converted to positive affinities relative to the maximum retained distance at that snapshot.

## Graph operators

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Resolve by string: Supported names: Operators are primarily configured through explicit spectral/eigenspace analysis objects.

## Analyses

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## `ComponentsAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Records component count, largest-component size, edge density, parameter, and node labels at every snapshot.

## `PCSCSAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Extends components with:

## `PercolationAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Observables:

## `SpectralAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Returns a `SpectralTrajectory`.

## `EigenspaceAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Records overlap matrices and principal angles between consecutive low-dimensional eigenspaces.

## `BridgesAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Records bridge edges per snapshot.

## `KCoreAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Records surviving node indices and population fraction.

## `CommunitiesAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Records community partitions returned by the graph community routine.

## `FactorAlignmentAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: If factors are omitted, all metadata keys observed in the probe population are considered. Complete factors are compared with component labels using NMI and ARI.

## `ClassStructureAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Reports internal and external edge density per factor level.

## `TransitionsAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Produces component-derivative, susceptibility-peak, and second-component-peak candidates and a simple consensus.

## `LocalizationAnalysis`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Available under keyword `"localization"`. Consult the implementation when using this experimental analysis; its API is not yet as stable as the major analysis classes above.

## Results

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## `ExperimentResult`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: `result[site]` is equivalent to `result.layers[site]`.

## `LayerResult`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## `AnalysisResult`

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## Persistence

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The current implementation creates the directory and writes: NumPy arrays are converted to lists, NumPy scalar values are converted to Python scalars, and dataclass-like results are recursively converted. Spectral eigenvectors are deliberately omitted from JSON serialization. There is **no current `ExperimentResult.load()` API** and no NPZ sidecar written by `save()`.

## Visualization

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: All return a Matplotlib `Figure`.

## Presets

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## PCSCS

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Uses flattening, cosine similarity, threshold filtration, `pcscs`, and `spectra`.

## Full

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Defaults analyses to components, percolation, spectra, eigenspaces, factor alignment, class structure, bridges, k-core, and communities.

## Current non-features

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The v1 alpha interface does not currently provide: - an `operators=` parameter on `Experiment`; - a `cache=` parameter or persistent content-addressed execution cache; - `ExperimentResult.load()`; - raw-activation persistence despite the existing `retain_raw` configuration field; - automatic semantic selection of "meaningful" layers for arbitrary architectures. These are intentionally stated here so reference documentation does not promise behavior absent from the current implementation.
