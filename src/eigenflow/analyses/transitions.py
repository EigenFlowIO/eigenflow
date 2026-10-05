import numpy as np
from .base import Analysis, AnalysisResult
from ..graphs import component_labels
from ..percolation import percolation_observables
from ..transitions import derivative_transition, peak_transition, consensus_transitions

class TransitionsAnalysis(Analysis):
    name="transitions"
    def run(self,ctx):
        p=ctx.filtration.parameters
        counts=[]; chi=[]; second=[]
        for s in ctx.filtration:
            counts.append(component_labels(s)[0])
            o=percolation_observables(s); chi.append(o["susceptibility"]); second.append(o["second_component_fraction"])
        candidates=[]
        if len(p):
            candidates.append({"name":"component_derivative",**derivative_transition(p,counts)})
            candidates.append({"name":"susceptibility_peak",**peak_transition(p,chi)})
            candidates.append({"name":"second_component_peak",**peak_transition(p,second)})
        span=float(np.ptp(p)) if len(p)>1 else 0.0
        consensus=consensus_transitions(candidates,max(span*0.05,1e-12)) if candidates else None
        return AnalysisResult(self.name,observables={"candidates":candidates,"consensus":consensus},records=[])
