# Eigenflow documentation

Eigenflow is easiest to learn as an experimental method first and a Python API second. The documentation therefore follows the dependencies of the reasoning task rather than the source-code tree.

A first-time reader should leave the instructional path able to decide whether Eigenflow is appropriate for a feature-interpretation question, design a probe population that distinguishes competing hypotheses, choose a representation reducer, metric, filtration, and analysis because they answer the intended question, read the resulting structural observables across network depth and control scale, and make a bounded inference about latent feature organization.

## Choose your path

If you are **designing an interpretability experiment**, read [The experimental model](concepts/experimental_model.md) first. It explains the inverse problem, probe design, confounding, prediction of structural outcomes, and robustness.

If you are **interpreting graph-growth behavior**, continue with [Percolation-style analysis](concepts/percolation.md).

If you are **using eigenvalues, eigenvectors, or graph operators**, read [Spectral analysis](concepts/spectral_analysis.md) before interpreting spectral output.

If you want a **complete image-model walkthrough**, use the [VGG16 probe experiment](guides/vgg16_probe_experiment.md).

If you want to understand the **complete visualization surface**, including PCSCS-compatible component trajectories/dendrograms and generalized Eigenflow spectral, factor, robustness, and layer×control views, read the [Visualization guide](guides/visualization_guide.md).

If you already have results and need to decide what they mean, use [Interpreting results](guides/interpreting_results.md).

If you are an **existing PCSCS user**, begin with [`examples/pcscs_compatibility.py`](../examples/pcscs_compatibility.py). PCSCS is represented in Eigenflow as a cosine-similarity, threshold-filtration, component-sifting preset.

If you are extending or integrating the package, use the reference specifications after you understand the conceptual model:

- [API specification](spec/API_SPEC.md)
- [Data-model specification](spec/DATA_MODEL_SPEC.md)
- [Execution specification](spec/EXECUTION_SPEC.md)

## Conceptual learning path

The recommended sequence is:

1. **Frame the interpretability problem.** Decide whether the question is about population-level relational organization and whether post hoc structural evidence is relevant.
2. **Establish the experimental object.** Understand the probe population, layerwise representation population, pairwise geometry, graph filtration, and structural observable.
3. **Design identifying probes.** Construct contrasts that make competing hypotheses predict different observable patterns.
4. **Choose the measurement geometry.** Select representation sites, reducers, metrics, filtrations, and control coordinates deliberately.
5. **Read structural observables.** Learn what components, percolation quantities, graph spectra, eigenspaces, cores, communities, bridges, and factor-alignment statistics actually measure.
6. **Interpret across layer and scale.** Read quantities as fields \(Q(\ell,p)\), not as isolated numbers chosen after inspection.
7. **Apply inferential discipline.** Separate direct observation, candidate interpretation, alternatives, robustness evidence, and unsupported claims.
8. **Demonstrate applied competence.** Design, run, compare, interpret, and report a complete experiment.

The ordering matters. A spectral gap cannot tell you what feature a network has learned if the probe population does not distinguish that feature from a confound. Likewise, an excellent probe design does not justify a claim if the chosen metric or reducer measures a different relation than the one implied by the claim.

## Task-based navigation

### I need to build a probe population

Read [The experimental model](concepts/experimental_model.md). Then use the `ProbePopulation` construction, balancing, factorial, stratification, and matching examples in the [API specification](spec/API_SPEC.md).

### I need to choose cosine, Euclidean, correlation, or a kernel

Read the measurement-design section of [The experimental model](concepts/experimental_model.md) and the metric reference in the [API specification](spec/API_SPEC.md). A metric is part of the experiment's measurement model, not a cosmetic option.

### I need to compare different metrics

Prefer a common graph-scale coordinate such as edge density when the comparison requires matched sparsity. See [Percolation-style analysis](concepts/percolation.md) for the distinction between native thresholds and edge density.

### I need to know what a susceptibility peak or giant-component curve means

Read [Percolation-style analysis](concepts/percolation.md), then [Interpreting results](guides/interpreting_results.md).

### I need to know what a spectral gap, algebraic connectivity, or IPR means

Read [Spectral analysis](concepts/spectral_analysis.md), then [Interpreting results](guides/interpreting_results.md).

### I need to compare early and late network layers

Read the layer-by-control sections in [The experimental model](concepts/experimental_model.md) and [Interpreting results](guides/interpreting_results.md). The primary object is the changing relational organization of the same probe population across internal representation sites.

### I need exact syntax

Use the [API specification](spec/API_SPEC.md). The conceptual documents explain why a choice is made; the API spec explains the exact current interface.

### I need to choose or interpret a visualization

Use the [Visualization guide](guides/visualization_guide.md). It organizes views by the experimental question they answer and distinguishes primary evidential views from diagnostics and summary/report dashboards. For PCSCS migration, see the [PCSCS visualization parity map](PCSCS_VISUALIZATION_PARITY.md).

### I need to understand saved output

Use the [Data-model specification](spec/DATA_MODEL_SPEC.md). It distinguishes the in-memory object graph from the current JSON persistence format.

## Reference versus instruction

The reference specifications are deliberately not the entry point for first-time users. They are exact descriptions of the current software interface and data structures. The conceptual and guide documents establish the reasoning required to use those interfaces well.

The central interpretive rule throughout the documentation is:

> Eigenflow measures structural consequences of learned representations under a defined probe design and measurement configuration. Human interpretation reasons from those observations toward latent-feature hypotheses; the software does not make that semantic inference automatically.
