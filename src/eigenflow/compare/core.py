from __future__ import annotations
import numpy as np

def compare_scalar_observable(result_a,result_b,site,analysis,observable):
    a=result_a.layers[site].analyses[analysis].observables[observable]; b=result_b.layers[site].analyses[analysis].observables[observable]
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    if aa.shape!=bb.shape: raise ValueError("Observable shapes differ; align control coordinates before comparison")
    return {"difference":(aa-bb),"mean_absolute_difference":float(np.mean(np.abs(aa-bb)))}
