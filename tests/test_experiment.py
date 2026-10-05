import torch
import numpy as np
import eigenflow as ef

def make():
    torch.manual_seed(1)
    model=torch.nn.Sequential(torch.nn.Linear(2,4,bias=False),torch.nn.ReLU(),torch.nn.Linear(4,2,bias=False))
    xs=[torch.tensor([1.,0.])+0.03*torch.randn(2) for _ in range(8)] + [torch.tensor([0.,1.])+0.03*torch.randn(2) for _ in range(8)]
    meta=[{"class":"a"}]*8+[{"class":"b"}]*8
    return model,ef.ProbePopulation.from_items(xs,metadata=meta)

def test_end_to_end_population_analysis(tmp_path):
    model,p=make()
    r=ef.Experiment(model,p,filtration=ef.filtrations.EdgeDensityFiltration(densities=[0,.1,.3,.6]),analyses=["components","percolation","spectra","eigenspaces","factor_alignment","class_structure"]).run()
    assert len(r.layers)>=3
    for lr in r.layers.values():
        assert "percolation" in lr.analyses
        assert len(lr.analyses["percolation"].records)==4
    r.save(tmp_path/"saved")
    assert (tmp_path/"saved"/"result.json").exists()
