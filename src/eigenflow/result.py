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
        out={}
        for site,r in self.layers.items():
            analyses={}
            for name,ar in r.analyses.items():
                analyses[name]=ar.status_summary() if hasattr(ar,"status_summary") else {"status":"ok"}
            out[site]={"metric":r.metric,"filtration":r.filtration,"analyses":analyses}
        return out
    def save(self,path):
        p=Path(path); p.mkdir(parents=True,exist_ok=True)
        def clean(x):
            if isinstance(x,np.ndarray):
                if np.iscomplexobj(x):
                    return {"__complex_array__":{"real":np.real(x).tolist(),"imag":np.imag(x).tolist()}}
                return x.tolist()
            if isinstance(x,(complex,np.complexfloating)):
                return {"__complex__":[float(np.real(x)),float(np.imag(x))]}
            if hasattr(x,"__dataclass_fields__"):
                return {k:clean(v) for k,v in vars(x).items() if k not in {"eigenvectors","artifacts"}}
            if isinstance(x,dict): return {str(k):clean(v) for k,v in x.items()}
            if isinstance(x,(list,tuple)): return [clean(v) for v in x]
            if isinstance(x,(np.floating,np.integer)): return x.item()
            return x
        data={"provenance":clean(self.provenance),"metadata":clean(self.metadata),"layers":{k:clean(v) for k,v in self.layers.items()}}
        (p/"result.json").write_text(json.dumps(data,indent=2))

        # Persist spectral eigenvectors in a compact binary sidecar.  JSON keeps
        # the portable scalar/record surface; NPZ preserves complex arrays
        # losslessly without inflating result.json.
        spectral_arrays={}
        for site,layer in self.layers.items():
            ar=layer.analyses.get("spectra") if hasattr(layer,"analyses") else None
            traj=getattr(ar,"observables",{}).get("trajectory") if ar is not None else None
            if traj is None: continue
            for i,snap in enumerate(traj.snapshots):
                if snap.eigenvectors is not None:
                    spectral_arrays[f"{site}::{i}"]=np.asarray(snap.eigenvectors)
        if spectral_arrays:
            np.savez_compressed(p/"spectral_eigenvectors.npz",**spectral_arrays)
        return p
