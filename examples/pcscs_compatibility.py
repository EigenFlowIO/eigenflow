import torch
import eigenflow as ef
model=torch.nn.Sequential(torch.nn.Linear(4,6),torch.nn.ReLU(),torch.nn.Linear(6,3))
probes=ef.ProbePopulation.from_items([torch.randn(4) for _ in range(12)])
result=ef.presets.pcscs(model,probes,steps=25)
print(result.summary())
