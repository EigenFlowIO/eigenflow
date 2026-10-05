import numpy as np

def derivative_transition(parameters, values):
    p=np.asarray(parameters,float); q=np.asarray(values,float)
    if len(p)<2:return {"parameter":float(p[0]) if len(p) else None,"index":0,"derivative":[0.]}
    d=np.gradient(q,p); i=int(np.argmax(np.abs(d))); return {"parameter":float(p[i]),"index":i,"derivative":d.tolist(),"magnitude":float(abs(d[i]))}
def peak_transition(parameters,values):
    p=np.asarray(parameters,float); q=np.asarray(values,float); i=int(np.argmax(q)); return {"parameter":float(p[i]),"index":i,"value":float(q[i])}
def consensus_transitions(candidates,tolerance):
    vals=np.array([c["parameter"] for c in candidates if c.get("parameter") is not None],float)
    if not len(vals):return None
    med=float(np.median(vals)); support=int(np.sum(np.abs(vals-med)<=tolerance)); return {"parameter":med,"support":support,"total":len(vals)}
