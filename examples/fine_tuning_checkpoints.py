"""Longitudinal fine-tuning example: target acquisition and retention.

A small network is first trained on a retained factor and then fine-tuned on a new
target factor. The same target and retention probe populations are measured at every
checkpoint, producing Q(layer, control, time) trajectories and a retention dashboard.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import torch
from torch import nn
import eigenflow as ef
from eigenflow.development import (
    ProbeSuite,ExperimentSeries,BehavioralRecord,retention_summary,peft_targeting_scores,save_series,
)


def population(role,n=48,seed=12):
    g=torch.Generator().manual_seed(seed+(0 if role=="retain" else 100)); xs=[]; meta=[]
    for i in range(n):
        retain=i%2; target=(i//2)%2
        x=torch.randn(4,generator=g)*.22
        x[0]+= -1.0 if retain==0 else 1.0
        x[1]+= -1.0 if target==0 else 1.0
        cls=retain if role=="retain" else target
        xs.append(x); meta.append({"class":f"c{cls}","retain":retain,"target":target})
    return ef.ProbePopulation.from_items(xs,metadata=meta,name=f"{role}_probes")


def training_data(n=256,seed=7):
    g=torch.Generator().manual_seed(seed); x=torch.randn(n,4,generator=g)*.25
    retain=torch.arange(n)%2; target=(torch.arange(n)//2)%2
    x[:,0]+=torch.where(retain==0,-1.0,1.0); x[:,1]+=torch.where(target==0,-1.0,1.0)
    return x,retain.long(),target.long()


def train_steps(model,x,y,steps,lr=.025):
    opt=torch.optim.Adam(model.parameters(),lr=lr)
    for _ in range(steps):
        opt.zero_grad(); loss=nn.functional.cross_entropy(model(x),y); loss.backward(); opt.step()


def accuracy(model,x,y):
    with torch.no_grad(): return float((model(x).argmax(1)==y).float().mean())


def experiment(model,probes,role):
    return ef.Experiment(
        model,probes,
        extraction=ef.ExtractionConfig(sites=["0","1","2"]),
        filtration=ef.filtrations.EdgeDensityFiltration(start=0,stop=.7,steps=20),
        analyses=["components","percolation","spectra","factor_alignment","bridges"],
        measurement_metadata={"role":role,"workflow":"fine_tuning"},
    )


def main():
    torch.manual_seed(3); x,y_retain,y_target=training_data()
    model=nn.Sequential(nn.Linear(4,8),nn.Tanh(),nn.Linear(8,2))
    train_steps(model,x,y_retain,120)
    checkpoints=[("pretrained",0,copy.deepcopy(model.state_dict()))]
    for step in [15,40,100]:
        train_steps(model,x,y_target,step if len(checkpoints)==1 else step-checkpoints[-1][1])
        checkpoints.append((f"target_{step}",step,copy.deepcopy(model.state_dict())))
    suite=ProbeSuite({"target":population("target"),"retain":population("retain")},name="post_training_suite",version="v1")
    by_role={role:ExperimentSeries(f"{role}_checkpoint_series") for role in suite.roles}
    for key,t,state in checkpoints:
        model.load_state_dict(state)
        behavior=BehavioralRecord({"target_accuracy":accuracy(model,x,y_target),"retain_accuracy":accuracy(model,x,y_retain)})
        for role,probes in suite.populations.items():
            by_role[role].add_experiment(key,experiment(model,probes,role),time=t,checkpoint=key,behavior=behavior)
    summary=retention_summary(by_role)
    target_series=by_role["target"]
    scores=peft_targeting_scores(target_series)
    print("Checkpoints:",[e.key for e in target_series])
    print("Behavior:",{e.key:e.behavior.metrics for e in target_series})
    print("Retention summary records:",summary.records)
    print("Most changed representation sites:",scores[:3])
    Path("retention_summary.json").write_text(json.dumps(summary.records,indent=2,default=str))
    Path("peft_targeting_scores.json").write_text(json.dumps(scores,indent=2,default=str))
    suite.save_manifest("probe_suite")
    save_series(by_role["target"],"target_checkpoint_series")
    save_series(by_role["retain"],"retain_checkpoint_series")
    fig=ef.visualization.retention_dashboard(by_role)
    fig.savefig("fine_tuning_retention_dashboard.png",dpi=140)
    site=list(target_series.entries[0].result.layers)[-1]
    fig2=ef.visualization.longitudinal_surface(target_series.longitudinal(),site,"components","component_count",baseline_delta=True)
    fig2.savefig("fine_tuning_longitudinal_surface.png",dpi=140)


if __name__=="__main__": main()
