# Complex spectra

Eigenflow preserves genuinely complex eigenvalues and eigenvectors instead of coercing them to real values. This matters most for nonsymmetric operators such as the non-backtracking operator, whose spectra can be intrinsically complex even on ordinary undirected graphs.

The public interface remains deliberately small. `SpectralAnalysis` accepts one keyword:

```python
from eigenflow.analyses import SpectralAnalysis

spectral = SpectralAnalysis(
    operator="nonbacktracking",
    complex="modulus",
)
```

The allowed values are `"auto"`, `"preserve"`, `"modulus"`, `"real"`, `"phase"`, `"imag"`, and `"error"`.

## Policies

`complex="auto"` is the default. Effectively real spectra behave exactly like ordinary Eigenflow spectra and do not produce extra noise. If meaningfully complex eigenvalues appear, Eigenflow preserves them, emits one actionable diagnostic for the analysis, and skips scalar summaries that would require an undeclared projection.

`complex="preserve"` states that complex structure is intentional. Raw complex values remain authoritative and only intrinsically complex-safe summaries are used unless another projection is requested explicitly.

`complex="modulus"` uses `|lambda|` for scalar ordering, gap-like summaries, and one-dimensional trajectories while preserving raw complex values. For discrete propagation operators this is often the most natural scalar treatment because repeated application scales a mode by `|lambda|^k`.

`complex="real"` uses `Re(lambda)` for scalar summaries. This should be selected only when the research interpretation specifically supports the real part.

`complex="phase"` uses `arg(lambda)` for phase-oriented analysis. Eigenflow treats phase as circular data and unwraps phase only after mode matching across adjacent snapshots.

`complex="imag"` uses `Im(lambda)` when explicitly requested. It is supported for specialist analyses but is not promoted as a generic structural interpretation.

`complex="error"` asserts that a materially complex spectrum violates the intended analysis assumptions and raises `ComplexSpectrumAssumptionError`.

## What the coordinates mean

For

\[
\lambda = a + ib = r e^{i\theta},
\]

`r = |lambda|` describes amplification or decay under repeated application of a discrete operator, while `theta = arg(lambda)` describes rotation or oscillation per application. `Re(lambda)` and `Im(lambda)` are Cartesian coordinates of the same mode; they should not automatically be interpreted as independent scientific quantities.

A complex eigenvalue is structural evidence about the induced graph operator. It is not, by itself, evidence that a learned latent feature has a particular semantic meaning.

## Operator expectations

Eigenflow records internal expectations so diagnostics can distinguish ordinary complex spectra from surprising ones.

Expected effectively real under the current graph constructions:

- adjacency
- combinatorial Laplacian
- normalized Laplacian
- signed Laplacian
- signed normalized Laplacian
- modularity

Conditionally real under the current undirected, nonnegative assumptions:

- random walk

Potentially complex:

- non-backtracking

If an operator expected to be real produces materially complex values, `complex="auto"` emits a stronger diagnostic because numerical instability, graph asymmetry, or an invalid construction may be involved.

## Detection

Eigenflow does not test `imag != 0`. It classifies an eigenvalue as meaningfully complex using an absolute-plus-relative tolerance:

\[
|\operatorname{Im}\lambda| > \epsilon_{abs} + \epsilon_{rel}|\lambda|.
\]

The package defaults and the observed diagnostics are persisted in analysis metadata.

## Complex-safe mathematics

Complex eigenspaces use Hermitian inner products. Eigenspace overlap therefore uses `V.conj().T @ W`. Localization uses magnitude-based inverse participation ratio,

\[
\operatorname{IPR}(v)=\sum_i |v_i|^4,
\]

so arbitrary global phase does not change the result.

Spectral radius remains

\[
\rho(M)=\max_i |\lambda_i|.
\]

Generic gaps do not silently change meaning. A modulus policy produces a `modulus_gap`; a real policy produces a real-order gap; phase uses circular phase gaps. Under `auto` or `preserve`, genuinely complex spectra do not receive an invented scalar gap.

## Trajectories

Eigenflow does not treat sorted eigenvalue index as mode identity. Adjacent spectra are matched by minimum-cost assignment in the complex plane using

\[
c_{ij}=|\lambda_i^{(t)}-\lambda_j^{(t+1)}|.
\]

This supports complex eigenvalue trajectories even when ordering changes. It does not solve changing ambient eigenspaces. Non-backtracking eigenspace comparisons remain explicitly incompatible when directed-edge dimension changes unless an edge-space alignment is supplied in a future extension.

## Visualization

`static_spectrum(result_layer)` remains a conventional one-dimensional plot for effectively real spectra and for explicit scalar policies. If a genuinely complex spectrum is preserved without a scalar projection, it automatically renders the canonical complex-plane view.

`complex_spectrum_plot(result_layer)` explicitly plots `Re(lambda)` against `Im(lambda)` with a unit circle and spectral-radius circle.

`spectral_flow(result_layer)` uses matched modes. It plots the selected scalar coordinate for `modulus`, `real`, `imag`, or `phase`, and a complex-plane trajectory when complex values are preserved without projection.

## Comparison and persistence

Scalar spectral comparisons require compatible policies. Comparing a modulus summary with a real-part summary returns a structured incompatibility rather than silently subtracting unlike quantities. Raw complex spectra can still be compared explicitly in the complex plane.

`ExperimentResult.save()` stores complex eigenvalues in portable JSON and stores spectral eigenvectors in a compressed `spectral_eigenvectors.npz` sidecar. `load_result_object()` reconstructs both when the sidecar is present. Older real-only results without the sidecar remain readable.

## Scope

This feature does not attempt to provide a full nonnormal transient-growth or pseudospectral framework. Those are separate research capabilities and should only be added when the scientific use case justifies the additional API and computational cost.
