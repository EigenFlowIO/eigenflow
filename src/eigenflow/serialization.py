from __future__ import annotations
from pathlib import Path
import json


def _decode_complex(x):
    if isinstance(x, dict):
        if set(x) == {"__complex__"}:
            r, i = x["__complex__"]
            return complex(r, i)
        if set(x) == {"__complex_array__"}:
            import numpy as np
            d=x["__complex_array__"]
            return np.asarray(d["real"],dtype=float)+1j*np.asarray(d["imag"],dtype=float)
        return {k:_decode_complex(v) for k,v in x.items()}
    if isinstance(x, list):
        return [_decode_complex(v) for v in x]
    return x


def save_result(result,path): return result.save(path)


def load_result(path):
    """Load a portable serialized result as a plain dictionary."""
    p=Path(path)
    if p.is_dir(): p=p/"result.json"
    return _decode_complex(json.loads(p.read_text()))


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
    base=Path(path); base=base if base.is_dir() else base.parent
    eigenvector_file=base/"spectral_eigenvectors.npz"
    eigenvector_store=np.load(eigenvector_file,allow_pickle=False) if eigenvector_file.exists() else None
    layers={}
    for site,row in data.get("layers",{}).items():
        analyses={}
        for name,ar in row.get("analyses",{}).items():
            obs=dict(ar.get("observables",{})); rec=list(ar.get("records",[])); meta=dict(ar.get("metadata",{}))
            if name=="spectra" and rec:
                snaps=[]; operator=meta.get("operator","unknown"); policy=meta.get("complex_policy","auto")
                for r in rec:
                    raw=r.get("eigenvalues",[])
                    eig=np.asarray([] if raw is None else raw,dtype=complex)
                    if not np.any(np.abs(eig.imag)>0): eig=eig.real
                    o={k:v for k,v in r.items() if k not in {"parameter","eigenvalues"}}
                    key=f"{site}::{len(snaps)}"
                    vecs=eigenvector_store[key] if eigenvector_store is not None and key in eigenvector_store.files else None
                    snaps.append(SpectralSnapshot(float(r.get("parameter",0.0)),eig,vecs,operator,o,policy))
                obs["trajectory"]=SpectralTrajectory(snaps,operator)
            analyses[name]=AnalysisResult(name,obs,rec,meta)
        layers[site]=LayerResult(site,row.get("metric","unknown"),row.get("filtration","unknown"),analyses,row.get("relational_metadata",{}),None)
    if eigenvector_store is not None: eigenvector_store.close()
    return ExperimentResult(layers,data.get("provenance",{}),data.get("metadata",{}),None)
