# Section-Level Instructional Trajectory Map

This map decomposes each human-facing document into conceptually coherent sections and assigns the global instructional trajectory moves each section is responsible for accomplishing.

## Global trajectory moves

- **move_01 — Frame the interpretability problem:** Recognize Eigenflow as a controlled post hoc interpretability method for population-level relational structure rather than an automatic semantic explanation system.
- **move_02 — Establish the experimental object:** Understand probe population, layerwise representations, relational geometry, filtration, control scale, and structural observables as the core experimental chain.
- **move_03 — Design identifying probes:** Construct probe populations whose controlled contrasts make competing latent-feature hypotheses empirically distinguishable.
- **move_04 — Choose measurement geometry:** Choose representation reduction, metric, filtration, control coordinate, and sites in a way that matches the experimental question.
- **move_05 — Read structural observables:** Understand component, percolation, spectral, core/community, bridge, and factor-alignment outputs as distinct measurements of relational organization.
- **move_06 — Interpret across layer and scale:** Read Q(layer, control) as a developmental map of relational organization across network depth and structural scale.
- **move_07 — Apply inferential discipline:** Separate direct observation, candidate latent-feature inference, alternative explanations, robustness evidence, and unsupported claims.
- **move_08 — Demonstrate applied competence:** Design, execute, compare, interpret, and report a complete experiment with justified methodological choices and bounded conclusions.

## `README.md`

### 1. What Eigenflow is for
**Trajectory moves:** move_01

Establish the problem class and the package's epistemic role.

### 2. The experimental object
**Trajectory moves:** move_02

Introduce the complete population-level chain before syntax.

### 3. When Eigenflow is indicated
**Trajectory moves:** move_01, move_03

Connect research questions to probe-identifiable relational hypotheses.

### 4. Quick start: one complete experiment
**Trajectory moves:** move_02, move_04, move_05, move_08

Show the smallest end-to-end implementation with conceptual annotations.

### 5. How to read the first outputs
**Trajectory moves:** move_05, move_06, move_07

Teach observation before interpretation using one concrete result bundle.

### 6. What the choices mean
**Trajectory moves:** move_04

Explain sites, reducers, metrics, filtrations, analyses, and edge density.

### 7. What you may and may not conclude
**Trajectory moves:** move_07

Define evidential scope and central failure modes.

### 8. Where to go next
**Trajectory moves:** move_08

Route readers into design, spectral, percolation, interpretation, API, and PCSCS material.

## `docs/index.md`

### 1. Choose your path
**Trajectory moves:** move_01, move_08

Route users by role and goal.

### 2. Conceptual learning path
**Trajectory moves:** move_01, move_02, move_03, move_04, move_05, move_06, move_07, move_08

Expose the prerequisite order.

### 3. Task-based navigation
**Trajectory moves:** move_03, move_04, move_05, move_07, move_08

Route by experimental action.

### 4. Reference material
**Trajectory moves:** move_08

Separate instruction from technical reference.

## `docs/concepts/experimental_model.md`

### 1. The inverse problem
**Trajectory moves:** move_01, move_07

Define latent feature organization as unobserved and structural observables as evidence.

### 2. The population as the unit of analysis
**Trajectory moves:** move_02

Establish why the relational population, not one activation path, is primary.

### 3. From hypothesis to probe contrast
**Trajectory moves:** move_03

Translate semantic questions into distinguishable empirical hypotheses.

### 4. Probe factors and experimental control
**Trajectory moves:** move_03

Define manipulated, controlled, nuisance, and observational variables.

### 5. Factorial and matched designs
**Trajectory moves:** move_03, move_08

Teach concrete probe construction patterns.

### 6. Predicting structural outcomes
**Trajectory moves:** move_03, move_05, move_07

Require pre-analysis predictions tied to observables.

### 7. Confounds and competing explanations
**Trajectory moves:** move_07

Enumerate design- and measurement-level alternatives.

### 8. Robustness as part of the experiment
**Trajectory moves:** move_04, move_07, move_08

Plan metric/reducer/probe/resampling checks.

### 9. Worked inverse-problem examples
**Trajectory moves:** move_03, move_04, move_05, move_06, move_07, move_08

Integrate design through bounded inference.

## `docs/concepts/percolation.md`

### 1. Why graph growth is useful
**Trajectory moves:** move_05

Motivate percolation-style observables for representation filtrations.

### 2. Control direction and graph growth
**Trajectory moves:** move_04, move_05

Relate parameter orientation to edge addition/removal.

### 3. Native threshold and edge density
**Trajectory moves:** move_04, move_06

Explain comparable control coordinates.

### 4. Giant-component fraction
**Trajectory moves:** move_05, move_06

Teach P∞ as global coalescence observable.

### 5. Second-largest component
**Trajectory moves:** move_05, move_06

Teach competing large-scale structure.

### 6. Susceptibility
**Trajectory moves:** move_05, move_06

Teach mesoscale organization and peak interpretation.

### 7. Cluster-size distributions
**Trajectory moves:** move_05, move_06

Teach fragmentation/hierarchy signatures.

### 8. Merge jumps and bridge probes
**Trajectory moves:** move_05, move_07

Connect structural transitions to pivotal samples.

### 9. Factor-conditioned percolation
**Trajectory moves:** move_03, move_05, move_06, move_07

Relate graph growth to semantic factors.

### 10. Finite-size analysis
**Trajectory moves:** move_07

Assess sample-dependence versus stable behavior.

### 11. Criticality language and limits
**Trajectory moves:** move_07

Bound statistical-physics claims.

### 12. Worked neural-network interpretation
**Trajectory moves:** move_05, move_06, move_07, move_08

Synthesize multiple curves in context.

## `docs/concepts/spectral_analysis.md`

### 1. Why spectra add information
**Trajectory moves:** move_05

Motivate global operator-level structure beyond components.

### 2. Choosing a graph operator
**Trajectory moves:** move_04, move_05

Map operators to distinct structural questions.

### 3. Eigenvalue observables
**Trajectory moves:** move_05

Explain radius, connectivity, gaps, entropy, energy, effective rank.

### 4. Eigenvectors and eigenspaces
**Trajectory moves:** move_05, move_07

Interpret structural modes without reifying coordinates.

### 5. Localization and IPR
**Trajectory moves:** move_05, move_07

Distinguish distributed from probe-localized structure.

### 6. Spectral flow across the control parameter
**Trajectory moves:** move_05, move_06

Teach trajectories rather than isolated spectra.

### 7. Spectral flow across network depth
**Trajectory moves:** move_06

Interpret emergence/change through layers.

### 8. Crossings, degeneracy, and correspondence
**Trajectory moves:** move_05, move_07

Prevent naive eigenvector-index interpretations.

### 9. Numerical scope and solver choices
**Trajectory moves:** move_04, move_07

Relate computation to trustworthy measurement.

### 10. Connecting spectra to probe hypotheses
**Trajectory moves:** move_03, move_05, move_07

Make spectral interpretation experimentally grounded.

### 11. Worked triangulated example
**Trajectory moves:** move_05, move_06, move_07, move_08

Combine spectra with topology and factor alignment.

## `docs/guides/vgg16_probe_experiment.md`

### 1. Question and hypothesis
**Trajectory moves:** move_01, move_03

Start from an interpretability claim that the probe can test.

### 2. Model and preprocessing
**Trajectory moves:** move_02, move_04

Make representation generation reproducible.

### 3. Build the probe population
**Trajectory moves:** move_03

Construct controlled image factors and metadata.

### 4. Inspect and choose VGG16 sites
**Trajectory moves:** move_02, move_04

Connect PyTorch modules to representational stages.

### 5. Choose representation reduction
**Trajectory moves:** move_04, move_07

Explain flattening/pooling consequences.

### 6. Choose metric and filtration
**Trajectory moves:** move_04

Justify geometry and control scale.

### 7. Run the analyses
**Trajectory moves:** move_05, move_08

Execute the configured experiment.

### 8. Navigate the result object
**Trajectory moves:** move_05, move_08

Retrieve actual outputs correctly.

### 9. Visualize layer × control behavior
**Trajectory moves:** move_06

See the population sequence across depth and scale.

### 10. Interpret the outputs
**Trajectory moves:** move_07

Write observation/inference/alternatives/not-supported.

### 11. Stress-test the interpretation
**Trajectory moves:** move_04, move_07, move_08

Repeat with alternate measurement choices.

### 12. Save and reproduce
**Trajectory moves:** move_08

Preserve provenance and rerunability.

## `docs/guides/interpreting_results.md`

### 1. The interpretation protocol
**Trajectory moves:** move_07

Establish observation → inference → alternatives → unsupported claim.

### 2. Connected components and merge structure
**Trajectory moves:** move_05, move_06, move_07

Interpret coherence, fragmentation, merge order, and bridges.

### 3. Percolation observables
**Trajectory moves:** move_05, move_06, move_07

Interpret graph-growth patterns.

### 4. Spectral observables
**Trajectory moves:** move_05, move_06, move_07

Interpret operator-level structure and modes.

### 5. Factor and class alignment
**Trajectory moves:** move_03, move_05, move_07

Relate structural patterns to controlled variables.

### 6. Cores, communities, and bridge probes
**Trajectory moves:** move_05, move_07

Interpret robustness and pivotal examples.

### 7. Transition summaries
**Trajectory moves:** move_05, move_06, move_07

Treat transition detectors as summaries, not semantics.

### 8. Convergent evidence
**Trajectory moves:** move_05, move_07

Combine complementary observables.

### 9. Divergent evidence
**Trajectory moves:** move_07

Diagnose disagreement rather than average it away.

### 10. Robustness and sensitivity
**Trajectory moves:** move_04, move_07

Assess dependence on design and measurement choices.

### 11. Writing a bounded conclusion
**Trajectory moves:** move_07, move_08

Produce a human-interpretable feature claim with evidential qualifiers.

### 12. Failure modes
**Trajectory moves:** move_07, move_08

Recognize experiments that do not identify the intended feature question.

## `examples/basic_mlp.py`

### 1. Example objective
**Trajectory moves:** move_01

State what the executable example demonstrates.

### 2. Deterministic probe population
**Trajectory moves:** move_02, move_03

Construct a population with interpretable metadata.

### 3. Inspect representation sites
**Trajectory moves:** move_02

Show where population representations are captured.

### 4. Configure metric and filtration
**Trajectory moves:** move_04

Tie code choices to the measurement geometry.

### 5. Run structural analyses
**Trajectory moves:** move_05, move_08

Demonstrate the actual callable pipeline.

### 6. Inspect outputs
**Trajectory moves:** move_05, move_06

Retrieve meaningful values across sites/control.

### 7. Interpret and modify
**Trajectory moves:** move_07, move_08

Explain bounds and invite one controlled variation.

## `examples/pcscs_compatibility.py`

### 1. PCSCS as a special case
**Trajectory moves:** move_01, move_02

Map the old method into the general framework.

### 2. Run the PCSCS preset
**Trajectory moves:** move_08

Provide deterministic compatibility syntax.

### 3. Expand the preset
**Trajectory moves:** move_04

Expose cosine, threshold filtration, and component analysis explicitly.

### 4. Inspect PCSCS outputs
**Trajectory moves:** move_05, move_06

Retrieve layerwise merge/component results.

### 5. Add spectral/percolation analyses
**Trajectory moves:** move_05, move_08

Demonstrate the generalization beyond PCSCS.

### 6. Interpret continuity and limits
**Trajectory moves:** move_07

Clarify what transfers from PCSCS interpretation.

## `docs/spec/API_SPEC.md`

### 1. Scope and stability
**Trajectory moves:** move_08

Define the supported public surface.

### 2. Experiment
**Trajectory moves:** move_02, move_04, move_08

Give exact orchestration syntax and semantics.

### 3. ProbePopulation
**Trajectory moves:** move_03, move_08

Specify construction/design APIs.

### 4. Extraction and site selection
**Trajectory moves:** move_02, move_04, move_08

Specify model-boundary APIs.

### 5. Reducers and representation transforms
**Trajectory moves:** move_04, move_08

Specify feature-vector construction.

### 6. Metrics
**Trajectory moves:** move_04, move_08

Specify orientation/configuration/extension.

### 7. Filtrations
**Trajectory moves:** move_04, move_08

Specify control semantics and snapshots.

### 8. Operators
**Trajectory moves:** move_05, move_08

Specify spectral operator APIs.

### 9. Analyses and keywords
**Trajectory moves:** move_05, move_08

Specify available analyses and config mappings.

### 10. Results and serialization
**Trajectory moves:** move_05, move_08

Specify navigation/persistence behavior.

### 11. Visualization
**Trajectory moves:** move_06, move_08

Specify supported visualization calls.

### 12. Extension protocols
**Trajectory moves:** move_08

Specify custom component contracts.

### 13. Errors and validation
**Trajectory moves:** move_07, move_08

Specify misuse/failure behavior.

## `docs/spec/DATA_MODEL_SPEC.md`

### 1. End-to-end object chain
**Trajectory moves:** move_02, move_08

Define the persistent computational objects.

### 2. Probe identity and ordering
**Trajectory moves:** move_03, move_08

Preserve population semantics.

### 3. Representation shapes
**Trajectory moves:** move_02, move_04, move_08

Specify raw/reduced dimensions.

### 4. Relational matrices
**Trajectory moves:** move_04, move_08

Specify metric orientation and metadata.

### 5. Filtration snapshots
**Trajectory moves:** move_04, move_05, move_08

Specify graph-family state.

### 6. Analysis payloads
**Trajectory moves:** move_05, move_08

Specify result structures by family.

### 7. Provenance
**Trajectory moves:** move_07, move_08

Specify lineage required for interpretation/reproduction.

### 8. Persistence and reconstruction
**Trajectory moves:** move_08

Specify actual save/load behavior.

### 9. Schema evolution
**Trajectory moves:** move_08

Specify compatibility/migrations.

### 10. Concrete serialized example
**Trajectory moves:** move_05, move_08

Make the hierarchy inspectable.

## `docs/spec/EXECUTION_SPEC.md`

### 1. Current execution path
**Trajectory moves:** move_02, move_08

Describe actual ordering.

### 2. Computational dependency graph
**Trajectory moves:** move_04, move_05, move_08

Show what depends on what.

### 3. Reuse within a run
**Trajectory moves:** move_08

Explain actual reuse semantics.

### 4. Invalidation by configuration change
**Trajectory moves:** move_04, move_08

Connect experimental choices to recomputation.

### 5. Batching, device, and model state
**Trajectory moves:** move_02, move_04, move_08

Specify execution boundary.

### 6. Failure and partial results
**Trajectory moves:** move_08

Specify failure semantics.

### 7. Performance model
**Trajectory moves:** move_04, move_05, move_08

Explain computational scaling.

### 8. Caching: current versus planned
**Trajectory moves:** move_08

Avoid overstating implementation.

### 9. Worked recomputation cases
**Trajectory moves:** move_04, move_08

Demonstrate dependency reasoning.

## `CONTRIBUTING.md`

### 1. Development setup
**Trajectory moves:** move_08

Make contribution environment reproducible.

### 2. Repository architecture
**Trajectory moves:** move_02, move_08

Orient contributors to subsystem boundaries.

### 3. Adding a metric
**Trajectory moves:** move_04, move_08

Concrete extension recipe.

### 4. Adding a filtration
**Trajectory moves:** move_04, move_08

Concrete extension recipe.

### 5. Adding an operator or analysis
**Trajectory moves:** move_05, move_08

Concrete extension recipe.

### 6. Testing and numerical validation
**Trajectory moves:** move_07, move_08

Require evidence for correctness.

### 7. Scientific documentation requirements
**Trajectory moves:** move_07, move_08

Require indications and interpretive limits.

### 8. Persistent-state workflow
**Trajectory moves:** move_08

Explain project governance.

### 9. Pull-request checklist
**Trajectory moves:** move_08

Operational acceptance criteria.

## `CHANGELOG.md`

### 1. Release summary
**Trajectory moves:** move_08

Expose release identity/stability.

### 2. Added
**Trajectory moves:** move_08

List new user-visible capabilities.

### 3. Changed
**Trajectory moves:** move_04, move_05, move_07, move_08

Surface changes that alter behavior or interpretation.

### 4. Fixed
**Trajectory moves:** move_08

Record correctness repairs.

### 5. Deprecated and removed
**Trajectory moves:** move_08

Support migration.

### 6. Known limitations
**Trajectory moves:** move_07

Expose current evidential/implementation boundaries.

### 7. Scientific interpretation changes
**Trajectory moves:** move_07, move_08

Flag changes affecting comparability or meaning.

## `SECURITY.md`

### 1. Supported versions
**Trajectory moves:** move_08

State support boundary.

### 2. Reporting a vulnerability
**Trajectory moves:** move_08

Provide an actionable route.

### 3. Model and serialization trust boundary
**Trajectory moves:** move_07, move_08

Explain untrusted artifact risks.

### 4. Custom callable boundary
**Trajectory moves:** move_07, move_08

Explain arbitrary-code risk.

### 5. Resource exhaustion
**Trajectory moves:** move_04, move_08

Explain expensive workloads.

### 6. Sensitive probe data
**Trajectory moves:** move_03, move_08

Explain data-handling responsibility.

### 7. Disclosure process
**Trajectory moves:** move_08

Set expectations.

## `CODE_OF_CONDUCT.md`

### 1. Our standards
**Trajectory moves:** move_08

Define expected conduct.

### 2. Unacceptable behavior
**Trajectory moves:** move_08

Define prohibited behavior.

### 3. Scientific disagreement
**Trajectory moves:** move_07, move_08

Anchor disagreement in evidence and reproducibility.

### 4. Scope
**Trajectory moves:** move_08

Define applicability.

### 5. Reporting and enforcement
**Trajectory moves:** move_08

Define process.

## `CITATION.cff`

### 1. Software identity
**Trajectory moves:** move_08

Encode canonical package identity.

### 2. Release identity
**Trajectory moves:** move_08

Encode version/date.

### 3. Archival identity
**Trajectory moves:** move_08

Encode DOI if present.

### 4. Preferred citation
**Trajectory moves:** move_08

Support accurate citation.

## `LICENSE`

### 1. License grant
**Trajectory moves:** move_08

Preserve legal terms.

### 2. Ownership metadata consistency
**Trajectory moves:** move_08

Keep holder/year consistent elsewhere.

## `pyproject.toml`

### 1. Build system
**Trajectory moves:** move_08

Specify build backend.

### 2. Runtime requirements
**Trajectory moves:** move_08

Specify compatibility.

### 3. Project metadata
**Trajectory moves:** move_01, move_08

Expose concise indication/identity.

### 4. Project URLs
**Trajectory moves:** move_08

Route users to docs/issues/source.

### 5. Optional dependency groups
**Trajectory moves:** move_08

Expose install variants.

### 6. Development tooling
**Trajectory moves:** move_08

Configure tests/lint/type tools if adopted.

## `project_state/STATE_PROTOCOL.md`

### 1. Purpose and scope
**Trajectory moves:** move_08

Separate project-development state from scientific experiment state.

### 2. Authority
**Trajectory moves:** move_08

Define canonical sources.

### 3. Mutation cycle
**Trajectory moves:** move_08

Define durable change workflow.

### 4. Schema evolution
**Trajectory moves:** move_08

Define migration.

### 5. Execution manifest
**Trajectory moves:** move_08

Define interruption/resumption.

### 6. Git and remote synchronization
**Trajectory moves:** move_08

Separate state mutation, local commit, and push.

### 7. Human-facing documentation governance
**Trajectory moves:** move_01, move_07, move_08

Persist instructional objectives, audits, and acceptance criteria.
