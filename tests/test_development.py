import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import eigenflow as ef
from eigenflow.development import (
    ExperimentSpec,ComparisonSpec,ExperimentSeries,BehavioralRecord,StructuralDiff,
    SiteAlignment,ProbeSuite,validate_compatibility,save_series,load_series,
    peft_targeting_scores,select_checkpoint,training_data_diagnostics,development_report,
)


def make(seed=0, shift=0.0, sites="all"):
    torch.manual_seed(seed)
    model=torch.nn.Sequential(torch.nn.Linear(3,5),torch.nn.Tanh(),torch.nn.Linear(5,2))
    xs=[]; meta=[]
    for c,mu in enumerate([-1.0,1.0]):
        for j in range(8):
            x=torch.randn(3)*.08; x[0]+=mu+shift; x[1]+=0.25*c
            xs.append(x); meta.append({"class":f"c{c}","background":"a" if j%2==0 else "b"})
    probes=ef.ProbePopulation.from_items(xs,metadata=meta,name="dev_probes")
    exp=ef.Experiment(model,probes,filtration=ef.filtrations.EdgeDensityFiltration(densities=[0,.15,.35,.6]),analyses=["components","percolation","spectra","factor_alignment","bridges"],extraction=ef.ExtractionConfig(sites=sites),measurement_metadata={"purpose":"development-test"})
    return exp


def _close(fig):
    assert hasattr(fig,"savefig"); plt.close(fig)


def test_experiment_spec_and_compatibility():
    a=make(1); b=make(2)
    sa=ExperimentSpec.from_experiment(a); sb=ExperimentSpec.from_experiment(b)
    assert sa.probe_fingerprint==sb.probe_fingerprint
    report=validate_compatibility(sa,sb)
    assert report.compatible
    c=make(2); c.metric="euclidean"
    report2=validate_compatibility(sa,ExperimentSpec.from_experiment(c))
    assert not report2.compatible
    assert any(i.field=="metric" for i in report2.errors)


def test_probe_suite_and_series_longitudinal_diff(tmp_path):
    a=make(3); b=make(4)
    suite=ProbeSuite({"target":a.probes,"retain":a.probes},name="suite",version="v1")
    assert len(suite.fingerprint)==64
    assert suite.save_manifest(tmp_path/"suite").exists()
    series=ExperimentSeries("checkpoints")
    e0=series.add_experiment("base",a,time=0,checkpoint="0",behavior=BehavioralRecord({"accuracy":.7},{"latency_ms":2.0}))
    e1=series.add_experiment("step1",b,time=1,checkpoint="1",behavior=BehavioralRecord({"accuracy":.8},{"latency_ms":2.1}))
    long=series.longitudinal("base")
    site=list(e0.result.layers)[-1]
    traj=long.trajectory(site,"components","component_count")
    assert traj.shape==(2,4)
    assert np.allclose(long.baseline_delta(site,"components","component_count")[0],0)
    diff=StructuralDiff.between(e0,e1)
    assert diff.compatibility.compatible
    saved=save_series(series,tmp_path/"series")
    loaded=load_series(saved)
    assert [e.key for e in loaded.entries]==["base","step1"]
    assert loaded.entries[1].behavior.metrics["accuracy"]==.8
    assert loaded.longitudinal().trajectory(site,"components","component_count").shape==(2,4)


def test_site_alignment_and_diagnostics():
    a=make(5).run(); b=make(6).run()
    sa=ExperimentSpec.from_dict(a.metadata["experiment_spec"]); sb=ExperimentSpec.from_dict(b.metadata["experiment_spec"])
    series=ExperimentSeries("diag")
    series.add_result("base",a,sa,time=0)
    series.add_result("later",b,sb,time=1)
    scores=peft_targeting_scores(series)
    assert scores and "site" in scores[0]
    selection=select_checkpoint(series,lambda e: 1.0 if e.key=="later" else 0.0)
    assert selection["key"]=="later"
    diag=training_data_diagnostics(b)
    assert "bridge_probes" in diag
    report=development_report(series)
    assert report.series=="diag"
    alignment=SiteAlignment.normalized_depth(list(a.layers),list(b.layers))
    assert alignment.mapping


def test_development_visualizations():
    series=ExperimentSeries("viz")
    series.add_experiment("base",make(7),time=0,behavior=BehavioralRecord({"accuracy":.60},{"latency":1.0}))
    series.add_experiment("one",make(8),time=1,behavior=BehavioralRecord({"accuracy":.75},{"latency":1.1}))
    series.add_experiment("two",make(9),time=2,behavior=BehavioralRecord({"accuracy":.82},{"latency":1.2}))
    long=series.longitudinal(); site=list(series.entries[0].result.layers)[-1]; v=ef.visualization
    _close(v.checkpoint_trajectory(long,site,"components","component_count"))
    _close(v.longitudinal_surface(long,site,"components","component_count"))
    _close(v.longitudinal_surface(long,site,"components","component_count",baseline_delta=True))
    _close(v.layer_time_heatmap(long,"components","component_count"))
    diff=StructuralDiff.between(series.entries[0],series.entries[-1])
    _close(v.structural_diff_heatmap(diff,"components","component_count"))
    _close(v.architecture_comparison(series))
    _close(v.retention_dashboard({"target":series,"retain":series},site=site))
    _close(v.development_dashboard(series,site=site))
