import numpy as np
from ..graphs import component_sizes

def percolation_observables(snapshot):
    sizes=np.sort(component_sizes(snapshot))[::-1]
    n=snapshot.n
    giant=float(sizes[0]/n) if len(sizes) else 0.0
    second=float(sizes[1]/n) if len(sizes)>1 else 0.0
    finite=sizes[1:] if len(sizes)>1 else np.array([],int)
    susceptibility=float((finite.astype(float)**2).sum()/finite.sum()) if finite.sum()>0 else 0.0
    unique,counts=np.unique(sizes,return_counts=True)
    return {"giant_component_fraction":giant,"second_component_fraction":second,"susceptibility":susceptibility,"component_size_distribution":{int(s):int(c) for s,c in zip(unique,counts)}}
