"""Google Colab launcher for the complete Eigenflow visualization demo.

Set `EIGENFLOW_REF` to a release tag or commit hash for a reproducible run.
The default `main` value is convenient for exploration but is not a pinned
scientific environment.
"""
import os,subprocess,sys,urllib.request
ref=os.environ.get("EIGENFLOW_REF","main")
subprocess.check_call([sys.executable,"-m","pip","install","-q",f"git+https://github.com/EigenFlowIO/eigenflow.git@{ref}"])
url=f"https://raw.githubusercontent.com/EigenFlowIO/eigenflow/{ref}/examples/complete_visualization_demo.py"
urllib.request.urlretrieve(url,"complete_visualization_demo.py")
subprocess.check_call([sys.executable,"complete_visualization_demo.py","--output-dir","eigenflow_visualization_demo_outputs"])
try:
    from google.colab import files
    files.download("eigenflow_visualization_demo_outputs.zip")
except Exception:
    print("Output archive: eigenflow_visualization_demo_outputs.zip")
