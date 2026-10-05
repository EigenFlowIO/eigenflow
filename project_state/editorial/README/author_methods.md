# Draft C — Research methods training material

# Eigenflow

Eigenflow helps you run a particular kind of neural-network interpretability experiment:

> You design a set of probes so that competing explanations of the network's internal representation would organize those probes differently. Eigenflow measures that organization as the probes move through the network.

The package is useful only after you can answer the first methods question:

**What distinction are you trying to test?**

A good Eigenflow experiment begins with a contrast. For example:

- Does the representation organize dog images by breed or by background?
- Does rotation stop mattering at later layers?
- Do subclasses become coherent before they merge into a superclass?
- Which examples act as bridges between two categories?
- Does an apparent grouping survive a change of similarity metric?

## 1. Start with a probe population

A probe population is not just a batch of convenient data. It is your experimental instrument.

Suppose you want to test object identity against background. A useful design crosses both:

| object | background |
|---|---|
| wolf | snow |
| wolf | grass |
| husky | snow |
| husky | grass |

If you only use wolves in snow and huskies on grass, object and background are confounded. No analysis can tell you which factor explains the resulting organization.

Encode the factors in metadata:

```python
probes = ef.ProbePopulation.from_items(
    images,
    ids=ids,
    metadata=[
        {"class": cls, "background": bg}
        for cls, bg in conditions
    ],
)
```

Eigenflow includes helpers for balancing, factorial selection, and matched contrasts, but those helpers do not decide whether your experiment identifies the question you care about. That remains a research-design judgment.

## 2. Observe the whole population at internal sites

PyTorch already knows how to run the model. Eigenflow hooks internal modules and captures their outputs while the probe population passes through.

At one site, the complete population can be represented as

\[
Z^{(\ell)} = \{z_1^{(\ell)},\ldots,z_N^{(\ell)}\}.
\]

Eigenflow is primarily interested in how these probes relate to one another at that site.

This is different from tracing one image through the model. The main object is the population configuration at each depth.

## 3. Decide how "near" and "far" will be measured

A metric turns the population into pairwise relations.

Cosine similarity asks about angular alignment. Euclidean distance asks about absolute geometric separation. Correlation removes some offset/scale information. Kernels impose additional geometry.

There is no universally correct metric. Your choice defines what kind of relational structure you are measuring.

```python
metric = ef.metrics.CosineSimilarity()
```

A strong study often checks whether its substantive conclusion survives at least one reasonable alternative.

## 4. Sweep a control parameter

Eigenflow does not force you to choose one threshold and pretend it is natural.

Instead, a filtration generates a family of graphs over a control parameter. At one end, only the strongest relations survive. As the parameter changes, additional relations enter and groups merge.

```python
filtration = ef.filtrations.EdgeDensityFiltration(
    start=0.0,
    stop=0.5,
    steps=100,
)
```

Edge density is useful when comparing metrics because a density of `0.10` means that 10% of possible undirected relations are retained regardless of the raw units of the metric.

## 5. Ask structural questions

Different analyses answer different questions.

`components` asks: how fragmented is the probe population?

`percolation` asks: how does connectivity move from local groups toward global integration?

`spectra` asks: what large-scale operator structure exists, and how does it reorganize?

`factor_alignment` asks: how closely do emergent component labels agree with your known experimental factors?

The package does not collapse all of these into one "interpretability score."

```python
experiment = ef.Experiment(
    model=model,
    probes=probes,
    metric=metric,
    filtration=filtration,
    analyses=[
        "components",
        "percolation",
        "spectra",
        "factor_alignment",
    ],
)

result = experiment.run()
```

## 6. Read across layer and scale

The scientifically interesting object is often

\[
Q(\ell,p),
\]

where \(\ell\) is the representation site and \(p\) is the filtration control parameter.

A class grouping that occurs at only one arbitrary threshold is weak evidence. A class grouping that is stable across a broad control interval, becomes stronger across depth, aligns with several structural observables, and survives an alternative metric is much more persuasive.

## 7. Interpret in four steps

Do not jump directly from a curve to a semantic claim.

Use this sequence:

1. **Observation:** describe the output without adding meaning.
2. **Candidate interpretation:** connect it to the hypothesis the probe design was constructed to test.
3. **Alternative:** state another plausible explanation.
4. **Boundary:** state what the experiment did not establish.

Example:

**Observation:** At later sites, component partitions have higher NMI with class labels over a wider edge-density range, while alignment with background decreases.

**Candidate interpretation:** Under this probe design, the representation becomes increasingly organized by class rather than background.

**Alternative:** The apparent change may depend on the representation reducer or metric.

**Boundary:** The result does not establish that a particular unit explicitly encodes class or that class organization causally drives the prediction.

## Minimal runnable example

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

probes = ef.ProbePopulation.from_items(inputs, metadata=metadata)

result = ef.Experiment(
    model=model,
    probes=probes,
    metric="cosine",
    filtration=ef.filtrations.EdgeDensityFiltration(
        start=0.0,
        stop=0.5,
        steps=40,
    ),
    analyses=["components", "percolation", "spectra", "factor_alignment"],
).run()

print(result.summary())
```

Then inspect one captured site:

```python
site = next(iter(result.layers))
layer = result.layers[site]

print(layer.analyses["components"].observables["component_count"])
print(layer.analyses["percolation"].observables["giant_component_fraction"])
print(layer.analyses["factor_alignment"].records[:3])
```

Your next step should not be "find the most impressive curve." It should be to compare these results with the predictions you wrote before the run.

## When not to use Eigenflow

Do not use Eigenflow as the sole basis for a claim requiring:

- causal necessity or sufficiency;
- localization of a concept to a particular neuron;
- feature visualization in input space;
- attribution of a single prediction;
- semantic interpretation without a probe contrast that distinguishes alternatives.

Those questions may require interventions, attribution methods, activation maximization, causal tracing, or other tools.

## PCSCS users

PCSCS is one configuration of this general workflow. The Eigenflow preset retains cosine similarity, threshold filtration, and PCSCS-style connected-component analysis:

```python
result = ef.presets.pcscs(model, probes)
```

Eigenflow then lets you change the metric, control coordinate, or analysis family while keeping the same probe experiment.

## Learn next

If you are planning a study, read the experimental-model guide first. If you already have an experiment and need to understand graph-growth outputs, read the percolation guide. If you are using eigenvalues or eigenspaces, read the spectral-analysis guide before interpreting them. After a run, use the result-interpretation guide to write the claim.
