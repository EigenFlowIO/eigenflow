"""Google Colab launcher for the complete Eigenflow development demo.

After the development-instrumentation phase is present on the selected repository
revision, this script installs Eigenflow, runs the complete demo, and downloads the
result ZIP when executed inside Colab.
"""
from pathlib import Path
import subprocess,sys,shutil

REPO="https://github.com/EigenFlowIO/eigenflow.git"
REF="main"  # replace with a release tag or commit for archival reproduction
ROOT=Path("/content/eigenflow-development-demo")
if ROOT.exists(): shutil.rmtree(ROOT)
subprocess.run(["git","clone",REPO,str(ROOT)],check=True)
subprocess.run(["git","-C",str(ROOT),"checkout",REF],check=True)
subprocess.run([sys.executable,"-m","pip","install","-q","-e",str(ROOT)],check=True)
subprocess.run([sys.executable,str(ROOT/"examples"/"complete_development_demo.py")],cwd=ROOT,check=True)
zip_path=ROOT/"eigenflow_development_demo_outputs.zip"
print("Created",zip_path)
try:
    from google.colab import files
    files.download(str(zip_path))
except Exception:
    pass
