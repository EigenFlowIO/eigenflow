from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from ..exceptions import ValidationError

@dataclass
class Representation:
    values: np.ndarray
    site: str
    probe_ids: list[str]
    raw_shape: tuple|None=None
    reducer: str|None=None
    metadata: dict = field(default_factory=dict)
    def __post_init__(self):
        self.values=np.asarray(self.values)
        if self.values.ndim!=2: raise ValidationError(f"Representation at {self.site} must be 2D")
        if self.values.shape[0]!=len(self.probe_ids): raise ValidationError("Probe IDs do not align with representation rows")

@dataclass
class RepresentationCollection:
    representations: dict[str,Representation]
    probe_ids: list[str]
    def __getitem__(self,k): return self.representations[k]
    def __iter__(self): return iter(self.representations)
    def items(self): return self.representations.items()
    @property
    def sites(self): return list(self.representations)
