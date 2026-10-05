# Visualization phase validation

## Scope

This validation covers the visualization ontology, public plotting API, PCSCS parity layer, generalized Eigenflow views, runtime result-artifact retention, complete demonstration script, generated reference artifacts, documentation integration, and regression tests.

## Implementation validation

- Existing core test suite continues to pass.
- Visualization regression tests exercise every canonical public visualization family on real `ExperimentResult` / `LayerResult` objects.
- Runtime artifacts retain the original probe population, reduced representation, relational matrix, and graph filtration in memory.
- Runtime artifacts are omitted from `ExperimentResult.save()` so JSON persistence behavior remains report-like and does not silently expand.
- PCSCS-compatible component trajectories, merge-event views, dendrograms, combined-layer views, static spectra, spectral flow, and spectral-property summaries have Eigenflow equivalents.
- Generalized views cover probe design, relational matrices, component membership, percolation, graph snapshots, eigenspaces, factor alignment, class connectivity, bridge probes, layer×control structure, robustness, cross-result comparison, and integrated interpretation.

## Demonstration validation

`examples/complete_visualization_demo.py` executes successfully against the working implementation.

The reference run:

- trains a real three-class MLP;
- uses an exact 3 class × 2 background balanced held-out probe population with 10 probes per cell;
- reaches 1.0 probe classification accuracy;
- runs cosine and Euclidean experiments at matched edge density;
- generates 22 canonical figures;
- saves numerical tables, native `result.json`, model state, configuration, environment metadata, figure manifest, and SHA-256 checksums;
- creates a ZIP archive containing the complete generated artifact set.

The generated checksum manifest validates successfully.

## Documentation validation

- `docs/guides/visualization_guide.md` contains real generated figures and runnable examples.
- Each canonical view is documented by analyst question, encoding/use, interpretation, and claim boundary.
- `docs/PCSCS_VISUALIZATION_PARITY.md` maps the former PCSCS plotting surface to the generalized Eigenflow interface.
- README includes representative real outputs and routes to the complete guide.
- API, data-model, and execution specifications document the new runtime artifact and visualization surfaces.
- Public/local Markdown links and embedded image paths resolve.

## Test results

At the completion gate the repository test suite reports **12 passing tests**.

The following executable examples also complete successfully:

- `examples/basic_mlp.py`
- `examples/pcscs_compatibility.py`
- `examples/complete_visualization_demo.py`

Python source/examples compile, `pyproject.toml` parses, and `git fsck --full` passes for the locally available Git history.

## Git-history note

## Documentation/adjudication status

The visualization ontology, parity map, complete visualization guide, visualization-specific README/index additions, runtime-artifact/API specification changes, demonstration scripts, and reference-output READMEs have been reviewed under the incremental adjudication protocol. Previously adjudicated unrelated prose was preserved rather than redrafted. The region-level ledger is stored under `project_state/editorial/ADJUDICATION_LEDGER.md`.

## Distribution status

The complete repository package includes the visualization implementation, tests, documentation assets, generated reference metadata, editorial provenance, and canonical project state. Git ancestry is packaged against the user's known remote baseline `9ca109c327f0af3fcd99c79f08451748d2b8c839`; the packaged repository is configured to obtain that baseline from `origin` when network access is available.
