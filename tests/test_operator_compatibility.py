import numpy as np
import pytest

import eigenflow as ef
from eigenflow.analyses import AnalysisContext, EigenspaceAnalysis, LocalizationAnalysis, SpectralAnalysis
from eigenflow.exceptions import OperatorCompatibilityError
from eigenflow.filtrations import EdgeDensityFiltration, WeightedThresholdFiltration
from eigenflow.metrics import CosineSimilarity
from eigenflow.operators import (
    NormalizedLaplacianOperator,
    RandomWalkOperator,
    SignedLaplacianOperator,
    SignedNormalizedLaplacianOperator,
)
from eigenflow.representations import Representation


def _signed_context():
    # Includes antipodal probes so cosine produces negative retained weights.
    X = np.array([
        [1.0, 0.0],
        [0.8, 0.2],
        [-1.0, 0.0],
        [-0.8, -0.2],
    ])
    ids = ["a", "b", "c", "d"]
    rep = Representation(X, "hidden", ids)
    rel = CosineSimilarity().pairwise(rep)
    probes = ef.ProbePopulation.from_items([row for row in X])
    gf = WeightedThresholdFiltration(values=[0.5, 0.0, -1.0]).build(rel)
    return AnalysisContext("hidden", rep, rel, gf, probes)


def test_normalized_laplacian_rejects_negative_weights_before_scipy():
    ctx = _signed_context()
    signed_snapshot = ctx.filtration.snapshots[-1]
    with pytest.raises(OperatorCompatibilityError) as exc:
        NormalizedLaplacianOperator().matrix(signed_snapshot)
    assert exc.value.reason == "negative_edge_weights"
    assert exc.value.details["negative_edge_count"] > 0


def test_random_walk_rejects_negative_weights():
    ctx = _signed_context()
    with pytest.raises(OperatorCompatibilityError) as exc:
        RandomWalkOperator().matrix(ctx.filtration.snapshots[-1])
    assert exc.value.reason == "negative_edge_weights"


def test_spectral_analysis_records_signed_incompatibility_instead_of_failing():
    ctx = _signed_context()
    out = SpectralAnalysis(operator="normalized_laplacian").run(ctx)
    assert len(out.records) == len(ctx.filtration.snapshots)
    assert out.metadata["incompatible_snapshots"] >= 1
    incompatible = [r for r in out.records if r["status"] == "incompatible"]
    assert incompatible
    assert all(r["reason"] == "negative_edge_weights" for r in incompatible)
    assert all(r["eigenvalues"] is None for r in incompatible)


def test_localization_analysis_propagates_compatibility_records():
    ctx = _signed_context()
    out = LocalizationAnalysis(operator="normalized_laplacian").run(ctx)
    assert len(out.records) == len(ctx.filtration.snapshots)
    assert any(r["status"] == "incompatible" for r in out.records)
    assert len(out.observables["ipr"]) == len(ctx.filtration.snapshots)


def test_signed_laplacians_are_finite_on_signed_graphs():
    ctx = _signed_context()
    snap = ctx.filtration.snapshots[-1]
    for operator in (SignedLaplacianOperator(), SignedNormalizedLaplacianOperator()):
        M = operator.matrix(snap).toarray()
        assert np.isfinite(M).all()
        assert np.allclose(M, M.T)


def test_signed_normalized_spectral_analysis_succeeds():
    ctx = _signed_context()
    out = SpectralAnalysis(operator="signed_normalized_laplacian").run(ctx)
    assert out.metadata["incompatible_snapshots"] == 0
    assert all(r["status"] == "ok" for r in out.records)
    assert all(np.isfinite(r["eigenvalues"]).all() for r in out.records)


def test_nonbacktracking_eigenspace_dimension_change_is_structured_incompatibility():
    X = np.array([
        [1.0, 0.0],
        [0.9, 0.1],
        [0.7, 0.3],
        [0.0, 1.0],
        [0.1, 0.9],
    ])
    ids = [str(i) for i in range(len(X))]
    rep = Representation(X, "hidden", ids)
    rel = CosineSimilarity().pairwise(rep)
    gf = EdgeDensityFiltration(densities=[0.2, 0.5, 0.8]).build(rel)
    probes = ef.ProbePopulation.from_items([row for row in X])
    ctx = AnalysisContext("hidden", rep, rel, gf, probes)

    out = EigenspaceAnalysis(operator="nonbacktracking", dimensions=2).run(ctx)

    assert len(out.records) == 3
    assert out.metadata["operator_space"] == "directed_edge"
    assert out.metadata["incompatible_comparisons"] >= 1
    changed = [r for r in out.records if r["status"] == "incompatible"]
    assert changed
    assert all(r["reason"] == "changing_ambient_space" for r in changed)
    assert all(r["overlap"] is None for r in changed)
    assert all(r["principal_angles"] is None for r in changed)
