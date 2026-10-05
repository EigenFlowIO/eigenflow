from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Sequence
import numpy as np
import torch
from .reducers import resolve_reducer
from ..representations import Representation, RepresentationCollection
from ..probes import ProbePopulation
from ..exceptions import ExtractionError

@dataclass
class ExtractionConfig:
    sites: str|Sequence[str]="all"
    reducer: object="flatten"
    batch_size: int=32
    retain_raw: bool=False
    leaf_modules_only: bool=True

class PyTorchExtractor:
    def __init__(self, model: torch.nn.Module, config: ExtractionConfig|None=None, device=None):
        self.model=model; self.config=config or ExtractionConfig(); self.device=device or next(model.parameters(),torch.empty(0)).device

    def available_sites(self): return [n for n,_ in self.model.named_modules() if n]
    def _selected(self):
        modules=dict(self.model.named_modules())
        if self.config.sites!="all":
            missing=[n for n in self.config.sites if n not in modules]
            if missing: raise ExtractionError(f"Unknown module sites: {missing}")
            return [(n,modules[n]) for n in self.config.sites]
        out=[]
        for n,m in modules.items():
            if not n: continue
            if self.config.leaf_modules_only and any(True for _ in m.children()): continue
            out.append((n,m))
        return out

    def extract(self, probes: ProbePopulation, collate_fn: Callable|None=None):
        reducer=resolve_reducer(self.config.reducer); selected=self._selected(); captured={n:[] for n,_ in selected}; raw_shapes={}
        hooks=[]
        def hook_for(name):
            def h(module, inputs, output):
                y=output
                if isinstance(y,(tuple,list)): y=next((v for v in y if torch.is_tensor(v)),None)
                elif isinstance(y,dict): y=next((v for v in y.values() if torch.is_tensor(v)),None)
                if not torch.is_tensor(y): return
                raw_shapes[name]=tuple(y.shape)
                captured[name].append(reducer.reduce(y.detach()).cpu())
            return h
        for n,m in selected: hooks.append(m.register_forward_hook(hook_for(n)))
        was_training=self.model.training; self.model.eval()
        try:
            with torch.no_grad():
                for start in range(0,len(probes.samples),self.config.batch_size):
                    xs=[s.input for s in probes.samples[start:start+self.config.batch_size]]
                    if collate_fn: batch=collate_fn(xs)
                    elif torch.is_tensor(xs[0]): batch=torch.stack(xs)
                    else: raise ExtractionError("Non-tensor probe inputs require collate_fn")
                    if torch.is_tensor(batch): batch=batch.to(self.device)
                    self.model(batch)
        finally:
            for h in hooks: h.remove()
            self.model.train(was_training)
        reps={}
        for n,_ in selected:
            if not captured[n]: continue
            arr=torch.cat(captured[n],dim=0).numpy()
            reps[n]=Representation(arr,n,probes.ids,raw_shape=raw_shapes.get(n),reducer=reducer.name)
        if not reps: raise ExtractionError("No tensor activations were captured")
        return RepresentationCollection(reps, probes.ids)
