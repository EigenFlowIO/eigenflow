# The experimental model

Eigenflow is best understood as an inverse-problem framework for post hoc interpretability.

A neural network produces internal representations, but the semantic features that organize those representations are not directly labeled inside the model. The experimenter observes the consequences of those representations for a deliberately constructed probe population and reasons backward from those consequences toward hypotheses about latent feature organization.

That is a different epistemic task from reading an activation value or assigning a concept name to a neuron.

## The inverse problem

Let a probe input \(x_i\) produce an internal representation \(z_i^{(\ell)}\) at site \(\ell\). A latent organizational hypothesis \(H\)—for example, "this layer is primarily organized by object identity rather than background"—is not directly observable.

What is observable is a relational structure induced by the set of representations. For a metric \(m\),

\[
S_{ij}^{(\ell)} = m(z_i^{(\ell)}, z_j^{(\ell)}).
\]

A filtration converts those pairwise relations into a family of graphs \(G_{\ell,p}\), and analyses produce measurable quantities \(Q(\ell,p)\).

The forward evidential chain is therefore

\[
\text{latent feature organization}
\rightarrow
\text{representation geometry}
\rightarrow
\text{structural observables}.
\]

The interpretability experiment reasons in the opposite direction:

\[
\text{controlled probe manipulation}
+
\text{observed structural response}
\rightarrow
\text{evidence about latent organization}.
\]

This inversion is only informative when competing hypotheses predict different observable outcomes.

## The population is the primary unit of analysis

Eigenflow is not primarily a method for tracing one input through a sequence of activations.

The central object at a representation site is the complete probe population

\[
Z^{(\ell)} =
\{z_1^{(\ell)},\ldots,z_N^{(\ell)}\}.
\]

The question is how relationships among the probes change as the population passes through the network.

An individual probe matters through its structural role in that population: it may join a group early, remain isolated, occupy a robust core, or bridge two otherwise distinct regions. Single-probe trajectories are therefore secondary diagnostics embedded in a population-level experiment.

## From a semantic question to competing hypotheses

A useful Eigenflow question must be translated into alternatives that make different predictions.

Suppose an image classifier confuses wolves and huskies. Consider:

- \(H_1\): later representations are organized primarily by animal morphology.
- \(H_2\): later representations remain strongly organized by snowy-background cues.

A probe population containing only wolves in snow and huskies on grass does not distinguish the hypotheses. Both predict separation.

A crossed population does:

\[
\{\text{wolf},\text{husky}\}
\times
\{\text{snow},\text{grass}\}.
\]

Now morphology and background imply different relational partitions.

The package can measure which partition better describes observed structure, but the identifying power came from the probe design.

## Probe factors

Probe metadata can encode several kinds of variables.

**Manipulated factors** are deliberately varied to test a hypothesis.

**Controlled factors** are held fixed or balanced so that they do not explain the contrast of interest.

**Nuisance factors** are variables that may influence representation structure but are not the substantive target.

**Observational factors** are recorded attributes that are not experimentally manipulated but may still help diagnose structure.

For example:

```python
metadata = [
    {
        "class": "wolf",
        "background": "snow",
        "pose": "profile",
        "source": "camera_A",
    },
    ...
]
```

The package treats these as metadata. Their experimental status comes from the design, not their names.

## Factorial and matched designs

### Factorial designs

A factorial design crosses levels of multiple factors so that their contributions can be distinguished.

```python
factorial = probes.factorial(
    factors=["class", "background"],
    n_per_cell=20,
    seed=7,
)
```

This helper samples an equal number from each observed factor cell. It does not create missing cells. If the raw population never contains `wolf × grass`, no function can manufacture that identification from metadata.

### Matched contrasts

A matched design compares treatment and control conditions while matching on specified attributes.

```python
matched = probes.match(
    treatment={"background": "snow"},
    control={"background": "grass"},
    on=["class", "pose"],
)
```

This is useful when the experimental question is about one factor and suitable controls exist.

### Balance and stratification

```python
balanced = probes.balance("class", seed=7)
cells = probes.stratify(["class", "background"])
```

Balancing prevents gross group-size differences from dominating some structural statistics. Stratification exposes the available design cells before an experiment is run.

Neither operation guarantees that all relevant confounds have been controlled.

## Predict the structural outcome before looking

A strong experiment specifies what each hypothesis should produce before inspecting the result.

For the morphology-versus-background example, one might predict:

- under \(H_1\), class-aligned partitions should persist over a broader control interval than background-aligned partitions at later sites;
- under \(H_2\), background alignment should remain comparatively strong;
- if the representation becomes invariant to background with depth, within-class connectivity across backgrounds should strengthen while background-conditioned separation weakens.

The prediction can involve multiple observables. That is often preferable because different observables have different failure modes.

For example, a hypothesis could predict simultaneous changes in:

- component partition alignment;
- within-factor versus between-factor density;
- giant-component behavior;
- spectral gaps;
- eigenspace alignment;
- bridge identities.

## Measurement geometry is part of the design

After the probe population, several choices define what is actually measured.

### Representation site

Different internal modules expose different stages of computation. A claim about "the network" should normally be grounded in a specified set of sites, not an unspecified activation.

### Representation reducer

A convolutional activation might have shape

\[
N\times C\times H\times W.
\]

Flattening treats every retained activation value as a feature. Global pooling summarizes spatial positions. Token selection in a transformer selects a different representational object again.

Changing the reducer changes \(Z^{(\ell)}\). It is therefore a measurement choice.

### Metric

Cosine similarity, Euclidean distance, correlation distance, and kernels do not encode the same notion of relational proximity.

Metric robustness strengthens an inference when the substantive pattern survives reasonable alternatives. Metric dependence is itself information.

### Filtration

A filtration determines how pairwise relations are admitted into a graph family. Threshold, edge-density, and k-nearest-neighbor constructions answer different scale questions.

### Observable

Component count, susceptibility, spectral gaps, localization, and factor alignment summarize different structural properties. They should not be treated as interchangeable estimates of one hidden "interpretability" quantity.

## Layer and control scale

For each site \(\ell\) and control value \(p\), Eigenflow can construct a graph \(G_{\ell,p}\). An observable is therefore naturally a field

\[
Q(\ell,p).
\]

The two axes answer different questions.

The **layer axis** asks how the representation changes through the network.

The **control axis** asks how the organization looks at different relational scales within one representation.

A phenomenon that appears at only one arbitrary threshold may be fragile. A phenomenon that persists across a broad control interval and changes systematically through depth is stronger structural evidence.

## Confounds and alternative explanations

An observed structural pattern can arise from several sources:

- the latent feature hypothesized by the experimenter;
- an uncontrolled probe factor;
- sampling imbalance;
- the representation reducer;
- metric geometry;
- filtration construction;
- finite population size;
- atypical bridge probes;
- a model preprocessing mismatch;
- a numerical artifact.

A good interpretation identifies plausible alternatives rather than treating every alternative as a reason not to infer anything.

The question is whether the design and robustness checks make some explanations more plausible than others.

## Robustness is part of the experiment

For a consequential conclusion, pre-plan at least some sensitivity analyses.

Useful checks include:

- an alternative reasonable metric;
- an alternative reducer;
- a second probe population or resample;
- matched edge density across metrics;
- a finer or shifted parameter grid;
- balanced factor levels;
- multiple model checkpoints;
- finite-size analysis;
- convergence of independent structural observables.

Robustness does not mean that every choice must produce numerically identical curves. It means the substantive interpretation should not hinge on an arbitrary unreported setting.

## Worked example: class versus background

Suppose a VGG16 probe experiment contains four balanced cells:

| class | background |
|---|---|
| wolf | snow |
| wolf | grass |
| husky | snow |
| husky | grass |

The analysis uses the outputs of several convolutional blocks, global-average pooling, cosine similarity, and an edge-density filtration.

At an early block, component partitions align moderately with background and weakly with class. At a late block, class NMI rises over a wide density interval while background NMI falls. The late-layer class groups also show higher internal than external density, and the relevant spectral mode becomes more aligned with class.

A disciplined interpretation is:

**Observation.** Several independent structural measurements become more class-aligned and less background-aligned across depth.

**Candidate inference.** Under this crossed probe design, later VGG16 representations provide evidence of stronger organization by class relative to background.

**Alternative.** The effect could depend on global-average pooling or cosine geometry, or on a third factor correlated with class.

**Robustness test.** Repeat with flattening and Euclidean distance at matched edge densities; resample probes within each factorial cell.

**Unsupported conclusion.** The experiment does not identify a unique "wolf feature," prove that class organization causally drives logits, or establish that the same organization holds for all possible images.

The method becomes informative because the probe design, measurement definition, structural observations, and inferential boundary are all explicit.
