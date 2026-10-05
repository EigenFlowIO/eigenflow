"""PCSCS compatibility and migration example."""
import torch
import eigenflow as ef

torch.manual_seed(11)

model = torch.nn.Sequential(
    torch.nn.Linear(6, 10),
    torch.nn.ReLU(),
    torch.nn.Linear(10, 4),
)

inputs = [torch.randn(6) for _ in range(24)]
metadata = [{"class": i % 3} for i in range(24)]
probes = ef.ProbePopulation.from_items(inputs, metadata=metadata)

# 1. Canonical PCSCS preset.
preset_result = ef.presets.pcscs(
    model,
    probes,
    steps=30,
)

print("PCSCS preset:")
for site, layer in preset_result.layers.items():
    pcscs = layer.analyses["pcscs"]
    print(
        site,
        "critical=",
        pcscs.observables["critical_parameter"],
        "convergence=",
        pcscs.observables["convergence_parameter"],
    )

# 2. The same idea expanded into general Eigenflow configuration.
explicit_result = ef.Experiment(
    model=model,
    probes=probes,
    extraction=ef.ExtractionConfig(
        sites="all",
        reducer="flatten",
    ),
    metric=ef.metrics.CosineSimilarity(),
    filtration=ef.filtrations.ThresholdFiltration(
        steps=30,
    ),
    analyses=[
        "pcscs",
        "spectra",
    ],
).run()

# 3. Extend beyond PCSCS without changing the probe experiment.
extended_result = ef.Experiment(
    model=model,
    probes=probes,
    extraction=ef.ExtractionConfig(
        sites="all",
        reducer="flatten",
    ),
    metric=ef.metrics.CosineSimilarity(),
    filtration=ef.filtrations.EdgeDensityFiltration(
        start=0.0,
        stop=0.5,
        steps=30,
    ),
    analyses=[
        "components",
        "percolation",
        "spectra",
        "factor_alignment",
        "transitions",
    ],
).run()

print("\nExtended Eigenflow analysis:")
print(extended_result.summary())

# PCSCS interpretation remains component-centric: it describes progressive
# connectivity under a cosine-threshold sweep across captured representation
# populations. The broader Eigenflow configuration lets the experimenter ask
# whether the same substantive phenomenon is supported by other control
# coordinates and structural observables.
