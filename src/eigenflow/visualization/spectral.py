from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from ._utils import new_ax


def static_spectrum(layer_result,index=None,parameter=None,ax=None,highlight_gap=True):
    traj=layer_result.analyses["spectra"].observables["trajectory"]
    if index is None:
        if parameter is None: index=len(traj.snapshots)//2
        else: index=int(np.argmin(np.abs(np.asarray(traj.parameters)-float(parameter))))
    s=traj.snapshots[index]; vals=np.asarray(s.eigenvalues,float); ax=new_ax(ax)
    ax.plot(np.arange(len(vals)),vals,marker="o",ms=3); ax.set_xlabel("eigenvalue index"); ax.set_ylabel("eigenvalue")
    ax.set_title(f"{layer_result.site}: {s.operator} spectrum at p={s.parameter:.4g}")
    if s.operator in {"laplacian","normalized_laplacian"} and len(vals)>1: ax.axhline(vals[1],ls="--",label=f"algebraic connectivity={vals[1]:.3g}")
    if highlight_gap and len(vals)>2:
        gaps=np.diff(vals); j=int(np.argmax(np.abs(gaps))); ax.axvspan(j,j+1,alpha=.15,label=f"largest gap={gaps[j]:.3g}")
    if ax.get_legend_handles_labels()[0]: ax.legend(fontsize=8)
    ax.figure.tight_layout(); return ax.figure


def spectral_flow(layer_result,ax=None,max_modes=12):
    traj=layer_result.analyses["spectra"].observables["trajectory"]; ax=new_ax(ax,(8,5)); m=min(max_modes,min(len(s.eigenvalues) for s in traj.snapshots))
    for k in range(m): ax.plot(traj.parameters,[s.eigenvalues[k] for s in traj.snapshots],lw=1)
    ax.set_xlabel("control parameter"); ax.set_ylabel("eigenvalue"); ax.set_title(f"{layer_result.site}: spectral flow ({traj.operator})")
    ax.text(.01,.01,"Mode index is sorted per snapshot; use eigenspace stability near crossings.",transform=ax.transAxes,fontsize=7,va="bottom")
    ax.figure.tight_layout(); return ax.figure


def spectral_properties_dashboard(layer_result,fig=None):
    traj=layer_result.analyses["spectra"].observables["trajectory"]
    xs=np.asarray(traj.parameters,float)
    fig=fig or plt.figure(figsize=(10,8)); fig.clf(); axes=fig.subplots(2,2)
    obs=[("algebraic_connectivity","Algebraic connectivity"),("spectral_entropy","Spectral entropy"),("effective_rank","Effective rank"),("energy","Graph energy")]
    for ax,(key,title) in zip(axes.ravel(),obs):
        vals=[s.observables.get(key,np.nan) for s in traj.snapshots]; ax.plot(xs,vals); ax.set_title(title); ax.set_xlabel("control parameter")
    fig.suptitle(f"{layer_result.site}: spectral properties ({traj.operator})"); fig.tight_layout(); return fig


def localization_trajectory(layer_result,mode=0,ax=None):
    traj=layer_result.analyses["spectra"].observables["trajectory"]; ax=new_ax(ax)
    ys=[]
    for s in traj.snapshots:
        arr=s.observables.get("ipr")
        ys.append(np.nan if arr is None or len(arr)<=mode else arr[mode])
    ax.plot(traj.parameters,ys); ax.set_xlabel("control parameter"); ax.set_ylabel(f"IPR mode {mode}"); ax.set_title(f"{layer_result.site}: eigenvector localization"); ax.figure.tight_layout(); return ax.figure


def eigenspace_stability(layer_result,ax=None):
    ar=layer_result.analyses["eigenspaces"]; ax=new_ax(ax)
    xs=[]; ys=[]
    for r in ar.records:
        if r["principal_angles"] is None: continue
        xs.append(r["parameter"]); ys.append(float(np.max(r["principal_angles"])))
    ax.plot(xs,ys); ax.set_xlabel("control parameter"); ax.set_ylabel("maximum principal angle (rad)"); ax.set_title(f"{layer_result.site}: eigenspace stability"); ax.figure.tight_layout(); return ax.figure


def eigenspace_overlap_heatmap(layer_result,index=-1,ax=None):
    rec=[r for r in layer_result.analyses["eigenspaces"].records if r["overlap"] is not None]
    if not rec: raise ValueError("No eigenspace overlap matrices available")
    r=rec[index]; M=np.asarray(r["overlap"],float); ax=new_ax(ax,(5,4)); im=ax.imshow(M,vmin=0,vmax=1,aspect="equal")
    ax.set_title(f"{layer_result.site}: eigenspace overlap at p={r['parameter']:.4g}"); ax.set_xlabel("current basis"); ax.set_ylabel("previous basis"); ax.figure.colorbar(im,ax=ax,label="|overlap|"); ax.figure.tight_layout(); return ax.figure
