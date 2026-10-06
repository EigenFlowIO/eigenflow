import numpy as np
from scipy import sparse
from .base import GraphOperator


class NonBacktrackingOperator(GraphOperator):
    name = "nonbacktracking"
    space = "directed_edge"
    allows_negative_weights = True
    spectral_expectation = "potentially_complex"

    def matrix(self, snapshot):
        self.validate(snapshot)
        A = snapshot.adjacency.tocsr()
        rows, cols = A.nonzero()
        directed = [(int(i), int(j)) for i, j in zip(rows, cols) if i != j]
        index = {e: k for k, e in enumerate(directed)}
        rr = []
        cc = []
        data = []
        nbrs = {
            i: set(A.indices[A.indptr[i] : A.indptr[i + 1]])
            for i in range(A.shape[0])
        }
        for (i, j), r in index.items():
            for k in nbrs.get(j, ()):
                k = int(k)
                if k == i:
                    continue
                c = index.get((j, k))
                if c is not None:
                    rr.append(r)
                    cc.append(c)
                    data.append(1.0)
        return sparse.csr_matrix(
            (data, (rr, cc)), shape=(len(directed), len(directed))
        )
