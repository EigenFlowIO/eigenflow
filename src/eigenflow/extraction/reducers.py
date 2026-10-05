from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
import torch

class Reducer(Protocol):
    def reduce(self, x: torch.Tensor) -> torch.Tensor: ...
    @property
    def name(self) -> str: ...

@dataclass
class Flatten:
    name: str="flatten"
    def reduce(self,x): return x.reshape(x.shape[0],-1)
@dataclass
class GlobalAveragePool:
    name: str="global_average"
    def reduce(self,x):
        if x.ndim<=2: return x.reshape(x.shape[0],-1)
        return x.mean(dim=tuple(range(2,x.ndim))) if x.ndim>2 else x
@dataclass
class GlobalMaxPool:
    name: str="global_max"
    def reduce(self,x):
        if x.ndim<=2: return x.reshape(x.shape[0],-1)
        dims=tuple(range(2,x.ndim)); return torch.amax(x,dim=dims)
@dataclass
class SelectToken:
    index: int=0
    name: str="select_token"
    def reduce(self,x):
        if x.ndim!=3: raise ValueError("SelectToken expects [batch,tokens,features]")
        return x[:,self.index,:]
@dataclass
class MeanTokens:
    name: str="mean_tokens"
    def reduce(self,x):
        if x.ndim!=3: raise ValueError("MeanTokens expects [batch,tokens,features]")
        return x.mean(dim=1)

def resolve_reducer(r):
    if r is None or r=="flatten": return Flatten()
    if r=="global_average": return GlobalAveragePool()
    if r=="global_max": return GlobalMaxPool()
    if r=="mean_tokens": return MeanTokens()
    if hasattr(r,"reduce"): return r
    if callable(r):
        class CallableReducer:
            name=getattr(r,"__name__","callable")
            def reduce(self,x): return r(x)
        return CallableReducer()
    raise ValueError(f"Unknown reducer {r!r}")
