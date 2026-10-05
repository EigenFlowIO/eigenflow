from __future__ import annotations
from dataclasses import dataclass,field
from pathlib import Path
import json, numpy as np

@dataclass
class LayerArtifacts:
    """Non-persistent runtime objects retained for analysis/visualization."""
    representation: object|None=None
    relational_matrix: object|None=None
    filtration: object|None=None

@dataclass
class ExperimentArtifacts:
    """Non-persistent experiment objects retained for diagnostics/visualization."""
    probes: object|None=None

@dataclass
class LayerResult:
    site: str
    metric: str
    filtration: str
    analyses: dict
    relational_metadata: dict=field(default_factory=dict)
    artifacts: LayerArtifacts|None=None

@dataclass
class ExperimentResult:
    layers: dict[str,LayerResult]
    provenance: dict
    metadata: dict=field(default_factory=dict)
    artifacts: ExperimentArtifacts|None=None
    def __getitem__(self,site): return self.layers[site]
    def summary(self):
        return {s:{"metric":r.metric,"filtration":r.filtration,"analyses":list(r.analyses)} for s,r in self.layers.items()}
    def save(self,path):
        p=Path(path); p.mkdir(parents=True,exist_ok=True)
        def clean(x):
            if isinstance(x,np.ndarray): return x.tolist()
            if hasattr(x,"__dataclass_fields__"):
                return {k:clean(v) for k,v in vars(x).items() if k not in {"eigenvectors","artifacts"}}
            if isinstance(x,dict): return {str(k):clean(v) for k,v in x.items()}
            if isinstance(x,(list,tuple)): return [clean(v) for v in x]
            if isinstance(x,(np.floating,np.integer)): return x.item()
            return x
        data={"provenance":clean(self.provenance),"metadata":clean(self.metadata),"layers":{k:clean(v) for k,v in self.layers.items()}}
        (p/"result.json").write_text(json.dumps(data,indent=2))
        return p
