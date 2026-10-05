# Human-facing surface validation

## Status

All documentation work that can be completed without maintainer identity/legal/reporting-channel authority has been completed.

The surface was developed against the inverse instructional architecture, section-level trajectory map, and antagonistic author/editor protocol.

## Automated validation completed

- full Python test suite passes;
- editable installation succeeds with `--no-build-isolation` in the current environment;
- `examples/basic_mlp.py` executes successfully;
- `examples/pcscs_compatibility.py` executes successfully;
- all local Markdown links resolve;
- `pyproject.toml` parses successfully;
- Python source and examples compile;
- API, data-model, and execution specifications were reconciled against source.

## Known implementation/documentation reconciliations

The final specifications explicitly state that:

- `Experiment` has no current `operators=` parameter;
- `Experiment` has no current persistent `cache=` parameter;
- `ExperimentResult.save()` writes `result.json`;
- there is no current `ExperimentResult.load()`;
- saved JSON omits spectral eigenvectors;
- `ExtractionConfig.retain_raw` exists but current extraction does not persist raw activations;
- default automatic capture selects leaf modules;
- default reducer is `flatten`;
- analysis keywords instantiate default analysis objects; custom configurations use explicit objects.

## Instructional validation

The surface now contains explicit support for the target reader competencies:

1. indication/non-indication for Eigenflow;
2. population-level experimental object;
3. controlled probe design;
4. measurement choices and their consequences;
5. component, percolation, spectral, factor, bridge/core/community, and transition observables;
6. interpretation across network depth and control scale;
7. observation → inference → alternatives → unsupported-claim discipline;
8. end-to-end examples and a VGG16 workflow;
9. technical API/data/execution reference material;
10. PCSCS migration/compatibility.

## Release-authority fields resolved

The maintainer supplied and the repository now records:

- software author: Andrew Hedman;
- release: Eigenflow `1.0.0a1`, released on GitHub on 2026-10-04;
- DOI: none for this release;
- license: MIT;
- legal copyright holder: Andrew Hedman;
- security communication: GitHub Private Vulnerability Reporting / Security Advisories;
- conduct authority: Andrew Hedman, using GitHub-native private maintainer communication;
- no automated reporting or enforcement workflow.

No maintainer-authority documentation blockers remain.
