from __future__ import annotations
import numpy as np
from ..metrics.base import RelationalMatrix


def induced_relational(rel: RelationalMatrix, indices):
    idx=np.asarray(indices,int)
    return RelationalMatrix(rel.values[np.ix_(idx,idx)],rel.kind,rel.metric,[rel.probe_ids[i] for i in idx],dict(rel.metadata))


def finite_size_resample(rel, filtration, statistic, sizes, repeats=20, seed=0):
    """Estimate a filtration statistic on random induced subpopulations.

    statistic receives a GraphFiltration and returns either a scalar or mapping.
    """
    rng=np.random.default_rng(seed); n=rel.n; records=[]
    for size in sizes:
        if size>n: raise ValueError("Requested finite-size sample exceeds population")
        for repeat in range(repeats):
            idx=rng.choice(n,size=size,replace=False)
            sub=induced_relational(rel,idx); gf=filtration.build(sub); value=statistic(gf)
            records.append({"size":int(size),"repeat":repeat,"value":value})
    return records
