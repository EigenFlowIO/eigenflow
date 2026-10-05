# Technical software developer and documentation writer draft — `examples/pcscs_compatibility.py`

Prioritize exact implemented syntax, public interfaces, runnable examples, navigation, failure behavior, and consistency with source.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## Executable unit

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: """PCSCS compatibility and migration example.""" torch.manual_seed(11) model = torch.nn.Sequential( torch.nn.Linear(6, 10), torch.nn.ReLU(), torch.nn.Linear(10, 4), ) inputs = [torch.randn(6) for _ in range(24)] metadata = [{"class": i % 3} for i in range(24)] probes = ef.ProbePopulation.from_items(inputs, metadata=metadata)

## 1. Canonical PCSCS preset.

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: preset_result = ef.presets.pcscs( model, probes, steps=30, ) print("PCSCS preset:") for site, layer in preset_result.layers.items(): pcscs = layer.analyses["pcscs"] print( site, "critical=", pcscs.observables["critical_parameter"], "convergence=", pcscs.observables["convergence_parameter"], )

## 2. The same idea expanded into general Eigenflow configuration.

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: explicit_result = ef.Experiment( model=model, probes=probes, extraction=ef.ExtractionConfig( sites="all", reducer="flatten", ), metric=ef.metrics.CosineSimilarity(), filtration=ef.filtrations.ThresholdFiltration( steps=30, ), analyses=[ "pcscs", "spectra", ], ).run()

## 3. Extend beyond PCSCS without changing the probe experiment.

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: extended_result = ef.Experiment( model=model, probes=probes, extraction=ef.ExtractionConfig( sites="all", reducer="flatten", ), metric=ef.metrics.CosineSimilarity(), filtration=ef.filtrations.EdgeDensityFiltration( start=0.0, stop=0.5, steps=30, ), analyses=[ "components", "percolation", "spectra", "factor_alignment", "transitions", ], ).run() print("\nExtended Eigenflow analysis:") print(extended_result.summary())
