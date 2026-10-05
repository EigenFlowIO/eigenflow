# Academic author for a computational interpretability journal draft — `docs/index.md`

Prioritize formal definitions, conceptual precision, epistemic scope, scholarly claim discipline, and the relation between measurements and latent-feature hypotheses.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## Choose your path

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: If you are **designing an interpretability experiment**, read [The experimental model](concepts/experimental_model.md) first. It explains the inverse problem, probe design, confounding, prediction of structural outcomes, and robustness. If you are **interpreting graph-growth behavior**, continue with [Percolation-style analysis](concepts/percolation.md). If you are **using eigenvalues, eigenvectors, or graph operators**, read [Spectral analysis](concepts/spectral_analysis.md) before interpreting spectral output. If you want a **complete image-model walkthrough**, use the [VGG16 probe experiment](guides/vgg16_probe_experiment.md). If you already have results and need to decide what they mean,

## Conceptual learning path

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The recommended sequence is: 1. **Frame the interpretability problem.** Decide whether the question is about population-level relational organization and whether post hoc structural evidence is relevant. 2. **Establish the experimental object.** Understand the probe population, layerwise representation population, pairwise geometry, graph filtration, and structural observable. 3. **Design identifying probes.** Construct contrasts that make competing hypotheses predict different observable patterns. 4. **Choose the measurement geometry.** Select representation sites, reducers, metrics, filtrations, and control coordinates deliberately. 5. **Read structural observables.** Learn what components

## Task-based navigation

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: 

## I need to build a probe population

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Read [The experimental model](concepts/experimental_model.md). Then use the `ProbePopulation` construction, balancing, factorial, stratification, and matching examples in the [API specification](spec/API_SPEC.md).

## I need to choose cosine, Euclidean, correlation, or a kernel

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Read the measurement-design section of [The experimental model](concepts/experimental_model.md) and the metric reference in the [API specification](spec/API_SPEC.md). A metric is part of the experiment's measurement model, not a cosmetic option.

## I need to compare different metrics

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Prefer a common graph-scale coordinate such as edge density when the comparison requires matched sparsity. See [Percolation-style analysis](concepts/percolation.md) for the distinction between native thresholds and edge density.

## I need to know what a susceptibility peak or giant-component curve means

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Read [Percolation-style analysis](concepts/percolation.md), then [Interpreting results](guides/interpreting_results.md).

## I need to know what a spectral gap, algebraic connectivity, or IPR means

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Read [Spectral analysis](concepts/spectral_analysis.md), then [Interpreting results](guides/interpreting_results.md).

## I need to compare early and late network layers

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Read the layer-by-control sections in [The experimental model](concepts/experimental_model.md) and [Interpreting results](guides/interpreting_results.md). The primary object is the changing relational organization of the same probe population across internal representation sites.

## I need exact syntax

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Use the [API specification](spec/API_SPEC.md). The conceptual documents explain why a choice is made; the API spec explains the exact current interface.

## I need to understand saved output

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Use the [Data-model specification](spec/DATA_MODEL_SPEC.md). It distinguishes the in-memory object graph from the current JSON persistence format.

## Reference versus instruction

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The reference specifications are deliberately not the entry point for first-time users. They are exact descriptions of the current software interface and data structures. The conceptual and guide documents establish the reasoning required to use those interfaces well. The central interpretive rule throughout the documentation is: > Eigenflow measures structural consequences of learned representations under a defined probe design and measurement configuration. Human interpretation reasons from those observations toward latent-feature hypotheses; the software does not make that semantic inference automatically.
