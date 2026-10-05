import torch
import eigenflow as ef

def test_pcscs_preset_runs():
    model=torch.nn.Sequential(torch.nn.Linear(3,5),torch.nn.ReLU(),torch.nn.Linear(5,2))
    probes=ef.ProbePopulation.from_items([torch.randn(3) for _ in range(10)])
    r=ef.presets.pcscs(model,probes,steps=8)
    assert r.layers
    assert all("pcscs" in x.analyses for x in r.layers.values())
