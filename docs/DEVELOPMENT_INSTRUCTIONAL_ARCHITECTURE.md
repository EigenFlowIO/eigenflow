# Development-instrumentation instructional architecture

This architecture governs documentation for Eigenflow's development-instrumentation and longitudinal-analysis phase. It extends the existing interpretability learning path without replacing it.

## Terminal reader state

A competent reader can design, execute, validate, interpret, and report a controlled Eigenflow comparison across architectures or checkpoints. They can distinguish model change from measurement change, construct role-specific probe suites, read \(Q(\ell,p,t)\), combine structural evidence with behavioral/efficiency evidence without collapsing them into a universal score, and make a bounded engineering decision.

## Prerequisite reader state

The reader should already understand the atomic Eigenflow experiment:

\[
\text{probes}\rightarrow Z^{(\ell)}\rightarrow S^{(\ell)}\rightarrow G_{\ell,p}\rightarrow Q(\ell,p).
\]

They should understand controlled probe design, reducer/metric/filtration choices, and the distinction between structural observation and semantic inference.

## Development learning trajectory

1. **Reframe the development problem.** Treat architecture/checkpoint/fine-tuning questions as repeated controlled representation experiments rather than isolated model inspections.
2. **Establish the comparison contract.** Learn `ExperimentSpec`, `ComparisonSpec`, and compatibility validation before computing differences.
3. **Design development probes.** Use fixed matched populations and, where needed, versioned target/retain/nuisance/boundary `ProbeSuite`s.
4. **Index model-development conditions.** Represent architecture candidates, checkpoints, runs, or interventions as `ExperimentSeries` entries.
5. **Read longitudinal structure.** Interpret \(Q(\ell,p,t)\), absolute trajectories, and baseline-relative structural displacement.
6. **Localize and compare change.** Use site alignment, structural diffs, layer×checkpoint views, and role-specific summaries.
7. **Triangulate evidence.** Keep behavioral, efficiency, and representation-structure measurements separate while reasoning across them.
8. **Make bounded engineering decisions.** Use explicit objectives for checkpoint selection, PEFT investigation, architecture revision, or data inspection; do not convert Eigenflow into an automatic optimizer.
9. **Report reproducibly.** Preserve probe-suite version, experiment specification, compatibility report, baseline, structural/behavioral evidence, alternatives, and limitations.

## Document roles

### `concepts/development_instrumentation.md`

Terminal state: reader understands why higher-order development objects exist, what each represents, and the methodological constraints that govern cross-model/checkpoint inference.

Trajectory moves: 1–3, 5–9.

### `guides/architecture_development.md`

Terminal state: reader can design and run a matched architecture comparison, choose comparable sites, inspect compatibility, and interpret structural differences conditional on an architectural hypothesis.

Trajectory moves: 1–4, 6–9.

### `guides/fine_tuning_post_training.md`

Terminal state: reader can build target/retention probe suites, create checkpoint series, identify acquisition/forgetting patterns, use diagnostics without automating intervention claims, and apply an explicit checkpoint objective.

Trajectory moves: 1–9.

### `guides/longitudinal_results.md`

Terminal state: reader can interpret absolute and baseline-relative \(Q(\ell,p,t)\), distinguish layer/control/time effects, understand site-alignment limitations, and report longitudinal evidence with alternatives and robustness.

Trajectory moves: 2, 5–9.

### README and documentation index

Terminal state: reader can recognize development instrumentation as a supported use case and navigate to the correct conceptual/guide material without mistaking it for automatic model optimization.

### Reference specifications

Terminal state: an integrating developer can identify the exact current signatures, data objects, execution behavior, persistence semantics, and non-features without relying on conceptual prose.

## Common instructional contract for development features

Where applicable, a feature explanation should state:

1. the development question it addresses;
2. the controlled variables required for a valid comparison;
3. the object/API used;
4. the output shape or data semantics;
5. how to inspect compatibility;
6. how to read absolute and baseline-relative evidence;
7. what engineering inference the evidence may support;
8. alternative explanations and robustness checks;
9. what the feature does not decide automatically.

## Claim discipline

Documentation must not state or imply that:

- structural displacement is inherently improvement or degradation;
- PEFT-targeting diagnostics identify a uniquely correct adapter location;
- normalized-depth site alignment establishes semantic equivalence;
- a checkpoint is optimal absent a declared objective;
- a probe-suite alignment statistic is proof of causal encoding;
- Eigenflow owns or replaces the training/evaluation loop.
