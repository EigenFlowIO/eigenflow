from ..experiment import Experiment

def full(model,probes,**kwargs):
    kwargs.setdefault("analyses",["components","percolation","spectra","eigenspaces","factor_alignment","class_structure","bridges","kcore","communities"])
    return Experiment(model=model,probes=probes,**kwargs).run()
