# Graph/operator compatibility

Eigenflow treats graph construction and graph operators as separate experimental choices. Not every graph/operator pairing is mathematically meaningful.

## Signed weighted graphs

`weighted_threshold` may preserve negative weights when the relational matrix is a similarity matrix such as cosine or dot product. Negative weights are legitimate relational measurements; Eigenflow does not silently clip, shift, or take their absolute value.

The ordinary `normalized_laplacian` and `random_walk` operators require nonnegative weights under their standard degree-normalization semantics. They therefore reject signed graphs with a structured `OperatorCompatibilityError` before matrix normalization. `SpectralAnalysis`, `EigenspaceAnalysis`, and `LocalizationAnalysis` convert that condition into result records with `status="incompatible"`.

For deliberate signed-graph analysis, Eigenflow provides:

- `signed_laplacian`: `D_abs - A`, where `D_abs[i,i] = sum_j |w_ij|`.
- `signed_normalized_laplacian`: `I - D_abs^(-1/2) A D_abs^(-1/2)`.

These are explicit alternative operators, not silent fallbacks.

## Non-backtracking eigenspaces

The non-backtracking operator acts in directed-edge space. Its ambient dimension changes when the filtration changes the number of edges. Spectra remain well-defined at each snapshot, but direct eigenspace overlap/principal-angle calculations require a common ambient space.

`EigenspaceAnalysis(operator="nonbacktracking")` therefore records `status="incompatible"` with `reason="changing_ambient_space"` whenever consecutive snapshots differ in directed-edge dimension. It does not invent an implicit edge-space alignment.

A future explicit edge-alignment method may make some such comparisons meaningful, but that would be a separate analysis choice.
