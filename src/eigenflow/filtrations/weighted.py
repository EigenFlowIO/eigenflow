from __future__ import annotations
import numpy as np
from scipy import sparse
from .base import Filtration, GraphFiltration, GraphSnapshot, density

class WeightedThresholdFiltration(Filtration):
    name="weighted_threshold"
    def __init__(self, values=None, steps=100): self.values=values; self.steps=steps
    def build(self, rel):
        R=np.asarray(rel.values,float); tri=R[np.triu_indices_from(R,1)]
        vals=np.asarray(self.values if self.values is not None else np.linspace(np.max(tri),np.min(tri),self.steps),float)
        if rel.kind=="distance" and vals[0]>vals[-1]: vals=vals[::-1]
        snaps=[]
        for t in vals:
            keep=R>=t if rel.kind=="similarity" else R<=t
            W=np.where(keep,R,0.0); np.fill_diagonal(W,0.0)
            # Distances are converted to positive affinities only for retained edges.
            if rel.kind=="distance":
                nz=W!=0
                if np.any(nz):
                    maxv=float(np.max(W[nz])); W[nz]=maxv-W[nz]+np.finfo(float).eps
            W=np.maximum(W,W.T)
            A=sparse.csr_matrix(W)
            snaps.append(GraphSnapshot(float(t),A,density((A!=0).astype(float)),native_parameter=float(t),metadata={"weighted":True}))
        return GraphFiltration(snaps,rel,self.name,monotone=True)
