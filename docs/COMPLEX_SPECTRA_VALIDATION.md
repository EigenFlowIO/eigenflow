# Complex-spectrum validation

The complex-spectrum implementation was validated against the authoritative repository baseline `66b83c9c17a0d51bb29239d7da76799fce5b2fee`.

## Regression suite

The complete repository test suite passes with 35 tests.

The complex-spectrum regression tests cover:

- preservation of genuinely complex nonsymmetric eigenpairs;
- tolerance-aware complex detection;
- all seven `complex=` policies;
- once-per-analysis diagnostics under `auto`;
- stronger diagnostics for expected-real operators;
- Hermitian eigenspace overlap and phase-invariant complex IPR;
- minimum-cost complex-plane eigenvalue matching;
- adaptive static/flow visualizations and explicit complex-plane plots;
- complex eigenvalue and eigenvector persistence round-trip;
- policy-aware comparison incompatibilities;
- summary/status propagation.

## Focused pressure test

`benchmarks/complex_spectrum_pressure_test.py` deliberately uses a triangle non-backtracking operator, whose directed-edge dynamics produce genuinely complex roots, and exercises:

- `auto`;
- `preserve`;
- `modulus`;
- `real`;
- `phase`;
- `imag`;
- `error`.

Every policy reached the intended terminal state. `error` raised the declared assumption exception; the other policies completed numerically. The run rendered 18 figures, round-tripped complex eigenvalues and eigenvectors, produced no non-finite eigenvalues, and confirmed that scalar comparison between `modulus` and `real` returns a structured `complex_policy_mismatch` while explicit raw-complex comparison succeeds.

The warning log records category, message, filename, and line number. The run produced exactly the two intended diagnostic families: `UnspecifiedComplexTreatmentWarning` for non-backtracking under `auto`, and `UnexpectedComplexSpectrumWarning` for an intentionally expected-real test operator forced to return a complex spectrum.

No uncontrolled NaN/Inf, silent complex-to-real coercion, shape exception, or complex serialization failure occurred.

The corresponding notebook is `examples/Eigenflow_Complex_Spectrum_Pressure_Test.ipynb`.
