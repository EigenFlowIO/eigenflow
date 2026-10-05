from .base import Filtration,GraphFiltration,GraphSnapshot
from .standard import ThresholdFiltration,EdgeDensityFiltration,EpsilonFiltration,KNNFiltration,MutualKNNFiltration

def resolve_filtration(x):
    if isinstance(x,Filtration): return x
    if x=="threshold": return ThresholdFiltration()
    if x=="edge_density": return EdgeDensityFiltration()
    if x=="knn": return KNNFiltration()
    if x=="mutual_knn": return MutualKNNFiltration()
    if x=="weighted_threshold": return WeightedThresholdFiltration()
    raise ValueError(f"Unknown filtration {x!r}")
from .weighted import WeightedThresholdFiltration
