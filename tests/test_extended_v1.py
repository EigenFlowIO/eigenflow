import numpy as np
import torch
import eigenflow as ef
from eigenflow.metrics import MetricPipeline, Center, L2Normalize
from eigenflow.filtrations import WeightedThresholdFiltration
from eigenflow.operators import NonBacktrackingOperator
from eigenflow.percolation import finite_size_resample
from eigenflow.serialization import load_result


def test_metric_pipeline_and_weighted_filtration():
    X=np.array([[1.,0.],[.8,.2],[0.,1.]])
    rep=ef.representations.Representation(X,"x",["a","b","c"])
    rel=MetricPipeline([Center(),L2Normalize()],"cosine").pairwise(rep)
    gf=WeightedThresholdFiltration(values=[0.0]).build(rel)
    assert gf.snapshots[0].metadata["weighted"] is True


def test_nonbacktracking_operator_shape():
    X=np.array([[1.,0.],[.9,.1],[0.,1.]])
    rep=ef.representations.Representation(X,"x",["a","b","c"])
    rel=ef.metrics.CosineSimilarity().pairwise(rep)
    snap=ef.filtrations.EdgeDensityFiltration(densities=[1.0]).build(rel).snapshots[0]
    B=NonBacktrackingOperator().matrix(snap)
    assert B.shape[0] == snap.adjacency.nnz


def test_transitions_keyword_and_portable_load(tmp_path):
    model=torch.nn.Sequential(torch.nn.Linear(2,4),torch.nn.ReLU(),torch.nn.Linear(4,2))
    probes=ef.ProbePopulation.from_items([torch.randn(2) for _ in range(10)])
    r=ef.Experiment(model,probes,filtration=ef.filtrations.EdgeDensityFiltration(densities=[0,.2,.5,1]),analyses=["transitions","localization"]).run()
    assert all("transitions" in lr.analyses for lr in r.layers.values())
    r.save(tmp_path)
    d=load_result(tmp_path)
    assert "layers" in d


def test_finite_size_resampling():
    X=np.eye(6)
    rep=ef.representations.Representation(X,"x",[str(i) for i in range(6)])
    rel=ef.metrics.CosineSimilarity().pairwise(rep)
    filt=ef.filtrations.EdgeDensityFiltration(densities=[0,.5])
    rec=finite_size_resample(rel,filt,lambda gf: len(gf.snapshots),sizes=[4],repeats=3,seed=2)
    assert len(rec)==3 and all(r["value"]==2 for r in rec)
