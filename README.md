# Eigenflow

Eigenflow is a PyTorch-first toolkit for **controlled post hoc experiments on the relational organization of learned representations**.

The central question is not “what does this neuron mean?” It is:

> Given a deliberately constructed population of probes, how does the network organize the relationships among those probes as computation proceeds, and what does that organization provide evidence about?

Eigenflow is designed for questions such as:

- When does a class or semantic distinction become structurally coherent across network depth?
- Does a representation organize probes more strongly by object identity or by background?
- Do subclasses remain distinct over a meaningful range of relational scale before merging?
- Which probes bridge otherwise separated groups?
- Does an apparent grouping survive a change of similarity metric or representation reducer?
- How do graph spectra and percolation-style observables change as the same probe population passes through the network?

Eigenflow does **not** automatically assign semantics to neurons, prove causal mechanisms, or turn a clustering pattern into a semantic explanation. Its role is narrower and more experimentally useful: it measures population-level structure so that a well-designed probe experiment can provide evidence for or against hypotheses about latent feature organization.

## The experimental object

Start with a probe population

\[
\mathcal P=\{x_1,\ldots,x_N\}.
\]

A probe population is not merely a convenient batch of examples. It is an experimental instrument. Its composition and metadata determine which interpretations are identifiable.

When the probes pass through a PyTorch model, Eigenflow captures the population at internal representation sites. At site \(\ell\), each probe has a representation \(z_i^{(\ell)}\), giving a population-level representation matrix

\[
Z^{(\ell)}=
\begin{bmatrix}
z_1^{(\ell)}\\
\vdots\\
z_N^{(\ell)}
\end{bmatrix}.
\]

A chosen metric produces pairwise relations among the probes,

\[
S_{ij}^{(\ell)}
=
m\!\left(z_i^{(\ell)},z_j^{(\ell)}\right).
\]

A filtration varies a control parameter \(p\) and converts that relational geometry into a family of graphs,

\[
G_{\ell,p}.
\]

Structural analyses then produce observables

\[
Q(\ell,p).
\]

The primary object is therefore the **relational organization of the whole probe population across network depth and control scale**.

```text
controlled probe population
        ↓
PyTorch representations at internal sites
        ↓
one vector per probe at each site
        ↓
pairwise similarity / distance / affinity
        ↓
graph filtration across a control parameter
        ↓
components / percolation / spectra / factor alignment / transitions
        ↓
bounded human inference about latent feature organization
```

PyTorch performs the model-specific forward computation. Eigenflow uses the standard `nn.Module` interface and forward hooks to capture intermediate tensor outputs. Once those population representations have been extracted, downstream analysis is architecture-independent.

## When Eigenflow is indicated

Eigenflow is most useful when you can construct probes for which competing explanations of the representation predict different relational outcomes.

Suppose you want to know whether an image model is organizing wolves and huskies by animal morphology or by snowy backgrounds. A weak probe set might contain wolves only in snow and huskies only on grass. In that population, class and background are confounded; no graph or spectrum can tell you which factor explains the separation.

A stronger probe design crosses the factors:

| class | background |
|---|---|
| wolf | snow |
| wolf | grass |
| husky | snow |
| husky | grass |

If same-class probes become structurally coherent across backgrounds, while same-background probes do not show the same persistence, that pattern can provide evidence for class-related organization. If the opposite occurs, it supports a different hypothesis.

The important point is methodological:

> Eigenflow can measure the structure present in a probe population, but sophisticated analysis cannot repair a probe design that fails to distinguish the hypotheses of interest.

Eigenflow is therefore well suited to relational questions about coherence, separation, hierarchy, invariance, entanglement, bridge cases, and change across depth. It is not by itself a substitute for causal intervention, single-prediction attribution, neuron-level semantic localization, or input-space feature visualization.

## Install

From a clone of the repository:

```bash
python -m pip install -e .
```

For development:

```bash
python -m pip install -e ".[dev]"
pytest
```

## Quick start: one complete experiment

The following example is intentionally small. Its purpose is to show the complete computational object before introducing more elaborate probe designs.

```python
import torch
import eigenflow as ef

torch.manual_seed(7)

model = torch.nn.Sequential(
    torch.nn.Linear(4, 8),
    torch.nn.ReLU(),
    torch.nn.Linear(8, 2),
)

inputs = [torch.randn(4) for _ in range(32)]
metadata = [
    {"class": "A" if i < 16 else "B"}
    for i in range(32)
]

probes = ef.ProbePopulation.from_items(
    inputs,
    metadata=metadata,
    name="demo",
)

experiment = ef.Experiment(
    model=model,
    probes=probes,
    metric=ef.metrics.CosineSimilarity(),
    filtration=ef.filtrations.EdgeDensityFiltration(
        start=0.0,
        stop=0.5,
        steps=40,
    ),
    analyses=[
        "components",
        "percolation",
        "spectra",
        "factor_alignment",
    ],
)

result = experiment.run()
print(result.summary())
```

The default extractor captures **leaf PyTorch modules that emit tensors**. The default reducer is `flatten`, which turns each probe activation into one feature vector.

For an arbitrary model, inspect available module names with:

```python
extractor = ef.PyTorchExtractor(model)
print(extractor.available_sites())
```

Then choose explicit sites when the experiment calls for them:

```python
extraction = ef.ExtractionConfig(
    sites=["0", "1", "2"],
    reducer="flatten",
    batch_size=32,
)

experiment = ef.Experiment(
    model=model,
    probes=probes,
    extraction=extraction,
    metric="cosine",
    filtration="edge_density",
)
```

“Site” means an internal module output chosen for representation capture. In simple models this often corresponds naturally to a layer. In modern architectures, a useful site may instead be an attention block, residual output, normalization module, or other `nn.Module`.

## How to read the first outputs

`ExperimentResult.layers` contains one `LayerResult` for each captured site.

```python
for site, layer in result.layers.items():
    print(site)
    print("metric:", layer.metric)
    print("filtration:", layer.filtration)
    print("analyses:", layer.analyses.keys())
```

Select one site:

```python
site = next(iter(result.layers))
layer = result.layers[site]
```

Connected-component analysis records how fragmented the population is over the control sweep:

```python
components = layer.analyses["components"]

print(components.observables["component_count"])
print(components.records[0])
```

Percolation analysis records macroscopic and mesoscale connectivity:

```python
percolation = layer.analyses["percolation"]

print(percolation.observables["giant_component_fraction"])
print(percolation.observables["second_component_fraction"])
print(percolation.observables["susceptibility"])
print(percolation.observables["susceptibility_peak_parameter"])
```

Spectral analysis returns a trajectory of spectra across the filtration:

```python
spectral = layer.analyses["spectra"]
trajectory = spectral.observables["trajectory"]

for snapshot in trajectory.snapshots:
    print(snapshot.parameter, snapshot.eigenvalues[:5])
```

Factor alignment compares the connected-component partition with known probe metadata using normalized mutual information (NMI) and adjusted Rand index (ARI):

```python
alignment = layer.analyses["factor_alignment"]

for row in alignment.records[:3]:
    print(row)
```

These outputs answer different structural questions. They should not be collapsed into a single generic “interpretability score.”

## How to interpret a result

A useful first interpretation has four parts.

**1. Observation — what was directly measured?**

> At a later representation site, the probe population remained separated into two large components over a wider edge-density interval than at an earlier site, and the component labels had higher NMI with the controlled class factor.

**2. Candidate inference — what hypothesis does that support under the probe design?**

> Under this probe design and measurement geometry, the later representation provides stronger evidence of relational organization by class.

**3. Alternative explanation — what else could produce the pattern?**

> The effect may depend on the chosen representation reducer, cosine geometry, the sampled probes, or another uncontrolled feature correlated with class.

**4. Claim boundary — what was not established?**

> The experiment does not show that a unique internal dimension encodes class, that class structure is causally necessary for the model's prediction, or that the same result would hold under arbitrary probes and metrics.

This distinction between observation and interpretation is part of the method, not a disclaimer added after the analysis.

## What the experimental choices mean

### Probe population

`ProbePopulation` preserves stable sample IDs and metadata and provides helpers for balancing, stratification, factorial selection, and matched contrasts.

```python
probes = ef.ProbePopulation.from_items(
    images,
    ids=image_ids,
    metadata=[
        {"class": cls, "background": bg}
        for cls, bg in conditions
    ],
)

balanced = probes.balance("class")

factorial = probes.factorial(
    ["class", "background"],
    n_per_cell=20,
)

matched = probes.match(
    treatment={"background": "snow"},
    control={"background": "grass"},
    on=["class"],
)
```

These helpers make designs easier to construct. They do not decide whether a particular design identifies the scientific question.

### Representation sites and reducers

A captured module may emit a tensor such as

\[
N\times C\times H\times W
\]

for a convolutional representation or

\[
N\times T\times d
\]

for a transformer representation.

A reducer converts each probe activation into one vector before pairwise geometry is computed.

`flatten` preserves all activation values but removes the explicit tensor structure. Pooling or token-selection reducers answer different measurement questions. Reducer choice therefore belongs in the experiment specification.

### Metrics

A metric converts a population representation into an \(N\times N\) relational matrix.

Eigenflow includes cosine similarity, Euclidean and squared Euclidean distance, Manhattan distance, correlation distance, dot-product similarity, Mahalanobis distance, RBF kernels, polynomial kernels, metric pipelines, and callable custom metrics.

Different metrics expose different geometries. If a substantive result exists only under one convenient metric, that dependence is part of the result.

### Filtrations and control scale

A filtration varies a graph-construction parameter rather than committing the analysis to one arbitrary graph.

Eigenflow includes similarity/distance thresholding, edge-density filtration, k-nearest-neighbor and mutual-kNN filtration, and weighted filtration tools.

For cross-metric comparison, edge density is useful because

\[
\rho
=
\frac{|E|}{\binom N2}
\]

places graphs on a common retained-edge scale. Matching edge density does not make different metrics equivalent; it makes graph sparsity comparable.

### Structural analyses

Built-in analyses include:

- `components`
- `pcscs`
- `percolation`
- `spectra`
- `eigenspaces`
- `bridges`
- `kcore`
- `communities`
- `factor_alignment`
- `class_structure`
- `transitions`

Component structure describes fragmentation and merger. Percolation-style quantities describe graph growth from local to macroscopic connectivity. Spectral analyses describe operator-level global organization. Eigenspace analyses track changes in structural modes. Bridge and core analyses identify pivotal and robustly connected probes. Factor analyses compare emergent structure with variables encoded in probe metadata.

A strong interpretation often comes from **convergent evidence across observables with different failure modes**, not from choosing one statistic and calling it the explanation.

## Layer × control scale

The central comparative object is often

\[
Q(\ell,p),
\]

where \(\ell\) indexes network depth and \(p\) indexes relational scale.

This supports questions such as:

- Does factor-aligned structure occupy a wider control interval at later sites?
- Does class coherence move toward stricter similarity as depth increases?
- Does a spectral gap emerge at the same site where components become label-aligned?
- Does a nuisance factor dominate early organization and then disappear?
- Are important structural changes distributed gradually or concentrated at particular representation sites?

Words such as “emerges” or “transition” should refer to defined observable behavior. They do not, by themselves, establish a thermodynamic phase transition or a unique semantic mechanism.

## Visualization

Eigenflow includes basic plotting utilities:

```python
from eigenflow.visualization import (
    observable_curve,
    layer_control_heatmap,
    eigenflow_plot,
)

fig = observable_curve(
    layer,
    analysis="percolation",
    observable="giant_component_fraction",
)

fig = layer_control_heatmap(
    result,
    analysis="components",
    observable="component_count",
)

fig = eigenflow_plot(layer)
```

The spectral plot is literally an eigenvalue flow across the control parameter at one representation site. Layer-control heatmaps show how an observable changes across both network depth and filtration scale.

## PCSCS

PCSCS is a canonical special case within Eigenflow.

```python
result = ef.presets.pcscs(model, probes)
```

The preset configures flattened activations, cosine similarity, threshold filtration, PCSCS-style connected-component sifting, and spectral diagnostics across captured representation sites.

Eigenflow generalizes the experimental framework by allowing the metric, filtration, graph operator, and structural analyses to vary while retaining the same population-level logic.

## Persistence and provenance

Save a result with:

```python
result.save("results/my_experiment")
```

The current implementation writes a JSON representation of the experiment result and provenance. The model, probe design, preprocessing, selected sites, reducer, metric, filtration, and analysis configuration should be treated as part of the reported experimental method.

For exact persistence guarantees, consult the data-model specification for the installed version.

## What Eigenflow can and cannot establish

Eigenflow can provide evidence that, for a defined probe population and measurement configuration, a network representation exhibits particular relational organization.

It can support statements such as:

> Class-related organization becomes more persistent across relational scale at later representation sites.

or:

> A small set of ambiguous probes repeatedly bridges two otherwise distinct groups.

or:

> A spectral mode aligned with background dominates early layers but weakens relative to class alignment later.

Those statements remain conditional on the experiment.

Eigenflow alone does not establish:

- that a semantic concept is localized to a particular neuron or coordinate;
- that a measured feature is causally necessary or sufficient for a prediction;
- that a structural transition is a true statistical-physics critical point;
- that one metric or reducer gives the uniquely correct geometry;
- that an uncontrolled correlation in the probe population has a semantic interpretation.

The objective is not automatic explanation. It is **better experimental evidence for human interpretation**.

## Where to go next

If you are designing a study, start with [The experimental model](docs/concepts/experimental_model.md). It develops the inverse-problem logic, probe construction, competing hypotheses, confounds, and robustness planning.

Use [Percolation-style analysis](docs/concepts/percolation.md) before interpreting giant-component growth, susceptibility, component-size distributions, or transition-like behavior.

Use [Spectral analysis](docs/concepts/spectral_analysis.md) before interpreting eigenvalues, spectral gaps, localization, or eigenspace trajectories.

Use the [VGG16 probe experiment](docs/guides/vgg16_probe_experiment.md) for a complete image-model workflow from probe construction through interpretation.

Use [Interpreting results](docs/guides/interpreting_results.md) after running an experiment to turn multiple outputs into a bounded scientific conclusion.

Use the [API](docs/spec/API_SPEC.md), [data-model](docs/spec/DATA_MODEL_SPEC.md), and [execution](docs/spec/EXECUTION_SPEC.md) specifications as technical reference material rather than as the primary instructional path.

Existing PCSCS users can begin with [`examples/pcscs_compatibility.py`](examples/pcscs_compatibility.py) and then expand the preset into explicit Eigenflow configuration.
