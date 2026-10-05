# Contributing to Eigenflow

Eigenflow combines software engineering with experimental-method semantics. A contribution is complete only when the code, tests, documentation, and scientific interpretation of the new behavior agree.

## Development setup

Clone the repository and create an environment with Python 3.10 or later.

```bash
python -m pip install -e ".[dev]"
pytest
```

The current core runtime depends on NumPy, SciPy, NetworkX, scikit-learn, PyTorch, and Matplotlib.

Before submitting a change, run the complete test suite from the repository root.

## Repository architecture

The major boundaries are:

```text
probes          experimental population construction
extraction      PyTorch model boundary and activation capture
representations standardized population representations
metrics         pairwise relational geometry
filtrations     parameterized graph construction
graphs          graph primitives
operators       graph-to-matrix operators
analyses        user-facing structural analyses
percolation     percolation-style observables
spectra         eigensolvers and spectral quantities
transitions     transition summaries
visualization   Matplotlib views
presets         canonical configurations such as PCSCS
```

Code downstream of representation extraction should not depend on architecture-specific PyTorch behavior.

## Adding a metric

Subclass `Metric` and define `name`, `kind`, and `pairwise_values`.

```python
from eigenflow.metrics.base import Metric

class MyMetric(Metric):
    name = "my_metric"
    kind = "similarity"

    def pairwise_values(self, X):
        ...
```

Requirements:

- return an `N × N` numeric matrix;
- document whether larger values mean stronger similarity or larger distance;
- preserve probe order;
- add unit tests for symmetry or asymmetry assumptions;
- document mathematical meaning and intended use;
- add a resolver alias only if a stable keyword is warranted.

## Adding a filtration

Subclass `Filtration` and implement `build(rel)`.

The returned `GraphFiltration` must preserve node order and record the exposed control parameter, actual edge density, and native parameter where useful.

Document:

- expected metric orientation;
- whether graph growth is monotone;
- what increasing the control parameter means;
- how ties are handled;
- whether edges are weighted.

## Adding an operator

Subclass `GraphOperator` and implement `matrix(snapshot)`.

State clearly:

- matrix dimension;
- symmetry;
- expected spectrum;
- graph assumptions;
- what structural question the operator is intended to answer.

Spectral code must not silently use a symmetric eigensolver on an operator for which that assumption does not hold.

## Adding an analysis

Subclass `Analysis` and return an `AnalysisResult`.

```python
class MyAnalysis(Analysis):
    name = "my_analysis"

    def run(self, ctx):
        ...
```

Use:

- `observables` for named aggregate outputs;
- `records` for per-control-step data;
- `metadata` for analysis configuration.

Every new scientific analysis needs documentation covering:

1. indication;
2. mathematical object;
3. exact output;
4. interpretation;
5. alternative explanations;
6. unsupported claims;
7. at least one test with an analytically or structurally predictable fixture.

## Tests

Use the smallest test that establishes the invariant.

Expected categories include:

- unit tests for local numerical behavior;
- integration tests for end-to-end population experiments;
- regression tests for PCSCS compatibility;
- property-style tests for ordering, monotonicity, or invariants;
- deterministic fixtures with fixed seeds.

Avoid tests that merely assert that a function runs. Prefer tests that establish the meaning of the result.

## Documentation

Human-facing scientific documentation follows the inverse instructional architecture in `docs/INSTRUCTIONAL_ARCHITECTURE.md`.

A substantive section should explain, where applicable:

- why the object is needed;
- what it represents;
- when it is indicated;
- how to invoke it;
- what output it produces;
- how to read the output;
- what inference it may support;
- what alternatives remain;
- what it does not establish.

Do not introduce a new statistic as a self-explanatory interpretability score.

## Persistent project state

Project-development state is governed by `project_state/STATE_PROTOCOL.md`.

Important semantic decisions should be committed to canonical state before or with dependent artifacts. Schema evolution is permitted through controlled migration.

The current conversation or an editor's local notes are not substitutes for persistent project state.

## Pull-request checklist

Before a change is ready:

- [ ] tests pass;
- [ ] public API documentation matches implementation;
- [ ] new behavior has an indication and interpretation;
- [ ] numerical assumptions are stated;
- [ ] relevant examples are updated;
- [ ] persistent project state is updated when the change modifies scope, architecture, or committed behavior;
- [ ] changelog is updated for user-visible changes;
- [ ] no documentation promises unimplemented functionality.
