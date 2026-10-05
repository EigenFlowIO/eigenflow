from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from ._utils import new_ax


def factor_alignment_trajectory(layer_result,factors=None,metric="nmi",ax=None):
    ar=layer_result.analyses["factor_alignment"]; factors=list(factors or ar.metadata.get("factors",[])); ax=new_ax(ax,(8,5))
    for f in factors:
        xs=[]; ys=[]
        for r in ar.records:
            if f in r: xs.append(r["parameter"]); ys.append(r[f][metric])
        if xs: ax.plot(xs,ys,label=f)
    ax.set_xlabel("control parameter"); ax.set_ylabel(metric.upper()); ax.set_ylim(-.05,1.05); ax.set_title(f"{layer_result.site}: factor alignment"); ax.legend(); ax.figure.tight_layout(); return ax.figure


def factor_connectivity(layer_result,classes=None,ax=None):
    ar=layer_result.analyses["class_structure"]; factor=ar.metadata.get("factor","class"); ax=new_ax(ax,(8,5))
    all_classes=sorted({c for r in ar.records for c in r["classes"]}); classes=list(classes or all_classes)
    for c in classes:
        xs=[]; internal=[]; external=[]
        for r in ar.records:
            if c in r["classes"]:
                xs.append(r["parameter"]); internal.append(r["classes"][c]["internal_density"]); external.append(r["classes"][c]["external_density"])
        ax.plot(xs,internal,label=f"{c} internal"); ax.plot(xs,external,ls="--",label=f"{c} external")
    ax.set_xlabel("control parameter"); ax.set_ylabel("edge density"); ax.set_title(f"{layer_result.site}: {factor} internal vs external connectivity"); ax.legend(fontsize=7,ncol=2); ax.figure.tight_layout(); return ax.figure


def bridge_probe_frequency(layer_result,probes=None,top_n=15,ax=None):
    ar=layer_result.analyses["bridges"]; counts={}
    for r in ar.records:
        for u,v in r["bridges"]:
            counts[u]=counts.get(u,0)+1; counts[v]=counts.get(v,0)+1
    order=sorted(counts,key=counts.get,reverse=True)[:top_n]; vals=[counts[i] for i in order]
    labels=[str(i) for i in order]
    if probes is not None: labels=[probes.samples[i].id for i in order]
    ax=new_ax(ax,(8,4.5)); ax.bar(np.arange(len(order)),vals); ax.set_xticks(np.arange(len(order)),labels,rotation=45,ha="right"); ax.set_ylabel("bridge appearances"); ax.set_title(f"{layer_result.site}: structurally pivotal probes"); ax.figure.tight_layout(); return ax.figure
