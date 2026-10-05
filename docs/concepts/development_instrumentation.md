# Development instrumentation and representation observability

Eigenflow can be used as more than a post-hoc interpretability tool. Its atomic experiment measures how a controlled probe population is organized across representation sites and relational scale. Once those experiments are made comparable across models or checkpoints, the same machinery becomes a representation-observability layer for neural-network development.

The extension is conceptually simple:

\[
Q(\ell,p)
\quad\longrightarrow\quad
Q(\ell,p,t),
\]

where \(\ell\) is representation site, \(p\) is relational scale, and \(t\) indexes a checkpoint, training step, model version, architecture candidate, or other controlled development condition.

The important change is not merely adding another axis to a plot. A longitudinal or cross-model claim is valid only when the measurements being compared are compatible.

## Why a higher-order layer is needed

A single `Experiment` remains Eigenflow's atomic measurement object. It answers questions about one model under one probe population and one measurement configuration.

Development questions are different:

- Did fine-tuning change target structure without damaging retained structure?
- Which representation sites changed most after an intervention?
- Do two architectures with similar behavioral scores implement the same internal solution?
- Where should additional plasticity be investigated?
- Which checkpoint best balances target acquisition and retention?

Those questions require multiple compatible experiments. Eigenflow therefore adds a higher-order layer around `ExperimentResult` rather than replacing the existing experiment engine.

## The development object model

The main objects are:

- `ExperimentSpec`: a serializable description of the measurement contract.
- `ComparisonSpec`: a declaration of which dimensions may vary and which must remain controlled.
- `CompatibilityReport`: an explicit validation result for a proposed comparison.
- `ExperimentSeries`: an indexed collection of compatible experiment results.
- `StructuralDiff`: a baseline-relative structural comparison between two compatible results.
- `LongitudinalResult`: a view of a series as \(Q(\ell,p,t)\).
- `ProbeSuite`: a versioned collection of probe populations with roles such as target, retain, nuisance, or boundary.
- `SiteAlignment`: an explicit correspondence between representation sites when architectures are not identical.
- `BehavioralRecord`: external behavioral and efficiency measurements associated with a model/checkpoint.
- `DevelopmentReport`: a joint report that keeps behavioral, efficiency, and structural evidence distinct.

These objects deliberately separate *measurement* from *development condition*.

## Measurement compatibility is part of the inference

A structural difference is meaningful only if the compared measurements answer the same measurement question.

By default, Eigenflow requires equality of:

- probe population fingerprint;
- representation-site specification;
- reducer;
- metric;
- filtration;
- configured analyses;
- preprocessing descriptor.

A `CompatibilityReport` makes mismatches explicit. Site differences can be permitted only when the comparison deliberately supplies a site-alignment strategy.

This is not defensive API ceremony. Without compatibility checking, an apparent training effect can actually be a reducer change, a different probe set, a metric change, or a different graph scale.

## Probe suites for development work

Post-training experiments often need more than one probe population. `ProbeSuite` assigns named roles to independently controlled populations.

A useful fine-tuning suite may contain:

- `target`: the capability being acquired;
- `retain`: pretrained distinctions that should survive;
- `nuisance`: variables that should ideally become less structurally influential;
- `boundary`: ambiguous, adversarial, transitional, or difficult examples.

The suite has a stable manifest and fingerprint. Each population remains an ordinary `ProbePopulation`, so factorial design, balancing, matching, and factor metadata continue to apply.

## Longitudinal structural analysis

Given compatible checkpoint results \(R_0,\ldots,R_T\), `LongitudinalResult` exposes trajectories such as

\[
Q(\ell,p,t_0),\ldots,Q(\ell,p,t_T).
\]

It also computes baseline-relative displacement:

\[
\Delta Q(\ell,p,t)=Q(\ell,p,t)-Q(\ell,p,t_0).
\]

A displacement is descriptive. It does not by itself mean improvement or degradation. Its interpretation comes from the experimental role of the probe set and the stated hypothesis.

For example, increasing class alignment on a target probe suite may be desirable while the same kind of displacement on a retention suite may indicate forgetting.

## Architecture comparison and site alignment

Two architectures may not have identical module names or depths. Eigenflow therefore does not infer equivalence from raw layer index.

`SiteAlignment` supports explicit mappings. Exact-name alignment is safest when architectures expose corresponding semantic sites. A normalized-depth alignment is available as an approximate diagnostic, but it is explicitly labeled as such and should not be treated as semantic equivalence.

Architecture comparison is strongest when the experiment is designed around named functional sites such as:

- pre-bottleneck / post-bottleneck;
- residual input / branch output / residual sum;
- embedding / attention output / MLP output;
- encoder stage boundaries.

## Behavioral and computational evidence remain separate

Eigenflow accepts externally computed behavioral metrics through `BehavioralRecord`. These can include accuracy, loss, benchmark score, latency, memory, or other development measurements.

The package does not combine them automatically into a universal score. A `DevelopmentReport` places them alongside structural evidence so a user can make a declared multi-objective decision.

This preserves an important distinction:

\[
\text{Behavior}
+\text{Efficiency}
+\text{Representation structure}
\]

are complementary evidence channels, not interchangeable measurements.

## Post-training diagnostics

The current development subsystem supports several diagnostic workflows:

- baseline-relative structural diffs;
- target/retention summaries across matched checkpoint series;
- ranking representation sites by the magnitude of structural change;
- user-defined checkpoint selection functions;
- bridge-case and factor-alignment summaries for dataset inspection.

PEFT-targeting output is intentionally diagnostic. A site that changes strongly, or appears structurally deficient for a target probe suite, is a candidate for investigation—not an automatic instruction to place an adapter there.

## What Eigenflow does not become

This phase does not turn Eigenflow into a training framework. It does not own optimizers, schedulers, checkpoint production, or model deployment.

It also does not automatically declare:

- that more structural change is better;
- that less change is better;
- that a larger spectral gap is desirable;
- that an aligned factor is causally encoded;
- that a particular layer should be fine-tuned;
- that a checkpoint is universally optimal.

The correct sequence remains:

\[
\text{development hypothesis}
\rightarrow
\text{controlled measurement}
\rightarrow
\text{structural evidence}
\rightarrow
\text{engineering decision}.
\]

## Where to continue

Use [Architecture development](../guides/architecture_development.md) for matched model comparisons, [Fine-tuning and post-training](../guides/fine_tuning_post_training.md) for target/retention workflows, and [Interpreting longitudinal results](../guides/longitudinal_results.md) for \(Q(\ell,p,t)\), structural diffs, and checkpoint-level interpretation.
