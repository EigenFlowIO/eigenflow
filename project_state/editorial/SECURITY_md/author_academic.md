# Academic author for a computational interpretability journal draft — `SECURITY.md`

Prioritize formal definitions, conceptual precision, epistemic scope, scholarly claim discipline, and the relation between measurements and latent-feature hypotheses.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## Supported versions

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The current repository is an alpha release (`1.0.0a1`). Security fixes target the current development line unless a later release policy states otherwise.

## Reporting a vulnerability

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: A private reporting channel has not yet been designated in canonical project state. Until that project-maintainer decision is supplied, do **not** place sensitive exploit details in a public issue. Repository maintainers should configure a private vulnerability-reporting mechanism before public release. This is one of the remaining maintainer-intervention items for release readiness.

## Untrusted model artifacts

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: PyTorch model-loading workflows can execute or deserialize unsafe content depending on how artifacts are stored and loaded. Eigenflow does not make an untrusted model file safe merely because it is used only for interpretability. Treat model artifacts, checkpoints, and arbitrary Python model definitions as executable/untrusted code unless their provenance is trusted. Prefer safe serialization/loading practices supported by the installed PyTorch version and obtain models from trusted sources.

## Custom callables

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Eigenflow permits custom reducers, metrics, collate functions, and analysis objects. A Python callable runs with the privileges of the current process. Do not execute custom extension code from an untrusted source.

## Resource exhaustion

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Relational matrices scale quadratically with the number of probes, and full eigendecomposition can scale cubically in matrix dimension. An unexpectedly large probe population, dense non-backtracking operator, or high-resolution spectral sweep can exhaust memory or CPU resources. For untrusted experiment specifications, impose resource limits outside Eigenflow.

## Sensitive probe data

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Probe inputs and metadata may contain sensitive or proprietary data. The core package performs local computation and does not itself upload probe data to a network service. However, users remain responsible for: - model code that may perform network operations; - custom callables; - external logging; - saved result files; - filesystem permissions; - applicable data-governance requirements. Saved `result.json` files can contain probe-derived structural records and metadata about the experiment even though raw probe inputs are not serialized by `ExperimentResult.save()`.

## Dependency security

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Keep PyTorch, NumPy, SciPy, NetworkX, scikit-learn, Matplotlib, and Python patched according to their upstream security guidance. Report dependency-specific vulnerabilities upstream when the issue does not arise from Eigenflow behavior.

## Disclosure process

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: A formal response-time and disclosure policy will be added when the project maintainer designates the private reporting channel and release-support policy.
