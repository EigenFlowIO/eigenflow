import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import laplacian
from .base import GraphOperator

class AdjacencyOperator(GraphOperator):
    name="adjacency"
    def matrix(self,snapshot): return snapshot.adjacency.astype(float)
class LaplacianOperator(GraphOperator):
    name="laplacian"
    def matrix(self,snapshot): return laplacian(snapshot.adjacency,normed=False).tocsr()
class NormalizedLaplacianOperator(GraphOperator):
    name="normalized_laplacian"
    def matrix(self,snapshot): return laplacian(snapshot.adjacency,normed=True).tocsr()
class RandomWalkOperator(GraphOperator):
    name="random_walk"
    def matrix(self,snapshot):
        A=snapshot.adjacency.astype(float); d=np.asarray(A.sum(axis=1)).ravel(); inv=np.divide(1,d,out=np.zeros_like(d),where=d>0)
        return sparse.diags(inv)@A
class ModularityOperator(GraphOperator):
    name="modularity"
    def matrix(self,snapshot):
        A=snapshot.adjacency.toarray().astype(float); d=A.sum(axis=1); m=d.sum()/2
        return sparse.csr_matrix(A-np.outer(d,d)/(2*m)) if m else sparse.csr_matrix(A)
