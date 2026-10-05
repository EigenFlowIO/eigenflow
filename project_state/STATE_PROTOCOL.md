# Eigenflow Persistent State Management Protocol

## 1. Authority

`project_state.json` is the canonical semantic state of the Eigenflow project.

`execution_manifest.json` is the canonical execution/resumption state.

Derivative documents, implementation files, diagrams, examples, and prose summaries are subordinate artifacts. They may explain or instantiate canonical state, but they do not override it unless their content is explicitly committed back into `project_state.json`.

The originating conversation is provenance for initialization only. After initialization, conversational context is temporary working memory and is not authoritative over committed project state.

## 2. Work-cycle protocol

Every substantial work cycle follows this sequence:

1. Read the relevant portions of `project_state.json` and `execution_manifest.json`.
2. Identify the intended operation and the bounded execution unit.
3. Identify affected objects, relations, decisions, dependencies, outputs, and invariants.
4. Construct proposed changes in working memory or temporary artifacts.
5. Validate the proposal against current committed state.
6. Commit semantic changes to `project_state.json`.
7. Update execution status in `execution_manifest.json`.
8. Generate or revise only derivative artifacts affected by the committed changes.
9. Record provenance and completion state.
10. Set the next resumable unit.

A work cycle is not complete until the canonical state and execution manifest agree about what was committed.

## 3. Object identity

Durable semantic objects receive stable identifiers when they may be referenced, depended upon, revised, compared, or cited by provenance.

Identifiers should be opaque enough to survive renaming. Current conventions use prefixes such as:

- `proj_` project
- `scope_` scope
- `sc_` success criterion
- `con_` constraint
- `term_` terminology
- `obj_` domain object or abstraction
- `rel_` relation
- `dec_` decision
- `asm_` assumption
- `q_` unresolved question
- `out_` planned output
- `prov_` provenance record
- `unit_` execution unit

New prefixes may be introduced when a new durable object class becomes useful.

Renaming a human-readable label does not change the stable identifier.

## 4. Ordinary state mutation

An ordinary state mutation changes values within the existing semantic structure without redefining the schema.

Examples:

- changing an unresolved question from `open` to `resolved`;
- adding a new decision;
- revising a scope item;
- adding a dependency edge;
- changing an output from `pending` to `complete`;
- updating a description or rationale.

Ordinary mutations must:

1. identify affected IDs;
2. preserve stable IDs unless object identity genuinely changes;
3. update dependent relations if needed;
4. increment `execution.state_revision`;
5. add provenance sufficient to identify the work cycle responsible.

## 5. Structural/schema evolution

Schema evolution is legitimate and expected.

Structural change includes:

- adding a new top-level collection;
- introducing a new durable object type;
- adding relation classes;
- splitting one concept into multiple object types;
- replacing a field with a better structured representation;
- introducing validation invariants;
- changing how dependencies or provenance are represented.

Schema changes require a migration operation with:

- a migration ID;
- previous and new schema versions;
- rationale;
- affected object classes;
- migration steps;
- backfill rules;
- compatibility notes;
- validation checks.

Prefer additive evolution first. Deprecate old fields before removal when persisted state or derivative artifacts may depend on them.

Do not restart the project merely because the schema evolves.

## 6. Provisional versus stable structures

New concepts may enter state with status `provisional`.

A provisional object may become:

- `committed` or `stable` when accepted;
- `revised` when replaced or materially changed;
- `deprecated` when retained for historical compatibility but no longer used;
- `superseded` when another object explicitly replaces it;
- `rejected` when evaluated and not adopted.

Supersession should be represented explicitly by a relation or field identifying the replacement object.

## 7. Dependency tracking

Dependencies must be explicit whenever a downstream object or artifact could become invalid after an upstream change.

Dependencies may exist among:

- semantic objects;
- implementation modules;
- execution units;
- analysis outputs;
- derivative documents;
- generated visualizations;
- serialized results.

The execution manifest records unit dependencies. Project state may additionally record semantic dependency relations.

When an upstream object changes:

1. identify dependents;
2. classify impact as `none`, `review`, `invalidate`, or `regenerate`;
3. revise only affected dependents;
4. avoid regenerating unaffected completed work.

## 8. Provenance

Provenance records external workflow lineage, not hidden model reasoning.

Where useful, a durable or derived object should record:

- creating work unit;
- source object IDs;
- source files or external sources;
- transformation or operation name;
- timestamp;
- author/agent;
- relevant configuration;
- replaced or superseded object IDs.

Derived artifacts should be traceable to the state objects and decisions that produced them.

## 9. Derivative artifacts

Derivative artifacts include implementation specifications, documentation, code, diagrams, examples, tests, reports, and release artifacts.

Each important derivative artifact should identify:

- artifact ID or path;
- source state revision;
- dependencies;
- producing execution unit;
- status;
- whether it is canonical or derivative.

Artifacts are regenerated only when their dependencies change materially.

Changes made directly in a derivative artifact are not durable project decisions until reflected back into canonical state.

## 10. Execution manifest and resumption

`execution_manifest.json` tracks bounded units of work.

Every unit records:

- stable unit ID;
- title;
- status;
- dependencies;
- intended outputs;
- optional affected state IDs.

Allowed statuses are initially:

- `pending`
- `in_progress`
- `blocked`
- `complete`
- `invalidated`

Before starting a unit:

- all required dependencies must be complete, unless the unit is explicitly exploratory;
- set the unit to `in_progress`;
- set `current_unit`.

On successful completion:

- commit semantic state changes;
- persist derivative artifacts;
- set the unit to `complete`;
- set `last_committed_unit`;
- choose `resume_unit`;
- clear `current_unit`.

After interruption, resume from `current_unit` if it contains uncommitted recoverable work; otherwise resume from `resume_unit`.

Completed valid units are not rerun merely because the conversation has restarted.

## 11. Inconsistency handling

An inconsistency exists when canonical state contains incompatible claims, broken references, invalid dependency edges, conflicting committed decisions, or manifest/state disagreement.

On detection:

1. do not silently choose one side;
2. identify the conflicting object IDs;
3. determine whether one object supersedes another;
4. resolve through an explicit mutation or migration;
5. record provenance;
6. invalidate affected dependents if necessary.

If the inconsistency does not block current work, record it as an unresolved question or validation issue and continue with unaffected units.

## 12. Validation

Before a work unit is considered complete, perform validation appropriate to the unit.

State validation includes:

- unique stable IDs;
- all relation endpoints exist;
- dependency references resolve;
- committed decisions do not directly contradict one another without an explicit supersession relation;
- required project fields remain present;
- execution manifest and state revision agree;
- completed outputs exist when they are file artifacts.

Implementation validation will later include:

- import/package checks;
- unit tests;
- integration tests;
- regression tests;
- deterministic fixture tests where appropriate;
- numerical invariants;
- provenance serialization checks.

Scientific-method validation includes:

- separating observation from interpretation;
- recording metric orientation and filtration direction;
- preserving probe IDs across transformations;
- ensuring cross-metric comparisons use a legitimate common coordinate such as edge density when required;
- treating eigenspace degeneracy correctly;
- avoiding unqualified criticality claims from descriptive transition statistics.

## 13. Change propagation

When an object changes, downstream impact should be determined from explicit dependencies rather than re-inferred from prose.

Examples:

- changing the `Metric` protocol may invalidate API specification, metric implementations, experiment orchestration, tests, and documentation;
- changing the canonical result hierarchy may invalidate serialization, visualization access paths, examples, and documentation;
- changing only a visualization label should not invalidate numerical analysis;
- changing a probe metadata schema may require factor-analysis and serialization review but not graph spectral algorithms.

Selective propagation is preferred over global regeneration.

## 14. Completion and checkpoints

A checkpoint is a committed state revision at which:

- state validates;
- the manifest is synchronized;
- completed units have their outputs persisted;
- no unit is falsely marked complete;
- the next resume point is known.

The project is complete only when the canonical completion fields and the manifest both indicate completion of the required release units and final validation has passed.

## 15. State-file editing discipline

Use deterministic structured edits whenever possible.

For JSON:

- preserve stable IDs;
- avoid wholesale reformatting solely for cosmetic reasons;
- prefer append/update operations over reconstruction when practical;
- validate JSON syntax after every commit.

When a schema migration is required, create a migration record before or together with the migrated state.

## 16. Initial invariants

The following invariants are active immediately:

1. `project_state.json` is canonical.
2. `execution_manifest.json` is authoritative for execution progress.
3. Every `relations[*].source` and `relations[*].target` must resolve to a durable object ID.
4. Every execution dependency must resolve to a unit ID.
5. PCSCS is represented as a special case of Eigenflow, not as the general architecture.
6. Post-extraction analyses operate on representation populations and must not depend on model-architecture-specific behavior.
7. Probe-population organization is the primary analytical level; single-probe trajectories are secondary diagnostics.
8. v1 is intended to be conceptually complete.
9. Interpretation remains the experimenter's inference from controlled structural evidence.
10. Schema evolution is allowed through controlled migration rather than project restart.
