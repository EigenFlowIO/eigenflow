from .base import Analysis,AnalysisResult,AnalysisContext
from .standard import *

from .transitions import TransitionsAnalysis
from .localization import LocalizationAnalysis

_BASE_RESOLVE = resolve_analysis
def resolve_analysis(a):
    if isinstance(a, Analysis): return a
    if a == "transitions": return TransitionsAnalysis()
    if a == "localization": return LocalizationAnalysis()
    return _BASE_RESOLVE(a)
