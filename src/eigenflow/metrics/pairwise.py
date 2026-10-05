from __future__ import annotations
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import cosine_similarity, rbf_kernel, polynomial_kernel
from .base import Metric

class CosineSimilarity(Metric):
    name="cosine"; kind="similarity"
    def pairwise_values(self,X): return cosine_similarity(X)
class EuclideanDistance(Metric):
    name="euclidean"; kind="distance"
    def pairwise_values(self,X): return cdist(X,X,"euclidean")
class SquaredEuclideanDistance(Metric):
    name="squared_euclidean"; kind="distance"
    def pairwise_values(self,X): return cdist(X,X,"sqeuclidean")
class ManhattanDistance(Metric):
    name="manhattan"; kind="distance"
    def pairwise_values(self,X): return cdist(X,X,"cityblock")
class CorrelationDistance(Metric):
    name="correlation"; kind="distance"
    def pairwise_values(self,X): return np.nan_to_num(cdist(X,X,"correlation"),nan=0.0)
class DotProductSimilarity(Metric):
    name="dot_product"; kind="similarity"
    def pairwise_values(self,X): return X@X.T
class MahalanobisDistance(Metric):
    name="mahalanobis"; kind="distance"
    def __init__(self, regularization=1e-6): self.regularization=regularization
    def pairwise_values(self,X):
        cov=np.cov(X,rowvar=False)+self.regularization*np.eye(X.shape[1]); VI=np.linalg.pinv(cov)
        return cdist(X,X,"mahalanobis",VI=VI)
class RBFKernel(Metric):
    name="rbf"; kind="similarity"
    def __init__(self,gamma=None): self.gamma=gamma
    def pairwise_values(self,X): return rbf_kernel(X,gamma=self.gamma)
class PolynomialKernel(Metric):
    name="polynomial"; kind="similarity"
    def __init__(self,degree=3,gamma=None,coef0=1): self.degree=degree; self.gamma=gamma; self.coef0=coef0
    def pairwise_values(self,X): return polynomial_kernel(X,degree=self.degree,gamma=self.gamma,coef0=self.coef0)
class CallableMetric(Metric):
    def __init__(self,fn,name="callable",kind="similarity"): self.fn=fn; self.name=name; self.kind=kind
    def pairwise_values(self,X): return np.asarray(self.fn(X),float)

def resolve_metric(metric):
    if isinstance(metric,Metric): return metric
    table={"cosine":CosineSimilarity,"euclidean":EuclideanDistance,"squared_euclidean":SquaredEuclideanDistance,"manhattan":ManhattanDistance,"correlation":CorrelationDistance,"dot_product":DotProductSimilarity,"mahalanobis":MahalanobisDistance,"rbf":RBFKernel,"polynomial":PolynomialKernel}
    if isinstance(metric,str) and metric in table: return table[metric]()
    if hasattr(metric,"pairwise"): return metric
    raise ValueError(f"Unknown metric {metric!r}")
