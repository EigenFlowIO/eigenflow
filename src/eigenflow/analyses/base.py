from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any

@dataclass
class AnalysisResult:
    name: str
    observables: dict[str,Any]=field(default_factory=dict)
    records: list[dict[str,Any]]=field(default_factory=list)
    metadata: dict[str,Any]=field(default_factory=dict)

    @property
    def status(self):
        statuses=[r.get("status","ok") for r in self.records]
        if any(s=="error" for s in statuses): return "error"
        if any(s=="incompatible" for s in statuses): return "incompatible"
        return "ok"

    @property
    def incompatibility_count(self):
        return sum(r.get("status")=="incompatible" for r in self.records)

    def status_summary(self):
        out={"status":self.status,"incompatibility_count":self.incompatibility_count}
        for key in ("complex_policy","complex_snapshots","unexpected_complex_snapshots","incompatible_snapshots","incompatible_comparisons"):
            if key in self.metadata: out[key]=self.metadata[key]
        return out

@dataclass
class AnalysisContext:
    site: str
    representation: Any
    relational: Any
    filtration: Any
    probes: Any
    operator: Any=None

class Analysis:
    name="analysis"
    def run(self,ctx:AnalysisContext)->AnalysisResult: raise NotImplementedError
