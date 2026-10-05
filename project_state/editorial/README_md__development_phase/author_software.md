# Technical software developer/documentation writer — independent draft

## Unit

`README.md` (incremental region)

## Assigned scope

Development-instrumentation positioning, API example, and navigation links only.

## Drafting objective

Prioritize exact implemented symbols, runnable signatures, failure behavior, persistence boundaries, and reproducibility. Do not describe features that are only proposed.

## Proposed content

The public text should expose the implemented hierarchy `Experiment -> ExperimentResult -> ExperimentSeries/LongitudinalResult`, show imports from `eigenflow.development`, state compatibility failures explicitly, and distinguish single-result JSON persistence from series persistence. Examples should be runnable from the repository and should not imply Eigenflow owns training. For API-bearing material, include the exact public development symbols.

## Acceptance concerns

- Preserve already adjudicated surrounding content where this is an incremental region.
- State non-goals next to tempting overinterpretations.
- Keep behavioral, efficiency, and representation-structure evidence distinct.
- Ensure every code claim is exercised by tests or runnable examples.
