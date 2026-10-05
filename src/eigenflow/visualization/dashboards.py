from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt


def percolation_dashboard(layer_result,fig=None):
    fig=fig or plt.figure(figsize=(10,8)); fig.clf(); axes=fig.subplots(2,2); xs=None
    comp=layer_result.analyses.get("components") or layer_result.analyses.get("pcscs")
    if comp is None: raise ValueError("percolation_dashboard requires components or pcscs analysis")
    xs=[r["parameter"] for r in comp.records]; axes[0,0].plot(xs,comp.observables["component_count"]); axes[0,0].set_title("Connected components")
    p=layer_result.analyses["percolation"]; px=[r["parameter"] for r in p.records]
    axes[0,1].plot(px,p.observables["giant_component_fraction"]); axes[0,1].set_title("Giant-component fraction")
    axes[1,0].plot(px,p.observables["second_component_fraction"]); axes[1,0].set_title("Second-largest component")
    axes[1,1].plot(px,p.observables["susceptibility"]); axes[1,1].set_title("Susceptibility")
    for ax in axes.ravel(): ax.set_xlabel("control parameter")
    fig.suptitle(f"{layer_result.site}: filtration structure dashboard"); fig.tight_layout(); return fig


def interpretation_dashboard(layer_result,factor="class",fig=None):
    fig=fig or plt.figure(figsize=(11,8)); fig.clf(); axes=fig.subplots(2,2)
    p=layer_result.analyses["percolation"]; px=[r["parameter"] for r in p.records]; axes[0,0].plot(px,p.observables["giant_component_fraction"]); axes[0,0].set_title("Giant component")
    fa=layer_result.analyses["factor_alignment"]; xs=[]; ys=[]
    for r in fa.records:
        if factor in r: xs.append(r["parameter"]); ys.append(r[factor]["nmi"])
    axes[0,1].plot(xs,ys); axes[0,1].set_ylim(-.05,1.05); axes[0,1].set_title(f"{factor} NMI")
    sp=layer_result.analyses["spectra"].observables["trajectory"]; sx=sp.parameters; ac=[s.observables.get("algebraic_connectivity",np.nan) for s in sp.snapshots]; axes[1,0].plot(sx,ac); axes[1,0].set_title("Algebraic connectivity")
    cs=layer_result.analyses.get("class_structure")
    if cs is not None:
        dif=[]; cx=[]
        for r in cs.records:
            vals=[d["internal_density"]-d["external_density"] for d in r["classes"].values()]; cx.append(r["parameter"]); dif.append(float(np.mean(vals)) if vals else np.nan)
        axes[1,1].plot(cx,dif); axes[1,1].set_title("Mean internal − external density")
    else: axes[1,1].text(.5,.5,"class_structure not available",ha="center",va="center")
    for ax in axes.ravel(): ax.set_xlabel("control parameter")
    fig.suptitle(f"{layer_result.site}: experimental interpretation dashboard"); fig.tight_layout(); return fig
