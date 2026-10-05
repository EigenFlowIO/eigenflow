from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from ._utils import new_ax


def checkpoint_trajectory(longitudinal, site, analysis, observable, *, control_index=None, aggregate="mean", ax=None):
    data=np.asarray(longitudinal.trajectory(site,analysis,observable),dtype=float)
    if data.ndim==1:
        y=data
    elif control_index is not None:
        y=data[:,control_index]
    elif aggregate=="mean":
        y=np.nanmean(data.reshape(data.shape[0],-1),axis=1)
    elif aggregate=="max":
        y=np.nanmax(data.reshape(data.shape[0],-1),axis=1)
    else:
        raise ValueError("aggregate must be 'mean' or 'max', or provide control_index")
    ax=new_ax(ax,(8,5)); ax.plot(longitudinal.times,y,marker="o")
    ax.set_xlabel("training/checkpoint coordinate"); ax.set_ylabel(observable.replace("_"," "))
    ax.set_title(f"{site}: {observable} across checkpoints"); ax.figure.tight_layout(); return ax.figure


def longitudinal_surface(longitudinal, site, analysis, observable, *, baseline_delta=False, ax=None):
    data=np.asarray(longitudinal.baseline_delta(site,analysis,observable) if baseline_delta else longitudinal.trajectory(site,analysis,observable),dtype=float)
    if data.ndim==1: data=data[:,None]
    if data.ndim!=2: raise ValueError("longitudinal_surface requires a scalar trajectory over control scale")
    ax=new_ax(ax,(9,5)); im=ax.imshow(data,aspect="auto",origin="lower")
    ax.set_yticks(range(len(longitudinal.entries)),[e.key for e in longitudinal.entries]); ax.set_xlabel("control step"); ax.set_ylabel("checkpoint")
    ax.set_title(f"{site}: {'baseline-relative ' if baseline_delta else ''}{observable}"); ax.figure.colorbar(im,ax=ax); ax.figure.tight_layout(); return ax.figure


def layer_time_heatmap(longitudinal, analysis, observable, *, aggregate="mean", baseline_delta=False, ax=None):
    common=sorted(set.intersection(*(set(e.result.layers) for e in longitudinal.entries)))
    rows=[]
    for site in common:
        d=np.asarray(longitudinal.baseline_delta(site,analysis,observable) if baseline_delta else longitudinal.trajectory(site,analysis,observable),dtype=float)
        if d.ndim==1: vals=d
        elif aggregate=="mean": vals=np.nanmean(d.reshape(d.shape[0],-1),axis=1)
        elif aggregate=="max": vals=np.nanmax(d.reshape(d.shape[0],-1),axis=1)
        else: raise ValueError("aggregate must be 'mean' or 'max'")
        rows.append(vals)
    data=np.stack(rows) if rows else np.empty((0,len(longitudinal.entries)))
    ax=new_ax(ax,(9,5)); im=ax.imshow(data,aspect="auto",origin="lower")
    ax.set_yticks(range(len(common)),common); ax.set_xticks(range(len(longitudinal.entries)),[e.key for e in longitudinal.entries],rotation=30,ha="right")
    ax.set_xlabel("checkpoint"); ax.set_ylabel("representation site"); ax.set_title(f"Layer × checkpoint: {observable}"); ax.figure.colorbar(im,ax=ax); ax.figure.tight_layout(); return ax.figure


def structural_diff_heatmap(diff, analysis, observable, ax=None):
    sites=[]; rows=[]
    for site,by_analysis in diff.differences.items():
        if analysis not in by_analysis or observable not in by_analysis[analysis]: continue
        arr=np.asarray(by_analysis[analysis][observable]["difference"],dtype=float).reshape(-1)
        sites.append(site); rows.append(arr)
    if not rows: raise ValueError(f"No numeric structural differences for {analysis}.{observable}")
    m=min(map(len,rows)); data=np.stack([r[:m] for r in rows])
    ax=new_ax(ax,(9,5)); im=ax.imshow(data,aspect="auto",origin="lower")
    ax.set_yticks(range(len(sites)),sites); ax.set_xlabel("control / observable index"); ax.set_ylabel("representation site")
    ax.set_title(f"Structural diff: {diff.right_key} − {diff.left_key}"); ax.figure.colorbar(im,ax=ax); ax.figure.tight_layout(); return ax.figure


def architecture_comparison(series, analysis="percolation", observable="susceptibility_peak_parameter", ax=None):
    sites=sorted(set.intersection(*(set(e.result.layers) for e in series.entries))) if series.entries else []
    ax=new_ax(ax,(9,5)); x=np.arange(len(sites)); width=.8/max(1,len(series.entries))
    for j,e in enumerate(series.entries):
        vals=[]
        for s in sites:
            ar=e.result.layers[s].analyses.get(analysis); v=np.nan if ar is None else ar.observables.get(observable,np.nan)
            vals.append(float(v) if np.isscalar(v) else np.nan)
        ax.bar(x+(j-(len(series.entries)-1)/2)*width,vals,width=width,label=e.key)
    ax.set_xticks(x,sites,rotation=30,ha="right"); ax.set_ylabel(observable.replace("_"," ")); ax.set_title("Matched architecture / model comparison"); ax.legend(); ax.figure.tight_layout(); return ax.figure


def retention_dashboard(series_by_role, *, site=None, factor="class", metric="nmi", fig=None):
    fig=fig or plt.figure(figsize=(11,5)); fig.clf(); axes=fig.subplots(1,2)
    for role,series in series_by_role.items():
        long=series.longitudinal(); s=site or list(long.entries[0].result.layers)[-1]
        vals=[]
        for e in long.entries:
            ar=e.result.layers[s].analyses["factor_alignment"]
            ys=[r[factor][metric] for r in ar.records if factor in r]
            vals.append(float(np.nanmax(ys)) if ys else np.nan)
        axes[0].plot(long.times,vals,marker="o",label=role)
    axes[0].set_title("Target / retention structural alignment"); axes[0].set_xlabel("training/checkpoint coordinate"); axes[0].set_ylabel(metric.upper()); axes[0].legend()
    # Baseline-relative displacement for each role.
    for role,series in series_by_role.items():
        long=series.longitudinal(); s=site or list(long.entries[0].result.layers)[-1]
        vals=[]
        base=None
        for e in long.entries:
            ar=e.result.layers[s].analyses["factor_alignment"]; ys=[r[factor][metric] for r in ar.records if factor in r]; v=float(np.nanmax(ys)) if ys else np.nan
            if base is None: base=v
            vals.append(v-base)
        axes[1].plot(long.times,vals,marker="o",label=role)
    axes[1].axhline(0,linewidth=1); axes[1].set_title("Baseline-relative structural displacement"); axes[1].set_xlabel("training/checkpoint coordinate"); axes[1].set_ylabel("change"); axes[1].legend()
    fig.tight_layout(); return fig


def development_dashboard(series, *, site=None, structural_analysis="factor_alignment", factor="class", metric="nmi", fig=None):
    fig=fig or plt.figure(figsize=(12,8)); fig.clf(); axes=fig.subplots(2,2)
    long=series.longitudinal(); s=site or list(long.entries[0].result.layers)[-1]
    align=[]
    for e in long.entries:
        ar=e.result.layers[s].analyses.get(structural_analysis); ys=[r[factor][metric] for r in ar.records if factor in r] if ar else []
        align.append(float(np.nanmax(ys)) if ys else np.nan)
    axes[0,0].plot(long.times,align,marker="o"); axes[0,0].set_title(f"{factor} structural alignment")
    behavior_keys=sorted(set().union(*(set(e.behavior.metrics) if e.behavior else set() for e in series.entries)))
    for k in behavior_keys:
        axes[0,1].plot(long.times,[np.nan if e.behavior is None else e.behavior.metrics.get(k,np.nan) for e in series.entries],marker="o",label=k)
    axes[0,1].set_title("Behavioral metrics");
    if behavior_keys: axes[0,1].legend()
    efficiency_keys=sorted(set().union(*(set(e.behavior.efficiency) if e.behavior else set() for e in series.entries)))
    for k in efficiency_keys:
        axes[1,0].plot(long.times,[np.nan if e.behavior is None else e.behavior.efficiency.get(k,np.nan) for e in series.entries],marker="o",label=k)
    axes[1,0].set_title("Efficiency metrics")
    if efficiency_keys: axes[1,0].legend()
    axes[1,1].plot(long.times,np.asarray(align)-align[0],marker="o"); axes[1,1].axhline(0,linewidth=1); axes[1,1].set_title("Structural displacement from baseline")
    for ax in axes.ravel(): ax.set_xlabel("training/checkpoint coordinate")
    fig.suptitle(f"{series.name}: development report dashboard"); fig.tight_layout(); return fig
