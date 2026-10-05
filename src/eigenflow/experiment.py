from __future__ import annotations
from dataclasses import dataclass,field
from .probes import ProbePopulation
from .extraction import PyTorchExtractor,ExtractionConfig
from .metrics import resolve_metric,metric_diagnostics
from .filtrations import resolve_filtration
from .analyses import resolve_analysis,AnalysisContext
from .result import ExperimentResult,LayerResult
from .provenance import collect_provenance

@dataclass
class Experiment:
    model: object
    probes: ProbePopulation
    metric: object="cosine"
    filtration: object="edge_density"
    analyses: list=field(default_factory=lambda:["components","percolation","spectra"])
    extraction: ExtractionConfig=field(default_factory=ExtractionConfig)
    device: object=None
    collate_fn: object=None

    def run(self):
        metric=resolve_metric(self.metric); filtration=resolve_filtration(self.filtration); analysis_objs=[resolve_analysis(a) for a in self.analyses]
        reps=PyTorchExtractor(self.model,self.extraction,self.device).extract(self.probes,self.collate_fn)
        layers={}
        for site,rep in reps.items():
            rel=metric.pairwise(rep); gf=filtration.build(rel); ctx=AnalysisContext(site,rep,rel,gf,self.probes)
            results={a.name:a.run(ctx) for a in analysis_objs}
            layers[site]=LayerResult(site,metric.name,gf.name,results,{"diagnostics":metric_diagnostics(rel),"representation_shape":list(rep.values.shape),"reducer":rep.reducer})
        prov=collect_provenance(self.model,metric=metric.name,filtration=filtration.name,analyses=[a.name for a in analysis_objs],sites=self.extraction.sites,reducer=str(self.extraction.reducer))
        return ExperimentResult(layers,prov,{"probe_population":self.probes.name,"probe_count":len(self.probes.samples)})
