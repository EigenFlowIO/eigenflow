# Incremental statistics/research-design review

**File:** `examples/complete_visualization_demo.py`  
**Region:** Module contract and reproducibility-facing comments

The changed claims should remain conditional on the probe sample, reducer, metric, filtration/control coordinate, operator, and finite-sample design. Code behavior remains the authority; prose must not promise unsupported reproducibility.

Proposed treatment: use matched coordinates for comparisons where required, distinguish descriptive transitions from criticality claims, and identify robustness or alternative explanations rather than presenting visual separation as self-validating.

Acceptance: the region does not imply stronger identification than the experimental design supports.
