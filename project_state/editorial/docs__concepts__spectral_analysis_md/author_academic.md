# Academic author for a computational interpretability journal draft — `docs/concepts/spectral_analysis.md`

Prioritize formal definitions, conceptual precision, epistemic scope, scholarly claim discipline, and the relation between measurements and latent-feature hypotheses.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## Choosing an operator

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Different graph operators answer different questions.

## Adjacency

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: \[ A \] The adjacency spectrum is sensitive to global connectivity, degree structure, hubs, and dense subgraphs. Its spectral radius can summarize overall connectivity strength, but interpretation may be dominated by degree heterogeneity.

## Combinatorial Laplacian

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: \[ L=D-A. \] The multiplicity of zero eigenvalues equals the number of connected components. The second-smallest eigenvalue, algebraic connectivity, measures how strongly the graph is connected beyond mere component membership.

## Normalized Laplacian

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: \[ L_{\mathrm{sym}}=I-D^{-1/2}AD^{-1/2}. \] Normalization reduces some degree-scale effects and is often useful when graph density changes substantially across the filtration. Eigenflow's default `spectra` analysis uses the normalized Laplacian.

## Random-walk operator

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: \[ P=D^{-1}A. \] This operator emphasizes diffusion and mixing behavior. The current implementation is available through the operator interface, although the default spectral analysis assumes the same generic eigensolver behavior used elsewhere.

## Modularity

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The modularity operator compares observed connectivity with a degree-based null expectation. It can be useful for community-oriented structural questions.

## Non-backtracking

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The non-backtracking operator acts on directed edges rather than vertices and suppresses immediate edge reversals. It can be useful for some sparse-network spectral questions, but its matrix dimension is the number of directed edges and its interpretation differs from node-space Laplacians. Use an operator because its mathematical object matches the structural question, not because it produces a visually dramatic spectrum.

## Configuring spectral analysis

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The analysis keyword uses the default normalized-Laplacian configuration. For explicit control, supply an analysis object: `k=None` requests the full spectrum under the current solver logic. For larger graphs, a finite `k` permits sparse partial eigensolving where supported.

## Eigenvalue observables

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Each `SpectralSnapshot` stores eigenvalues, optional eigenvectors, the operator name, and derived observables.

## Spectral radius

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: \[ \rho(M)=\max_i|\lambda_i|. \] The meaning depends strongly on the operator. For adjacency matrices it often tracks global connectivity/degree scale. For normalized Laplacians, the bounded spectrum changes the interpretation.

## Algebraic connectivity

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: For Laplacian operators, \[ \lambda_2(L) \] is zero when the graph is disconnected and becomes positive after global connectivity. Larger values generally indicate stronger connectivity against bottlenecks. Because an unweighted threshold graph changes discontinuously as edges are added, algebraic connectivity can reveal strengthening that component count no longer sees after the graph has become connected.

## Spectral gaps

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Eigenflow computes differences between sorted eigenvalues. A pronounced gap can indicate separation between groups of structural modes. A gap does not, by itself, prove the existence of a semantic number of clusters. Semantic interpretation requires comparison with probe factors and other structural evidence.

## Spectral entropy and effective rank

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Eigenflow normalizes absolute eigenvalues to a probability-like mass and computes an entropy. The exponential of that entropy is reported as effective rank. These quantities summarize how concentrated or distributed spectral mass is. They are descriptive summaries of the chosen operator spectrum, not intrinsic dimensionality estimators of the neural representation itself.

## Graph energy

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Graph energy is the sum of absolute eigenvalues. Its meaning is operator dependent and should mainly be used comparatively under matched analysis conditions.

## Eigenvectors and eigenspaces

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Eigenvalues summarize magnitudes of structural modes; eigenvectors describe their node-space organization. A Laplacian Fiedler vector, for example, can distinguish the two sides of a weak graph bottleneck. Higher modes can describe additional structural variation. For interpretability, the important question is often whether a mode aligns with an experimentally manipulated probe factor. That inference must remain relational: > this graph mode aligns with the factor partition under the chosen representation, metric, filtration, and operator. It should not be rewritten as: > this eigenvector is the network's factor feature. The eigenvector belongs to the graph operator constructed by the analy

## Localization and IPR

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: For a normalized eigenvector \(v\), Eigenflow reports inverse participation ratio \[ \operatorname{IPR}(v)=\sum_i v_i^4. \] High IPR means the mode is concentrated on fewer probes. Low IPR means it is more distributed. This helps distinguish two kinds of structural phenomena: - a spectral change driven by a small set of unusual probes; - a mode distributed across much of the population. Localization is particularly useful when a dramatic spectral feature might otherwise be mistaken for a population-wide semantic organization.

## Spectral flow across the control parameter

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: A filtration gives a sequence \[ M_{\ell,p_1}, M_{\ell,p_2}, \ldots. \] Eigenflow stores these as a `SpectralTrajectory`. The plotting helper draws eigenvalue branches across the control parameter for one representation site. The interpretation is the trajectory: where modes separate, collapse, or change rapidly—not merely the spectrum at one selected threshold.

## Spectral flow across network depth

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Repeat the same analysis across representation sites. The resulting family \[ \lambda_k(\ell,p) \] lets the experimenter ask when a structural mode appears, whether its characteristic scale moves, whether it becomes more distributed, or whether factor alignment strengthens. This is one reason Eigenflow captures the same probe population across multiple internal sites.

## Crossings, degeneracy, and eigenspace correspondence

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Sorted eigenvector index is not a stable identity across a changing graph. Eigenvalues can cross. Repeated or nearly repeated eigenvalues define subspaces whose individual basis vectors are not unique. Eigenflow's `eigenspaces` analysis therefore compares consecutive low-dimensional eigenspaces using overlap matrices and principal angles rather than assuming that "eigenvector 3" at one control value is the same mode as "eigenvector 3" at the next. Interpret stable subspaces when degeneracy is present.

## Numerical scope

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: The current eigensolver uses dense decomposition for small matrices or when a full spectrum is requested. For larger symmetric matrices with finite `k`, it can use sparse `eigsh`. Several practical consequences follow. - Full spectra scale poorly with probe count. - Non-backtracking operators can be much larger than node-space operators. - Very small eigengaps make individual eigenvectors numerically unstable. - Comparing spectra across graphs with different sizes or operators requires care. - Weighted and unweighted filtrations may produce qualitatively different spectra. Numerical instability is not a semantic transition. When a conclusion depends on one narrow eigenvalue crossing, inspect

## Connecting spectral evidence to probe hypotheses

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Suppose a factorial probe manipulates class and background. A strong spectral analysis does not begin by asking "what does \(\lambda_3\) mean?" It begins with a hypothesis: > If later representations organize by class, a class-consistent low-dimensional structural mode should become more stable and less dependent on background. Evidence might include: - a spectral gap opening over the same control interval where class-aligned components persist; - an eigenspace with strong class alignment; - decreasing localization, showing that the mode is distributed rather than caused by one outlier; - the pattern strengthening across depth; - persistence under a second metric at matched edge density. The

## Worked triangulated example

Draft move: define the conceptual object and qualify the inferential claim before presenting implementation details. Core proposition to preserve or sharpen: Imagine a late representation site where: - component count falls from many groups to two persistent groups; - those groups have high NMI with the class factor; - susceptibility peaks near the start of that two-group regime; - the normalized-Laplacian spectrum shows a stable separation among the first few modes; - the relevant eigenspace changes little over that interval; - IPR is low enough that the mode is distributed across many probes. Together, these observations support a stronger statement than any one curve: > Under this probe design and measurement configuration, the representation contains a stable, distributed, class-aligned mesoscale organization over a substantial relational sca
