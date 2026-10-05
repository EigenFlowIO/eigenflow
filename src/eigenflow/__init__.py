"""Eigenflow: multiscale relational interpretability for neural-network probe populations."""
__version__="1.0.0a1"
from .experiment import Experiment
from .result import ExperimentResult,LayerResult,LayerArtifacts,ExperimentArtifacts
from .probes import ProbePopulation,ProbeSample
from .extraction import ExtractionConfig,PyTorchExtractor
from . import metrics,filtrations,analyses,operators,spectra,percolation,transitions,visualization,presets
__all__=["Experiment","ExperimentResult","LayerResult","LayerArtifacts","ExperimentArtifacts","ProbePopulation","ProbeSample","ExtractionConfig","PyTorchExtractor","metrics","filtrations","analyses","operators","spectra","percolation","transitions","visualization","presets"]
