import numpy as np
from eigenflow.representations import Representation
from eigenflow.metrics import CosineSimilarity,EuclideanDistance
from eigenflow.filtrations import ThresholdFiltration,EdgeDensityFiltration

def rep(): return Representation(np.array([[1.,0.],[.9,.1],[0.,1.]]),"x",["a","b","c"])
def test_metric_orientation_and_filtration():
    c=CosineSimilarity().pairwise(rep()); e=EuclideanDistance().pairwise(rep())
    assert c.kind=="similarity" and e.kind=="distance"
    f=EdgeDensityFiltration(densities=[0,.5,1]).build(c)
    assert [round(x.edge_density,3) for x in f]==[0.0,0.667,1.0]
    t=ThresholdFiltration(values=[1,.5,0]).build(c)
    assert len(t)==3
