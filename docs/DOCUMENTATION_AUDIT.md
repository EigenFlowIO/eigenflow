# Documentation Audit

Status: **historical audit complete; original remediation tasks resolved.**

The entries below preserve the original audit findings and acceptance criteria as provenance. They are no longer an open-work list. The original human-facing remediation was completed before the visualization phase; subsequent visualization additions are governed by `VISUALIZATION_ONTOLOGY.md`, `VISUALIZATION_TASKS.md`, and `HUMAN_FACING_REVISION_TASKS.md`.

This audit reviews the repository's human-facing documentation for installation/use-case guidance, syntax, implementation examples, conceptual discussion, instructional commentary, experimental interpretation, and consistency with the implemented package. The structured source of truth for these tasks is `project_state/project_state.json` under `documentation_audit`.

## doc_task_001 — `README.md`

**Priority:** high  
**Status:** open

Strong architectural overview and minimal quick start, but incomplete as the primary entry point for a new experimenter.

Open work:
- Add installation instructions for PyPI/editable/source installs, supported Python/PyTorch versions, and alpha-release status.
- Expand the quick start into a complete runnable experiment that inspects captured sites, accesses analysis outputs, plots at least one observable, and saves results.
- Explain how to choose probe populations, reducers, metrics, filtrations, analyses, and control coordinates, including when edge density is preferable to native thresholds.
- Add a worked interpretation section showing how observed component/percolation/spectral/factor outputs support cautious human inference about latent features.
- Add navigation links to conceptual docs, guides, API/spec docs, examples, and PCSCS migration/compatibility material.
- Document important limitations and current implementation status, including any features described in design specs but not yet implemented.

**Acceptance:** A technically competent first-time user can install Eigenflow, run an experiment, inspect outputs, and understand what conclusions are and are not supported without consulting source code.

## doc_task_002 — `CONTRIBUTING.md`

**Priority:** medium  
**Status:** open

Currently a single policy paragraph; insufficient for contributors.

Open work:
- Add development setup, editable install, test commands, repository layout, code/documentation conventions, and expected Python compatibility.
- Document how to add a metric, filtration, operator, analysis, reducer, visualization, or preset using the extension interfaces.
- Define PR expectations, regression-test requirements, numerical/scientific validation expectations, and documentation requirements.
- Explain the persistent-state workflow and when changes must update project_state, execution manifest, specs, tests, and derivative documentation.

**Acceptance:** A new contributor can set up the project and make a compliant extension without reverse-engineering repository conventions.

## doc_task_003 — `CHANGELOG.md`

**Priority:** medium  
**Status:** open

Only a one-line initial release summary.

Open work:
- Expand the initial release entry into user-visible capabilities grouped by probes/extraction, metrics, filtrations, analyses, visualization, serialization, and PCSCS compatibility.
- List known limitations and incomplete/documentation-sensitive features.
- Establish changelog conventions for breaking API changes, behavioral changes, deprecations, bug fixes, and scientific-method changes.

**Acceptance:** Users can determine what changed, what is supported, and what limitations apply in each release.

## doc_task_004 — `SECURITY.md`

**Priority:** medium  
**Status:** open

Contains one safety warning and no operational reporting policy.

Open work:
- Add a concrete private vulnerability-reporting channel or GitHub security-advisory procedure.
- Document supported versions and disclosure/response expectations.
- Expand model/data safety guidance: untrusted torch/pickle artifacts, arbitrary callables/custom metrics, dependency risks, resource-exhaustion considerations, and handling of sensitive probe data.

**Acceptance:** The file provides an actionable vulnerability-reporting path and describes the main security boundaries relevant to Eigenflow.

## doc_task_005 — `CITATION.cff`

**Priority:** medium  
**Status:** open

Valid-looking minimal citation metadata, but release and authorship metadata require review.

Open work:
- Verify author/maintainer identity and preferred citation form.
- Verify version and release date against the actual published release; current date-released is 2026-10-05 and should not precede the real release event.
- Add DOI/archive metadata if a Zenodo or equivalent release DOI is created.
- Ensure repository URL/casing and software title match the canonical GitHub project.

**Acceptance:** Citation metadata matches the actual release, authorship, canonical repository, and archival identifier if available.

## doc_task_006 — `CODE_OF_CONDUCT.md`

**Priority:** low  
**Status:** open

Expresses desired norms but is not a complete code-of-conduct policy.

Open work:
- Adopt or adapt a recognized code of conduct (for example Contributor Covenant) with scope, unacceptable behavior, enforcement responsibilities, and reporting process.
- Preserve the project-specific expectation that methodological disagreements are resolved through evidence and reproducible tests.

**Acceptance:** Contributors have clear behavioral expectations, reporting procedures, and enforcement scope.

## doc_task_007 — `LICENSE`

**Priority:** low  
**Status:** open

Standard MIT license is structurally complete.

Open work:
- Verify copyright year and legal copyright holder/name match the intended project ownership before release.
- Confirm README, pyproject metadata, and CITATION.cff consistently identify the same license and owner.

**Acceptance:** License metadata is legally and bibliographically consistent across the repository.

## doc_task_008 — `docs/concepts/experimental_model.md`

**Priority:** high  
**Status:** open

Only states the core idea; does not teach experimental design or inference.

Open work:
- Formalize the hypothesis → probe design → representation population → relational geometry → observable → inference workflow.
- Explain manipulated factors, controls, matched/factorial designs, confounds, probe metadata, sampling balance, and reproducibility.
- Provide at least two complete experimental examples with competing hypotheses and predicted structural outcomes.
- Discuss the epistemic boundary between structural evidence and claims about latent features, including alternative explanations and robustness checks across metrics/reducers.

**Acceptance:** A reader can design a controlled post hoc interpretability experiment and state appropriately bounded conclusions from its outputs.

## doc_task_009 — `docs/concepts/percolation.md`

**Priority:** high  
**Status:** open

Correct caveat but essentially only an abstract.

Open work:
- Define graph-growth orientation and control coordinates, especially native threshold versus edge density.
- Give formulas and intuition for giant-component fraction, second-largest component, susceptibility, component-size distributions, jumps, and finite-size analysis.
- Explain class/factor-conditioned percolation and how coherence/mixing phenomena relate to neural representations.
- Provide synthetic or worked examples showing characteristic curves and how an experimenter should interpret peaks/transitions.
- Distinguish descriptive percolation-style analysis from claims of criticality, phase transition, scaling exponents, or universality.

**Acceptance:** A reader can select, compute, and interpret the implemented percolation observables in neural-network probe experiments.

## doc_task_010 — `docs/concepts/spectral_analysis.md`

**Priority:** high  
**Status:** open

States operator breadth and eigenspace caution but omits almost all practical spectral interpretation.

Open work:
- Define adjacency, combinatorial Laplacian, normalized Laplacian, random-walk, modularity, and non-backtracking operators and when each is informative.
- Explain spectral radius, algebraic connectivity, gaps, entropy, energy, effective rank, IPR/localization, eigenspace overlap, and principal angles.
- Explain eigenvalue/eigenspace trajectories over control scale and across network depth, including crossings and degeneracy.
- Add concrete neural-network interpretation examples and warnings against treating spectral signatures as semantic explanations without probe evidence.
- Document numerical/solver considerations, full versus partial spectra, and scale/performance implications.

**Acceptance:** A reader can choose an operator and spectral observable, understand its numerical meaning, and interpret it in a controlled experimental context.

## doc_task_011 — `docs/guides/vgg16_probe_experiment.md`

**Priority:** high  
**Status:** open

A short orientation paragraph rather than an executable guide.

Open work:
- Provide prerequisites/install commands and torchvision VGG16 loading/preprocessing code.
- Construct a realistic image ProbePopulation with metadata and stable IDs.
- Show available-site inspection and explain sensible VGG16 block endpoints versus default leaf-module capture.
- Compare flatten and global-average reducers and explain the scientific consequences of each.
- Run at least one cosine/threshold or edge-density experiment plus spectral/percolation/factor analyses.
- Show exact result-access syntax, plots, serialization, and human interpretation of observed class/group transitions.
- Include reproducibility, batching/device, memory/performance, and expected activation-shape commentary.

**Acceptance:** The guide is copy-runnable and takes a user from raw probe images to interpretable multi-layer Eigenflow results.

## doc_task_012 — `docs/spec/API_SPEC.md`

**Priority:** critical  
**Status:** open

Useful outline, but too terse for an API contract and currently diverges from implementation.

Open work:
- Reconcile the documented Experiment signature with implementation: the spec currently advertises operators=None and cache=True, which the Experiment dataclass does not expose.
- Add exact class/function signatures, argument types, defaults, return types, exceptions, accepted string aliases, and minimal examples for all public objects.
- Document configured Analysis objects versus keyword shortcuts and how custom extensions are registered/resolved.
- Document ExtractionConfig site/reducer semantics and callable/collate behavior.
- Define compatibility/deprecation expectations for the public v1 API.

**Acceptance:** Every public API claim is executable against the current package and sufficiently precise to serve as the stable v1 contract.

## doc_task_013 — `docs/spec/DATA_MODEL_SPEC.md`

**Priority:** critical  
**Status:** open

Correct high-level path but includes serialization claims not implemented by ExperimentResult.

Open work:
- Reconcile serialization claims: the spec says save writes JSON + NPZ and load reconstructs results, while current ExperimentResult.save writes only result.json and no load method exists.
- Document each dataclass/data object, field semantics, array shapes, probe-order invariants, metric orientation, graph snapshot contents, and analysis result structure.
- Define JSON/array portability, eigenvector persistence policy, versioning, backward compatibility, and provenance fields.
- Provide concrete serialized examples and result-navigation examples.

**Acceptance:** The data model spec exactly matches implementation and is sufficient to implement independent readers/writers for persisted results.

## doc_task_014 — `docs/spec/EXECUTION_SPEC.md`

**Priority:** critical  
**Status:** open

Describes an intended DAG/cache architecture that is not implemented in the current Experiment.run path.

Open work:
- Reconcile or implement the claimed dependency DAG and in-memory content-addressed cache; current Experiment.run recomputes directly and exposes no cache control.
- Document actual invalidation boundaries, object reuse, deterministic configuration keys, and execution ordering.
- Describe batching/device behavior, failure handling, partial results, performance characteristics, and future disk/distributed cache extension points.
- Add execution examples demonstrating what is recomputed when metric, filtration, or analysis configuration changes.

**Acceptance:** The execution spec describes actual behavior and gives developers a precise contract for caching, invalidation, and recomputation.

## doc_task_015 — `examples/basic_mlp.py`

**Priority:** high  
**Status:** open

Runnable smoke example but not instructional; compressed formatting hides the conceptual workflow.

Open work:
- Reformat idiomatically and add comments that map each code section to probe design, extraction, metric, filtration, analyses, and interpretation.
- Seed model and probe generation reproducibly.
- Inspect/print available sites and show explicit site selection at least once.
- Access concrete component/percolation/spectral/factor outputs instead of only summary(), and plot or save representative results.
- Add commentary explaining what the resulting values would mean experimentally and what they do not establish.

**Acceptance:** The example functions as an annotated first tutorial, not only a smoke test.

## doc_task_016 — `examples/pcscs_compatibility.py`

**Priority:** high  
**Status:** open

Demonstrates preset invocation only; insufficient as PCSCS compatibility/migration documentation.

Open work:
- Explain which PCSCS defaults are reproduced and which Eigenflow behaviors differ from the existing PCSCS repository.
- Use deterministic probes/model initialization and explicit threshold/siting examples.
- Show how to access PCSCS critical/convergence/component outputs and spectral diagnostics per layer.
- Provide an equivalent expanded Experiment configuration so users can see how the preset maps onto general Eigenflow primitives.
- Add interpretation commentary and a migration note for users moving existing PCSCS experiments into Eigenflow.

**Acceptance:** A PCSCS user can understand, reproduce, inspect, and customize the compatibility preset in Eigenflow.

## doc_task_017 — `project_state/STATE_PROTOCOL.md`

**Priority:** low  
**Status:** open

Substantive and operationally complete for internal project-state management; not product-user documentation.

Open work:
- Add a short scope preface clarifying that this protocol governs Eigenflow development state, not runtime experiment-state semantics.
- Add explicit repository/remote synchronization guidance so a committed local state mutation is not confused with a pushed GitHub state.
- Cross-reference the documentation-audit/open-task mechanism introduced by this work cycle.

**Acceptance:** Maintainers can distinguish canonical development state, local Git state, and remote GitHub state without ambiguity.

## doc_task_018 — `pyproject.toml`

**Priority:** medium  
**Status:** open

Sufficient to build/install in a normal connected environment, but sparse as public package metadata.

Open work:
- Add project URLs for repository, documentation, issues, and changelog.
- Add classifiers/keywords and verify license metadata format against current packaging standards.
- Consider optional documentation dependencies and any performance/visualization extras if the package grows.
- Ensure supported Python/PyTorch versions documented here remain synchronized with README and CI/test policy.

**Acceptance:** Package-index metadata directs users to all major project resources and accurately states compatibility.

## doc_task_019 — `docs/index.md (new)`

**Priority:** high  
**Status:** open

No documentation landing page currently exists.

Open work:
- Create a documentation index organized by getting started, experimental design, concepts, API/specification, worked guides, examples, and interpretation.
- Give readers recommended paths for first-time users, PCSCS users, contributors, and researchers designing controlled experiments.

**Acceptance:** All human-facing documentation is discoverable from a single navigable landing page.

## doc_task_020 — `docs/guides/interpreting_results.md (new)`

**Priority:** high  
**Status:** open

The repository lacks a dedicated guide translating numerical/graph outputs into appropriately bounded experimental interpretations.

Open work:
- Build a worked result-reading guide covering components, percolation, spectra/eigenspaces, class/factor alignment, bridges, k-core, communities, and transitions.
- For each output, include what it measures, indicative patterns, plausible neural-network interpretations, alternative explanations, and claims that are not warranted.
- Include examples of convergent evidence across multiple observables and robustness checks across metrics/reducers.

**Acceptance:** Experimenters can interpret Eigenflow outputs as evidence about latent feature organization without relying on undocumented intuition.


## Current disposition

All non-maintainer documentation tasks identified by this audit have been completed. Tasks requiring authoritative authorship/legal/reporting-channel information remain explicitly blocked in canonical project state. See `docs/DOCUMENTATION_VALIDATION.md` for validation results.
