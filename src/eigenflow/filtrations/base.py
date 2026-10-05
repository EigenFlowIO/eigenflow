from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from scipy import sparse
from ..metrics.base import RelationalMatrix

@dataclass
class GraphSnapshot:
    parameter: float
    adjacency: sparse.csr_matrix
    edge_density: float
    native_parameter: float|int|None=None
    metadata: dict=field(default_factory=dict)
    @property
    def n(self): return self.adjacency.shape[0]

@dataclass
class GraphFiltration:
    snapshots: list[GraphSnapshot]
    relational_matrix: RelationalMatrix
    name: str
    monotone: bool=True
    @property
    def parameters(self): return np.array([s.parameter for s in self.snapshots])
    @property
    def edge_densities(self): return np.array([s.edge_density for s in self.snapshots])
    def __iter__(self): return iter(self.snapshots)
    def __len__(self): return len(self.snapshots)

class Filtration:
    name="filtration"
    def build(self,rel:RelationalMatrix)->GraphFiltration: raise NotImplementedError

def adjacency_from_mask(mask):
    m=np.asarray(mask,bool).copy(); np.fill_diagonal(m,False); m=np.logical_or(m,m.T); return sparse.csr_matrix(m.astype(float))
def density(A):
    n=A.shape[0]; return float(A.nnz/(n*(n-1))) if n>1 else 0.0
