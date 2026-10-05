from __future__ import annotations
from dataclasses import dataclass,field
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.linalg import subspace_angles

@dataclass
class SpectralSnapshot:
    parameter: float
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray|None
    operator: str
    observables: dict=field(default_factory=dict)
@dataclass
class SpectralTrajectory:
    snapshots: list[SpectralSnapshot]
    operator: str
    @property
    def parameters(self): return np.array([s.parameter for s in self.snapshots])

def solve_spectrum(M,k=None,vectors=True,which=None):
    n=M.shape[0]
    if n==0:return np.array([]),None
    symmetric=(M-M.T).nnz==0 if sparse.issparse(M) else np.allclose(M,M.T)
    if n<=128 or k is None or k>=n-1:
        a=M.toarray() if sparse.issparse(M) else np.asarray(M)
        vals,vecs=(np.linalg.eigh(a) if symmetric else np.linalg.eig(a)); order=np.argsort(vals.real)
        vals=vals.real[order]; vecs=vecs.real[:,order]
    else:
        which=which or "SM"; vals,vecs=eigsh(M,k=min(k,n-2),which=which); order=np.argsort(vals); vals=vals[order]; vecs=vecs[:,order]
    return vals,(vecs if vectors else None)

def ipr(vecs): return np.sum(np.asarray(vecs)**4,axis=0)
def spectral_entropy(vals):
    a=np.abs(vals); s=a.sum()
    if s==0:return 0.0
    p=a/s; p=p[p>0]; return float(-(p*np.log(p)).sum())
def effective_rank(vals): return float(np.exp(spectral_entropy(vals)))
def graph_energy(vals): return float(np.abs(vals).sum())
def spectral_gaps(vals): return np.diff(np.sort(vals))
def eigenspace_overlap(V,W):
    if V is None or W is None:return None
    return np.abs(V.T@W)
def principal_angle_values(V,W): return subspace_angles(V,W)
