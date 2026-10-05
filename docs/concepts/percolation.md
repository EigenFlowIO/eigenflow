# Percolation-style analysis

Eigenflow uses percolation-style observables to describe how representation-induced graphs reorganize as a control parameter changes.

The analogy is useful because a filtration progressively admits relations among probes. At strict scale, most probes may be isolated. As the graph grows, local groups form, larger groups merge, and eventually a macroscopic component may dominate.

The package uses these observables descriptively. A susceptibility peak or abrupt giant-component change is not, by itself, evidence that a neural representation belongs to a statistical-physics universality class.

## Graph growth and control direction

For a similarity threshold \(t\),

\[
A_{ij}(t)=\mathbf 1[S_{ij}\ge t].
\]

Lowering \(t\) admits weaker similarities and usually adds edges.

For a distance threshold \(\epsilon\),

\[
A_{ij}(\epsilon)=\mathbf 1[D_{ij}\le \epsilon].
\]

Increasing \(\epsilon\) adds edges.

Eigenflow stores the metric orientation (`similarity` or `distance`) so threshold filtrations can orient the sweep correctly.

Before interpreting a curve, always know what increasing the displayed control parameter means. With edge density, interpretation is simple: larger density means more retained edges. With native thresholds, direction depends on the metric.

## Native threshold versus edge density

A native threshold preserves the units of the metric. This is useful when the threshold itself has scientific meaning.

But cosine `0.8`, Euclidean `3.1`, and an RBF affinity `0.6` are not directly comparable. For cross-metric comparisons, use edge density

\[
\rho=\frac{|E|}{\binom N2}.
\]

A graph at \(\rho=0.10\) retains 10% of all possible undirected edges.

Matching \(\rho\) does not make metrics equivalent. It holds graph sparsity approximately constant so that differences in organization are less confounded by different threshold scales.

```python
filtration = ef.filtrations.EdgeDensityFiltration(
    start=0.0,
    stop=0.5,
    steps=100,
)
```

## Giant-component fraction

The giant-component fraction is

\[
P_\infty(p)=\frac{|C_{\max}(p)|}{N}.
\]

It measures how much of the probe population belongs to the largest connected component.

In a neural representation, early growth of \(P_\infty\) means that a large fraction of probes can be connected using relatively strong admitted relations under the chosen filtration. Late growth means large-scale integration requires admitting weaker relations.

This statistic is global. It does not tell you whether the giant component is semantically coherent.

## Second-largest component

Eigenflow also tracks the fraction in the second-largest component.

A large second component indicates that two substantial structures coexist before they merge. This can be especially informative when the probe population contains two superclasses or two competing semantic regions.

A peak in the second component near a merger is often a useful transition marker, but its interpretation still depends on the probe labels and graph construction.

## Susceptibility

The implemented susceptibility is a finite-cluster size statistic excluding the giant component. Conceptually, it gives extra weight to larger non-giant components and can highlight a regime rich in mesoscale organization.

Eigenflow reports the susceptibility trajectory and the control parameter where it peaks.

```python
p = layer.analyses["percolation"]
print(p.observables["susceptibility"])
print(p.observables["susceptibility_peak_parameter"])
```

A peak can indicate that the graph contains substantial competing clusters before one dominates.

It does not automatically define a thermodynamic critical point.

## Cluster-size distributions

A component-count curve can hide whether fragmentation consists of many singletons, several medium groups, or a few large groups.

Cluster-size distributions expose that distinction.

In interpretability experiments, useful questions include:

- Does a class form several stable subgroups before cohering?
- Are there many small atypical groups around a dominant semantic region?
- Do two large structures coexist over a broad interval?
- Does the representation pass through a hierarchy of merging scales?

Power-law claims require much more evidence than visually inspecting a log-log plot. Treat empirical cluster-size distributions first as descriptive summaries.

## Merge jumps and bridge probes

A large change in component structure may be caused by a small number of newly admitted relations.

Eigenflow's bridge analysis can identify graph edges whose removal would increase the number of components at a given snapshot.

```python
bridges = layer.analyses["bridges"]

for row in bridges.records:
    print(row["parameter"], row["bridges"])
```

Bridge probes can be experimentally interesting. A probe repeatedly involved in cross-class bridges may be ambiguous, mislabeled, morphologically intermediate, or representative of a feature shared by two groups.

The bridge relation is the observation. The semantic explanation requires inspection of the probe and the experimental factors.

## Factor-conditioned interpretation

Probe metadata gives the percolation trajectory semantic context.

Suppose `class` and `background` are both recorded. You can compare component/factor alignment over the same control sweep or use `class_structure` to examine within-class and external density.

```python
result = ef.Experiment(
    model=model,
    probes=probes,
    filtration=ef.filtrations.EdgeDensityFiltration(
        start=0.0, stop=0.5, steps=100
    ),
    analyses=[
        "percolation",
        "factor_alignment",
        "class_structure",
        "bridges",
    ],
).run()
```

A useful class-separation story might be:

1. members of a class become densely internally connected at relatively low edge density;
2. the class remains weakly connected to other classes over a substantial interval;
3. factor alignment is high in the same interval;
4. only a small set of probes bridge the eventual merger.

That is stronger evidence than component count alone.

## Finite-size analysis

Graph transitions can move when the number or composition of probes changes.

If an apparent transition is central to the claim, repeat the experiment across resampled probe populations or several population sizes. Ask whether the transition region is stable, whether its variance shrinks, and whether the qualitative interpretation persists.

Finite-size stability supports the claim that the phenomenon belongs to the representation distribution sampled by the probes rather than to one accidental finite graph.

Eigenflow currently provides finite-size utilities rather than an automatic universal critical-exponent inference system. The experimenter remains responsible for choosing a defensible resampling design.

## Criticality language

Use language proportional to the evidence.

Safe descriptive language includes:

- transition region;
- susceptibility peak;
- maximal component-count derivative;
- abrupt merger;
- giant-component onset under this probe/filtration;
- candidate critical scale.

Stronger language such as *critical point*, *phase transition*, or *universality class* requires evidence beyond the existence of a sharp finite-sample curve.

In particular, the similarity-induced graph sequence is deterministic conditional on the model representations and probe set. It is not automatically the same object as classical independent bond percolation.

## Worked interpretation

Suppose two VGG16 sites produce the following qualitative behavior under the same edge-density filtration.

At an early site:

- \(P_\infty\) grows gradually;
- the second-largest component remains modest;
- susceptibility has a broad low peak;
- factor alignment with class is weak.

At a late site:

- two large components coexist over a broad interval;
- susceptibility has a sharper maximum;
- class NMI is high in the same interval;
- a few bridge probes cause the final large merger.

A justified interpretation is:

> The later representation exhibits stronger mesoscale class-aligned organization: large class-consistent structures persist before a small set of probes connects them.

An alternative is that cosine geometry or the reducer creates this separation. A robustness check would repeat the analysis under another reasonable metric at matched edge densities.

An unjustified interpretation is:

> The late layer undergoes a universal percolation phase transition caused by the class feature.

The first statement is a structural inference grounded in the experimental design. The second adds a mechanism and statistical-physics claim not established by the observed curves.
