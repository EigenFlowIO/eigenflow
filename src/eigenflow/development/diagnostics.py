from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
import numpy as np
from .series import ExperimentSeries


@dataclass
class RetentionSummary:
    baseline_key: str
    target_role: str | None
    retain_role: str | None
    records: list[dict[str, Any]]


def retention_summary(series_by_role: dict[str, ExperimentSeries], *, analysis="factor_alignment", observable=None, factor="class", metric="nmi") -> RetentionSummary:
    """Summarize target acquisition / retention across role-specific matched series.

    For factor_alignment the requested factor/metric is extracted from records. For
    scalar/list analyses pass ``observable``.
    """
    if not series_by_role:
        raise ValueError("At least one role-specific series is required")
    keys = None
    for s in series_by_role.values():
        ks = s.longitudinal().keys
        keys = ks if keys is None else [k for k in keys if k in ks]
    records = []
    for key in keys or []:
        row = {"key": key, "roles": {}}
        for role, series in series_by_role.items():
            entry = series[key]
            vals = []
            for layer in entry.result.layers.values():
                ar = layer.analyses.get(analysis)
                if ar is None: continue
                if analysis == "factor_alignment":
                    ys = [r[factor][metric] for r in ar.records if factor in r]
                    if ys: vals.append(float(np.nanmax(ys)))
                elif observable in ar.observables:
                    a = np.asarray(ar.observables[observable], dtype=float)
                    vals.append(float(np.nanmean(a)))
            row["roles"][role] = float(np.nanmean(vals)) if vals else np.nan
        records.append(row)
    return RetentionSummary(
        baseline_key=next(iter(series_by_role.values())).entries[0].key,
        target_role="target" if "target" in series_by_role else None,
        retain_role="retain" if "retain" in series_by_role else None,
        records=records,
    )


def peft_targeting_scores(series: ExperimentSeries, *, baseline=None, analysis="factor_alignment", factor="class", metric="nmi"):
    """Rank sites by baseline-relative structural change; diagnostic only."""
    long = series.longitudinal(baseline)
    if len(long.entries) < 2:
        raise ValueError("PEFT targeting diagnostics require at least two series entries")
    final = long.entries[-1]
    base = long.baseline
    scores = []
    for site in set(base.result.layers) & set(final.result.layers):
        ba = base.result.layers[site].analyses.get(analysis); fa = final.result.layers[site].analyses.get(analysis)
        if ba is None or fa is None: continue
        if analysis == "factor_alignment":
            bv = [r[factor][metric] for r in ba.records if factor in r]
            fv = [r[factor][metric] for r in fa.records if factor in r]
            if not bv or not fv: continue
            n=min(len(bv),len(fv)); delta=np.asarray(fv[:n])-np.asarray(bv[:n])
        else:
            continue
        scores.append({"site": site, "mean_absolute_change": float(np.mean(np.abs(delta))), "signed_mean_change": float(np.mean(delta))})
    return sorted(scores, key=lambda r: r["mean_absolute_change"], reverse=True)


def select_checkpoint(series: ExperimentSeries, objective: Callable[[Any], float]):
    """Select a checkpoint using a user-supplied transparent multi-objective rule."""
    if not series.entries:
        raise ValueError("Cannot select from an empty ExperimentSeries")
    scored = [(float(objective(e)), e) for e in series.entries]
    score, entry = max(scored, key=lambda x: x[0])
    return {"key": entry.key, "score": score, "scores": {e.key: s for s, e in scored}}


def training_data_diagnostics(result, *, site=None, factor="class", top_n=10):
    site = site or list(result.layers)[-1]
    layer = result.layers[site]
    out = {"site": site, "bridge_probes": [], "factor_alignment_peak": None}
    probes = result.artifacts.probes if result.artifacts else None
    bridges = layer.analyses.get("bridges")
    if bridges is not None:
        counts = {}
        for rec in bridges.records:
            for u, v in rec.get("bridges", []):
                counts[u] = counts.get(u, 0) + 1; counts[v] = counts.get(v, 0) + 1
        order = sorted(counts, key=counts.get, reverse=True)[:top_n]
        out["bridge_probes"] = [
            {"index": i, "id": probes.samples[i].id if probes else str(i), "bridge_appearances": counts[i]}
            for i in order
        ]
    fa = layer.analyses.get("factor_alignment")
    if fa is not None:
        vals = [(r["parameter"], r[factor]["nmi"]) for r in fa.records if factor in r]
        if vals:
            p, v = max(vals, key=lambda x: x[1]); out["factor_alignment_peak"] = {"parameter": p, "nmi": v}
    return out
