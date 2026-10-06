from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from ._utils import new_ax
from ..spectra import characterize_spectrum, project_eigenvalues, matched_spectral_paths


def _snapshot_policy(snapshot):
    return getattr(snapshot, "complex_policy", snapshot.observables.get("complex_policy", "auto"))


def _project_snapshot(snapshot):
    return project_eigenvalues(snapshot.eigenvalues, _snapshot_policy(snapshot))


def complex_spectrum_plot(layer_result,index=None,parameter=None,ax=None,unit_circle=True,spectral_radius=True):
    """Plot one spectrum in the complex plane.

    This is the canonical view for a genuinely complex spectrum.  Real-valued
    spectra are also valid inputs and appear on the real axis.
    """
    traj=layer_result.analyses["spectra"].observables["trajectory"]
    if index is None:
        if parameter is None: index=len(traj.snapshots)//2
        else: index=int(np.argmin(np.abs(np.asarray(traj.parameters)-float(parameter))))
    s=traj.snapshots[index]
    vals=np.asarray(s.eigenvalues,dtype=complex)
    ax=new_ax(ax,(6,6))
    if len(vals):
        ax.scatter(vals.real,vals.imag,s=22)
    ax.axhline(0,lw=.8,alpha=.5); ax.axvline(0,lw=.8,alpha=.5)
    if unit_circle:
        th=np.linspace(0,2*np.pi,256); ax.plot(np.cos(th),np.sin(th),ls="--",lw=.8,alpha=.5,label="unit circle")
    if spectral_radius and len(vals):
        rho=float(np.max(np.abs(vals))); th=np.linspace(0,2*np.pi,256)
        ax.plot(rho*np.cos(th),rho*np.sin(th),ls=":",lw=.8,alpha=.7,label=f"spectral radius={rho:.3g}")
    ax.set_xlabel("Re(λ)"); ax.set_ylabel("Im(λ)")
    ax.set_title(f"{layer_result.site}: {s.operator} spectrum at p={s.parameter:.4g}")
    ax.set_aspect("equal",adjustable="datalim")
    if ax.get_legend_handles_labels()[0]: ax.legend(fontsize=8)
    ax.figure.tight_layout(); return ax.figure


def static_spectrum(layer_result,index=None,parameter=None,ax=None,highlight_gap=True):
    traj=layer_result.analyses["spectra"].observables["trajectory"]
    if index is None:
        if parameter is None: index=len(traj.snapshots)//2
        else: index=int(np.argmin(np.abs(np.asarray(traj.parameters)-float(parameter))))
    s=traj.snapshots[index]
    info=characterize_spectrum(s.eigenvalues)
    policy=_snapshot_policy(s)
    projected=_project_snapshot(s)
    if info["complex_detected"] and projected is None:
        return complex_spectrum_plot(layer_result,index=index,ax=ax)
    vals=np.asarray(projected if projected is not None else np.real(s.eigenvalues),float)
    ax=new_ax(ax)
    ax.plot(np.arange(len(vals)),vals,marker="o",ms=3)
    ax.set_xlabel("eigenvalue index")
    ylabel={"modulus":"|λ|","real":"Re(λ)","imag":"Im(λ)","phase":"arg(λ)"}.get(policy,"eigenvalue")
    ax.set_ylabel(ylabel)
    ax.set_title(f"{layer_result.site}: {s.operator} spectrum at p={s.parameter:.4g}")
    if s.operator in {"laplacian","normalized_laplacian","signed_laplacian","signed_normalized_laplacian"} and len(vals)>1 and not info["complex_detected"]:
        ax.axhline(vals[1],ls="--",label=f"algebraic connectivity={vals[1]:.3g}")
    gaps=s.observables.get("gaps")
    if highlight_gap and gaps:
        g=np.asarray(gaps,float); j=int(np.argmax(np.abs(g)))
        if policy != "phase" and j < len(vals)-1:
            ax.axvspan(j,j+1,alpha=.15,label=f"largest {s.observables.get('gap_kind','gap')}={g[j]:.3g}")
    if ax.get_legend_handles_labels()[0]: ax.legend(fontsize=8)
    ax.figure.tight_layout(); return ax.figure


def spectral_flow(layer_result,ax=None,max_modes=12):
    traj=layer_result.analyses["spectra"].observables["trajectory"]
    ax=new_ax(ax,(8,5))
    paths=matched_spectral_paths(traj,max_modes=max_modes)
    if paths.shape[1] == 0:
        ax.set_title(f"{layer_result.site}: spectral flow ({traj.operator})")
        return ax.figure
    # Policy is analysis-level; use the first populated snapshot as authority.
    first=next(s for s in traj.snapshots if len(s.eigenvalues))
    policy=_snapshot_policy(first)
    any_complex=any(characterize_spectrum(s.eigenvalues)["complex_detected"] for s in traj.snapshots if len(s.eigenvalues))
    if any_complex and policy in {"auto","preserve"}:
        for k in range(paths.shape[1]):
            z=paths[:,k]; mask=np.isfinite(z.real)&np.isfinite(z.imag)
            ax.plot(z.real[mask],z.imag[mask],lw=1,marker="o",ms=2)
        ax.axhline(0,lw=.8,alpha=.5); ax.axvline(0,lw=.8,alpha=.5)
        ax.set_xlabel("Re(λ)"); ax.set_ylabel("Im(λ)")
        ax.set_title(f"{layer_result.site}: matched complex spectral flow ({traj.operator})")
        ax.text(.01,.01,"Modes matched between adjacent snapshots by minimum complex-plane distance.",transform=ax.transAxes,fontsize=7,va="bottom")
    else:
        xs=traj.parameters
        for k in range(paths.shape[1]):
            z=paths[:,k]
            if policy=="modulus": y=np.abs(z)
            elif policy=="imag": y=np.imag(z)
            elif policy=="phase": y=np.unwrap(np.angle(z))
            else: y=np.real(z)
            mask=np.isfinite(y)
            ax.plot(xs[mask],np.asarray(y)[mask],lw=1)
        ax.set_xlabel("control parameter")
        ylabel={"modulus":"|λ|","imag":"Im(λ)","phase":"unwrapped arg(λ)","real":"Re(λ)"}.get(policy,"eigenvalue")
        ax.set_ylabel(ylabel)
        ax.set_title(f"{layer_result.site}: matched spectral flow ({traj.operator})")
        ax.text(.01,.01,"Modes matched between adjacent snapshots; paths are not sorted-index identities.",transform=ax.transAxes,fontsize=7,va="bottom")
    ax.figure.tight_layout(); return ax.figure


def spectral_properties_dashboard(layer_result,fig=None):
    traj=layer_result.analyses["spectra"].observables["trajectory"]
    xs=np.asarray(traj.parameters,float)
    fig=fig or plt.figure(figsize=(10,8)); fig.clf(); axes=fig.subplots(2,2)
    obs=[("algebraic_connectivity","Algebraic connectivity"),("spectral_radius","Spectral radius"),("spectral_entropy","Spectral entropy"),("effective_rank","Effective rank")]
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
