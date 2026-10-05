from .base import GraphOperator
from .standard import *
def resolve_operator(x):
    if isinstance(x,GraphOperator): return x
    table={"adjacency":AdjacencyOperator,"laplacian":LaplacianOperator,"normalized_laplacian":NormalizedLaplacianOperator,"random_walk":RandomWalkOperator,"modularity":ModularityOperator,"nonbacktracking":NonBacktrackingOperator}
    if x in table:return table[x]()
    raise ValueError(f"Unknown operator {x!r}")
from .nonbacktracking import NonBacktrackingOperator
