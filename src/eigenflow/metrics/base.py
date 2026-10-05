from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import numpy as np

@dataclass
class RelationalMatrix:
    values: np.ndarray
    kind: str
    metric: str
    probe_ids: list[str]
    metadata: dict[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        self.values=np.asarray(self.values,float)
        if self.values.ndim!=2 or self.values.shape[0]!=self.values.shape[1]: raise ValueError("Relational matrix must be square")
        if self.kind not in {"similarity","distance"}: raise ValueError("kind must be similarity or distance")
    @property
    def n(self): return self.values.shape[0]

class Metric:
    name="metric"; kind="similarity"
    def pairwise_values(self,X): raise NotImplementedError
    def pairwise(self, representation):
        X=representation.values if hasattr(representation,"values") else np.asarray(representation)
        ids=getattr(representation,"probe_ids",[str(i) for i in range(len(X))])
        return RelationalMatrix(self.pairwise_values(X),self.kind,self.name,list(ids))
