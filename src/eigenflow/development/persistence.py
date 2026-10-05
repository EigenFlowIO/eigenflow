from __future__ import annotations
from pathlib import Path
import json
import numpy as np
from .series import ExperimentSeries, SeriesEntry, BehavioralRecord
from .specs import ExperimentSpec, ComparisonSpec
from ..serialization import load_result_object


def save_series(series: ExperimentSeries, path):
    root=Path(path); root.mkdir(parents=True,exist_ok=True); (root/"results").mkdir(exist_ok=True)
    index={"name":series.name,"comparison":{"vary":list(series.comparison.vary),"require_same":list(series.comparison.require_same),"allow_site_alignment":series.comparison.allow_site_alignment,"notes":series.comparison.notes},"metadata":series.metadata,"entries":[]}
    arrays={}
    for i,e in enumerate(series.entries):
        sub=f"{i:04d}_{e.key}"; e.result.save(root/"results"/sub)
        index["entries"].append({
            "key":e.key,"spec":e.spec.to_dict(),"time":e.time,"checkpoint":e.checkpoint,"model":e.model,"architecture":e.architecture,"condition":e.condition,"run":e.run,
            "behavior":None if e.behavior is None else {"metrics":e.behavior.metrics,"efficiency":e.behavior.efficiency,"metadata":e.behavior.metadata},
            "metadata":e.metadata,"result_path":f"results/{sub}/result.json"
        })
        for site,layer in e.result.layers.items():
            for an,ar in layer.analyses.items():
                for ob,val in ar.observables.items():
                    try:
                        arr=np.asarray(val,dtype=float)
                    except (TypeError,ValueError):
                        continue
                    if arr.dtype!=object and arr.size and arr.ndim<=2:
                        arrays[f"{i}|{site}|{an}|{ob}"]=arr
    (root/"series.json").write_text(json.dumps(index,indent=2,default=str))
    if arrays: np.savez_compressed(root/"arrays.npz",**arrays)
    return root


def load_series(path):
    root=Path(path); data=json.loads((root/"series.json").read_text())
    c=data.get("comparison",{}); comparison=ComparisonSpec(tuple(c.get("vary",ComparisonSpec().vary)),tuple(c.get("require_same",ComparisonSpec().require_same)),bool(c.get("allow_site_alignment",False)),c.get("notes"))
    series=ExperimentSeries(data.get("name","experiment_series"),comparison=comparison,metadata=data.get("metadata",{}))
    for row in data.get("entries",[]):
        result=load_result_object(root/row["result_path"])
        behavior=row.get("behavior"); br=None if behavior is None else BehavioralRecord(**behavior)
        entry=SeriesEntry(row["key"],result,ExperimentSpec.from_dict(row["spec"]),row.get("time"),row.get("checkpoint"),row.get("model"),row.get("architecture"),row.get("condition"),row.get("run"),br,row.get("metadata",{}))
        series.entries.append(entry)
    return series
