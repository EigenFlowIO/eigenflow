from __future__ import annotations

import numpy as np

from ..exceptions import OperatorCompatibilityError


class GraphOperator:
    name = "operator"
    space = "node"
    allows_negative_weights = True
    spectral_expectation = "expected_real"

    def _weight_diagnostics(self, snapshot):
        A = snapshot.adjacency
        data = np.asarray(A.data, dtype=float)
        if data.size == 0:
            return {
                "finite_weights": True,
                "negative_edge_count": 0,
                "min_weight": 0.0,
                "max_weight": 0.0,
            }
        return {
            "finite_weights": bool(np.isfinite(data).all()),
            "negative_edge_count": int(np.count_nonzero(data < 0)),
            "min_weight": float(np.min(data)),
            "max_weight": float(np.max(data)),
        }

    def validate(self, snapshot):
        d = self._weight_diagnostics(snapshot)
        if not d["finite_weights"]:
            raise OperatorCompatibilityError(
                self.name,
                "nonfinite_edge_weights",
                f"{self.name} requires finite edge weights.",
                **d,
            )
        if not self.allows_negative_weights and d["negative_edge_count"]:
            raise OperatorCompatibilityError(
                self.name,
                "negative_edge_weights",
                f"{self.name} requires nonnegative edge weights; "
                f"graph contains {d['negative_edge_count']} negative weighted edges.",
                **d,
            )
        return d

    def matrix(self, snapshot):
        raise NotImplementedError
