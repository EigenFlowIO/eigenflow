from __future__ import annotations
import numpy as np
import networkx as nx
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from .base import Analysis,AnalysisResult
from ..graphs import component_labels,component_sizes,bridge_edges,kcore_nodes,communities,degree_array
from ..percolation import percolation_observables
from ..operators import resolve_operator
from ..exceptions import OperatorCompatibilityError
from ..spectra import solve_spectrum,ipr,spectral_entropy,effective_rank,graph_energy,spectral_gaps,SpectralSnapshot,SpectralTrajectory,eigenspace_overlap,principal_angle_values

class ComponentsAnalysis(Analysis):
    name="components"
    def run(self,ctx):
        rec=[]
        for s in ctx.filtration:
            ncomp,labels=component_labels(s); sizes=np.bincount(labels)
            rec.append({"parameter":s.parameter,"edge_density":s.edge_density,"component_count":int(ncomp),"largest_component":int(sizes.max()),"labels":labels.tolist()})
        return AnalysisResult(self.name,observables={"component_count":[r["component_count"] for r in rec]},records=rec)

class PCSCSAnalysis(ComponentsAnalysis):
    name="pcscs"
    def run(self,ctx):
        base=super().run(ctx); counts=np.array(base.observables["component_count"],float); p=ctx.filtration.parameters
        deriv=np.gradient(counts,p) if len(p)>1 else np.array([0.])
        idx=int(np.argmax(np.abs(deriv)))
        convergence=None
        for r in base.records:
            if r["component_count"]==1: convergence=r["parameter"]; break
        base.name=self.name; base.observables.update({"critical_parameter":float(p[idx]),"component_derivative":deriv.tolist(),"convergence_parameter":None if convergence is None else float(convergence)})
        return base

class PercolationAnalysis(Analysis):
    name="percolation"
    def run(self,ctx):
        rec=[]
        for s in ctx.filtration: rec.append({"parameter":s.parameter,"edge_density":s.edge_density,**percolation_observables(s)})
        obs={k:[r[k] for r in rec] for k in ["giant_component_fraction","second_component_fraction","susceptibility"]}
        if rec: obs["susceptibility_peak_parameter"]=float(rec[int(np.argmax(obs["susceptibility"]))]["parameter"])
        return AnalysisResult(self.name,obs,rec)

class SpectralAnalysis(Analysis):
    name="spectra"
    def __init__(self,operator="normalized_laplacian",k=None,vectors=True):
        self.operator=resolve_operator(operator); self.k=k; self.vectors=vectors
    def run(self,ctx):
        snaps=[]; rec=[]; incompatible=0
        for s in ctx.filtration:
            try:
                M=self.operator.matrix(s)
                vals,vecs=solve_spectrum(M,k=self.k,vectors=self.vectors)
                o={"status":"ok","spectral_radius":float(np.max(np.abs(vals))) if len(vals) else 0.,"spectral_entropy":spectral_entropy(vals),"effective_rank":effective_rank(vals),"energy":graph_energy(vals),"gaps":spectral_gaps(vals).tolist(),"ipr":ipr(vecs).tolist() if vecs is not None else None}
                if self.operator.name in {"laplacian","normalized_laplacian","signed_laplacian","signed_normalized_laplacian"}:
                    o["algebraic_connectivity"]=float(vals[1]) if len(vals)>1 else 0.
                snaps.append(SpectralSnapshot(s.parameter,vals,vecs,self.operator.name,o))
                rec.append({"parameter":s.parameter,**o,"eigenvalues":vals.tolist()})
            except OperatorCompatibilityError as exc:
                incompatible += 1
                o=exc.as_dict()
                o.update({"spectral_radius":None,"spectral_entropy":None,"effective_rank":None,"energy":None,"gaps":None,"ipr":None})
                snaps.append(SpectralSnapshot(s.parameter,np.array([]),None,self.operator.name,o))
                rec.append({"parameter":s.parameter,**o,"eigenvalues":None})
        return AnalysisResult(
            self.name,
            {"trajectory":SpectralTrajectory(snaps,self.operator.name)},
            rec,
            {"operator":self.operator.name,"operator_space":getattr(self.operator,"space","node"),"incompatible_snapshots":incompatible},
        )

class EigenspaceAnalysis(Analysis):
    name="eigenspaces"
    def __init__(self,operator="normalized_laplacian",dimensions=3):
        self.operator=resolve_operator(operator); self.dimensions=dimensions
    def run(self,ctx):
        prev=None; rec=[]; incompatible=0
        for s in ctx.filtration:
            try:
                M=self.operator.matrix(s)
                vals,V=solve_spectrum(M,vectors=True)
            except OperatorCompatibilityError as exc:
                incompatible += 1
                rec.append({
                    "parameter":s.parameter,
                    "overlap":None,
                    "principal_angles":None,
                    "ambient_dimension":None,
                    **exc.as_dict(),
                })
                prev=None
                continue

            d=min(self.dimensions,V.shape[1] if V is not None else 0)
            cur=V[:,:d] if d else None
            row={
                "parameter":s.parameter,
                "overlap":None,
                "principal_angles":None,
                "ambient_dimension":None if cur is None else int(cur.shape[0]),
                "status":"ok",
            }
            if prev is not None and cur is not None:
                if prev.shape[0] != cur.shape[0]:
                    incompatible += 1
                    row.update({
                        "status":"incompatible",
                        "reason":"changing_ambient_space",
                        "message":(
                            f"Cannot compare consecutive {self.operator.name} eigenspaces "
                            f"with ambient dimensions {prev.shape[0]} and {cur.shape[0]}."
                        ),
                        "previous_ambient_dimension":int(prev.shape[0]),
                        "current_ambient_dimension":int(cur.shape[0]),
                        "operator_space":getattr(self.operator,"space","node"),
                    })
                else:
                    row["overlap"]=eigenspace_overlap(prev,cur).tolist()
                    row["principal_angles"]=principal_angle_values(prev,cur).tolist()
            rec.append(row)
            prev=cur
        return AnalysisResult(
            self.name,
            records=rec,
            metadata={
                "operator":self.operator.name,
                "operator_space":getattr(self.operator,"space","node"),
                "dimensions":self.dimensions,
                "incompatible_comparisons":incompatible,
            },
        )

class BridgesAnalysis(Analysis):
    name="bridges"
    def run(self,ctx): return AnalysisResult(self.name,records=[{"parameter":s.parameter,"bridges":bridge_edges(s)} for s in ctx.filtration])
class KCoreAnalysis(Analysis):
    name="kcore"
    def __init__(self,k=2): self.k=k
    def run(self,ctx): return AnalysisResult(self.name,records=[{"parameter":s.parameter,"k":self.k,"nodes":kcore_nodes(s,self.k),"fraction":len(kcore_nodes(s,self.k))/s.n} for s in ctx.filtration])
class CommunitiesAnalysis(Analysis):
    name="communities"
    def run(self,ctx): return AnalysisResult(self.name,records=[{"parameter":s.parameter,"communities":communities(s)} for s in ctx.filtration])

class FactorAlignmentAnalysis(Analysis):
    name="factor_alignment"
    def __init__(self,factors=None): self.factors=factors
    def run(self,ctx):
        factors=self.factors or sorted(set().union(*(m.keys() for m in ctx.probes.metadata)))
        rec=[]
        for s in ctx.filtration:
            _,labels=component_labels(s); row={"parameter":s.parameter}
            for f in factors:
                y=ctx.probes.values(f)
                if any(v is None for v in y): continue
                row[f]={"nmi":float(normalized_mutual_info_score(y,labels)),"ari":float(adjusted_rand_score(y,labels))}
            rec.append(row)
        return AnalysisResult(self.name,records=rec,metadata={"factors":factors})

class ClassStructureAnalysis(Analysis):
    name="class_structure"
    def __init__(self,factor="class"): self.factor=factor
    def run(self,ctx):
        y=ctx.probes.values(self.factor); groups={}
        for i,v in enumerate(y): groups.setdefault(v,[]).append(i)
        rec=[]
        for s in ctx.filtration:
            A=s.adjacency; row={"parameter":s.parameter,"classes":{}}
            for c,idx in groups.items():
                sub=A[idx][:,idx]; n=len(idx); possible=n*(n-1); internal=float(sub.nnz/possible) if possible else 0.
                outside=[i for i in range(s.n) if i not in set(idx)]; cross=A[idx][:,outside].nnz if outside else 0; cross_possible=len(idx)*len(outside)
                row["classes"][str(c)]={"internal_density":internal,"external_density":float(cross/cross_possible) if cross_possible else 0.}
            rec.append(row)
        return AnalysisResult(self.name,records=rec,metadata={"factor":self.factor})

ANALYSIS_REGISTRY={c.name:c for c in [ComponentsAnalysis,PCSCSAnalysis,PercolationAnalysis,SpectralAnalysis,EigenspaceAnalysis,BridgesAnalysis,KCoreAnalysis,CommunitiesAnalysis,FactorAlignmentAnalysis,ClassStructureAnalysis]}
def resolve_analysis(a):
    if isinstance(a,Analysis): return a
    if isinstance(a,str) and a in ANALYSIS_REGISTRY: return ANALYSIS_REGISTRY[a]()
    raise ValueError(f"Unknown analysis {a!r}")
