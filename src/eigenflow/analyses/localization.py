from .standard import SpectralAnalysis

class LocalizationAnalysis(SpectralAnalysis):
    name="localization"
    def run(self,ctx):
        out=super().run(ctx); out.name=self.name
        out.observables={"trajectory":out.observables["trajectory"],"ipr":[r["ipr"] for r in out.records]}
        return out
