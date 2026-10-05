# Interpreting Eigenflow results

Eigenflow produces structural measurements. The experimenter produces the semantic interpretation.

This guide gives a disciplined procedure for moving from the result object to a human-interpretable claim without treating graph statistics as automatic explanations.

## The interpretation protocol

For every substantive result, write four statements.

### 1. Observation

Describe only what the measured object did.

> At later representation sites, component partitions have higher NMI with class labels over a broader edge-density interval.

### 2. Candidate inference

State the latent-feature hypothesis supported by the observation under the probe design.

> The later representation provides stronger evidence of organization by class.

### 3. Alternative explanation

State a plausible competing source of the same pattern.

> The effect may depend on cosine geometry, flattening, or an uncontrolled factor correlated with class.

### 4. Unsupported claim

State the stronger conclusion the experiment does not identify.

> This does not establish a unique class neuron or prove that class organization causally determines the output.

This protocol forces the evidential bridge to remain visible.

## Navigate the result hierarchy

An `ExperimentResult` contains one `LayerResult` per captured site.

```python
for site, layer in result.layers.items():
    print(site, layer.analyses.keys())
```

Access an analysis:

```python
layer = result.layers["features.16"]
percolation = layer.analyses["percolation"]
```

`AnalysisResult` objects expose:

- `observables`: named summary objects or trajectories;
- `records`: per-control-step records;
- `metadata`: configuration information for the analysis.

The exact payload differs by analysis family.

## Connected components and merge structure

`components` records:

- control parameter;
- edge density;
- number of connected components;
- largest-component size;
- component label for every probe.

Questions you can ask:

- Does a semantic group become internally connected?
- Does fragmentation decrease gradually or abruptly?
- Which groups coexist before merging?
- At what scale does the population become globally connected?

A decrease in component count does not necessarily mean "better representation." It means graph connectivity increased under the chosen filtration.

Compare component labels with probe factors before assigning semantic meaning.

## PCSCS output

`pcscs` extends component tracking with:

- `critical_parameter`: the parameter at maximum absolute component-count derivative;
- `component_derivative`;
- `convergence_parameter`: the first parameter where one component remains.

These are descriptive summaries of the component trajectory.

The `critical_parameter` is not automatically a physical critical point. It is the maximum derivative of the finite observed component-count curve.

## Percolation observables

### Giant-component fraction

A rising giant-component fraction means more probes belong to one connected structure.

Interpretation depends on context. Early macroscopic connectivity can mean global integration, but it can also reflect a metric that broadly connects unlike probes.

### Second-largest component

A large second component indicates a competing large structure. If it aligns with a controlled factor, it can support a hypothesis about a persistent partition.

### Susceptibility

A peak in susceptibility indicates a control region containing substantial non-giant cluster structure.

Use it to locate an interesting mesoscale regime, then inspect what the clusters contain.

### Merge and bridge structure

Bridge edges identify structurally pivotal relations at one graph snapshot. Inspect the probe identities on those edges. Repeated cross-factor bridges can reveal ambiguous or transitional examples.

## Spectral observables

### Algebraic connectivity

For Laplacian operators, a positive second eigenvalue appears after global connectivity. Changes in its magnitude can describe strengthening or weakening of bottlenecks.

Do not interpret the number without the operator and graph scale.

### Spectral gaps

A gap separates groups of operator modes. A stable gap can support the existence of a low-dimensional structural regime, but it does not assign semantic meaning to that regime.

### Spectral entropy and effective rank

These summarize how spectral magnitude is distributed. They can compare concentration of operator structure under matched conditions.

They are not direct estimates of the intrinsic dimensionality of the neural activation manifold.

### IPR and localization

High IPR means an eigenvector is concentrated on fewer probes. If a purportedly global semantic mode is highly localized, inspect the influential probes before treating it as population-wide evidence.

### Eigenspace overlap and principal angles

Use the `eigenspaces` analysis to judge whether low-dimensional modes persist across adjacent control values.

Near degeneracy, interpret the subspace, not one sorted eigenvector.

## Factor and class outputs

`factor_alignment` compares component labels with probe metadata using NMI and ARI.

High NMI says that two partitions share information. High ARI says their pair assignments agree beyond a chance-adjusted baseline.

Neither statistic proves that the network uniquely encodes the factor. A confounded probe design can create high alignment with several correlated factors.

`class_structure` reports internal and external edge densities for levels of a chosen factor, defaulting to `"class"`.

A useful separation regime has high internal density and comparatively low external density, but the meaningfulness of that regime still depends on the chosen metric and graph scale.

## Cores, communities, and bridge probes

`kcore` identifies nodes that survive iterative removal of degree-below-\(k\) vertices.

A large class-aligned core suggests robust mutual connectivity rather than a chain held together by a few bridges.

`communities` exposes a graph partition produced by the current community routine. Treat community labels as algorithmic partitions, not semantic truth.

`bridges` identifies graph edges whose removal would increase component count. They are useful for selecting probes for qualitative inspection.

## Transition summaries

`transitions` currently produces three candidate summaries:

- maximum component-count derivative;
- susceptibility peak;
- second-component peak;

and a simple consensus estimate when candidates fall within a tolerance.

A transition detector answers:

> Where does this observable change most strongly?

It does not answer:

> What semantic event occurred here?

Semantic interpretation comes from aligning the transition region with probe factors, graph structure, and other observables.

## Convergent evidence

The strongest results often involve observables that fail in different ways but support the same substantive claim.

Example:

- class NMI rises;
- within-class density rises relative to external density;
- a class-consistent two-component regime persists;
- a spectral gap is stable in the same interval;
- the relevant eigenspace is distributed rather than localized;
- the result survives Euclidean distance at matched edge density.

This convergence is stronger than maximizing one statistic.

## Divergent evidence

Do not average disagreement away.

Suppose component labels align with class, but the spectral mode is highly localized on three probes.

Possible interpretations include:

- the partition is real but structurally fragile;
- a few atypical probes dominate the operator;
- the graph construction produces connectivity that is not reflected in distributed spectral structure.

Divergence tells you which additional diagnostic to run.

## Robustness and sensitivity

A result can depend on:

- probe composition;
- reducer;
- metric;
- filtration family;
- parameter grid;
- selected sites;
- model checkpoint;
- graph operator;
- finite sample size.

Sensitivity is not automatically a defect. It becomes a problem when a strong semantic claim is presented as invariant while the evidence depends on an arbitrary unreported choice.

For important claims, document at least the major choices and test reasonable alternatives.

## Writing a bounded conclusion

A good conclusion names the design and the evidence.

Weak:

> Layer 12 learns species.

Better:

> In a balanced species × background probe population, class-aligned component structure and factor alignment become more persistent at later sites under both cosine and Euclidean geometry at matched edge densities. This supports the interpretation that later representations are increasingly organized by species relative to background within the tested population.

Then state a boundary:

> The experiment does not identify a unique species feature coordinate or establish causal necessity for prediction.

## Failure cases

Treat the experiment as non-identifying or weak when:

- the probe factors are confounded;
- the observed semantic factor has no appropriate control;
- the conclusion appears only after selecting one favorable threshold;
- the pattern disappears under small reasonable changes in metric/reducer;
- the effect is driven by a few uninspected outliers;
- factor alignment is reported without checking correlated metadata;
- a spectral crossing is interpreted as stable mode identity;
- a finite-sample peak is labeled a universal critical point;
- preprocessing differs across probe conditions.

The purpose of Eigenflow is not to guarantee an explanation. It is to make the structure of the evidence inspectable enough that the experimenter can tell when an explanation is or is not justified.
