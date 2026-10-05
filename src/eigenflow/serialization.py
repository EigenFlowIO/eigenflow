from __future__ import annotations
from pathlib import Path
import json

def save_result(result,path): return result.save(path)

def load_result(path):
    """Load a portable serialized result as a plain dictionary.

    Portable loading deliberately does not reconstruct model objects or large
    in-memory eigenspace classes; it is intended for downstream inspection,
    reporting, and compatibility-stable archival.
    """
    p=Path(path)
    if p.is_dir(): p=p/"result.json"
    return json.loads(p.read_text())


def load_result_object(path):
    """Reconstruct a portable ExperimentResult from ``result.json``.

    Runtime-only artifacts and eigenvectors are intentionally not reconstructed.
    Numeric spectral trajectories are rebuilt from saved spectral records so the
    standard spectral trajectory plots remain usable after loading.
    """
    from .result import ExperimentResult,LayerResult
    from .analyses.base import AnalysisResult
    from .spectra import SpectralSnapshot,SpectralTrajectory
    import numpy as np
    data=load_result(path)
    layers={}
    for site,row in data.get("layers",{}).items():
        analyses={}
        for name,ar in row.get("analyses",{}).items():
            obs=dict(ar.get("observables",{})); rec=list(ar.get("records",[])); meta=dict(ar.get("metadata",{}))
            if name=="spectra" and rec:
                snaps=[]; operator=meta.get("operator","unknown")
                for r in rec:
                    eig=np.asarray(r.get("eigenvalues",[]),dtype=float)
                    o={k:v for k,v in r.items() if k not in {"parameter","eigenvalues"}}
                    snaps.append(SpectralSnapshot(float(r.get("parameter",0.0)),eig,None,operator,o))
                obs["trajectory"]=SpectralTrajectory(snaps,operator)
            analyses[name]=AnalysisResult(name,obs,rec,meta)
        layers[site]=LayerResult(site,row.get("metric","unknown"),row.get("filtration","unknown"),analyses,row.get("relational_metadata",{}),None)
    return ExperimentResult(layers,data.get("provenance",{}),data.get("metadata",{}),None)
