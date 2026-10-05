# Technical software developer and documentation writer draft — `project_state/STATE_PROTOCOL.md`

Prioritize exact implemented syntax, public interfaces, runnable examples, navigation, failure behavior, and consistency with source.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## Authority

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: `project_state/project_state.json` is the canonical semantic project state. `project_state/execution_manifest.json` is authoritative for work-unit progress and resumption. Git records repository history. A local Git commit does not imply that the corresponding commit exists on a remote. Conversation context, scratch notes, author drafts, and derivative documentation are working material unless their semantic content is committed into canonical project state.

## Work cycle

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Substantial work follows: Do not regenerate valid completed work simply because a new conversation begins.

## Stable identifiers

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Durable objects receive stable IDs when reference, dependency, provenance, comparison, or revision matters. Renaming a human label does not require changing the durable ID.

## Ordinary mutation

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: An ordinary mutation changes values within the current schema. Examples include: - opening or resolving a task; - adding a decision; - revising scope; - updating completion status; - adding a dependency; - recording an implementation result. Every committed mutation should identify affected objects, preserve stable identity, update dependencies where needed, increment the state revision, and record provenance.

## Schema evolution

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Schema evolution is expected. A structural change can introduce new object types, fields, relation types, validation invariants, or normalization rules. Prefer controlled extension, migration, and backfill over restarting the project. A migration should record: - prior and new schema version; - rationale; - affected object classes; - transformation rules; - validation checks; - compatibility consequences.

## Dependencies and invalidation

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: A change to an upstream object can affect derivative artifacts. Classify dependent impact as: Revise only affected dependents. Examples: - changing the public `Metric` protocol affects API docs, implementations, extension examples, and tests; - changing a visualization title should not invalidate numerical analyses; - changing probe metadata semantics may affect factor-analysis docs and serialization without affecting spectral algorithms.

## Provenance

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Provenance records inspectable workflow lineage, not hidden model reasoning. A useful provenance record may include: - work-unit ID; - source object IDs; - input files or external sources; - transformation name; - timestamp; - producing agent/role; - replaced or superseded objects.

## Execution manifest

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Work is decomposed into bounded units with dependencies and statuses such as: Before work begins, dependencies should be complete unless the unit is explicitly exploratory. On completion: 1. persist semantic state; 2. persist derivative artifacts; 3. mark the unit complete; 4. record the last committed unit; 5. choose the next resume unit.

## Git and remote synchronization

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Project state, local Git history, and remote Git history are distinct. A typical sequence is: A state mutation can exist without a Git commit. A Git commit can exist locally without being pushed. Remote validation should compare commit hashes explicitly when exact synchronization matters.

## Human-facing documentation governance

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Documentation follows an inverse instructional architecture. For each human-facing document, canonical state records: - audience; - terminal reader state; - prerequisite state; - section objectives; - assigned instructional-trajectory moves; - representation task / acceptance evidence. Substantive prose is developed through the antagonistic drafting protocol in `project_state/EDITORIAL_DRAFTING_PROTOCOL.md`: Author/editor drafts are provenance artifacts. The synthesized document is the human-facing artifact. Documentation is not complete merely because every file contains text. It is complete when the surface supports the target reader state and matches actual implementation.

## Validation

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: State validation includes: - unique stable IDs; - valid relation endpoints; - valid execution dependencies; - synchronized state and manifest revisions; - explicit supersession for conflicting committed decisions. Documentation validation includes: - implementation/API fidelity; - no unimplemented feature claims; - correct conceptual prerequisite order; - runnable examples where promised; - explicit interpretive limits; - cross-document terminology consistency. Scientific-method validation includes: - preserving probe identity/order; - recording metric orientation; - interpreting filtration direction correctly; - using common control coordinates appropriately in cross-metric comparison; - ha

## Checkpoints

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: A checkpoint is valid when: - canonical state parses and validates; - manifest agrees with state revision; - completed units have their outputs; - no unit is falsely marked complete; - the next resume point is explicit. The project is complete only when release-required units are complete and final validation passes.
