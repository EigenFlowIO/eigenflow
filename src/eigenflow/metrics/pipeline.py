from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from .base import Metric
from .pairwise import resolve_metric

class Transform:
    name = "transform"
    def apply(self, X):
        raise NotImplementedError

@dataclass
class Center(Transform):
    name: str = "center"
    def apply(self, X):
        X=np.asarray(X,float); return X-X.mean(axis=0,keepdims=True)

@dataclass
class Standardize(Transform):
    eps: float = 1e-12
    name: str = "standardize"
    def apply(self, X):
        X=np.asarray(X,float); mu=X.mean(axis=0,keepdims=True); sd=X.std(axis=0,keepdims=True); return (X-mu)/np.maximum(sd,self.eps)

@dataclass
class L2Normalize(Transform):
    eps: float = 1e-12
    name: str = "l2_normalize"
    def apply(self, X):
        X=np.asarray(X,float); n=np.linalg.norm(X,axis=1,keepdims=True); return X/np.maximum(n,self.eps)

@dataclass
class MetricPipeline(Metric):
    transforms: list = field(default_factory=list)
    metric: object = "cosine"
    name: str = "pipeline"
    def __post_init__(self):
        self.metric=resolve_metric(self.metric)
        self.kind=self.metric.kind
        self.name="pipeline:"+self.metric.name
    def pairwise_values(self,X):
        Y=np.asarray(X,float)
        for t in self.transforms:
            Y=t.apply(Y) if hasattr(t,"apply") else t(Y)
        return self.metric.pairwise_values(Y)
