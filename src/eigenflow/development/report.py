from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import numpy as np
from .series import ExperimentSeries


@dataclass
class DevelopmentReport:
    name: str
    series: str
    entries: list[dict[str, Any]]
    structural: dict[str, Any]
    interpretation_boundary: str = (
        "Structural observables are hypothesis-conditioned evidence. This report does not define a universal representation-quality score."
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "name": self.name,
            "series": self.series,
            "entries": self.entries,
            "structural": self.structural,
            "interpretation_boundary": self.interpretation_boundary,
            "metadata": self.metadata,
        }


def development_report(series: ExperimentSeries, *, analysis="percolation", observable="susceptibility_peak_parameter", name=None):
    rows=[]
    for e in series.entries:
        rows.append({
            "key": e.key,
            "time": e.time,
            "checkpoint": e.checkpoint,
            "model": e.model,
            "architecture": e.architecture,
            "condition": e.condition,
            "behavior": None if e.behavior is None else e.behavior.metrics,
            "efficiency": None if e.behavior is None else e.behavior.efficiency,
        })
    structural={}
    for site in sorted(set.intersection(*(set(e.result.layers) for e in series.entries))) if series.entries else []:
        vals=[]
        for e in series.entries:
            ar=e.result.layers[site].analyses.get(analysis)
            v=np.nan if ar is None else ar.observables.get(observable,np.nan)
            vals.append(float(v) if np.isscalar(v) else np.nan)
        structural[site]={observable: vals}
    return DevelopmentReport(name or f"{series.name}_development_report",series.name,rows,structural)
