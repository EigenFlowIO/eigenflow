# Incremental statistics/research-design review

**File:** `docs/spec/DATA_MODEL_SPEC.md`  
**Region:** LayerResult/ExperimentResult runtime artifacts

The changed claims should remain conditional on the probe sample, reducer, metric, filtration/control coordinate, operator, and finite-sample design. Dataclass signatures must include artifacts; JSON omission must be explicit.

Proposed treatment: use matched coordinates for comparisons where required, distinguish descriptive transitions from criticality claims, and identify robustness or alternative explanations rather than presenting visual separation as self-validating.

Acceptance: the region does not imply stronger identification than the experimental design supports.
