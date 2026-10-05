# Human-Facing Content Dependency Map

Status: instructional objectives established; prose development not yet performed.

Each document is treated as an instructional instrument. Its objective is defined as a terminal reader state, then backstepped into finer section objectives. Sections should be written only if they establish a prerequisite belief, skill, distinction, or evidential judgment required by the document's terminal state.

## Common section contract

Where a section teaches a scientific or analytical object, it should answer, as applicable: **why this object is needed; what it represents; when it is indicated; how to invoke it; what output it produces; how to read that output; what inference it may support; what alternatives remain; and what it does not establish.**

## `README.md`

**Audience:** first-encounter analyst or NN systems architect

**Terminal reader state:** Reader can determine whether Eigenflow is relevant, understand its experimental object and evidential scope, install it, run a minimal experiment, locate the right deeper documentation, and avoid the most important category errors.

**Prerequisite state:** General competence with Python/PyTorch and neural-network layers; no Eigenflow-specific knowledge.

**Backstepped section objectives:**

1. **Problem and indication.** Recognize the class of interpretability questions Eigenflow can address and distinguish them from neuron attribution, saliency, causal intervention, or automatic semantic labeling.
2. **Core experimental object.** Represent the method as probe population → layerwise representations → relational geometry → filtration → structural observables → bounded inference.
3. **When to use / not use.** Decide whether a proposed question has a controllable probe contrast and whether relational population structure is relevant evidence.
4. **Minimal worked experiment.** Execute a small complete experiment whose code mirrors the conceptual pipeline.
5. **Reading the result.** Retrieve at least one component/percolation/spectral/factor output and state what is directly observed.
6. **First interpretation.** Translate the observation into one candidate latent-feature inference, one alternative explanation, and one unsupported claim.
7. **Configuration map.** Know why probe design, reducer, metric, filtration, analysis, and layer selection are experimental choices rather than arbitrary syntax.
8. **Navigation.** Know which document to read next for experiment design, spectral analysis, percolation, VGG16, results interpretation, API, or PCSCS.

**Representation task / acceptance evidence:** Given a candidate interpretability question, explain whether Eigenflow is indicated, run the quick start, and produce a four-part observation/inference/alternative/not-supported statement.

## `docs/index.md`

**Audience:** all documentation users

**Terminal reader state:** Reader can choose an instructional path appropriate to role and current knowledge without encountering concepts before their prerequisites.

**Prerequisite state:** Recognition that Eigenflow is an interpretability toolkit.

**Backstepped section objectives:**

1. **Orientation paths.** Route first-time analysts, PCSCS users, contributors, and researchers to different entry sequences.
2. **Concept dependency map.** Expose the recommended order: experimental model → measurement geometry → structural observables → execution → interpretation.
3. **Task-based navigation.** Route by goal: design probes, choose metric, choose filtration, inspect spectra, interpret results, compare models, extend package.
4. **Reference navigation.** Separate conceptual instruction from API/specification/reference material.

**Representation task / acceptance evidence:** Select and justify a reading path for a stated user goal.

## `docs/concepts/experimental_model.md`

**Audience:** analyst designing an experiment

**Terminal reader state:** Reader can formulate a controlled post hoc interpretability experiment whose probe design makes competing hypotheses about latent feature organization empirically distinguishable.

**Prerequisite state:** Population-level relational organization is understood as the unit of analysis.

**Backstepped section objectives:**

1. **Interpretability as inverse inference.** Distinguish latent feature hypotheses from directly measured structural observables.
2. **Hypothesis formulation.** Express at least two competing hypotheses that predict different relational outcomes.
3. **Probe factors and metadata.** Identify manipulated, controlled, nuisance, and observational factors.
4. **Factorial and matched designs.** Construct contrasts that isolate a semantic variable.
5. **Population adequacy.** Reason about balance, coverage, replication, sample size, and representativeness.
6. **Predicted structural outcomes.** State before analysis what patterns would count as evidence under each hypothesis.
7. **Confounds and alternative explanations.** List probe, model, metric, reducer, and sampling explanations that could mimic the predicted pattern.
8. **Robustness plan.** Specify cross-metric, cross-reducer, resampling, or alternate-probe checks.
9. **Worked experiments.** Carry two hypotheses from design through predicted outputs and bounded conclusions.

**Representation task / acceptance evidence:** Design a probe population for a feature question and write competing predictions and robustness checks before running Eigenflow.

## `docs/concepts/percolation.md`

**Audience:** analyst choosing or interpreting graph-growth observables

**Terminal reader state:** Reader can select and interpret percolation-style observables as descriptions of how representation-induced connectivity reorganizes across a control sweep without making unjustified phase-transition claims.

**Prerequisite state:** Metric-induced relational matrix and filtration/control parameter are understood.

**Backstepped section objectives:**

1. **Graph-growth orientation.** Understand which direction of the control parameter adds edges and why orientation matters.
2. **Native threshold vs edge density.** Choose an interpretable control coordinate and understand cross-metric comparability.
3. **Giant component.** Explain what P∞ measures and what early/late growth can indicate.
4. **Second-largest component.** Interpret competing macroscopic group structure near mergers.
5. **Susceptibility.** Interpret mesoscale cluster organization and peaks without equating them automatically with criticality.
6. **Cluster-size distribution.** Recognize fragmented, hierarchical, and dominant-group regimes.
7. **Jumps and merge events.** Relate abrupt graph changes to specific bridge relations or probes.
8. **Factor-conditioned percolation.** Use class/factor-specific coherence and mixing behavior as experimental evidence.
9. **Finite-size analysis.** Distinguish sample-specific crossover from stable population behavior.
10. **Interpretation limits.** Separate descriptive transition language from thermodynamic criticality/universality.
11. **Worked neural example.** Read several curves jointly and form a bounded representational interpretation.

**Representation task / acceptance evidence:** Given percolation curves from two layers, explain the structural differences, identify plausible feature implications, and specify what cannot be claimed.

## `docs/concepts/spectral_analysis.md`

**Audience:** analyst choosing or interpreting graph spectra

**Terminal reader state:** Reader can choose an operator and spectral observable for a specific structural question, track spectral organization across control scale/layer depth, and interpret the result with eigenspace and numerical caveats.

**Prerequisite state:** Graph filtration and population-level relational structure are understood.

**Backstepped section objectives:**

1. **Why spectra.** Connect spectral quantities to global organization not easily captured by components alone.
2. **Operator choice.** Distinguish adjacency, Laplacian, normalized Laplacian, random-walk, modularity, and non-backtracking questions.
3. **Eigenvalues as observables.** Interpret radius, algebraic connectivity, gaps, entropy, energy, effective rank.
4. **Eigenvectors/eigenspaces.** Interpret modes, partitions, and factor alignment.
5. **Localization.** Use IPR/localization to distinguish distributed structure from a few influential probes.
6. **Trajectories over control scale.** Understand eigenvalue flow rather than isolated spectra.
7. **Trajectories across depth.** Interpret when spectral organization emerges or changes through the network.
8. **Crossings and degeneracy.** Use overlap/principal-angle reasoning instead of naive eigenvector index identity.
9. **Numerical scope.** Understand full vs partial spectra, sparse solvers, scale, and instability.
10. **Experimental interpretation.** Tie spectral patterns to controlled probe hypotheses and alternative explanations.
11. **Worked example.** Triangulate spectral evidence with components/percolation/factor alignment.

**Representation task / acceptance evidence:** Choose an operator/observable for a stated hypothesis and interpret a hypothetical trajectory with one alternative explanation and one robustness check.

## `docs/guides/vgg16_probe_experiment.md`

**Audience:** first-time practitioner with image probes

**Terminal reader state:** Reader can perform a reproducible VGG16 experiment from raw images through site selection, representation reduction, filtration analyses, result navigation, visualization, and bounded interpretation.

**Prerequisite state:** Basic Eigenflow conceptual model and PyTorch familiarity.

**Backstepped section objectives:**

1. **Experimental question.** Begin with a concrete feature hypothesis rather than code.
2. **Environment and model.** Install dependencies, load pretrained VGG16, set eval/device, document preprocessing.
3. **Probe population.** Build stable IDs and metadata with a controlled contrast.
4. **Inspect representation sites.** Use available_sites and choose meaningful block endpoints.
5. **Reducer comparison.** Compare flatten vs global average and state what each preserves/discards.
6. **Metric and filtration choice.** Justify cosine/native threshold or edge density for the demonstration.
7. **Run analyses.** Execute components, percolation, spectra, factor alignment, transitions.
8. **Navigate results.** Use exact syntax to access layerwise outputs.
9. **Visualize.** Plot at least one layer×control observable and one spectral/percolation trajectory.
10. **Interpret.** Produce observation → inference → alternatives → unsupported claim.
11. **Robustness.** Repeat with an alternate reducer/metric or resample probes.
12. **Persist/reproduce.** Save outputs/configuration and document batching/device/performance.

**Representation task / acceptance evidence:** Reproduce the guide and write a defensible conclusion about where a controlled image factor becomes relationally organized in VGG16.

## `docs/guides/interpreting_results.md`

**Audience:** analyst after running an experiment

**Terminal reader state:** Reader can convert Eigenflow outputs into calibrated, human-interpretable evidence statements and triangulate across observables and robustness checks.

**Prerequisite state:** Experiment design, filtration, and major observable families are understood.

**Backstepped section objectives:**

1. **Interpretation protocol.** Apply observation → candidate inference → alternatives → unsupported claim.
2. **Components and merge structure.** Read coherence, fragmentation, merge order, bridge samples.
3. **Percolation outputs.** Read giant/second component, susceptibility, size distributions, transition regions.
4. **Spectral outputs.** Read gaps, algebraic connectivity, localization, eigenspace alignment and flow.
5. **Factor/class outputs.** Read within/between structure, NMI/ARI, coherence/mixing, spectral alignment.
6. **Cores/communities/bridges.** Interpret robust centers, partitions, and pivotal probes.
7. **Transition outputs.** Treat transition detectors as summaries of observable changes, not semantic events by themselves.
8. **Convergent evidence.** Combine observables that answer different structural questions.
9. **Divergent evidence.** Diagnose when observables disagree rather than averaging them away.
10. **Robustness and alternatives.** Use metric/reducer/filtration/resampling/probe changes to test dependence.
11. **Writing the conclusion.** Produce a bounded feature-interpretation statement tied explicitly to design.
12. **Failure cases.** Recognize weak, confounded, unstable, or non-identifying experiments.

**Representation task / acceptance evidence:** Given a multi-observable result bundle, produce a short interpretation with explicit evidential support, alternatives, and uncertainty.

## `examples/basic_mlp.py`

**Audience:** first-time code reader

**Terminal reader state:** Reader can map executable code line-by-line onto the conceptual experiment and inspect meaningful outputs instead of treating the library as a black box.

**Prerequisite state:** README orientation.

**Backstepped section objectives:**

1. **Deterministic setup.** Create a reproducible model/probe population.
2. **Probe metadata.** Show why metadata exists and how it supports factor analysis.
3. **Site inspection.** Demonstrate the extraction boundary.
4. **Experiment construction.** Map each constructor argument to an experimental choice.
5. **Result access.** Print specific observables from multiple layers/control values.
6. **Interpretive comments.** Explain what the example's outputs could and could not support.
7. **Optional visualization.** Produce a simple plot or structured output for inspection.

**Representation task / acceptance evidence:** Modify one experimental choice, predict the consequence, rerun, and identify the changed output.

## `examples/pcscs_compatibility.py`

**Audience:** existing PCSCS user

**Terminal reader state:** Reader can reproduce PCSCS behavior in Eigenflow, understand the mapping from PCSCS concepts to general Eigenflow abstractions, and know how to extend beyond cosine/component-centric analysis.

**Prerequisite state:** Familiarity with PCSCS.

**Backstepped section objectives:**

1. **Compatibility claim.** State exactly what the preset reproduces and where behavior differs.
2. **Deterministic example.** Run a repeatable PCSCS preset.
3. **Expanded equivalent configuration.** Show the underlying metric, filtration, extraction, and analyses explicitly.
4. **PCSCS outputs.** Retrieve convergence/critical/component trajectories per layer.
5. **Spectral extension.** Show how Eigenflow exposes richer spectral tools.
6. **Migration path.** Translate an existing PCSCS workflow into general Eigenflow configuration.
7. **Interpretation continuity.** Explain which prior PCSCS interpretations remain valid and which require broader qualification.

**Representation task / acceptance evidence:** Convert a PCSCS preset run into an explicit Experiment configuration and add one non-PCSCS analysis.

## `docs/spec/API_SPEC.md`

**Audience:** advanced user, extension author, maintainer

**Terminal reader state:** Reader can write correct code against the public API without inspecting source and can distinguish stable public behavior from internal implementation.

**Prerequisite state:** Conceptual model is already understood; this is reference, not first instruction.

**Backstepped section objectives:**

1. **Public surface and stability.** Define supported imports, aliases, and stability expectations.
2. **Experiment signature.** Exact parameters, defaults, types, exceptions, result semantics.
3. **Probe APIs.** Exact constructors, metadata rules, IDs, design helpers.
4. **Extraction APIs.** Exact site selection, reducers, batching/device/raw activation semantics.
5. **Metric protocol and built-ins.** Exact orientation, output shape, config, extension requirements.
6. **Filtration protocol and built-ins.** Exact control parameter semantics and snapshot guarantees.
7. **Operators and analyses.** Exact object/keyword mappings and configuration interfaces.
8. **Results and serialization.** Exact navigation, save/load behavior actually implemented.
9. **Visualization.** Exact callable surface and accepted result inputs.
10. **Extension protocols.** Minimal implementation contract for third-party reducers/metrics/filtrations/operators/analyses.
11. **Error behavior.** Validation failures and common misuse.

**Representation task / acceptance evidence:** Implement or configure a custom extension solely from the API spec and pass its documented contract.

## `docs/spec/DATA_MODEL_SPEC.md`

**Audience:** integration developer or maintainer

**Terminal reader state:** Reader can understand and independently consume or serialize Eigenflow result/data objects without reverse-engineering source code.

**Prerequisite state:** Public API and conceptual pipeline understood.

**Backstepped section objectives:**

1. **Object chain.** Define ProbePopulation → RepresentationCollection → RelationalMatrix → GraphFiltration → AnalysisResult → ExperimentResult.
2. **Identity/order invariants.** Specify stable probe IDs and row/column ordering.
3. **Shapes and dtypes.** Specify tensor/array dimensions at each stage.
4. **Metric semantics.** Persist similarity/distance orientation and configuration.
5. **Filtration snapshots.** Specify parameter, edge density, threshold, adjacency, monotonicity.
6. **Analysis payloads.** Specify scalar/vector/record conventions by analysis family.
7. **Provenance schema.** Specify runtime/model/config/source metadata.
8. **Persistence format.** Describe only actual serialization behavior and reconstruction guarantees.
9. **Versioning/compatibility.** Define schema version and future migration policy.
10. **Concrete serialized example.** Show a real small result tree and access paths.

**Representation task / acceptance evidence:** Write an independent reader that correctly locates a chosen layer's spectral and factor outputs from a persisted result.

## `docs/spec/EXECUTION_SPEC.md`

**Audience:** maintainer/performance integrator

**Terminal reader state:** Reader can predict what computation occurs, what is reused or recomputed, and where future caching/parallelization can be added without changing scientific semantics.

**Prerequisite state:** Data model and API understood.

**Backstepped section objectives:**

1. **Actual execution order.** Describe current extraction → metric → filtration → analyses path exactly.
2. **Dependency graph.** State computational dependencies independently of whether caching is implemented.
3. **Reuse semantics.** Document what objects are reused within a run.
4. **Invalidation logic.** Explain which upstream configuration changes invalidate which descendants.
5. **Batch/device behavior.** Specify model execution, memory movement, eval/no-grad expectations.
6. **Failure and partial-result behavior.** Specify errors and whether partial work persists.
7. **Performance model.** Identify N, D, layers, control steps, sparse/dense eigensolver scaling concerns.
8. **Caching status.** Clearly separate current implementation from planned extension architecture.
9. **Worked recomputation cases.** Show consequences of changing metric, filtration, or analysis only.

**Representation task / acceptance evidence:** Given two experiment configurations, predict which computational stages must differ and which results can be reused.

## `CONTRIBUTING.md`

**Audience:** new contributor

**Terminal reader state:** Contributor can set up development, extend one subsystem correctly, update tests/docs/state, and submit a scientifically and architecturally compliant change.

**Prerequisite state:** Basic package concept; Python development competence.

**Backstepped section objectives:**

1. **Development setup.** Clone/install/test commands and supported versions.
2. **Repository architecture.** Locate core subsystems and dependency boundaries.
3. **Extension recipes.** Add metric, reducer, filtration, operator, analysis, visualization, preset.
4. **Testing expectations.** Unit/integration/regression/numerical validation.
5. **Scientific documentation expectations.** Require indication, assumptions, output semantics, interpretive limits.
6. **Persistent-state workflow.** Explain canonical state, manifests, schema evolution, derivative artifacts.
7. **PR checklist.** Specify required updates and validation.

**Representation task / acceptance evidence:** Add a small custom metric plus tests/docs/state updates following only CONTRIBUTING.

## `CHANGELOG.md`

**Audience:** user upgrading or evaluating a release

**Terminal reader state:** Reader can determine what capabilities, behaviors, limitations, and breaking/scientific-method changes apply to a release.

**Prerequisite state:** None beyond knowing the package.

**Backstepped section objectives:**

1. **Release status.** Version/date/stability.
2. **Added.** User-visible capabilities grouped by subsystem.
3. **Changed.** Behavioral/API/scientific-method changes.
4. **Fixed.** Correctness bugs.
5. **Deprecated/removed.** Migration-relevant changes.
6. **Known limitations.** Unimplemented or caveated behavior.
7. **Scientific interpretation changes.** Changes that affect meaning/comparability of outputs.

**Representation task / acceptance evidence:** Determine whether a saved experiment remains comparable after upgrading.

## `SECURITY.md`

**Audience:** user or vulnerability reporter

**Terminal reader state:** Reader can identify relevant trust boundaries, avoid unsafe model/data loading practices, and report a vulnerability through a clear channel.

**Prerequisite state:** Basic package use.

**Backstepped section objectives:**

1. **Supported versions.** Know what receives security fixes.
2. **Reporting.** Actionable private reporting path.
3. **Model serialization boundary.** Understand torch/pickle risks.
4. **User-callable extensions.** Understand arbitrary callable/custom metric risk.
5. **Resource exhaustion.** Understand large probe/spectral workloads.
6. **Sensitive probe data.** Understand local data handling responsibilities.
7. **Disclosure process.** Know expected handling lifecycle.

**Representation task / acceptance evidence:** Given a proposed workflow involving an untrusted model artifact, identify the unsafe step and safer boundary.

## `CODE_OF_CONDUCT.md`

**Audience:** contributors/community

**Terminal reader state:** Reader knows behavioral expectations, reporting routes, enforcement scope, and project-specific norms for scientific disagreement.

**Prerequisite state:** None.

**Backstepped section objectives:**

1. **Expected behavior.** Professional and inclusive conduct.
2. **Unacceptable behavior.** Concrete prohibited conduct.
3. **Scientific disagreement norm.** Evidence/reproducibility over personal conflict.
4. **Scope.** Where policy applies.
5. **Reporting/enforcement.** Who receives reports and how action is handled.

**Representation task / acceptance evidence:** Know how to report a conduct issue and what process follows.

## `CITATION.cff`

**Audience:** researcher citing software

**Terminal reader state:** Researcher can produce an accurate citation for the exact software release.

**Prerequisite state:** Use of Eigenflow in research.

**Backstepped section objectives:**

1. **Identity.** Canonical title/authors/repository.
2. **Release.** Correct version/date.
3. **Archive.** DOI or archival identifier if present.
4. **Preferred citation.** Machine-readable citation metadata.

**Representation task / acceptance evidence:** Generate a citation matching the installed/published release.

## `LICENSE`

**Audience:** user/contributor/legal reviewer

**Terminal reader state:** Reader can determine permissions and obligations unambiguously and see consistent ownership/license metadata across repository surfaces.

**Prerequisite state:** None.

**Backstepped section objectives:**

1. **License text.** Preserve standard legal text.
2. **Ownership consistency.** Verify holder/year against package metadata.

**Representation task / acceptance evidence:** Determine whether intended reuse is permitted under the stated license.

## `pyproject.toml`

**Audience:** installer/package-index user and tooling

**Terminal reader state:** Package tooling and users can determine install requirements, compatibility, project links, metadata, and optional dependency groups accurately.

**Prerequisite state:** Python packaging familiarity.

**Backstepped section objectives:**

1. **Build metadata.** Correct backend/build requirements.
2. **Runtime compatibility.** Python/PyTorch dependency ranges.
3. **Project metadata.** Description/license/authors/keywords/classifiers.
4. **URLs.** Repository/docs/issues/changelog.
5. **Optional dependencies.** Docs/dev/performance groups if supported.
6. **Tooling.** Test/lint/type configuration as adopted.

**Representation task / acceptance evidence:** Install the intended package configuration and navigate from package metadata to documentation/issues.

## `project_state/STATE_PROTOCOL.md`

**Audience:** maintainer/AI collaborator

**Terminal reader state:** Maintainer can distinguish canonical semantic state, local Git state, remote state, derivative artifacts, and execute/resume project mutations without losing provenance.

**Prerequisite state:** Repository maintenance role.

**Backstepped section objectives:**

1. **Scope.** State clearly that this governs project-development state, not experiment result semantics.
2. **Authority.** Define canonical state versus conversation/derivatives.
3. **Mutation cycle.** Read → propose → validate → persist → derive → checkpoint.
4. **Schema evolution.** Migration/deprecation/backfill rules.
5. **Execution manifest.** Resume/invalidation semantics.
6. **Git and remote synchronization.** Differentiate state commit, Git commit, and push.
7. **Documentation task governance.** Explain open-task/audit/objective mechanisms.

**Representation task / acceptance evidence:** Resume an interrupted project unit and determine whether a local committed change has also reached the remote.
