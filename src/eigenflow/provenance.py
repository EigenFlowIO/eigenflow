from __future__ import annotations
import platform,sys,datetime
import numpy as np
try:
 import torch
except Exception: torch=None

def collect_provenance(model=None,**config):
    return {"created_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"python":sys.version.split()[0],"platform":platform.platform(),"numpy":np.__version__,"torch":getattr(torch,"__version__",None),"model_class":None if model is None else f"{model.__class__.__module__}.{model.__class__.__name__}","config":config}
