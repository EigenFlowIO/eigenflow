import numpy as np

def metric_diagnostics(rel):
    A=np.asarray(rel.values); tri=A[np.triu_indices_from(A,1)]
    return {"min":float(np.min(tri)),"max":float(np.max(tri)),"mean":float(np.mean(tri)),"std":float(np.std(tri)),"ties":int(len(tri)-len(np.unique(tri))),"symmetric":bool(np.allclose(A,A.T,equal_nan=True)),"finite":bool(np.isfinite(A).all()),"rank":int(np.linalg.matrix_rank(A))}
