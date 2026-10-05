# Draft A — Technical software developer and documentation writer

# Eigenflow

Eigenflow is a PyTorch-first toolkit for post hoc analysis of how a population of probe inputs is organized inside a neural network.

The package captures activations from internal PyTorch modules, converts each probe's activation into a vector representation, computes pairwise relations among the complete probe population, sweeps a graph-construction parameter, and evaluates structural observables at every captured representation site.

The basic computational chain is:

```text
probe population
    ↓
PyTorch activations at internal modules
    ↓
one vector per probe at each site
    ↓
pairwise similarity or distance matrix
    ↓
graph filtration over a control parameter
    ↓
components / percolation / spectra / factor alignment / transitions
```

Eigenflow analyzes representation populations rather than model architectures. PyTorch remains responsible for executing the model; Eigenflow uses standard `nn.Module` inspection and forward hooks to capture intermediate outputs.

## When to use Eigenflow

Use Eigenflow when the question can be expressed in terms of relations among deliberately chosen inputs. Examples include:

- At what network depth do examples from the same class become structurally coherent?
- Does a representation organize images more strongly by object identity or background?
- Which probes bridge otherwise distinct groups?
- Do structural transitions occur at similar control scales under cosine and Euclidean geometry?
- Does a spectral mode align with an experimental factor?
- How does the organization of the same probe population change from early to late layers?

Eigenflow is not a saliency method, feature-visualization method, causal intervention framework, or automatic semantic labeling system. It does not tell you that a neuron "means" a concept. It provides measurements of relational structure that can support bounded inferences when the probe experiment is designed to distinguish competing explanations.

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

## Quick start

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
metadata = [{"class": "A" if i < 16 else "B"} for i in range(32)]

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

With the default `ExtractionConfig`, Eigenflow selects leaf modules and captures tensor outputs. To choose explicit modules:

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
)
```

Use `PyTorchExtractor(model).available_sites()` to inspect possible module names before choosing them.

## How results are organized

`ExperimentResult.layers` is a mapping from captured module name to `LayerResult`.

```python
for site, layer in result.layers.items():
    print(site, layer.metric, layer.filtration)
    print(layer.analyses.keys())
```

For example, component counts are available as:

```python
site = next(iter(result.layers))
layer = result.layers[site]

component_result = layer.analyses["components"]
print(component_result.observables["component_count"])
```

Percolation results include giant-component fraction, second-component fraction, susceptibility, and the parameter at the susceptibility peak.

```python
p = layer.analyses["percolation"]
print(p.observables["giant_component_fraction"])
print(p.observables["susceptibility_peak_parameter"])
```

Spectral results include a `SpectralTrajectory`:

```python
spectral = layer.analyses["spectra"]
trajectory = spectral.observables["trajectory"]

for snapshot in trajectory.snapshots:
    print(snapshot.parameter, snapshot.eigenvalues[:5])
```

Factor alignment compares connected-component labels with probe metadata using NMI and ARI:

```python
alignment = layer.analyses["factor_alignment"]
print(alignment.records[0])
```

## Probe populations are experimental objects

A `ProbePopulation` stores inputs, stable IDs, and metadata.

```python
probes = ef.ProbePopulation.from_items(
    images,
    ids=image_ids,
    metadata=[
        {"class": cls, "background": bg}
        for cls, bg in labels
    ],
)
```

Probe helpers include balancing, stratification, factorial selection, and matched contrasts.

```python
balanced = probes.balance("class")
factorial = probes.factorial(["class", "background"], n_per_cell=20)
matched = probes.match(
    treatment={"background": "snow"},
    control={"background": "grass"},
    on=["class"],
)
```

These operations matter because factor interpretation is only as good as the contrast represented in the probe population.

## Representation reduction

A module may return a tensor that is not already shaped as `samples × features`. Eigenflow reducers convert captured activations into one feature vector per probe.

The default reducer is `flatten`, which preserves every activation value but discards the tensor's explicit spatial or token structure. Alternative reducers should be selected according to the scientific question.

Reducer choice is part of the measurement definition, not merely a performance setting.

## Metrics

A metric converts a representation matrix into an `N × N` relational matrix over probes. Built-ins include cosine similarity, Euclidean distance, squared Euclidean distance, Manhattan distance, correlation distance, dot-product similarity, Mahalanobis distance, RBF kernels, and polynomial kernels.

The metric records whether large values mean greater similarity or greater distance so filtrations can orient the control sweep correctly.

## Filtrations

A filtration converts a relational matrix into an ordered family of graphs.

Eigenflow includes threshold, epsilon/distance, edge-density, k-nearest-neighbor, mutual-kNN, and weighted filtration tools.

Edge density is especially useful for comparing metrics because raw thresholds such as cosine `0.8` and Euclidean distance `3.1` are not directly commensurable. The density

\[
\rho = |E| / \binom{N}{2}
\]

provides a common graph-scale coordinate.

## Structural analyses

Built-in analysis keywords include:

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

Different observables answer different questions. A component count measures fragmentation. Giant-component growth measures macroscopic coalescence. Susceptibility emphasizes finite-cluster organization. Spectral quantities describe operator-level global organization. Factor alignment compares observed graph partitions with controlled metadata.

These are complementary measurements rather than interchangeable estimates of one hidden quantity.

## PCSCS

PCSCS is retained as a canonical Eigenflow preset:

```python
result = ef.presets.pcscs(model, probes)
```

The preset uses flattened activations, cosine similarity, threshold filtration, PCSCS-style component analysis, and spectral diagnostics across captured representation sites.

## Interpretation

A correct interpretation starts with what was measured.

For example:

> At the third captured representation site, the probe population forms two large components over a wider edge-density interval than at the first site, and those components have higher NMI with the controlled class label.

That is an observation.

A candidate interpretation is:

> Under this probe design and measurement geometry, the later representation provides stronger relational evidence of organization by class.

An alternative explanation might be that the observed effect depends on the chosen reducer or metric.

The experiment does not, by itself, establish:

> The network contains a discrete internal "class feature," or the class relation is causally responsible for the final prediction.

Eigenflow is designed to make this distinction operational.

## Visualization

```python
from eigenflow.visualization import observable_curve, layer_control_heatmap, eigenflow_plot

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

## Persistence

```python
result.save("results/my_experiment")
```

Current persistence writes a JSON representation suitable for inspection and provenance. Consult the data-model documentation for the exact persistence guarantees of the installed version.

## Next

Start with the experimental-model documentation if you are designing a probe study. Read the percolation or spectral documents before using those observables for substantive interpretation. Use the VGG16 guide for an image-model walkthrough and the result-interpretation guide when turning outputs into scientific claims. The API specification is reference material for advanced configuration and extension work.
