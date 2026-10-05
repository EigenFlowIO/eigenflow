"""Matched architecture comparison with Eigenflow development instrumentation.

This example trains two small architectures on the same controlled synthetic task,
then compares their internal representation structure with one fixed probe population.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import torch
from torch import nn
import eigenflow as ef
from eigenflow.development import ExperimentSeries,ComparisonSpec,BehavioralRecord,development_report,save_series


def make_data(n=240,seed=10):
    g=torch.Generator().manual_seed(seed); xs=[]; ys=[]; metadata=[]
    for i in range(n):
        cls=i%2; background=(i//2)%2
        x=torch.randn(4,generator=g)*0.25
        x[0]+= -1.1 if cls==0 else 1.1
        x[1]+= -0.8 if background==0 else 0.8
        xs.append(x); ys.append(cls); metadata.append({"class":f"c{cls}","background":f"b{background}"})
    return torch.stack(xs),torch.tensor(ys),metadata


class Candidate(nn.Module):
    def __init__(self,width=8,extra=False):
        super().__init__(); self.stem=nn.Linear(4,width); self.activation=nn.Tanh()
        self.representation=nn.Sequential(nn.Linear(width,width),nn.Tanh(),*( [nn.Linear(width,width),nn.Tanh()] if extra else []))
        self.head=nn.Linear(width,2)
    def forward(self,x):
        x=self.activation(self.stem(x)); x=self.representation(x); return self.head(x)


def train(model,x,y,steps=180):
    opt=torch.optim.Adam(model.parameters(),lr=.03)
    for _ in range(steps):
        opt.zero_grad(); loss=nn.functional.cross_entropy(model(x),y); loss.backward(); opt.step()
    with torch.no_grad(): return float((model(x).argmax(1)==y).float().mean())


def main():
    torch.manual_seed(1)
    x,y,meta=make_data(); train_x,probe_x=x[:180],x[180:]; train_y=y[:180]; probe_meta=meta[180:]
    probes=ef.ProbePopulation.from_items(list(probe_x),metadata=probe_meta,name="architecture_probe")
    series=ExperimentSeries("architecture_candidates",comparison=ComparisonSpec())
    for name,model in [("compact",Candidate(8,False)),("deeper",Candidate(8,True))]:
        acc=train(model,train_x,train_y)
        exp=ef.Experiment(
            model,probes,
            extraction=ef.ExtractionConfig(sites=["stem","representation","head"]),
            filtration=ef.filtrations.EdgeDensityFiltration(start=0,stop=.65,steps=18),
            analyses=["components","percolation","spectra","factor_alignment","class_structure"],
            measurement_metadata={"comparison":"architecture","candidate":name},
        )
        series.add_experiment(name,exp,architecture=name,behavior=BehavioralRecord({"training_accuracy":acc}))
    report=development_report(series)
    compatibility=series.compatibility_matrix()[("compact","deeper")]
    print("Compatibility:",compatibility.compatible)
    print("Behavior:",{e.key:e.behavior.metrics for e in series})
    print("Structural summary sites:",list(report.structural))
    fig=ef.visualization.architecture_comparison(series)
    fig.savefig("architecture_comparison.png",dpi=140)
    Path("architecture_compatibility.json").write_text(json.dumps(compatibility.to_dict(),indent=2,default=str))
    Path("architecture_development_report.json").write_text(json.dumps(report.to_dict(),indent=2,default=str))
    save_series(series,"architecture_series")


if __name__=="__main__": main()
