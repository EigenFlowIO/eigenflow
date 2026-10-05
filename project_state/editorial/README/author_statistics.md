# Draft D — Computational statistics and research design perspective

# Eigenflow

Eigenflow is a post hoc interpretability package for treating a neural network as a generator of multiscale relational data.

For a fixed population of experimental probes, each internal representation site induces a sample-by-feature matrix. A chosen metric converts that matrix into a sample-by-sample relational matrix. A filtration then varies a control parameter to produce a family of graphs. Structural statistics computed over those graphs form trajectories through network depth and relational scale.

The inferential objective is not to estimate an intrinsic "interpretability score." It is to obtain structured empirical evidence that can discriminate among hypotheses about what features organize the learned representation.

## The design problem comes first

Suppose an investigator wants to know whether a model's representation is organized by object category or by image background.

The model does not expose a variable named "background dependence." The investigator must therefore design probes for which those explanations predict different relational patterns.

A crossed design is stronger than an observationally confounded sample:

\[
\{\text{class A},\text{class B}\}
\times
\{\text{background X},\text{background Y}\}.
\]

If the sample contains only class A on X and class B on Y, any later graph separation is non-identifying: both hypotheses explain it.

Eigenflow can quantify the observed organization, but it cannot repair a non-identifying probe design.

## The measurement model

At site \(\ell\), define the representation matrix

\[
Z^{(\ell)} \in \mathbb R^{N\times d_\ell}.
\]

A relational functional \(m\) produces

\[
S^{(\ell)}_{ij}=m(z_i^{(\ell)},z_j^{(\ell)}).
\]

A filtration maps \(S^{(\ell)}\) to graph states \(G_{\ell,p}\), and an observable \(Q\) gives

\[
Q(\ell,p)=Q(G_{\ell,p}).
\]

This decomposition is statistically important because each stage introduces assumptions.

The reducer determines which activation information is retained.

The metric determines the geometry.

The filtration determines how the geometry is sampled across scale.

The observable determines which structural property is summarized.

The probe population determines what semantic interpretation can be attached to the result.

A conclusion is therefore conditional on the complete measurement design, not merely on the model.

## A minimal experiment

```python
import torch
import eigenflow as ef

model = ...
probes = ef.ProbePopulation.from_items(
    probe_inputs,
    ids=probe_ids,
    metadata=probe_metadata,
)

result = ef.Experiment(
    model=model,
    probes=probes,
    metric=ef.metrics.CosineSimilarity(),
    filtration=ef.filtrations.EdgeDensityFiltration(
        start=0.0,
        stop=0.5,
        steps=100,
    ),
    analyses=[
        "components",
        "percolation",
        "spectra",
        "factor_alignment",
    ],
).run()
```

The default extractor captures leaf-module tensor outputs and uses flattened activations. Those defaults define a measurement; they should not be mistaken for universal methodological choices.

## Why a filtration is preferable to one threshold

Selecting a single threshold after looking at the result creates an obvious researcher degree of freedom. A filtration makes the behavior across a range of thresholds observable.

A persistent phenomenon across a broad region of \(p\) is qualitatively different from one occurring only at a narrow selected value.

This does not eliminate researcher choice—the metric, filtration family, parameter range, and observable remain choices—but it externalizes more of the sensitivity structure.

## Edge density and cross-metric comparison

Raw metric thresholds are often incommensurate. Cosine similarity, Euclidean distance, and an RBF kernel do not share a meaningful numerical scale.

Edge density

\[
\rho=\frac{|E|}{\binom N2}
\]

allows graph states to be compared at a common retained-relation fraction.

This is a normalization of graph sparsity, not a proof that the metrics encode the same geometry. A conclusion that is stable across metrics at matched edge densities is stronger evidence of a metric-robust relational phenomenon.

## What the observables say

Component counts summarize fragmentation.

Giant-component fraction summarizes the emergence of macroscopic connectivity.

The second-largest component can identify regimes with competing large structures.

Susceptibility emphasizes the scale of non-giant clusters.

Graph spectra summarize global operator structure. Algebraic connectivity, spectral gaps, entropy, effective rank, and localization each have different interpretations.

Factor alignment compares emergent partitions with recorded experimental variables. High NMI with class is evidence that the current graph partition agrees with class labels; it is not proof that the underlying feature geometry contains only class information.

## Layerwise interpretation

A single site provides one representation system. Comparing sites asks how that system changes through the model.

If an observable has trajectory \(Q(\ell,p)\), then useful questions include:

- Does the factor-aligned regime widen with depth?
- Does a transition move to stricter relational scale?
- Does a spectral mode become less localized?
- Does within-class structure strengthen while cross-class connectivity weakens?
- Are the changes monotone, abrupt, or reversible across adjacent modules?

The word "emerges" should be used carefully. It may mean that the observable crosses a defined criterion at a particular layer, not that the underlying semantic feature did not exist in any form before that point.

## A disciplined inference template

A result should be written in four layers.

**Observed statistic:** state the measured graph or spectral pattern.

**Design-conditioned inference:** state the latent-feature hypothesis the pattern supports given the probe design.

**Sensitivity/alternative:** identify measurement choices or competing hypotheses that could reproduce the pattern.

**Claim boundary:** state what is not identified by the experiment.

This format makes the epistemic chain inspectable.

## Robustness

For important claims, consider at least some of:

- alternative reasonable metrics;
- alternative representation reducers;
- resampled or independently constructed probe populations;
- changed parameter grids;
- class/factor balancing;
- matched controls;
- multiple checkpoints or models;
- finite-size analyses;
- convergence of independent observables.

Convergent evidence is strongest when distinct observables with different failure modes agree on the substantive structural conclusion.

Disagreement is not necessarily a failure. It may reveal that, for example, component connectivity has changed while spectral organization remains diffuse.

## PCSCS as a special case

PCSCS corresponds to a fixed measurement configuration based on cosine similarity, threshold filtration, and component-centric sifting. Eigenflow preserves this configuration and adds the ability to test whether the observed phenomenon survives changes in measurement geometry and analysis family.

```python
result = ef.presets.pcscs(model, probes)
```

## Interpretability scope

Eigenflow is well suited to relational questions about coherence, separation, hierarchy, mixing, bridge structure, and changes across depth.

It is not sufficient by itself for causal claims about mechanisms, neuron-level semantic identity, or necessity/sufficiency of a feature for prediction.

Its strength is experimental rather than declarative: the investigator creates a probe design that makes alternatives disagree, and the package measures the resulting organization with enough multiscale structure to support or weaken those alternatives.
