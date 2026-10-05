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
