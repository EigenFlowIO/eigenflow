from __future__ import annotations
import numpy as np
from ._utils import new_ax


def layer_control_heatmap(result,analysis,observable,ax=None):
    sites=list(result.layers); rows=[]; xs=None
    for s in sites:
        ar=result.layers[s].analyses[analysis]; y=ar.observables.get(observable)
        if not isinstance(y,list): y=[r[observable] for r in ar.records]
        rows.append(np.asarray(y,float));
        if xs is None: xs=np.asarray([r.get("parameter",i) for i,r in enumerate(ar.records)],float)
    m=min(map(len,rows)); data=np.stack([r[:m] for r in rows]); ax=new_ax(ax,(8,5)); im=ax.imshow(data,aspect="auto",origin="lower")
    ax.set_yticks(range(len(sites)),sites); ax.set_xlabel("control step"); ax.set_ylabel("representation site"); ax.set_title(observable.replace("_"," ")); ax.figure.colorbar(im,ax=ax); ax.figure.tight_layout(); return ax.figure


def robustness_comparison(results,labels=None,site=None,analysis="factor_alignment",factor="class",metric="nmi",ax=None):
    labels=list(labels or [f"run {i+1}" for i in range(len(results))]); ax=new_ax(ax,(8,5))
    for result,label in zip(results,labels):
        s=site or list(result.layers)[-1]; ar=result.layers[s].analyses[analysis]
        xs=[]; ys=[]
        if analysis=="factor_alignment":
            for r in ar.records:
                if factor in r: xs.append(r["parameter"]); ys.append(r[factor][metric])
        else:
            y=ar.observables.get(factor); xs=[r["parameter"] for r in ar.records]; ys=y
        ax.plot(xs,ys,label=label)
    ax.set_xlabel("control parameter"); ax.set_ylabel(f"{factor} {metric}" if analysis=="factor_alignment" else factor); ax.set_title("Measurement robustness comparison"); ax.legend(); ax.figure.tight_layout(); return ax.figure


def cross_result_summary(results,labels=None,analysis="percolation",observable="susceptibility_peak_parameter",ax=None):
    labels=list(labels or [f"result {i+1}" for i in range(len(results))]); sites=sorted(set.intersection(*(set(r.layers) for r in results)))
    ax=new_ax(ax,(8,5)); x=np.arange(len(sites)); width=.8/max(1,len(results))
    for j,(result,label) in enumerate(zip(results,labels)):
        vals=[]
        for s in sites:
            v=result.layers[s].analyses[analysis].observables.get(observable,np.nan); vals.append(v if np.isscalar(v) else np.nan)
        ax.bar(x+(j-(len(results)-1)/2)*width,vals,width=width,label=label)
    ax.set_xticks(x,sites,rotation=30,ha="right"); ax.set_ylabel(observable.replace("_"," ")); ax.set_title("Cross-result structural summary"); ax.legend(); ax.figure.tight_layout(); return ax.figure
