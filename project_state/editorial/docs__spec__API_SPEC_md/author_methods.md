# Research methods author writing training materials for research practitioners draft — `docs/spec/API_SPEC.md`

Prioritize prerequisite order, experimental decisions, examples, transfer tasks, confounds, and explicit guidance for designing a defensible study.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## Top-level exports

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: The package exports:

## `Experiment`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Run:

## `model`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Expected to be a PyTorch `nn.Module`. Eigenflow relies on `named_modules()`, forward hooks, `.eval()`, `.train()`, and ordinary PyTorch forward execution.

## `probes`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: A `ProbePopulation`.

## `metric`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Either: - a metric keyword; - a `Metric` instance; - an object exposing `.pairwise(...)`. Supported keywords:

## `filtration`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Either a `Filtration` instance or supported keyword: `"epsilon"` is represented by the `EpsilonFiltration` class but is not currently registered as a string alias in `resolve_filtration`.

## `analyses`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: A list containing analysis keywords or `Analysis` instances. Supported keywords: Keywords instantiate default configurations. Use explicit analysis objects for non-default parameters.

## `device`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Device passed to the `PyTorchExtractor`. If omitted, the extractor uses the device of the first model parameter when available, otherwise CPU.

## `collate_fn`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Optional callable used to combine non-tensor probe inputs into a model batch. If probe inputs are tensors and no `collate_fn` is supplied, Eigenflow uses `torch.stack`.

## Probe population

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## `ProbeSample`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## `ProbePopulation`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Probe IDs must be unique and a population may not be empty.

## `ProbePopulation.from_items`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: If IDs are omitted, stable IDs of the form `probe_000000` are generated for the constructed population.

## Properties

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## `subset`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## `balance`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: If `n_per_group` is omitted, the smallest observed group size is used.

## `stratify`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Returns a dictionary from factor-value tuples to sample indices.

## `factorial`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: This samples existing cells. It does not synthesize missing factor combinations.

## `match`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Returns matched treatment/control samples for available keys.

## Extraction

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## `ExtractionConfig`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: `retain_raw` is present in the configuration but the current extractor does not persist raw activation tensors in the returned `Representation` objects. Do not rely on this field as an implemented raw-activation cache.

## Site selection

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: `sites="all"` with `leaf_modules_only=True` selects named leaf modules. Explicit site selection: Explicit names are validated against `model.named_modules()`.

## `PyTorchExtractor`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: List all named module sites: Extract: During extraction the model is placed in evaluation mode and the forward pass runs under `torch.no_grad()`. The previous training/eval state is restored afterward. For tuple/list or dict module outputs, the extractor captures the first tensor value it finds. Modules producing no tensor output are skipped.

## Reducers

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Import from `eigenflow.extraction`. Accepted reducer keywords: `SelectToken` must currently be passed as an object: A callable can also be used. It receives the captured tensor and must return a tensor whose first dimension is batch.

## Representations

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: A representation contains the reduced population matrix, site name, probe IDs, raw output shape metadata, and reducer name. The downstream metric layer expects rows to correspond exactly to probe order.

## Metrics

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## Metric protocol

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Subclass `Metric` and implement: The base `.pairwise(...)` method constructs a `RelationalMatrix`.

## Built-ins

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## Metric pipeline

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Transforms are applied to the representation matrix before the final metric.

## Metric diagnostics

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Experiment execution stores metric diagnostics in each `LayerResult.relational_metadata`.

## Filtrations

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## Threshold

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: For similarities, larger relations enter first as threshold decreases. For distances, orientation is reversed as necessary.

## Edge density

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: The control parameter is requested edge density. Ties may cause multiple pairwise values to share the same native threshold, but the implementation selects a fixed number of ranked pairs.

## Epsilon

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: This currently inherits threshold behavior and relies on a distance metric for epsilon-style semantics.

## k-nearest neighbors

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: The ordinary kNN graph symmetrizes directed neighbor choices by logical OR. Mutual kNN requires reciprocal neighbor selection.

## Weighted threshold

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Retained similarity values become edge weights. For distance matrices, retained distances are converted to positive affinities relative to the maximum retained distance at that snapshot.

## Graph operators

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Resolve by string: Supported names: Operators are primarily configured through explicit spectral/eigenspace analysis objects.

## Analyses

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## `ComponentsAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Records component count, largest-component size, edge density, parameter, and node labels at every snapshot.

## `PCSCSAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Extends components with:

## `PercolationAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Observables:

## `SpectralAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Returns a `SpectralTrajectory`.

## `EigenspaceAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Records overlap matrices and principal angles between consecutive low-dimensional eigenspaces.

## `BridgesAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Records bridge edges per snapshot.

## `KCoreAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Records surviving node indices and population fraction.

## `CommunitiesAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Records community partitions returned by the graph community routine.

## `FactorAlignmentAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: If factors are omitted, all metadata keys observed in the probe population are considered. Complete factors are compared with component labels using NMI and ARI.

## `ClassStructureAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Reports internal and external edge density per factor level.

## `TransitionsAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Produces component-derivative, susceptibility-peak, and second-component-peak candidates and a simple consensus.

## `LocalizationAnalysis`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Available under keyword `"localization"`. Consult the implementation when using this experimental analysis; its API is not yet as stable as the major analysis classes above.

## Results

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## `ExperimentResult`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: `result[site]` is equivalent to `result.layers[site]`.

## `LayerResult`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## `AnalysisResult`

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## Persistence

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: The current implementation creates the directory and writes: NumPy arrays are converted to lists, NumPy scalar values are converted to Python scalars, and dataclass-like results are recursively converted. Spectral eigenvectors are deliberately omitted from JSON serialization. There is **no current `ExperimentResult.load()` API** and no NPZ sidecar written by `save()`.

## Visualization

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: All return a Matplotlib `Figure`.

## Presets

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: 

## PCSCS

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Uses flattening, cosine similarity, threshold filtration, `pcscs`, and `spectra`.

## Full

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: Defaults analyses to components, percolation, spectra, eigenspaces, factor alignment, class structure, bridges, k-core, and communities.

## Current non-features

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: The v1 alpha interface does not currently provide: - an `operators=` parameter on `Experiment`; - a `cache=` parameter or persistent content-addressed execution cache; - `ExperimentResult.load()`; - raw-activation persistence despite the existing `retain_raw` configuration field; - automatic semantic selection of "meaningful" layers for arbitrary architectures. These are intentionally stated here so reference documentation does not promise behavior absent from the current implementation.
