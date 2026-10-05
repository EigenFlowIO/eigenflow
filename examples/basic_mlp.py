"""Basic Eigenflow experiment.

The example is deliberately small. It demonstrates the complete population-level
pipeline and prints outputs that can be interpreted without treating Eigenflow as
a black box.
"""
import torch
import eigenflow as ef

torch.manual_seed(7)

# A small deterministic model. The scientific object is not this architecture;
# it is the relational organization of the probe population at its internal sites.
model = torch.nn.Sequential(
    torch.nn.Linear(4, 8),
    torch.nn.ReLU(),
    torch.nn.Linear(8, 2),
)

# Build two probe groups. In a real experiment, metadata should encode
# deliberately manipulated/controlled factors rather than arbitrary labels.
inputs = []
metadata = []
for i in range(16):
    inputs.append(torch.randn(4) * 0.35 + torch.tensor([1.0, 0.0, 0.0, 0.0]))
    metadata.append({"class": "A"})
for i in range(16):
    inputs.append(torch.randn(4) * 0.35 + torch.tensor([-1.0, 0.0, 0.0, 0.0]))
    metadata.append({"class": "B"})

probes = ef.ProbePopulation.from_items(
    inputs,
    metadata=metadata,
    name="two_group_demo",
)

print("Available PyTorch capture sites:")
print(ef.PyTorchExtractor(model).available_sites())

experiment = ef.Experiment(
    model=model,
    probes=probes,
    metric=ef.metrics.CosineSimilarity(),
    filtration=ef.filtrations.EdgeDensityFiltration(
        start=0.0,
        stop=0.40,
        steps=20,
    ),
    analyses=[
        "components",
        "percolation",
        "spectra",
        "factor_alignment",
        "transitions",
    ],
)

result = experiment.run()

print("\nExperiment summary:")
print(result.summary())

for site, layer in result.layers.items():
    print(f"\n--- site {site} ---")

    components = layer.analyses["components"]
    print("component counts:")
    print(components.observables["component_count"])

    percolation = layer.analyses["percolation"]
    print(
        "susceptibility peak:",
        percolation.observables["susceptibility_peak_parameter"],
    )

    alignment = layer.analyses["factor_alignment"]
    if alignment.records:
        # Find the control step with the highest observed class NMI.
        rows = [r for r in alignment.records if "class" in r]
        if rows:
            best = max(rows, key=lambda r: r["class"]["nmi"])
            print(
                "best class NMI:",
                best["class"]["nmi"],
                "at parameter",
                best["parameter"],
            )

    transitions = layer.analyses["transitions"]
    print("transition candidates:")
    print(transitions.observables["candidates"])

# Interpretation discipline:
#
# Observation:
#   Report how component structure, factor alignment, percolation, or spectra
#   actually changed.
#
# Candidate inference:
#   Connect that pattern to the controlled feature hypothesis.
#
# Alternative:
#   Consider metric/reducer/probe dependence.
#
# Boundary:
#   Do not claim that the graph statistic identifies a unique neuron or causal
#   mechanism.
#
# Exercise:
#   Replace CosineSimilarity() with EuclideanDistance() while keeping the same
#   EdgeDensityFiltration. Predict which substantive conclusions should survive
#   if the observed grouping is metric-robust, then rerun and compare.
