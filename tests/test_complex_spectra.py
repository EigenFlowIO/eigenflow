import warnings
from types import SimpleNamespace

import matplotlib
matplotlib.use("Agg")
import numpy as np
import pytest

from eigenflow.analyses import AnalysisContext, SpectralAnalysis
from eigenflow.analyses.base import AnalysisResult
from eigenflow.exceptions import (
    ComplexSpectrumAssumptionError,
    UnspecifiedComplexTreatmentWarning,
    UnexpectedComplexSpectrumWarning,
)
from eigenflow.operators import GraphOperator
from eigenflow.result import ExperimentResult, LayerResult
from eigenflow.serialization import load_result_object
from eigenflow.spectra import (
    SpectralSnapshot,
    SpectralTrajectory,
    characterize_spectrum,
    compare_spectral_snapshots,
    eigenspace_overlap,
    ipr,
    match_eigenvalues,
    project_eigenvalues,
    solve_spectrum,
    spectral_gaps,
)
from eigenflow.visualization import complex_spectrum_plot, spectral_flow, static_spectrum


class _FixedOperator(GraphOperator):
    name = "fixed_complex"
    spectral_expectation = "potentially_complex"
    def matrix(self, snapshot):
        return np.array([[0.0, -1.0], [1.0, 0.0]])


class _ExpectedRealFixedOperator(_FixedOperator):
    name = "fixed_expected_real"
    spectral_expectation = "expected_real"


def _ctx(n=3):
    filtration = [SimpleNamespace(parameter=float(i)) for i in range(n)]
    return AnalysisContext("hidden", None, None, filtration, None)


def test_nonsymmetric_solver_preserves_complex_eigenpairs():
    vals, vecs = solve_spectrum(np.array([[0.0, -1.0], [1.0, 0.0]]))
    assert np.iscomplexobj(vals)
    assert np.allclose(np.sort(np.abs(vals)), [1.0, 1.0])
    assert np.max(np.abs(vals.imag)) == pytest.approx(1.0)
    assert np.iscomplexobj(vecs)


def test_complex_detection_ignores_tiny_roundoff_but_detects_real_signal():
    tiny = characterize_spectrum(np.array([1 + 1e-14j]))
    genuine = characterize_spectrum(np.array([1 + 1e-3j]))
    assert not tiny["complex_detected"]
    assert genuine["complex_detected"]
    assert genuine["complex_count"] == 1


def test_projection_policies_are_non_destructive_and_explicit():
    vals = np.array([3 + 4j, -1 + 0j])
    assert project_eigenvalues(vals, "auto") is None
    assert project_eigenvalues(vals, "preserve") is None
    assert np.allclose(project_eigenvalues(vals, "modulus"), [5, 1])
    assert np.allclose(project_eigenvalues(vals, "real"), [3, -1])
    assert np.allclose(project_eigenvalues(vals, "imag"), [4, 0])
    assert np.allclose(project_eigenvalues(vals, "phase"), np.angle(vals))
    assert spectral_gaps(vals, "auto") is None
    assert spectral_gaps(vals, "modulus") is not None


def test_complex_error_policy_enforces_declared_real_assumption():
    with pytest.raises(ComplexSpectrumAssumptionError):
        SpectralAnalysis(operator=_FixedOperator(), complex="error").run(_ctx(1))


def test_auto_warns_once_for_expected_complex_operator_and_preserves_spectrum():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        out = SpectralAnalysis(operator=_FixedOperator(), complex="auto").run(_ctx(3))
    hits = [w for w in caught if issubclass(w.category, UnspecifiedComplexTreatmentWarning)]
    assert len(hits) == 1
    assert out.metadata["complex_snapshots"] == 3
    assert out.metadata["unexpected_complex_snapshots"] == 0
    assert all(r["projected_eigenvalues"] is None for r in out.records)
    assert all(r["gaps"] is None for r in out.records)
    assert np.iscomplexobj(out.observables["trajectory"].snapshots[0].eigenvalues)


def test_auto_escalates_message_for_operator_expected_real():
    with pytest.warns(UnexpectedComplexSpectrumWarning):
        out = SpectralAnalysis(operator=_ExpectedRealFixedOperator(), complex="auto").run(_ctx(1))
    assert out.metadata["unexpected_complex_snapshots"] == 1


def test_complex_eigenvector_math_is_phase_safe():
    v = np.array([[1.0], [1.0j]]) / np.sqrt(2)
    w = v * np.exp(1j * 0.73)
    assert eigenspace_overlap(v, w)[0, 0] == pytest.approx(1.0)
    assert ipr(v)[0] == pytest.approx(0.5)


def test_complex_matching_uses_plane_distance_not_sorted_index():
    prev = np.array([1j, -1j])
    cur = np.array([-0.9j, 0.9j])  # deliberately swapped order
    pairs = dict(match_eigenvalues(prev, cur))
    assert pairs[0] == 1
    assert pairs[1] == 0


def _complex_layer(policy="preserve"):
    vals0 = np.array([1j, -1j])
    vals1 = np.array([0.9j, -0.9j])
    vec0 = np.array([[1, 1], [1j, -1j]], dtype=complex) / np.sqrt(2)
    vec1 = vec0 * np.exp(0.25j)
    snaps = [
        SpectralSnapshot(0.0, vals0, vec0, "nonbacktracking", {"spectral_radius":1.0,"gaps":None,"complex_policy":policy}, policy),
        SpectralSnapshot(1.0, vals1, vec1, "nonbacktracking", {"spectral_radius":0.9,"gaps":None,"complex_policy":policy}, policy),
    ]
    ar = AnalysisResult("spectra", {"trajectory":SpectralTrajectory(snaps,"nonbacktracking")}, [
        {"parameter":0.0,"status":"ok","eigenvalues":vals0.tolist(),"complex_policy":policy},
        {"parameter":1.0,"status":"ok","eigenvalues":vals1.tolist(),"complex_policy":policy},
    ], {"operator":"nonbacktracking","complex_policy":policy,"complex_snapshots":2})
    return LayerResult("hidden","cosine","edge_density",{"spectra":ar})


def test_complex_visualizations_render_without_projection_guessing():
    layer = _complex_layer("preserve")
    for fn in (static_spectrum, complex_spectrum_plot, spectral_flow):
        fig = fn(layer)
        assert fig is not None


def test_complex_spectrum_persistence_round_trip(tmp_path):
    layer = _complex_layer("modulus")
    result = ExperimentResult({"hidden":layer},{"test":True})
    result.save(tmp_path)
    loaded = load_result_object(tmp_path)
    vals = loaded.layers["hidden"].analyses["spectra"].observables["trajectory"].snapshots[0].eigenvalues
    assert np.allclose(vals, np.array([1j,-1j]))
    assert loaded.layers["hidden"].analyses["spectra"].metadata["complex_policy"] == "modulus"
    vecs = loaded.layers["hidden"].analyses["spectra"].observables["trajectory"].snapshots[0].eigenvectors
    assert vecs is not None and np.iscomplexobj(vecs)
    assert np.allclose(vecs, layer.analyses["spectra"].observables["trajectory"].snapshots[0].eigenvectors)


def test_result_summary_surfaces_structured_status_and_complex_counts():
    layer = _complex_layer("preserve")
    result = ExperimentResult({"hidden":layer},{})
    summary = result.summary()
    assert summary["hidden"]["analyses"]["spectra"]["status"] == "ok"
    assert summary["hidden"]["analyses"]["spectra"]["complex_snapshots"] == 2


def test_policy_aware_comparison_rejects_mixed_scalar_semantics_but_allows_raw_complex():
    left=_complex_layer("modulus").analyses["spectra"].observables["trajectory"].snapshots[0]
    right=_complex_layer("real").analyses["spectra"].observables["trajectory"].snapshots[1]
    scalar=compare_spectral_snapshots(left,right,mode="policy")
    assert scalar["status"] == "incompatible"
    assert scalar["reason"] == "complex_policy_mismatch"
    raw=compare_spectral_snapshots(left,right,mode="complex")
    assert raw["status"] == "ok"
    assert raw["matched_modes"] == 2
