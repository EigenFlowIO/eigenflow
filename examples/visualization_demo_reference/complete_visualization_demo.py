"""Complete Eigenflow visualization demonstration.

Runs a genuinely trained synthetic three-class neural-network experiment on an
exactly balanced class × background probe design, generates the canonical
visualization suite, exports numerical results and provenance metadata, and
creates a self-contained ZIP. Designed to run locally or in Google Colab after
installing Eigenflow from the repository.
"""
from __future__ import annotations
import argparse,csv,json,os,platform,sys,zipfile,hashlib,shutil
from pathlib import Path
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import eigenflow as ef
from eigenflow.analyses import EigenspaceAnalysis,ClassStructureAnalysis

SEED=17


def make_dataset(n_per_cell=30,seed=SEED):
    g=torch.Generator().manual_seed(seed)
    xs=[]; ys=[]; meta=[]
    centers=[(-1.5,-0.8),(1.5,-0.8),(0.0,1.6)]
    for c,(a,b) in enumerate(centers):
        for bg in [0,1]:
            for j in range(n_per_cell):
                x=torch.randn(6,generator=g)*0.45
                x[0]+=a; x[1]+=b
                # nuisance/background factor intentionally visible but not predictive of class
                x[2]+=(-1.0 if bg==0 else 1.0)
                x[3]+=0.25*(-1.0 if bg==0 else 1.0)
                xs.append(x); ys.append(c)
                meta.append({"class":f"class_{c}","background":f"bg_{bg}","cell":f"c{c}_b{bg}"})
    return torch.stack(xs),torch.tensor(ys),meta


def build_model():
    return torch.nn.Sequential(
        torch.nn.Linear(6,16),torch.nn.ReLU(),
        torch.nn.Linear(16,10),torch.nn.ReLU(),
        torch.nn.Linear(10,3),
    )


def train(model,X,y,epochs=160):
    opt=torch.optim.Adam(model.parameters(),lr=0.03,weight_decay=1e-4)
    hist=[]
    for epoch in range(epochs):
        model.train(); opt.zero_grad(); logits=model(X); loss=torch.nn.functional.cross_entropy(logits,y); loss.backward(); opt.step()
        if epoch%5==0 or epoch==epochs-1:
            acc=(logits.argmax(1)==y).float().mean().item(); hist.append({"epoch":epoch,"loss":float(loss.item()),"accuracy":acc})
    model.eval(); return hist


def run_experiment(model,probes,metric):
    return ef.Experiment(
        model=model,
        probes=probes,
        metric=metric,
        filtration=ef.filtrations.EdgeDensityFiltration(start=0.0,stop=0.45,steps=32),
        analyses=[
            "components","pcscs","percolation","spectra",
            EigenspaceAnalysis(operator="normalized_laplacian",dimensions=3),
            "factor_alignment",ClassStructureAnalysis("class"),
            "bridges","kcore","communities","transitions",
        ],
    ).run()


def savefig(fig,path):
    fig.savefig(path,dpi=160,bbox_inches="tight"); plt.close(fig)


def write_csv(path,rows,fieldnames=None):
    rows=list(rows)
    if not rows:
        path.write_text(""); return
    if fieldnames is None: fieldnames=sorted(set().union(*(r.keys() for r in rows)))
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fieldnames); w.writeheader(); w.writerows(rows)


def main(output_dir="eigenflow_visualization_demo_outputs"):
    torch.manual_seed(SEED); np.random.seed(SEED)
    out=Path(output_dir); figs=out/"figures"; tables=out/"tables"; native=out/"native_result"; out.mkdir(parents=True,exist_ok=True); figs.mkdir(exist_ok=True); tables.mkdir(exist_ok=True)

    X,y,meta=make_dataset()
    # Deliberate balanced split: each of the 3 class × 2 background cells contributes
    # 20 training examples and 10 probe examples. The probe is therefore an exact
    # factorial instrument rather than a random held-out convenience sample.
    train_idx=[]; probe_idx=[]
    cell_size=30
    for cell in range(6):
        start=cell*cell_size
        train_idx.extend(range(start,start+20))
        probe_idx.extend(range(start+20,start+30))
    train_idx=torch.tensor(train_idx); probe_idx=torch.tensor(probe_idx)
    model=build_model(); history=train(model,X[train_idx],y[train_idx])
    with torch.no_grad(): probe_acc=float((model(X[probe_idx]).argmax(1)==y[probe_idx]).float().mean())
    pmeta=[meta[i] for i in probe_idx.tolist()]
    probes=ef.ProbePopulation.from_items([x for x in X[probe_idx]],metadata=pmeta,ids=[f"probe_{i:03d}" for i in range(len(probe_idx))],name="controlled_three_class_probe")

    cosine=run_experiment(model,probes,ef.metrics.CosineSimilarity())
    euclidean=run_experiment(model,probes,ef.metrics.EuclideanDistance())
    cosine.save(native)
    torch.save(model.state_dict(),out/"trained_model_state.pt")

    final_site=list(cosine.layers)[-1]; final=cosine.layers[final_site]
    v=ef.visualization
    manifest=[]
    def add(name,fig,question,source,tier):
        path=figs/f"{name}.png"; savefig(fig,path); manifest.append({"file":str(path.relative_to(out)),"visualization":name,"tier":tier,"question":question,"source":source,"site":final_site if "layer" in source.lower() or "final" in source.lower() else ""})

    add("01_probe_design",v.probe_design_view(cosine,["class","background"]),"Is the probe population factorially balanced?","ExperimentResult.artifacts.probes","primary evidential")
    add("02_relational_matrix",v.relational_matrix_heatmap(final,probes=probes,factor="class"),"What pairwise geometry exists before thresholding?","final LayerResult.artifacts.relational_matrix","primary evidential")
    add("03_component_trajectory",v.component_trajectory(final,analysis="pcscs"),"How does fragmentation collapse across scale?","final LayerResult pcscs","primary evidential")
    add("04_component_membership_raster",v.component_membership_raster(final,probes=probes,factor="class"),"Which probes remain grouped across scale?","final LayerResult filtration","primary evidential")
    add("05_merge_events",v.merge_event_plot(final),"Which component mergers occur and when?","final LayerResult filtration","primary evidential")
    add("06_dendrogram",v.dendrogram_view(final,probes=probes,factor="class"),"What hierarchical merge order is induced by the relational geometry?","final LayerResult relational matrix","primary evidential")
    add("07_percolation_dashboard",v.percolation_dashboard(final),"How does local structure become macroscopic connectivity?","final LayerResult components+percolation","summary/report")
    peak=final.analyses["percolation"].observables["susceptibility_peak_parameter"]
    add("08_graph_snapshot",v.graph_snapshot(final,parameter=peak,probes=probes,factor="class",highlight_bridges=True,kcore=2),"What probes and relations are structurally pivotal near the transition region?","final LayerResult graph snapshot","diagnostic")
    add("09_static_spectrum",v.static_spectrum(final,parameter=peak),"What operator-scale structure exists at the selected graph state?","final LayerResult spectral snapshot","primary evidential")
    add("10_spectral_flow",v.spectral_flow(final,max_modes=10),"How does the operator spectrum evolve across graph scale?","final LayerResult SpectralTrajectory","primary evidential")
    add("11_spectral_properties",v.spectral_properties_dashboard(final),"How do complementary spectral summaries evolve jointly?","final LayerResult SpectralTrajectory","summary/report")
    add("12_localization",v.localization_trajectory(final,mode=1),"Is a structural mode distributed or localized to a few probes?","final LayerResult spectral IPR","diagnostic")
    add("13_eigenspace_stability",v.eigenspace_stability(final),"Are low-dimensional structural modes stable through the filtration?","final LayerResult eigenspaces","primary evidential")
    add("14_eigenspace_overlap",v.eigenspace_overlap_heatmap(final,index=-1),"How strongly do adjacent low-dimensional eigenspaces correspond?","final LayerResult eigenspaces","primary evidential")
    add("15_factor_alignment",v.factor_alignment_trajectory(final,["class","background"]),"Which controlled factor best aligns with emergent graph structure?","final LayerResult factor_alignment","primary evidential")
    add("16_factor_connectivity",v.factor_connectivity(final),"Are class groups internally coherent relative to external mixing?","final LayerResult class_structure","primary evidential")
    add("17_layer_control_heatmap",v.layer_control_heatmap(cosine,"components","component_count"),"Where across depth and scale does fragmentation change?","ExperimentResult layers/components","primary evidential")
    add("18_combined_layer_dynamics",v.combined_layer_dynamics(cosine,"components","component_count"),"How do component dynamics compare across representation sites?","ExperimentResult layers/components","primary evidential")
    add("19_bridge_probe_frequency",v.bridge_probe_frequency(final,probes=probes),"Which probes repeatedly occupy structurally pivotal bridge positions?","final LayerResult bridges","diagnostic")
    add("20_robustness_comparison",v.robustness_comparison([cosine,euclidean],["cosine","euclidean"],site=final_site,factor="class"),"Does the class-alignment conclusion survive a reasonable metric change?","cosine+euclidean ExperimentResult","primary evidential")
    add("21_cross_result_summary",v.cross_result_summary([cosine,euclidean],["cosine","euclidean"]),"How do structural transition summaries differ by measurement geometry?","cosine+euclidean ExperimentResult","summary/report")
    add("22_interpretation_dashboard",v.interpretation_dashboard(final,"class"),"What combined evidence bears on the class-organization hypothesis?","final LayerResult multiple analyses","summary/report")

    # CSV/JSON exports
    write_csv(tables/"training_history.csv",history)
    probe_rows=[]
    for s,m in zip(probes.samples,probes.metadata): probe_rows.append({"probe_id":s.id,**m})
    write_csv(tables/"probe_metadata.csv",probe_rows)
    layer_rows=[]
    for site,layer in cosine.layers.items():
        pc=layer.analyses["pcscs"].observables; pp=layer.analyses["percolation"].observables
        layer_rows.append({"site":site,"metric":layer.metric,"filtration":layer.filtration,"critical_parameter":pc.get("critical_parameter"),"convergence_parameter":pc.get("convergence_parameter"),"susceptibility_peak_parameter":pp.get("susceptibility_peak_parameter")})
    write_csv(tables/"layer_summary.csv",layer_rows)
    write_csv(out/"figure_manifest.csv",manifest)

    spectral_rows=[]
    for site,layer in cosine.layers.items():
        for s in layer.analyses["spectra"].observables["trajectory"].snapshots:
            spectral_rows.append({"site":site,"parameter":s.parameter,"operator":s.operator,"algebraic_connectivity":s.observables.get("algebraic_connectivity"),"spectral_entropy":s.observables.get("spectral_entropy"),"effective_rank":s.observables.get("effective_rank"),"energy":s.observables.get("energy")})
    write_csv(tables/"spectral_observables.csv",spectral_rows)

    factor_rows=[]
    for site,layer in cosine.layers.items():
        for r in layer.analyses["factor_alignment"].records:
            for factor,d in r.items():
                if factor=="parameter": continue
                factor_rows.append({"site":site,"parameter":r["parameter"],"factor":factor,"nmi":d["nmi"],"ari":d["ari"]})
    write_csv(tables/"factor_alignment.csv",factor_rows)

    config={"seed":SEED,"probe_accuracy":probe_acc,"probe_count":len(probes.samples),"final_site":final_site,"filtration":{"name":"edge_density","start":0.0,"stop":0.45,"steps":32},"primary_metric":"cosine","robustness_metric":"euclidean","analyses":list(final.analyses)}
    (out/"configuration.json").write_text(json.dumps(config,indent=2))
    # Retain the exact generator and a machine-readable visualization catalog inside the bundle.
    try:
        shutil.copy2(Path(__file__),out/"complete_visualization_demo.py")
    except Exception:
        pass
    (out/"visualization_catalog.json").write_text(json.dumps(manifest,indent=2))
    env={"python":sys.version,"platform":platform.platform(),"torch":torch.__version__,"numpy":np.__version__,"eigenflow":ef.__version__}
    (out/"environment.json").write_text(json.dumps(env,indent=2))

    readme=f"""# Eigenflow complete visualization demonstration\n\nThis bundle was generated by `examples/complete_visualization_demo.py` from a genuinely trained three-class MLP and a held-out factorial probe population. Probe classification accuracy: **{probe_acc:.3f}**.\n\nThe `figures/` directory contains one real example of every public visualization family exercised by the current ontology. `figure_manifest.csv` maps each image to the analyst question it answers, its evidential tier, and its source result object.\n\nThe primary experiment uses cosine similarity and edge-density filtration. A matched Euclidean-distance run is included for measurement-robustness comparison.\n\nInterpret each figure as structural evidence conditioned on the probe design, reducer, metric, filtration, graph operator, and finite probe sample. None of the figures alone identifies a unique semantic neuron or causal mechanism.\n"""
    (out/"README.md").write_text(readme)

    # Checksums, then zip.
    checksum_rows=[]
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name!="SHA256SUMS.csv": checksum_rows.append({"file":str(p.relative_to(out)),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
    write_csv(out/"SHA256SUMS.csv",checksum_rows)
    zip_path=out.with_suffix(".zip")
    with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file(): z.write(p,p.relative_to(out.parent))
    print(json.dumps({"output_dir":str(out),"zip":str(zip_path),"probe_accuracy":probe_acc,"figures":len(manifest)},indent=2))
    return zip_path

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--output-dir",default="eigenflow_visualization_demo_outputs"); args=ap.parse_args(); main(args.output_dir)
