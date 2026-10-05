# Computational statistics professor with a background in computational research design draft — `README.md`

Prioritize identification, measurement assumptions, sensitivity, finite-sample behavior, alternative explanations, convergence of evidence, and calibrated interpretation.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## The experimental object

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: Start with a probe population \[ \mathcal P=\{x_1,\ldots,x_N\}. \] A probe population is not merely a convenient batch of examples. It is an experimental instrument. Its composition and metadata determine which interpretations are identifiable. When the probes pass through a PyTorch model, Eigenflow captures the population at internal representation sites. At site \(\ell\), each probe has a representation \(z_i^{(\ell)}\), giving a population-level representation matrix \[ Z^{(\ell)}= \begin{bmatrix} z_1^{(\ell)}\\ \vdots\\ z_N^{(\ell)} \end{bmatrix}. \] A chosen metric produces pairwise relations among the probes, \[ S_{ij}^{(\ell)} = m\!\left(z_i^{(\ell)},z_j^{(\ell)}\right). \] A filtrati

## When Eigenflow is indicated

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: Eigenflow is most useful when you can construct probes for which competing explanations of the representation predict different relational outcomes. Suppose you want to know whether an image model is organizing wolves and huskies by animal morphology or by snowy backgrounds. A weak probe set might contain wolves only in snow and huskies only on grass. In that population, class and background are confounded; no graph or spectrum can tell you which factor explains the separation. A stronger probe design crosses the factors: | class | background | |---|---| | wolf | snow | | wolf | grass | | husky | snow | | husky | grass | If same-class probes become structurally coherent across backgrounds, w

## Install

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: From a clone of the repository: For development:

## Quick start: one complete experiment

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: The following example is intentionally small. Its purpose is to show the complete computational object before introducing more elaborate probe designs. The default extractor captures **leaf PyTorch modules that emit tensors**. The default reducer is `flatten`, which turns each probe activation into one feature vector. For an arbitrary model, inspect available module names with: Then choose explicit sites when the experiment calls for them: “Site” means an internal module output chosen for representation capture. In simple models this often corresponds naturally to a layer. In modern architectures, a useful site may instead be an attention block, residual output, normalization module, or othe

## How to read the first outputs

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: `ExperimentResult.layers` contains one `LayerResult` for each captured site. Select one site: Connected-component analysis records how fragmented the population is over the control sweep: Percolation analysis records macroscopic and mesoscale connectivity: Spectral analysis returns a trajectory of spectra across the filtration: Factor alignment compares the connected-component partition with known probe metadata using normalized mutual information (NMI) and adjusted Rand index (ARI): These outputs answer different structural questions. They should not be collapsed into a single generic “interpretability score.”

## How to interpret a result

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: A useful first interpretation has four parts. **1. Observation — what was directly measured?** > At a later representation site, the probe population remained separated into two large components over a wider edge-density interval than at an earlier site, and the component labels had higher NMI with the controlled class factor. **2. Candidate inference — what hypothesis does that support under the probe design?** > Under this probe design and measurement geometry, the later representation provides stronger evidence of relational organization by class. **3. Alternative explanation — what else could produce the pattern?** > The effect may depend on the chosen representation reducer, cosine geom

## What the experimental choices mean

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: 

## Probe population

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: `ProbePopulation` preserves stable sample IDs and metadata and provides helpers for balancing, stratification, factorial selection, and matched contrasts. These helpers make designs easier to construct. They do not decide whether a particular design identifies the scientific question.

## Representation sites and reducers

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: A captured module may emit a tensor such as \[ N\times C\times H\times W \] for a convolutional representation or \[ N\times T\times d \] for a transformer representation. A reducer converts each probe activation into one vector before pairwise geometry is computed. `flatten` preserves all activation values but removes the explicit tensor structure. Pooling or token-selection reducers answer different measurement questions. Reducer choice therefore belongs in the experiment specification.

## Metrics

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: A metric converts a population representation into an \(N\times N\) relational matrix. Eigenflow includes cosine similarity, Euclidean and squared Euclidean distance, Manhattan distance, correlation distance, dot-product similarity, Mahalanobis distance, RBF kernels, polynomial kernels, metric pipelines, and callable custom metrics. Different metrics expose different geometries. If a substantive result exists only under one convenient metric, that dependence is part of the result.

## Filtrations and control scale

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: A filtration varies a graph-construction parameter rather than committing the analysis to one arbitrary graph. Eigenflow includes similarity/distance thresholding, edge-density filtration, k-nearest-neighbor and mutual-kNN filtration, and weighted filtration tools. For cross-metric comparison, edge density is useful because \[ \rho = \frac{|E|}{\binom N2} \] places graphs on a common retained-edge scale. Matching edge density does not make different metrics equivalent; it makes graph sparsity comparable.

## Structural analyses

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: Built-in analyses include: - `components` - `pcscs` - `percolation` - `spectra` - `eigenspaces` - `bridges` - `kcore` - `communities` - `factor_alignment` - `class_structure` - `transitions` Component structure describes fragmentation and merger. Percolation-style quantities describe graph growth from local to macroscopic connectivity. Spectral analyses describe operator-level global organization. Eigenspace analyses track changes in structural modes. Bridge and core analyses identify pivotal and robustly connected probes. Factor analyses compare emergent structure with variables encoded in probe metadata. A strong interpretation often comes from **convergent evidence across observables with

## Layer × control scale

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: The central comparative object is often \[ Q(\ell,p), \] where \(\ell\) indexes network depth and \(p\) indexes relational scale. This supports questions such as: - Does factor-aligned structure occupy a wider control interval at later sites? - Does class coherence move toward stricter similarity as depth increases? - Does a spectral gap emerge at the same site where components become label-aligned? - Does a nuisance factor dominate early organization and then disappear? - Are important structural changes distributed gradually or concentrated at particular representation sites? Words such as “emerges” or “transition” should refer to defined observable behavior. They do not, by themselves, es

## Visualization

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: Eigenflow includes basic plotting utilities: The spectral plot is literally an eigenvalue flow across the control parameter at one representation site. Layer-control heatmaps show how an observable changes across both network depth and filtration scale.

## PCSCS

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: PCSCS is a canonical special case within Eigenflow. The preset configures flattened activations, cosine similarity, threshold filtration, PCSCS-style connected-component sifting, and spectral diagnostics across captured representation sites. Eigenflow generalizes the experimental framework by allowing the metric, filtration, graph operator, and structural analyses to vary while retaining the same population-level logic.

## Persistence and provenance

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: Save a result with: The current implementation writes a JSON representation of the experiment result and provenance. The model, probe design, preprocessing, selected sites, reducer, metric, filtration, and analysis configuration should be treated as part of the reported experimental method. For exact persistence guarantees, consult the data-model specification for the installed version.

## What Eigenflow can and cannot establish

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: Eigenflow can provide evidence that, for a defined probe population and measurement configuration, a network representation exhibits particular relational organization. It can support statements such as: > Class-related organization becomes more persistent across relational scale at later representation sites. or: > A small set of ambiguous probes repeatedly bridges two otherwise distinct groups. or: > A spectral mode aligned with background dominates early layers but weakens relative to class alignment later. Those statements remain conditional on the experiment. Eigenflow alone does not establish: - that a semantic concept is localized to a particular neuron or coordinate; - that a measure

## Where to go next

Draft move: expose the measurement assumptions, competing explanations, sensitivity checks, and evidential boundary associated with this section. Statistical content to preserve: If you are designing a study, start with [The experimental model](docs/concepts/experimental_model.md). It develops the inverse-problem logic, probe construction, competing hypotheses, confounds, and robustness planning. Use [Percolation-style analysis](docs/concepts/percolation.md) before interpreting giant-component growth, susceptibility, component-size distributions, or transition-like behavior. Use [Spectral analysis](docs/concepts/spectral_analysis.md) before interpreting eigenvalues, spectral gaps, localization, or eigenspace trajectories. Use the [VGG16 probe experiment](docs/guides/vgg16_probe_experiment.md) for a complete image-model workflow from probe construction through interpr
