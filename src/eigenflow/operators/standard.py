from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import laplacian

from .base import GraphOperator
from ..exceptions import OperatorCompatibilityError


class AdjacencyOperator(GraphOperator):
    name = "adjacency"
    allows_negative_weights = True

    def matrix(self, snapshot):
        self.validate(snapshot)
        return snapshot.adjacency.astype(float)


class LaplacianOperator(GraphOperator):
    name = "laplacian"
    allows_negative_weights = True

    def matrix(self, snapshot):
        self.validate(snapshot)
        return laplacian(snapshot.adjacency, normed=False).tocsr()


class NormalizedLaplacianOperator(GraphOperator):
    name = "normalized_laplacian"
    allows_negative_weights = False

    def matrix(self, snapshot):
        self.validate(snapshot)
        M = laplacian(snapshot.adjacency, normed=True).tocsr()
        if M.data.size and not np.isfinite(M.data).all():
            raise OperatorCompatibilityError(
                self.name,
                "nonfinite_operator_matrix",
                "normalized_laplacian produced non-finite matrix entries.",
            )
        return M


class RandomWalkOperator(GraphOperator):
    name = "random_walk"
    allows_negative_weights = False
    spectral_expectation = "conditionally_real"

    def matrix(self, snapshot):
        self.validate(snapshot)
        A = snapshot.adjacency.astype(float)
        d = np.asarray(A.sum(axis=1)).ravel()
        if np.any(d < 0):
            raise OperatorCompatibilityError(
                self.name,
                "negative_degree",
                "random_walk requires nonnegative weighted degree.",
                negative_degree_count=int(np.count_nonzero(d < 0)),
                min_degree=float(np.min(d)) if d.size else 0.0,
            )
        inv = np.divide(1, d, out=np.zeros_like(d), where=d > 0)
        return sparse.diags(inv) @ A


class ModularityOperator(GraphOperator):
    name = "modularity"
    allows_negative_weights = True

    def matrix(self, snapshot):
        self.validate(snapshot)
        A = snapshot.adjacency.toarray().astype(float)
        d = A.sum(axis=1)
        m = d.sum() / 2
        return sparse.csr_matrix(A - np.outer(d, d) / (2 * m)) if m else sparse.csr_matrix(A)


class SignedLaplacianOperator(GraphOperator):
    """Signed combinatorial Laplacian using absolute weighted degree.

    D_ii = sum_j |w_ij| and L_s = D - A.
    """

    name = "signed_laplacian"
    allows_negative_weights = True

    def matrix(self, snapshot):
        self.validate(snapshot)
        A = snapshot.adjacency.astype(float).tocsr()
        d = np.asarray(np.abs(A).sum(axis=1)).ravel()
        return sparse.diags(d) - A


class SignedNormalizedLaplacianOperator(GraphOperator):
    """Signed normalized Laplacian using absolute weighted degree.

    L_s,norm = I - D_abs^{-1/2} A D_abs^{-1/2}, with zero-degree rows/cols
    handled by a zero inverse square root, matching the package's isolated-node
    convention for other normalized operators.
    """

    name = "signed_normalized_laplacian"
    allows_negative_weights = True

    def matrix(self, snapshot):
        self.validate(snapshot)
        A = snapshot.adjacency.astype(float).tocsr()
        d = np.asarray(np.abs(A).sum(axis=1)).ravel()
        invsqrt = np.divide(
            1.0,
            np.sqrt(d),
            out=np.zeros_like(d, dtype=float),
            where=d > 0,
        )
        Dm = sparse.diags(invsqrt)
        I = sparse.identity(A.shape[0], format="csr", dtype=float)
        M = (I - Dm @ A @ Dm).tocsr()
        if M.data.size and not np.isfinite(M.data).all():
            raise OperatorCompatibilityError(
                self.name,
                "nonfinite_operator_matrix",
                "signed_normalized_laplacian produced non-finite matrix entries.",
            )
        return M
