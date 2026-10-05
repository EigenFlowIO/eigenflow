from __future__ import annotations
from ._utils import new_ax
from .comparison import layer_control_heatmap
from .spectral import spectral_flow


def observable_curve(layer_result,analysis,observable,x="parameter",ax=None):
    ar=layer_result.analyses[analysis]; ax=new_ax(ax)
    if observable in ar.observables and isinstance(ar.observables[observable],list):
        y=ar.observables[observable]; xs=[r.get(x,i) for i,r in enumerate(ar.records)]
    else:
        y=[r[observable] for r in ar.records]; xs=[r.get(x,i) for i,r in enumerate(ar.records)]
    ax.plot(xs,y); ax.set_xlabel(x.replace("_"," ")); ax.set_ylabel(observable.replace("_"," ")); ax.set_title(f"{layer_result.site}: {analysis}/{observable}"); ax.figure.tight_layout(); return ax.figure


def eigenflow_plot(layer_result,ax=None,max_modes=12):
    return spectral_flow(layer_result,ax=ax,max_modes=max_modes)
