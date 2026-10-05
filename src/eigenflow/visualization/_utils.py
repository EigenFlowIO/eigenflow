from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import connected_components


def require_layer_artifacts(layer_result):
    art=getattr(layer_result,"artifacts",None)
    if art is None or art.filtration is None:
        raise ValueError("This visualization requires in-memory LayerResult.artifacts. Re-run the experiment in the current process.")
    return art


def require_probes(result_or_probes):
    if hasattr(result_or_probes,"samples"):
        return result_or_probes
    art=getattr(result_or_probes,"artifacts",None)
    probes=getattr(art,"probes",None) if art is not None else None
    if probes is None:
        raise ValueError("Probe-aware visualization requires an in-memory ExperimentResult with artifacts or an explicit ProbePopulation.")
    return probes


def new_ax(ax=None,figsize=(7,4.5)):
    if ax is not None: return ax
    _,ax=plt.subplots(figsize=figsize)
    return ax


def factor_values(probes,factor):
    vals=probes.values(factor)
    return ["<missing>" if v is None else str(v) for v in vals]


def stable_component_labels(snapshot):
    _,labels=connected_components(snapshot.adjacency,directed=False,return_labels=True)
    out=np.empty_like(labels)
    for lab in np.unique(labels):
        idx=np.where(labels==lab)[0]
        out[idx]=int(idx.min())
    return out


def component_sets(snapshot):
    labs=stable_component_labels(snapshot)
    return {int(k):set(np.where(labs==k)[0].tolist()) for k in np.unique(labs)}


def close_or_return(fig):
    return fig
