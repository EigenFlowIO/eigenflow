# Development Instrumentation and Longitudinal Representation Analysis

Status: **formalized next project phase**

## Objective

Extend Eigenflow from a single-model representation experiment engine into a first-class representation observability system for architecture development, fine-tuning, checkpoint analysis, PEFT targeting, dataset diagnosis, retention/forgetting analysis, and longitudinal model-development workflows.

The current `Experiment -> ExperimentResult` path remains the atomic measurement layer. This phase adds higher-order controlled-comparison abstractions above it.

## Core model

The current package primarily supports:

`Q(layer, control)`

This phase adds first-class support for:

`Q(layer, control, time)`

and controlled variation across model, architecture, run, checkpoint, and condition.

## Governing principles

- Preserve Experiment -> ExperimentResult as the atomic measurement layer.
- Add higher-order abstractions above ExperimentResult rather than replacing the core experiment engine.
- Treat longitudinal and cross-model comparisons as controlled experiments, not arbitrary result subtraction.
- Require compatibility validation before structural comparisons are interpreted.
- Keep probe design and measurement configuration explicit, versioned, and reproducible.
- Do not collapse representation structure into a universal quality score.
- Keep behavioral performance, computational efficiency, and representation structure as distinct evidence channels.
- Documentation and implementation must evolve together and remain implementation-faithful.

## First-class concepts

### ProbeSuite

Versioned, reusable collections of probe populations for target, retention, nuisance, boundary, or other experimental roles.

### ExperimentSpec

Serializable, comparable specification of model-independent measurement configuration and probe design.

### ExperimentSeries

Ordered or indexed collection of compatible experiments/results across checkpoints, models, architectures, runs, or conditions.

### ComparisonSpec

Explicit declaration of which dimensions vary and which must remain controlled for a comparison.

### CompatibilityReport

Machine-readable validation of probe, preprocessing, site, reducer, metric, filtration, and analysis compatibility.

### StructuralDiff

Structured delta between compatible ExperimentResults, including observable-level and layer/control differences.

### LongitudinalResult

Representation of Q(layer, control, time) and associated trajectories across checkpoints/training progress.

### SiteAlignment

Explicit semantic or normalized correspondence between representation sites across architectures or checkpoints.

### BehavioralRecord

Attach externally computed behavioral metrics to structural results without making Eigenflow responsible for training/evaluation.

### DevelopmentReport

Synthesize matched behavioral, computational, and structural evidence without reducing them to a single generic score.

## Workstreams

### devws_01 — Comparison and compatibility foundation

Make controlled comparison between ExperimentResults explicit, safe, and inspectable.

### devws_02 — Longitudinal checkpoint analysis

Support Q(layer, control, time), checkpoint trajectories, pretrained baselines, and structural displacement.

### devws_03 — Probe suites and benchmark semantics

Support reusable target/retain/nuisance/boundary probe suites with versioning and reproducibility metadata.

### devws_04 — Architecture and site comparison

Support matched architecture comparisons and declared site correspondences.

### devws_05 — Post-training diagnostics

Support forgetting, retention, PEFT targeting, checkpoint selection, and dataset-diagnostic workflows.

### devws_06 — Persistence and scale

Provide storage suitable for series of results, checkpoints, arrays, and derived comparisons.

### devws_07 — Visualization and reporting

Add longitudinal surfaces, structural diffs, retention dashboards, model/run comparisons, and development reports.

### devws_08 — Documentation and instructional integration

Teach development use cases with the same instructional-planning and incremental-adjudication protocols used elsewhere.

## Non-goals

- Eigenflow will not become a neural-network training framework.
- Eigenflow will not automatically prescribe architecture edits, adapter placement, or data-removal decisions.
- Eigenflow will not define a universal representation-quality scalar.
- Eigenflow will not infer causal feature semantics from structural observables alone.
- Eigenflow will not treat unmatched model/checkpoint results as directly comparable.

## Completion criteria

- Multiple checkpoints/models can be represented and analyzed as one controlled series.
- Compatibility validation prevents or clearly flags invalid structural comparisons.
- Structural diffs and longitudinal trajectories are first-class result objects.
- Probe suites and comparison specifications are serializable and versionable.
- Cross-architecture site alignment is explicit rather than implied by raw layer index.
- Behavioral metrics can be attached and jointly reported without semantic conflation.
- Persistence supports practical multi-checkpoint studies.
- Longitudinal and comparative visualizations are implemented and tested.
- At least one architecture-comparison example and one fine-tuning/checkpoint example are fully runnable.
- All new/mutated human-facing files follow the incremental adjudication protocol.
- API, data-model, execution, conceptual, guide, example, and README documentation agree with implementation.
