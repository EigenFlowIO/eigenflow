# Security policy

Eigenflow executes user-supplied PyTorch models and user-supplied Python callables. Its primary security boundary is therefore the Python environment in which the experiment runs.

## Supported versions

The current supported release is `1.0.0a1`. Security fixes target the current development/release line unless a later release policy states otherwise.

## Reporting a vulnerability

Use the repository's **GitHub Private Vulnerability Reporting / Security Advisory** channel for sensitive vulnerability reports. Keep exploit details out of public issues, pull requests, and discussions.

Security communication is handled inside GitHub. Eigenflow does not publish an email-based security intake channel and does not use automated vulnerability-reporting or automated enforcement workflows.

Reports are reviewed by the repository maintainer, Andrew Hedman. Include enough information to reproduce and assess the issue: affected version or commit, relevant configuration, impact, reproduction steps or proof of concept, and any suggested mitigation.

## Untrusted model artifacts

PyTorch model-loading workflows can execute or deserialize unsafe content depending on how artifacts are stored and loaded.

Eigenflow does not make an untrusted model file safe merely because it is used only for interpretability.

Treat model artifacts, checkpoints, and arbitrary Python model definitions as executable/untrusted code unless their provenance is trusted.

Prefer safe serialization/loading practices supported by the installed PyTorch version and obtain models from trusted sources.

## Custom callables

Eigenflow permits custom reducers, metrics, collate functions, and analysis objects.

A Python callable runs with the privileges of the current process. Do not execute custom extension code from an untrusted source.

## Resource exhaustion

Relational matrices scale quadratically with the number of probes, and full eigendecomposition can scale cubically in matrix dimension.

An unexpectedly large probe population, dense non-backtracking operator, or high-resolution spectral sweep can exhaust memory or CPU resources.

For untrusted experiment specifications, impose resource limits outside Eigenflow.

## Sensitive probe data

Probe inputs and metadata may contain sensitive or proprietary data.

The core package performs local computation and does not itself upload probe data to a network service. However, users remain responsible for:

- model code that may perform network operations;
- custom callables;
- external logging;
- saved result files;
- filesystem permissions;
- applicable data-governance requirements.

Saved `result.json` files can contain probe-derived structural records and metadata about the experiment even though raw probe inputs are not serialized by `ExperimentResult.save()`.

## Dependency security

Keep PyTorch, NumPy, SciPy, NetworkX, scikit-learn, Matplotlib, and Python patched according to their upstream security guidance.

Report dependency-specific vulnerabilities upstream when the issue does not arise from Eigenflow behavior.

## Disclosure and response

The maintainer will assess reports and coordinate remediation and disclosure through GitHub. No fixed response-time SLA is promised for this alpha release. Public disclosure should wait until the maintainer has had a reasonable opportunity to assess and address the issue.
