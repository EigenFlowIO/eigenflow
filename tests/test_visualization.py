import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
import eigenflow as ef
from eigenflow.analyses import EigenspaceAnalysis,ClassStructureAnalysis


def _result(metric=None):
    torch.manual_seed(3)
    model=torch.nn.Sequential(torch.nn.Linear(4,6),torch.nn.ReLU(),torch.nn.Linear(6,3))
    xs=[]; meta=[]
    for c,mu in enumerate([1.0,-1.0,0.0]):
        for j in range(5):
            x=torch.randn(4)*0.15
            x[0]+=mu; x[1]+=0.6*c
            xs.append(x); meta.append({"class":f"c{c}","background":"a" if j%2==0 else "b"})
    probes=ef.ProbePopulation.from_items(xs,metadata=meta)
    return ef.Experiment(
        model,probes,
        metric=metric or ef.metrics.CosineSimilarity(),
        filtration=ef.filtrations.EdgeDensityFiltration(start=0,stop=.7,steps=12),
        analyses=["components","pcscs","percolation","spectra",EigenspaceAnalysis(dimensions=2),"factor_alignment",ClassStructureAnalysis("class"),"bridges","kcore","communities","transitions"],
    ).run()


def _isfig(fig):
    assert hasattr(fig,"savefig")
    plt.close(fig)


def test_visualization_surface_smoke():
    result=_result(); layer=next(iter(result.layers.values())); probes=result.artifacts.probes; v=ef.visualization
    _isfig(v.probe_design_view(result,["class","background"]))
    _isfig(v.relational_matrix_heatmap(layer,probes=probes,factor="class"))
    _isfig(v.component_trajectory(layer,analysis="pcscs"))
    _isfig(v.component_membership_raster(layer,probes=probes,factor="class"))
    _isfig(v.merge_event_plot(layer))
    _isfig(v.dendrogram_view(layer,probes=probes,factor="class"))
    _isfig(v.percolation_dashboard(layer))
    _isfig(v.graph_snapshot(layer,probes=probes,factor="class",highlight_bridges=True,kcore=2))
    _isfig(v.static_spectrum(layer))
    _isfig(v.spectral_flow(layer,max_modes=5))
    _isfig(v.spectral_properties_dashboard(layer))
    _isfig(v.localization_trajectory(layer))
    _isfig(v.eigenspace_stability(layer))
    _isfig(v.eigenspace_overlap_heatmap(layer))
    _isfig(v.factor_alignment_trajectory(layer,["class","background"]))
    _isfig(v.factor_connectivity(layer))
    _isfig(v.layer_control_heatmap(result,"components","component_count"))
    _isfig(v.combined_layer_dynamics(result,"components","component_count"))
    _isfig(v.bridge_probe_frequency(layer,probes=probes))
    _isfig(v.interpretation_dashboard(layer,"class"))


def test_visualization_comparison_views():
    a=_result(ef.metrics.CosineSimilarity()); b=_result(ef.metrics.EuclideanDistance()); v=ef.visualization
    site=list(a.layers)[-1]
    _isfig(v.robustness_comparison([a,b],["cosine","euclidean"],site=site,factor="class"))
    _isfig(v.cross_result_summary([a,b],["cosine","euclidean"]))


def test_result_runtime_artifacts_are_not_serialized(tmp_path):
    result=_result(); result.save(tmp_path)
    text=(tmp_path/"result.json").read_text()
    assert '"artifacts"' not in text
    assert result.artifacts.probes is not None
    assert next(iter(result.layers.values())).artifacts.relational_matrix is not None
