"""Focused complex-spectrum pressure test for Eigenflow.

Usage:
    PYTHONPATH=src python benchmarks/complex_spectrum_pressure_test.py [OUTPUT_DIR]
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import sparse

from eigenflow.analyses import AnalysisContext, SpectralAnalysis
from eigenflow.analyses.base import AnalysisResult
from eigenflow.exceptions import ComplexSpectrumAssumptionError
from eigenflow.filtrations.base import GraphSnapshot
from eigenflow.operators import GraphOperator, NonBacktrackingOperator
from eigenflow.result import ExperimentResult, LayerResult
from eigenflow.serialization import load_result_object
from eigenflow.spectra import compare_spectral_snapshots
from eigenflow.visualization import complex_spectrum_plot, spectral_flow, static_spectrum

POLICIES=("auto","preserve","modulus","real","phase","imag","error")


def triangle_snapshots():
    A0=sparse.csr_matrix(np.array([[0,1,1],[1,0,1],[1,1,0]],dtype=float))
    A1=sparse.csr_matrix(np.array([[0,1,1,0],[1,0,1,1],[1,1,0,1],[0,1,1,0]],dtype=float))
    return [
        GraphSnapshot(0.0,A0,1.0),
        GraphSnapshot(1.0,A1,float(A1.nnz/(4*3))),
    ]


class ExpectedRealComplexOperator(GraphOperator):
    name="expected_real_complex_probe"
    spectral_expectation="expected_real"
    def matrix(self,snapshot):
        return np.array([[0.0,-1.0],[1.0,0.0]])


def main(outdir):
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    warnings_log=[]; rows=[]; figures=[]
    ctx=AnalysisContext("pressure_site",None,None,triangle_snapshots(),None)
    for policy in POLICIES:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                ar=SpectralAnalysis(operator=NonBacktrackingOperator(),complex=policy).run(ctx)
                if policy=="error":
                    raise AssertionError("complex='error' should reject genuinely complex non-backtracking spectrum")
                assert ar.metadata["complex_snapshots"] >= 1
                assert any(np.iscomplexobj(np.asarray(r["eigenvalues"])) for r in ar.records if r["eigenvalues"] is not None)
                rows.append({"policy":policy,"status":"ok","complex_snapshots":ar.metadata["complex_snapshots"]})
                layer=LayerResult("pressure_site","synthetic","synthetic",{"spectra":ar})
                for name,fn in (("static",static_spectrum),("complex_plane",complex_spectrum_plot),("flow",spectral_flow)):
                    fig=fn(layer); path=outdir/f"{policy}_{name}.png"; fig.savefig(path,dpi=100); plt.close(fig); figures.append(path.name)
                result=ExperimentResult({"pressure_site":layer},{"pressure_test":True,"policy":policy})
                save_dir=outdir/f"saved_{policy}"; result.save(save_dir)
                loaded=load_result_object(save_dir)
                ltraj=loaded.layers["pressure_site"].analyses["spectra"].observables["trajectory"]
                assert np.iscomplexobj(np.asarray(ltraj.snapshots[0].eigenvalues))
                assert ltraj.snapshots[0].eigenvectors is not None
            except ComplexSpectrumAssumptionError:
                if policy!="error": raise
                rows.append({"policy":policy,"status":"expected_error"})
            for w in caught:
                warnings_log.append({
                    "policy":policy,
                    "category":w.category.__name__,
                    "message":str(w.message),
                    "filename":str(w.filename),
                    "lineno":int(w.lineno),
                })

    # Expected-real surprise path: must warn and preserve rather than coerce.
    simple_ctx=AnalysisContext("expected_real_site",None,None,[GraphSnapshot(0.0,sparse.identity(2,format="csr"),0.0)],None)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        ar=SpectralAnalysis(operator=ExpectedRealComplexOperator(),complex="auto").run(simple_ctx)
        assert ar.metadata["unexpected_complex_snapshots"] == 1
        assert np.iscomplexobj(np.asarray(ar.records[0]["eigenvalues"]))
        for w in caught:
            warnings_log.append({"policy":"expected_real_auto","category":w.category.__name__,"message":str(w.message),"filename":str(w.filename),"lineno":int(w.lineno)})

    # Policy comparison must reject unlike scalar semantics but permit raw complex comparison.
    mod=SpectralAnalysis(operator=NonBacktrackingOperator(),complex="modulus").run(ctx).observables["trajectory"].snapshots[0]
    real=SpectralAnalysis(operator=NonBacktrackingOperator(),complex="real").run(ctx).observables["trajectory"].snapshots[0]
    scalar_cmp=compare_spectral_snapshots(mod,real,"policy")
    raw_cmp=compare_spectral_snapshots(mod,real,"complex")
    assert scalar_cmp["status"] == "incompatible"
    assert raw_cmp["status"] == "ok"

    # No uncontrolled numerical failures in successful records.
    for policy in ("preserve","modulus","real","phase","imag"):
        ar=SpectralAnalysis(operator=NonBacktrackingOperator(),complex=policy).run(ctx)
        for r in ar.records:
            eig=np.asarray(r["eigenvalues"],dtype=complex)
            assert np.isfinite(eig.real).all() and np.isfinite(eig.imag).all()

    report={
        "status":"passed",
        "policies":rows,
        "warnings":warnings_log,
        "figure_count":len(figures),
        "figures":figures,
        "comparison":{"scalar":scalar_cmp,"raw_complex":raw_cmp},
        "assertions":{
            "all_policies_terminal":True,
            "complex_preserved":True,
            "expected_real_violation_surfaced":True,
            "complex_persistence_roundtrip":True,
            "visualizations_rendered":True,
            "policy_mismatch_structured":True,
            "no_nonfinite_eigenvalues":True,
        },
    }
    (outdir/"complex_pressure_report.json").write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else "complex_pressure_evidence")
