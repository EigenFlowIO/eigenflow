from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np

def observable_curve(layer_result,analysis,observable,x="parameter",ax=None):
    ar=layer_result.analyses[analysis]; ax=ax or plt.subplots()[1]
    if observable in ar.observables and isinstance(ar.observables[observable],list):
        y=ar.observables[observable]; xs=[r.get(x,i) for i,r in enumerate(ar.records)]
    else:
        y=[r[observable] for r in ar.records]; xs=[r.get(x,i) for i,r in enumerate(ar.records)]
    ax.plot(xs,y); ax.set_xlabel(x.replace("_"," ")); ax.set_ylabel(observable.replace("_"," ")); ax.set_title(f"{layer_result.site}: {analysis}/{observable}")
    return ax.figure

def layer_control_heatmap(result,analysis,observable,ax=None):
    sites=list(result.layers); rows=[]
    for s in sites:
        ar=result.layers[s].analyses[analysis]; rows.append(np.asarray(ar.observables[observable],float))
    m=min(map(len,rows)); data=np.stack([r[:m] for r in rows]); ax=ax or plt.subplots()[1]
    im=ax.imshow(data,aspect="auto",origin="lower"); ax.set_yticks(range(len(sites)),sites); ax.set_xlabel("control step"); ax.set_ylabel("representation site"); ax.set_title(observable.replace("_"," ")); ax.figure.colorbar(im,ax=ax)
    return ax.figure

def eigenflow_plot(layer_result,ax=None,max_modes=12):
    traj=layer_result.analyses["spectra"].observables["trajectory"]; ax=ax or plt.subplots()[1]
    for k in range(min(max_modes,min(len(s.eigenvalues) for s in traj.snapshots))): ax.plot(traj.parameters,[s.eigenvalues[k] for s in traj.snapshots])
    ax.set_xlabel("control parameter"); ax.set_ylabel("eigenvalue"); ax.set_title(f"Eigenflow: {layer_result.site} ({traj.operator})"); return ax.figure
