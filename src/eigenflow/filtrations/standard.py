from __future__ import annotations
import numpy as np
from scipy import sparse
from .base import Filtration,GraphFiltration,GraphSnapshot,adjacency_from_mask,density

class ThresholdFiltration(Filtration):
    name="threshold"
    def __init__(self,values=None,steps=100): self.values=values; self.steps=steps
    def build(self,rel):
        A=rel.values; tri=A[np.triu_indices_from(A,1)]
        vals=np.asarray(self.values if self.values is not None else np.linspace(np.max(tri),np.min(tri),self.steps))
        if rel.kind=="distance" and vals[0]>vals[-1]: vals=vals[::-1]
        snaps=[]
        for t in vals:
            mask=A>=t if rel.kind=="similarity" else A<=t
            adj=adjacency_from_mask(mask); snaps.append(GraphSnapshot(float(t),adj,density(adj),native_parameter=float(t)))
        return GraphFiltration(snaps,rel,self.name,monotone=True)

class EdgeDensityFiltration(Filtration):
    name="edge_density"
    def __init__(self,densities=None,start=0.0,stop=1.0,steps=100): self.densities=np.asarray(densities if densities is not None else np.linspace(start,stop,steps),float)
    def build(self,rel):
        n=rel.n; pairs=np.triu_indices(n,1); vals=rel.values[pairs]
        order=np.argsort(vals)
        if rel.kind=="similarity": order=order[::-1]
        total=len(order); snaps=[]
        for rho in self.densities:
            k=int(round(np.clip(rho,0,1)*total)); chosen=order[:k]; rows=pairs[0][chosen]; cols=pairs[1][chosen]
            data=np.ones(2*k); rr=np.concatenate([rows,cols]); cc=np.concatenate([cols,rows])
            adj=sparse.csr_matrix((data,(rr,cc)),shape=(n,n))
            native=float(vals[order[k-1]]) if k else None
            snaps.append(GraphSnapshot(float(rho),adj,density(adj),native_parameter=native))
        return GraphFiltration(snaps,rel,self.name,monotone=True)

class EpsilonFiltration(ThresholdFiltration):
    name="epsilon"

class KNNFiltration(Filtration):
    name="knn"
    def __init__(self,k_values=range(1,11),mutual=False): self.k_values=list(k_values); self.mutual=mutual
    def build(self,rel):
        n=rel.n; snaps=[]; A=rel.values.copy()
        for k in self.k_values:
            k=min(int(k),n-1); mask=np.zeros((n,n),bool)
            for i in range(n):
                vals=A[i].copy(); vals[i]=(-np.inf if rel.kind=="similarity" else np.inf)
                idx=np.argsort(vals)[-k:] if rel.kind=="similarity" else np.argsort(vals)[:k]
                mask[i,idx]=True
            mask=np.logical_and(mask,mask.T) if self.mutual else np.logical_or(mask,mask.T)
            adj=adjacency_from_mask(mask); snaps.append(GraphSnapshot(float(k),adj,density(adj),native_parameter=k))
        return GraphFiltration(snaps,rel,"mutual_knn" if self.mutual else self.name,monotone=True)
class MutualKNNFiltration(KNNFiltration):
    def __init__(self,k_values=range(1,11)): super().__init__(k_values,mutual=True)
