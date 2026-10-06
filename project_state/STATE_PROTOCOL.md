# Eigenflow persistent state management protocol

This protocol governs **project-development state**: architecture, decisions, execution units, documentation objectives, implementation progress, and artifact lineage.

It is distinct from Eigenflow's scientific experiment-result model.

## Authority

`project_state/project_state.json` is the canonical semantic project state.

`project_state/execution_manifest.json` is authoritative for work-unit progress and resumption.

Git records repository history. A local Git commit does not imply that the corresponding commit exists on a remote.

Conversation context, scratch notes, author drafts, and derivative documentation are working material unless their semantic content is committed into canonical project state.

## Work cycle

Substantial work follows:

```text
read relevant canonical state
        ↓
determine bounded operation
        ↓
identify affected objects and dependencies
        ↓
construct proposed changes
        ↓
validate
        ↓
persist canonical state
        ↓
revise dependent artifacts
        ↓
record provenance and completion state
        ↓
establish resume point
```

Do not regenerate valid completed work simply because a new conversation begins.

## Formal planning directives

When the user says **formally plan**, **formally update**, or otherwise explicitly invokes formal project planning, the plan is not complete as conversation prose. It is a canonical-state mutation.

Before describing a formal plan as complete:

1. read the current canonical project state, execution manifest, and relevant protocol sections;
2. identify every mutated or newly introduced durable entity and its dependency relations;
3. classify dependent impact as `none`, `review`, `invalidate`, or `regenerate`;
4. define public-API effects, backward-compatibility consequences, persistence/provenance effects, documentation obligations, test obligations, and pressure-test implications;
5. add or revise canonical decisions, constraints, unresolved questions, planned outputs, and acceptance criteria;
6. create an ordered executable work-unit sequence with explicit dependencies, outputs, and resume point;
7. record schema evolution when the state model itself changes;
8. increment the canonical state revision and synchronize `execution_manifest.json`;
9. record provenance for the directive and mutation; and
10. persist and validate the canonical state artifacts before claiming the formal plan is established.

A chat-only outline may be useful working material, but it is not a formal project plan until these persistence requirements have been satisfied.

## Stable identifiers

Durable objects receive stable IDs when reference, dependency, provenance, comparison, or revision matters.

Renaming a human label does not require changing the durable ID.

## Ordinary mutation

An ordinary mutation changes values within the current schema.

Examples include:

- opening or resolving a task;
- adding a decision;
- revising scope;
- updating completion status;
- adding a dependency;
- recording an implementation result.

Every committed mutation should identify affected objects, preserve stable identity, update dependencies where needed, increment the state revision, and record provenance.

## Schema evolution

Schema evolution is expected.

A structural change can introduce new object types, fields, relation types, validation invariants, or normalization rules.

Prefer controlled extension, migration, and backfill over restarting the project.

A migration should record:

- prior and new schema version;
- rationale;
- affected object classes;
- transformation rules;
- validation checks;
- compatibility consequences.

## Dependencies and invalidation

A change to an upstream object can affect derivative artifacts.

Classify dependent impact as:

```text
none
review
invalidate
regenerate
```

Revise only affected dependents.

Examples:

- changing the public `Metric` protocol affects API docs, implementations, extension examples, and tests;
- changing a visualization title should not invalidate numerical analyses;
- changing probe metadata semantics may affect factor-analysis docs and serialization without affecting spectral algorithms.

## Provenance

Provenance records inspectable workflow lineage, not hidden model reasoning.

A useful provenance record may include:

- work-unit ID;
- source object IDs;
- input files or external sources;
- transformation name;
- timestamp;
- producing agent/role;
- replaced or superseded objects.

## Execution manifest

Work is decomposed into bounded units with dependencies and statuses such as:

```text
pending
in_progress
blocked
complete
invalidated
```

Before work begins, dependencies should be complete unless the unit is explicitly exploratory.

On completion:

1. persist semantic state;
2. persist derivative artifacts;
3. mark the unit complete;
4. record the last committed unit;
5. choose the next resume unit.

## Git and remote synchronization

Project state, local Git history, and remote Git history are distinct.

A typical sequence is:

```text
modify canonical state/artifacts
        ↓
validate
        ↓
git add / commit
        ↓
git push
        ↓
verify local HEAD == remote branch hash
```

A state mutation can exist without a Git commit.

A Git commit can exist locally without being pushed.

Remote validation should compare commit hashes explicitly when exact synchronization matters.

## Human-facing documentation governance

Documentation follows an inverse instructional architecture.

For each human-facing document, canonical state records:

- audience;
- terminal reader state;
- prerequisite state;
- section objectives;
- assigned instructional-trajectory moves;
- representation task / acceptance evidence.

Substantive prose is developed through the antagonistic drafting protocol in `project_state/EDITORIAL_DRAFTING_PROTOCOL.md`:

```text
four independent author drafts
        ↓
three-role editorial-board adjudication
        ↓
final synthesized document
```

Author/editor drafts are provenance artifacts. The synthesized document is the human-facing artifact.

Documentation is not complete merely because every file contains text. It is complete when the surface supports the target reader state and matches actual implementation.

## Validation

State validation includes:

- unique stable IDs;
- valid relation endpoints;
- valid execution dependencies;
- synchronized state and manifest revisions;
- explicit supersession for conflicting committed decisions.

Documentation validation includes:

- implementation/API fidelity;
- no unimplemented feature claims;
- correct conceptual prerequisite order;
- runnable examples where promised;
- explicit interpretive limits;
- cross-document terminology consistency.

Scientific-method validation includes:

- preserving probe identity/order;
- recording metric orientation;
- interpreting filtration direction correctly;
- using common control coordinates appropriately in cross-metric comparison;
- handling eigenspace degeneracy;
- separating descriptive transitions from stronger criticality claims;
- separating observation from semantic inference.

## Checkpoints

A checkpoint is valid when:

- canonical state parses and validates;
- manifest agrees with state revision;
- completed units have their outputs;
- no unit is falsely marked complete;
- the next resume point is explicit.

The project is complete only when release-required units are complete and final validation passes.
