# Draft B — Academic author for a computational interpretability journal

# Eigenflow: controlled relational experiments on learned representations

Eigenflow is a framework for post hoc neural-network interpretability in which a deliberately designed population of probes is propagated through a trained model and examined as a sequence of relational systems.

The method is motivated by an inverse problem. The latent features that organize an internal representation are not directly observed. What is observed is the representation produced for each probe. Eigenflow therefore constructs measurable structural consequences of those representations and uses controlled probe design to make alternative hypotheses about latent organization predict different outcomes.

For a probe population \(\mathcal P=\{x_i\}_{i=1}^N\), let \(z_i^{(\ell)}\) denote the representation of probe \(i\) at internal site \(\ell\). A metric \(m\) induces a relational matrix

\[
S_{ij}^{(\ell)} = m(z_i^{(\ell)},z_j^{(\ell)}).
\]

A filtration indexed by control parameter \(p\) induces a graph family

\[
G_{\ell,p}.
\]

Structural analyses produce observables

\[
Q(\ell,p),
\]

including component structure, percolation-style quantities, graph spectra, eigenspace behavior, core structure, bridge relations, and agreement with controlled metadata factors.

The empirical object is therefore not a single embedding or a single thresholded graph. It is the change in relational organization of the same probe population across network depth and structural scale.

## What claim can the method support?

The strongest intended use is a controlled contrast.

Suppose a probe population crosses object identity with background. One hypothesis predicts that a late representation will be organized primarily by object identity; another predicts that background remains dominant. If the experiment is balanced so that the factors are distinguishable, then the relative persistence, coherence, mixing, component alignment, or spectral alignment of those factors becomes evidence relevant to the competing hypotheses.

The structural observable is not itself the latent feature. It is evidence about the feature organization that could have produced the observed geometry.

This is the interpretive chain:

\[
\text{latent feature organization}
\rightarrow
\text{representation geometry}
\rightarrow
\text{measured relational structure}.
\]

The experimenter reasons backward through this chain under an explicit probe design.

## Scope

Eigenflow is appropriate when the inferential question can be represented through relations among a population of inputs. It is particularly suited to questions about emergence, separation, hierarchy, invariance, entanglement, bridge cases, and scale-dependent organization.

It is not, by itself, a causal intervention method. It does not identify a semantic concept with a single neuron or dimension. It does not establish that a measured structural distinction is necessary or sufficient for a model prediction.

## Computation

PyTorch performs model execution. Eigenflow registers forward hooks on selected `nn.Module` objects, captures their outputs for the full probe population, reduces each probe activation to a vector, and carries out all subsequent analysis independently of model architecture.

The user supplies:

1. a PyTorch model;
2. a compatible probe population;
3. optional metadata defining experimental factors;
4. extraction choices;
5. a metric;
6. a filtration;
7. requested analyses.

A minimal execution is:

```python
import torch
import eigenflow as ef

model = ...
probes = ef.ProbePopulation.from_items(
    inputs,
    metadata=metadata,
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

## Why the control sweep matters

A single graph requires an arbitrary scale choice. A filtration asks how the relational organization changes as that scale is varied.

At strict connectivity, probes may be isolated or form small local groups. As the control parameter changes, those groups cohere, persist, merge, or become globally connected. Different aspects of this trajectory expose different properties of the representation.

The same control sweep can be repeated at multiple network sites, yielding a field \(Q(\ell,p)\). This permits questions about where a structural distinction appears, whether it strengthens with depth, and whether its characteristic scale shifts through the model.

## Metrics and comparability

Eigenflow intentionally separates the relational metric from the filtration.

This matters because an apparent structure may depend on the geometry chosen to expose it. A phenomenon that persists under reasonable alternative metrics provides stronger evidence than one that occurs only under a single arbitrary measurement.

For cross-metric comparison, edge density can be used as a canonical control coordinate:

\[
\rho = \frac{|E|}{\binom N2}.
\]

This does not make different metrics equivalent. It merely compares graph states at the same proportion of retained relations.

## Structural observables

Connected components describe fragmentation and merging. Percolation-style observables characterize global and mesoscale coalescence. Spectral analyses characterize operator-level organization, including connectivity, gaps, effective dimensionality, and eigenvector localization. Factor-alignment analyses compare emergent graph organization with known probe annotations.

No single observable is privileged as a universal "critical point." Agreement among observables is convergent evidence; disagreement is diagnostically meaningful.

## Reading results

A useful interpretation should separate four statements.

**Observation.** What did the computed object actually do?

**Candidate inference.** What latent organizational hypothesis is supported by that observation under the probe design?

**Alternative explanation.** What other design or measurement choice could produce the same result?

**Unsupported claim.** What stronger conclusion is not established?

For example, if class-conditioned structure becomes coherent earlier and remains distinct longer at late sites than at early sites, this is evidence that class-related relational organization has strengthened across depth. It does not establish a unique class coordinate or a causal mechanism of prediction.

## PCSCS

PCSCS is a canonical special case of the Eigenflow framework: cosine similarity, threshold filtration, and connected-component sifting over captured representation populations. Eigenflow retains this workflow while generalizing the metric, graph construction, and structural analyses.

```python
result = ef.presets.pcscs(model, probes)
```

## Reproducibility

Probe identity, metadata, extraction configuration, metric, filtration, analyses, and model/runtime provenance are part of the experiment specification. Results can be serialized for inspection using `ExperimentResult.save()`.

A substantive claim should additionally report probe construction, preprocessing, model checkpoint, representation reducer, control coordinate, and robustness analyses.

## Documentation path

Readers new to the method should proceed from the experimental-model document to metric/filtration choices, then to percolation and spectral observables, and finally to the result-interpretation guide. The API and data-model specifications are references for implementation rather than substitutes for the methodological sequence.
