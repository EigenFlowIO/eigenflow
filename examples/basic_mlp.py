import torch
import eigenflow as ef

model=torch.nn.Sequential(torch.nn.Linear(4,8),torch.nn.ReLU(),torch.nn.Linear(8,2))
g=torch.Generator().manual_seed(7)
xs=[torch.randn(4,generator=g) for _ in range(20)]
meta=[{"class":"left" if i<10 else "right"} for i in range(20)]
probes=ef.ProbePopulation.from_items(xs,metadata=meta)
result=ef.Experiment(model,probes,metric="cosine",filtration=ef.filtrations.EdgeDensityFiltration(stop=.4,steps=20),analyses=["components","percolation","spectra","factor_alignment"]).run()
print(result.summary())
