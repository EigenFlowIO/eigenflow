import torch
from eigenflow import ProbePopulation

def test_balance_and_factorial():
    xs=[torch.tensor([float(i)]) for i in range(8)]
    meta=[{"class":"a" if i<4 else "b","bg":"x" if i%2==0 else "y"} for i in range(8)]
    p=ProbePopulation.from_items(xs,metadata=meta)
    assert len(p.balance("class",2).samples)==4
    q=p.factorial(["class","bg"],1)
    assert len(q.samples)==4
