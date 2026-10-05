from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any

@dataclass
class AnalysisResult:
    name: str
    observables: dict[str,Any]=field(default_factory=dict)
    records: list[dict[str,Any]]=field(default_factory=list)
    metadata: dict[str,Any]=field(default_factory=dict)

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
