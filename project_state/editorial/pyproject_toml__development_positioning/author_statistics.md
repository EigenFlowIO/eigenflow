# Computational statistics / research-design author — independent draft

## Unit

`pyproject.toml` (incremental region)

## Assigned scope

Package description/keywords updated to representation observability and development use.

## Drafting objective

Emphasize identification: measurement invariance, matched probes, explicit baselines, site comparability, alternative explanations, robustness, and the danger of a generic quality score.

## Proposed content

Treat comparability as an identification condition. A changed reducer, metric, probe population, preprocessing pipeline, or control grid can masquerade as a checkpoint effect. Baseline-relative deltas require matched support and identical shapes unless the analyst explicitly aligns coordinates. Site alignment is a modeling assumption and normalized depth is exploratory.

## Acceptance concerns

- Preserve already adjudicated surrounding content where this is an incremental region.
- State non-goals next to tempting overinterpretations.
- Keep behavioral, efficiency, and representation-structure evidence distinct.
- Ensure every code claim is exercised by tests or runnable examples.
