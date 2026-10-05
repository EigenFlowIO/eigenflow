# Interpreting longitudinal and comparative results

Longitudinal Eigenflow analysis adds a development coordinate to the existing layer-by-control object:

\[
Q(\ell,p) \rightarrow Q(\ell,p,t).
\]

This guide explains how to interpret that additional axis without turning structural change into a generic notion of model quality.

## Start with compatibility, not the delta

Before interpreting any difference, inspect the `CompatibilityReport`.

A valid longitudinal comparison normally keeps the following fixed:

- probe population and ordering;
- preprocessing;
- representation-site measurement contract;
- reducer;
- metric;
- filtration and control grid;
- analyses.

A mismatch can create an apparent checkpoint effect even if the model is unchanged.

## Absolute structure and structural displacement answer different questions

For a baseline checkpoint \(t_0\):

\[
\Delta Q(\ell,p,t)=Q(\ell,p,t)-Q(\ell,p,t_0).
\]

`StructuralDiff` and `LongitudinalResult.baseline_delta(...)` preserve the distinction between the absolute values and the displacement.

Always inspect both when the conclusion depends on magnitude. Two checkpoints can have the same difference but occupy very different structural regimes.

## Read the three dimensions separately before synthesizing them

### Layer/site \(\ell\)

Asks **where** the structural change occurs.

A localized change can motivate investigation of one block. A distributed change suggests a different developmental story. Neither is intrinsically better.

### Relational scale \(p\)

Asks **at what graph scale** the difference appears.

A change visible only at high edge density is not the same phenomenon as a persistent grouping that appears at sparse connectivity.

### Development coordinate \(t\)

Asks **when** the structure changes.

A structural transition that stabilizes early may support a different checkpoint decision than one that continues to drift after behavioral performance plateaus.

## Use trajectories for scalar summaries

```python
fig = ef.visualization.checkpoint_trajectory(
    longitudinal,
    site,
    "percolation",
    "susceptibility",
    aggregate="max",
)
```

Scalar trajectories are good for showing when a quantity changes. They should not replace the full surface when the location along control scale matters.

## Use longitudinal surfaces for scale-dependent change

```python
fig = ef.visualization.longitudinal_surface(
    longitudinal,
    site,
    "components",
    "component_count",
    baseline_delta=True,
)
```

This view keeps checkpoint and graph scale visible simultaneously.

## Use layer × checkpoint heatmaps to localize change through depth

```python
fig = ef.visualization.layer_time_heatmap(
    longitudinal,
    "components",
    "component_count",
    baseline_delta=True,
)
```

The heatmap collapses control scale by a declared aggregation. It is therefore a summary view, not a substitute for the underlying \(Q(\ell,p,t)\) data.

## Structural diffs are controlled contrasts

```python
diff = StructuralDiff.between(baseline, checkpoint)
fig = ef.visualization.structural_diff_heatmap(
    diff,
    "components",
    "component_count",
)
```

Interpret the difference as:

> Under the same probe and measurement contract, this observable changed by this amount at these representation sites and control values.

Do not jump directly to:

> The model learned concept X here.

That semantic inference still depends on the probe design and competing hypotheses.

## Target acquisition and forgetting require role-specific probes

A post-training run can exhibit target acquisition and retention loss simultaneously. One probe population cannot establish both unless its factorial design genuinely identifies both hypotheses.

Role-specific probe suites make the interpretation explicit:

- target structure should move in the predicted direction;
- retained structure should remain within the declared tolerance;
- nuisance structure may intentionally weaken;
- boundary probes can be inspected for unstable or bridge behavior.

## Behavioral and structural disagreement is informative

Several patterns matter:

- **behavior improves, target structure strengthens:** convergent evidence for the intended learning hypothesis;
- **behavior improves, target structure does not change:** the model may have found a different solution than predicted, or the probes/observable may not measure the relevant distinction;
- **behavior improves, retention structure deteriorates:** specialization may be accompanied by forgetting;
- **behavior plateaus, structure continues to drift:** later training may be changing internal organization without improving the measured task;
- **structure stabilizes before behavior:** structural observables may provide an additional checkpoint-selection signal, but not a universal stopping rule.

## Architecture comparisons need declared site correspondence

Exact module-name matches are strong only when those names actually denote comparable functions. For different architectures, prefer a `SiteAlignment` justified by the experimental design.

Normalized-depth alignment is exploratory. It should be reported as an approximation rather than presented as if layer 40% in one architecture were the same computation as layer 40% in another.

## Robustness remains necessary

A development conclusion is stronger when it survives reasonable changes in:

- probe resampling;
- random seed;
- reducer where scientifically defensible;
- metric at a matched graph-scale coordinate;
- repeated training runs;
- nearby checkpoints.

The presence of a time axis does not remove the original Eigenflow measurement assumptions.

## Recommended reporting structure

For longitudinal work, report:

1. development hypothesis;
2. baseline model/checkpoint;
3. fixed probe suite and version;
4. exact measurement specification;
5. compatibility report;
6. absolute structural trajectories;
7. baseline-relative displacement;
8. behavioral and efficiency metrics;
9. role-specific interpretation;
10. alternatives and robustness checks;
11. engineering decision made from the evidence.

The final decision remains a human or externally specified development decision. Eigenflow exposes the internal structural consequences of the run; it does not convert them into an automatic judgment of model quality.
