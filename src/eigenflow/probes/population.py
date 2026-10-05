from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence
import random
from ..exceptions import ValidationError

@dataclass(frozen=True)
class ProbeSample:
    input: Any
    id: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

@dataclass
class ProbePopulation:
    samples: list[ProbeSample]
    name: str = "probe_population"
    design: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        ids=[s.id for s in self.samples]
        if len(ids)!=len(set(ids)): raise ValidationError("Probe IDs must be unique")
        if not self.samples: raise ValidationError("Probe population cannot be empty")

    @classmethod
    def from_items(cls, inputs: Sequence[Any], metadata: Sequence[Mapping[str,Any]]|None=None, ids: Sequence[str]|None=None, name="probe_population"):
        metadata = metadata or [{} for _ in inputs]
        ids = ids or [f"probe_{i:06d}" for i in range(len(inputs))]
        if not (len(inputs)==len(metadata)==len(ids)): raise ValidationError("inputs, metadata, and ids must have equal length")
        return cls([ProbeSample(x,str(i),dict(m)) for x,m,i in zip(inputs,metadata,ids)], name=name)

    @property
    def ids(self): return [s.id for s in self.samples]
    @property
    def metadata(self): return [dict(s.metadata) for s in self.samples]
    @property
    def inputs(self): return [s.input for s in self.samples]
    def values(self, factor: str): return [s.metadata.get(factor) for s in self.samples]

    def subset(self, indices: Sequence[int], name: str|None=None):
        return ProbePopulation([self.samples[i] for i in indices], name=name or self.name, design={**self.design,"parent":self.name})

    def balance(self, factor: str, n_per_group: int|None=None, seed: int=0):
        groups={}
        for i,s in enumerate(self.samples): groups.setdefault(s.metadata.get(factor),[]).append(i)
        if None in groups: raise ValidationError(f"Missing metadata factor {factor!r}")
        n=n_per_group or min(map(len,groups.values()))
        rng=random.Random(seed); idx=[]
        for g in sorted(groups,key=str):
            if len(groups[g])<n: raise ValidationError(f"Group {g!r} has fewer than {n} samples")
            idx += rng.sample(groups[g], n)
        return self.subset(sorted(idx), name=f"{self.name}_balanced_{factor}")

    def stratify(self, by: Sequence[str]):
        cells={}
        for i,s in enumerate(self.samples):
            key=tuple(s.metadata.get(k) for k in by); cells.setdefault(key,[]).append(i)
        return cells

    def factorial(self, factors: Sequence[str], n_per_cell: int|None=None, seed: int=0):
        cells=self.stratify(factors); rng=random.Random(seed); idx=[]
        n=n_per_cell or min(map(len,cells.values()))
        for key in sorted(cells,key=str):
            if len(cells[key])<n: raise ValidationError(f"Cell {key!r} has fewer than {n} samples")
            idx += rng.sample(cells[key],n)
        out=self.subset(sorted(idx), name=f"{self.name}_factorial")
        out.design={"type":"factorial","factors":list(factors),"n_per_cell":n,"seed":seed}
        return out

    def match(self, treatment: Mapping[str,Any], control: Mapping[str,Any], on: Sequence[str]):
        def fits(s, cond): return all(s.metadata.get(k)==v for k,v in cond.items())
        t=[s for s in self.samples if fits(s,treatment)]; c=[s for s in self.samples if fits(s,control)]
        cmap={}
        for s in c: cmap.setdefault(tuple(s.metadata.get(k) for k in on),[]).append(s)
        paired=[]
        for s in t:
            key=tuple(s.metadata.get(k) for k in on)
            if cmap.get(key): paired += [s,cmap[key].pop(0)]
        if not paired: raise ValidationError("No matched pairs found")
        return ProbePopulation(paired, name=f"{self.name}_matched", design={"type":"matched","treatment":dict(treatment),"control":dict(control),"on":list(on)})
