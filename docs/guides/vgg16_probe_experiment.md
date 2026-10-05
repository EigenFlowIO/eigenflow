# VGG16 probe experiment

This guide develops a complete image-model experiment from an interpretability question to a bounded conclusion.

The example uses VGG16 because its PyTorch module structure is familiar and its convolutional stages make representation-site choices easy to inspect. Eigenflow itself does not contain VGG16-specific analysis code.

`torchvision` is used only to obtain the model and preprocessing. It is not currently a core Eigenflow dependency.

## Question and hypothesis

Suppose the question is:

> Does a pretrained VGG16 representation become more organized by object class than by background as depth increases?

Construct competing hypotheses.

- \(H_1\): later sites become increasingly organized by class, relatively invariant to background.
- \(H_2\): background remains a dominant organizing factor.

The experiment must contain probe combinations that distinguish these hypotheses.

## Build a crossed probe population

Assume you have images spanning two classes and two backgrounds:

| class | background |
|---|---|
| wolf | snow |
| wolf | grass |
| husky | snow |
| husky | grass |

Use equal or at least well-documented counts where possible.

```python
import eigenflow as ef

probes = ef.ProbePopulation.from_items(
    processed_images,
    ids=image_ids,
    metadata=[
        {
            "class": cls,
            "background": background,
        }
        for cls, background in conditions
    ],
    name="wolf_husky_background",
)

probes = probes.factorial(
    ["class", "background"],
    n_per_cell=20,
    seed=7,
)
```

If a factorial cell is absent in the original material, this helper cannot create it. The design is then confounded for the corresponding contrast.

## Load VGG16 reproducibly

```python
import torch
from torchvision.models import vgg16, VGG16_Weights

weights = VGG16_Weights.DEFAULT
model = vgg16(weights=weights)
model.eval()

preprocess = weights.transforms()
```

Apply the same preprocessing to every probe.

Store or report:

- weight/checkpoint identity;
- preprocessing;
- image source;
- probe construction;
- random seed used for sampling.

## Inspect representation sites

PyTorch exposes the module hierarchy.

```python
extractor = ef.PyTorchExtractor(model)

for name in extractor.available_sites():
    print(name)
```

VGG16's `features` stack contains convolution, ReLU, and pooling modules. A useful first analysis often chooses endpoints of major convolutional stages rather than every individual ReLU.

For example, inspect the actual model and choose explicit names:

```python
sites = [
    "features.4",
    "features.9",
    "features.16",
    "features.23",
    "features.30",
]
```

These names are examples for the canonical torchvision VGG16 layout. Verify them against `available_sites()` for the installed model.

The choice of sites determines which computational stages are compared.

## Choose a representation reducer

A VGG convolutional activation has shape

\[
N\times C\times H\times W.
\]

### Flatten

```python
extraction = ef.ExtractionConfig(
    sites=sites,
    reducer="flatten",
    batch_size=16,
)
```

Flatten preserves all activation values but treats the spatially arranged tensor as one long vector.

### Global average pooling

```python
extraction = ef.ExtractionConfig(
    sites=sites,
    reducer="global_average",
    batch_size=16,
)
```

Global average pooling summarizes each channel over spatial positions. This can reduce dimensionality substantially and changes the measurement question.

Neither reducer is universally correct. If the substantive conclusion depends strongly on reducer choice, report that dependence.

## Choose metric and filtration

For the first run, use cosine similarity and edge density.

```python
metric = ef.metrics.CosineSimilarity()

filtration = ef.filtrations.EdgeDensityFiltration(
    start=0.0,
    stop=0.35,
    steps=80,
)
```

Why edge density? The graph begins sparse and progressively admits more pairwise relations. If you later compare cosine with Euclidean distance, matching edge density supplies a common graph-sparsity coordinate.

Why cosine? It provides one reasonable angular relation for high-dimensional activation vectors. It is a measurement choice, not the ground-truth geometry of VGG16.

## Run complementary analyses

```python
experiment = ef.Experiment(
    model=model,
    probes=probes,
    extraction=extraction,
    metric=metric,
    filtration=filtration,
    analyses=[
        "components",
        "percolation",
        "spectra",
        "eigenspaces",
        "factor_alignment",
        "class_structure",
        "bridges",
        "kcore",
        "transitions",
    ],
)

result = experiment.run()
```

The same population is now analyzed at each selected VGG16 site.

## Navigate the result

```python
print(result.summary())
```

Inspect factor alignment at each site:

```python
for site, layer in result.layers.items():
    rows = layer.analyses["factor_alignment"].records

    print("\n", site)
    for row in rows[::10]:
        print(
            row["parameter"],
            row.get("class"),
            row.get("background"),
        )
```

Inspect class structure:

```python
for site, layer in result.layers.items():
    cs = layer.analyses["class_structure"]

    print(site)
    for row in cs.records[::10]:
        print(row["parameter"], row["classes"])
```

Inspect percolation:

```python
for site, layer in result.layers.items():
    p = layer.analyses["percolation"]
    print(
        site,
        p.observables["susceptibility_peak_parameter"],
    )
```

Inspect spectral trajectories:

```python
for site, layer in result.layers.items():
    trajectory = layer.analyses["spectra"].observables["trajectory"]

    print(site)
    for snapshot in trajectory.snapshots[::10]:
        print(
            snapshot.parameter,
            snapshot.observables.get("algebraic_connectivity"),
            snapshot.observables["spectral_entropy"],
        )
```

## Visualize layer × control behavior

```python
from eigenflow.visualization import (
    observable_curve,
    layer_control_heatmap,
    eigenflow_plot,
)

first_site = next(iter(result.layers))
first_layer = result.layers[first_site]

observable_curve(
    first_layer,
    analysis="percolation",
    observable="giant_component_fraction",
)

layer_control_heatmap(
    result,
    analysis="components",
    observable="component_count",
)

eigenflow_plot(first_layer)
```

The heatmap makes the two-dimensional object explicit: network site on one axis, relational scale on the other.

## Interpret the experiment

Imagine the results show:

- early sites: moderate background NMI and weak class NMI;
- middle sites: both factors visible;
- late sites: class NMI high over a broad density interval while background NMI falls;
- late sites: within-class density exceeds external density over the same interval;
- late sites: a stable low-dimensional spectral regime appears;
- bridge analysis identifies a few visually ambiguous probes connecting the final groups.

A disciplined conclusion is:

**Observation.** Multiple structural observables become more class-aligned and less background-aligned across depth.

**Candidate inference.** Within this factorial probe population, later VGG16 representations provide stronger evidence of organization by class relative to background.

**Alternative explanations.** Global-average pooling, cosine geometry, probe sampling, or an uncontrolled visual factor could contribute to the pattern.

**Unsupported claim.** The experiment does not identify a unique class feature dimension or prove that the observed class organization causally determines VGG16's final prediction.

## Stress-test the interpretation

Repeat the experiment with an alternative reducer:

```python
alt_extraction = ef.ExtractionConfig(
    sites=sites,
    reducer="flatten",
    batch_size=16,
)
```

Repeat with Euclidean distance at the same edge-density grid:

```python
alt_metric = ef.metrics.EuclideanDistance()
```

If the main conclusion persists, the evidence is less dependent on one geometry.

If it changes, that difference is itself informative. Report the dependence rather than selecting only the favorable configuration.

## Device and batching

Pass a device explicitly if needed:

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

experiment = ef.Experiment(
    model=model,
    probes=probes,
    extraction=ef.ExtractionConfig(
        sites=sites,
        reducer="global_average",
        batch_size=32,
    ),
    device=device,
    ...
)
```

The extractor temporarily switches the model to evaluation mode, runs under `torch.no_grad()`, and restores the model's previous training state after extraction.

Large probe populations and full spectra can be expensive. Reduce the number of sites, use pooling, reduce filtration steps, or configure partial spectral analysis for exploratory work.

## Save the result

```python
result.save("results/vgg16_wolf_husky")
```

The current implementation serializes a JSON representation to `result.json`. Eigenvectors are omitted from the serialized representation.

Record the complete experimental specification alongside any reported conclusion: probe construction, checkpoint, preprocessing, sites, reducer, metric, filtration, analyses, and robustness checks.
