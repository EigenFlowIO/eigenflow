from ..experiment import Experiment
from ..extraction import ExtractionConfig
from ..filtrations import ThresholdFiltration
from ..metrics import CosineSimilarity

def pcscs(model,probes,sites="all",thresholds=None,steps=100,device=None,collate_fn=None):
    return Experiment(model=model,probes=probes,extraction=ExtractionConfig(sites=sites,reducer="flatten"),metric=CosineSimilarity(),filtration=ThresholdFiltration(values=thresholds,steps=steps),analyses=["pcscs","spectra"],device=device,collate_fn=collate_fn).run()
