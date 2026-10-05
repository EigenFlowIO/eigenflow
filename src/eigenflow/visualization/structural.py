from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.signal import savgol_filter
from scipy.cluster.hierarchy import linkage,dendrogram
from scipy.spatial.distance import squareform
from ._utils import require_layer_artifacts,require_probes,new_ax,factor_values,stable_component_labels,component_sets


def probe_design_view(result_or_probes,factors=None,ax=None):
    """Visualize factorial coverage/counts for one or two probe factors."""
    probes=require_probes(result_or_probes)
    factors=list(factors or sorted(set().union(*(m.keys() for m in probes.metadata)))[:2])
    if not factors: raise ValueError("No probe metadata factors available")
    ax=new_ax(ax)
    if len(factors)==1:
        vals=factor_values(probes,factors[0]); cats,counts=np.unique(vals,return_counts=True)
        ax.bar(np.arange(len(cats)),counts); ax.set_xticks(np.arange(len(cats)),cats,rotation=30,ha="right")
        ax.set_ylabel("probe count"); ax.set_title(f"Probe design: {factors[0]}")
    else:
        a=factor_values(probes,factors[0]); b=factor_values(probes,factors[1])
        ca=sorted(set(a)); cb=sorted(set(b)); M=np.zeros((len(ca),len(cb)),int)
        ia={v:i for i,v in enumerate(ca)}; ib={v:i for i,v in enumerate(cb)}
        for x,y in zip(a,b): M[ia[x],ib[y]]+=1
        im=ax.imshow(M,aspect="auto")
        ax.set_yticks(range(len(ca)),ca); ax.set_xticks(range(len(cb)),cb,rotation=30,ha="right")
        ax.set_ylabel(factors[0]); ax.set_xlabel(factors[1]); ax.set_title("Probe factorial coverage")
        for i in range(M.shape[0]):
            for j in range(M.shape[1]): ax.text(j,i,str(M[i,j]),ha="center",va="center")
        ax.figure.colorbar(im,ax=ax,label="probe count")
    ax.figure.tight_layout(); return ax.figure


def relational_matrix_heatmap(layer_result,probes=None,factor=None,ax=None):
    art=require_layer_artifacts(layer_result); rel=art.relational_matrix
    order=np.arange(rel.n); labels=None
    if factor is not None:
        if probes is None: raise ValueError("Pass probes=... when ordering by factor")
        vals=np.array(factor_values(probes,factor),object); order=np.argsort(vals,kind="stable"); labels=vals[order]
    ax=new_ax(ax,(6,5)); im=ax.imshow(rel.values[np.ix_(order,order)],aspect="auto")
    ax.set_title(f"{layer_result.site}: {rel.metric} relational matrix")
    ax.set_xlabel("probe"); ax.set_ylabel("probe")
    if labels is not None:
        # factor boundaries
        changes=np.where(labels[1:]!=labels[:-1])[0]+1
        for c in changes:
            ax.axhline(c-.5,lw=.8); ax.axvline(c-.5,lw=.8)
    ax.figure.colorbar(im,ax=ax,label=rel.kind); ax.figure.tight_layout(); return ax.figure


def component_trajectory(layer_result,analysis=None,smooth=True,ax=None):
    analysis=analysis or ("pcscs" if "pcscs" in layer_result.analyses else "components")
    ar=layer_result.analyses[analysis]; xs=np.array([r["parameter"] for r in ar.records],float); y=np.array(ar.observables["component_count"],float)
    ax=new_ax(ax); ax.plot(xs,y,label="component count")
    if smooth and len(y)>=5:
        win=min(len(y) if len(y)%2 else len(y)-1,11)
        if win>=5:
            ys=savgol_filter(y,win,2); ax.plot(xs,ys,label="smoothed")
    crit=ar.observables.get("critical_parameter")
    if crit is None and len(y)>1: crit=float(xs[int(np.argmax(np.abs(np.gradient(y,xs))))])
    conv=ar.observables.get("convergence_parameter")
    if conv is None:
        hits=np.where(y<=1)[0]; conv=float(xs[hits[0]]) if len(hits) else None
    if crit is not None: ax.axvline(crit,ls="--",label="max |dC/dp|")
    if conv is not None: ax.axvline(conv,ls=":",label="convergence")
    ax.set_xlabel("control parameter"); ax.set_ylabel("connected components"); ax.set_title(f"{layer_result.site}: component trajectory"); ax.legend(); ax.figure.tight_layout(); return ax.figure


def component_membership_raster(layer_result,probes=None,factor=None,ax=None):
    art=require_layer_artifacts(layer_result); gf=art.filtration
    M=np.stack([stable_component_labels(s) for s in gf.snapshots],axis=1)
    order=np.arange(M.shape[0])
    if factor is not None:
        if probes is None: raise ValueError("Pass probes when ordering by factor")
        order=np.argsort(np.array(factor_values(probes,factor),object),kind="stable")
    ax=new_ax(ax,(8,5)); im=ax.imshow(M[order],aspect="auto",interpolation="nearest")
    ax.set_xlabel("control step"); ax.set_ylabel("probe (ordered)" if factor is None else f"probe ordered by {factor}")
    ax.set_title(f"{layer_result.site}: component membership across scale"); ax.figure.colorbar(im,ax=ax,label="stable component ID"); ax.figure.tight_layout(); return ax.figure


def merge_events(layer_result):
    """Return component merge events derived from consecutive monotone graph snapshots."""
    gf=require_layer_artifacts(layer_result).filtration
    events=[]
    prev=component_sets(gf.snapshots[0]) if len(gf.snapshots) else {}
    for snap in gf.snapshots[1:]:
        cur=component_sets(snap)
        for parent_id,parent in cur.items():
            children=[(cid,c) for cid,c in prev.items() if c and c.issubset(parent)]
            if len(children)>1:
                events.append({"parameter":float(snap.parameter),"native_parameter":snap.native_parameter,"parent":sorted(parent),"children":[sorted(c) for _,c in children]})
        prev=cur
    return events


def merge_event_plot(layer_result,ax=None):
    events=merge_events(layer_result); ax=new_ax(ax,(8,4.5))
    if not events:
        ax.text(.5,.5,"No multi-component merge events at sampled control steps",ha="center",va="center",transform=ax.transAxes)
    else:
        for i,e in enumerate(events):
            ax.scatter(e["parameter"],len(e["parent"]),s=40+8*len(e["children"]))
            ax.text(e["parameter"],len(e["parent"]),f" {len(e['children'])}→1",va="center",fontsize=8)
    ax.set_xlabel("control parameter"); ax.set_ylabel("merged component size"); ax.set_title(f"{layer_result.site}: component merge events"); ax.figure.tight_layout(); return ax.figure


def dendrogram_view(layer_result,probes=None,factor=None,ax=None):
    """Single-linkage dendrogram equivalent to threshold connected-component hierarchy."""
    art=require_layer_artifacts(layer_result); rel=art.relational_matrix; A=np.asarray(rel.values,float).copy(); n=A.shape[0]
    if n<2: raise ValueError("Dendrogram requires at least two probes")
    if rel.kind=="similarity":
        tri=A[np.triu_indices(n,1)]; mx=float(np.max(tri)); D=mx-A; np.fill_diagonal(D,0.); ylabel=f"dissimilarity = max({rel.metric}) - {rel.metric}"
    else:
        D=A.copy(); np.fill_diagonal(D,0.); ylabel=rel.metric
    D=(D+D.T)/2; D=np.maximum(D,0)
    Z=linkage(squareform(D,checks=False),method="single")
    labels=list(rel.probe_ids)
    if factor is not None:
        if probes is None: raise ValueError("Pass probes when labeling dendrogram by factor")
        vals=factor_values(probes,factor); labels=[f"{pid}\n{v}" for pid,v in zip(labels,vals)]
    ax=new_ax(ax,(10,5)); dendrogram(Z,labels=labels,leaf_rotation=90,leaf_font_size=7,ax=ax,color_threshold=None)
    ax.set_ylabel(ylabel); ax.set_title(f"{layer_result.site}: filtration merge hierarchy (single linkage)"); ax.figure.tight_layout(); return ax.figure


def graph_snapshot(layer_result,index=None,parameter=None,probes=None,factor=None,highlight_bridges=False,kcore=None,ax=None,seed=0):
    art=require_layer_artifacts(layer_result); gf=art.filtration
    if index is None:
        if parameter is None: index=len(gf.snapshots)//2
        else: index=int(np.argmin(np.abs(gf.parameters-float(parameter))))
    snap=gf.snapshots[index]; G=nx.from_scipy_sparse_array(snap.adjacency); pos=nx.spring_layout(G,seed=seed)
    ax=new_ax(ax,(7,6)); node_colors=None
    if factor is not None:
        if probes is None: raise ValueError("Pass probes when coloring graph by factor")
        vals=factor_values(probes,factor); cats={v:i for i,v in enumerate(sorted(set(vals)))}; node_colors=[cats[vals[i]] for i in G.nodes]
    if kcore is not None:
        core=set(nx.k_core(G,k=int(kcore)).nodes()) if G.number_of_edges() else set(); sizes=[120 if n in core else 45 for n in G.nodes]
    else: sizes=70
    nx.draw_networkx(G,pos,ax=ax,with_labels=False,node_size=sizes,node_color=node_colors,cmap=plt.cm.viridis,edge_color="0.75")
    if highlight_bridges and G.number_of_edges(): nx.draw_networkx_edges(G,pos,edgelist=list(nx.bridges(G)),ax=ax,width=2.5,edge_color="black")
    ax.set_title(f"{layer_result.site}: graph snapshot p={snap.parameter:.4g}, density={snap.edge_density:.3f}"); ax.axis("off"); ax.figure.tight_layout(); return ax.figure


def combined_layer_dynamics(result,analysis="components",observable="component_count",x="parameter",ax=None):
    ax=new_ax(ax,(8,5))
    for site,layer in result.layers.items():
        ar=layer.analyses[analysis]; xs=[r.get(x,i) for i,r in enumerate(ar.records)]
        y=ar.observables.get(observable)
        if not isinstance(y,list): y=[r[observable] for r in ar.records]
        ax.plot(xs,y,label=site)
    ax.set_xlabel(x.replace("_"," ")); ax.set_ylabel(observable.replace("_"," ")); ax.set_title(f"Combined-layer {observable}"); ax.legend(fontsize=8); ax.figure.tight_layout(); return ax.figure
