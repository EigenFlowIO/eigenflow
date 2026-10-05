from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping
import numpy as np
from .specs import ExperimentSpec, ComparisonSpec, CompatibilityReport, SiteAlignment, validate_compatibility


def _numeric(value):
    if isinstance(value, (int, float, np.number)):
        return np.asarray(value, dtype=float)
    if isinstance(value, np.ndarray) and np.issubdtype(value.dtype, np.number):
        return value.astype(float)
    if isinstance(value, (list, tuple)):
        try:
            arr = np.asarray(value, dtype=float)
            return arr if arr.dtype != object else None
        except (TypeError, ValueError):
            return None
    return None


def _observable(result, site, analysis, observable):
    ar = result.layers[site].analyses[analysis]
    value = ar.observables.get(observable)
    if value is None and ar.records and observable in ar.records[0]:
        value = [r.get(observable) for r in ar.records]
    return value


def _parameters(result, site, analysis):
    ar = result.layers[site].analyses[analysis]
    return np.asarray([r.get("parameter", i) for i, r in enumerate(ar.records)], dtype=float)


@dataclass
class BehavioralRecord:
    metrics: dict[str, float] = field(default_factory=dict)
    efficiency: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SeriesEntry:
    key: str
    result: Any
    spec: ExperimentSpec
    time: float | int | None = None
    checkpoint: str | None = None
    model: str | None = None
    architecture: str | None = None
    condition: str | None = None
    run: str | None = None
    behavior: BehavioralRecord | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class StructuralDiff:
    left_key: str
    right_key: str
    site_mapping: dict[str, str]
    differences: dict[str, Any]
    compatibility: CompatibilityReport
    skipped: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def between(cls, left: SeriesEntry, right: SeriesEntry, comparison: ComparisonSpec | None = None, site_alignment: SiteAlignment | None = None):
        comparison = comparison or ComparisonSpec()
        report = validate_compatibility(left.spec, right.spec, comparison)
        if not report.compatible:
            fields = ", ".join(i.field for i in report.errors)
            raise ValueError(f"Results are not structurally comparable; incompatible fields: {fields}")
        alignment = site_alignment or SiteAlignment.exact(left.result.layers, right.result.layers)
        if not alignment.mapping:
            raise ValueError("No aligned sites available for structural comparison")
        diffs = {}; skipped = []
        for ls, rs in alignment.mapping.items():
            if ls not in left.result.layers or rs not in right.result.layers:
                skipped.append({"site": ls, "reason": "site missing"}); continue
            l_layer, r_layer = left.result.layers[ls], right.result.layers[rs]
            common_analyses = sorted(set(l_layer.analyses) & set(r_layer.analyses))
            site_out = {}
            for an in common_analyses:
                la, ra = l_layer.analyses[an], r_layer.analyses[an]
                common_obs = sorted(set(la.observables) & set(ra.observables))
                obs_out = {}
                for ob in common_obs:
                    larr, rarr = _numeric(la.observables[ob]), _numeric(ra.observables[ob])
                    if larr is None or rarr is None or larr.shape != rarr.shape:
                        skipped.append({"site": ls, "analysis": an, "observable": ob, "reason": "non-numeric or shape mismatch"})
                        continue
                    delta = rarr - larr
                    obs_out[ob] = {
                        "left": larr,
                        "right": rarr,
                        "difference": delta,
                        "mean_absolute_difference": float(np.mean(np.abs(delta))),
                        "max_absolute_difference": float(np.max(np.abs(delta))) if delta.size else 0.0,
                    }
                if obs_out:
                    site_out[an] = obs_out
            if site_out:
                diffs[ls] = site_out
        return cls(left.key, right.key, dict(alignment.mapping), diffs, report, skipped)


@dataclass
class LongitudinalResult:
    entries: list[SeriesEntry]
    baseline_key: str | None = None
    comparison: ComparisonSpec = field(default_factory=ComparisonSpec)

    @property
    def keys(self): return [e.key for e in self.entries]
    @property
    def times(self):
        return np.asarray([i if e.time is None else e.time for i, e in enumerate(self.entries)], dtype=float)

    def entry(self, key):
        return next(e for e in self.entries if e.key == key)

    @property
    def baseline(self):
        return self.entry(self.baseline_key) if self.baseline_key else self.entries[0]

    def trajectory(self, site: str, analysis: str, observable: str):
        values = []
        for e in self.entries:
            if site not in e.result.layers:
                raise KeyError(f"Site {site!r} missing from series entry {e.key!r}")
            arr = _numeric(_observable(e.result, site, analysis, observable))
            if arr is None:
                raise TypeError(f"Observable {analysis}.{observable} is not a numeric scalar/array")
            values.append(arr)
        shape = values[0].shape
        if any(v.shape != shape for v in values[1:]):
            raise ValueError("Observable shape changes across series; align control coordinates before trajectory analysis")
        return np.stack(values, axis=0)

    def baseline_delta(self, site: str, analysis: str, observable: str):
        data = self.trajectory(site, analysis, observable)
        bidx = self.keys.index(self.baseline.key)
        return data - data[bidx]

    def structural_diffs(self, site_alignment: SiteAlignment | None = None):
        base = self.baseline
        return [StructuralDiff.between(base, e, self.comparison, site_alignment) for e in self.entries if e.key != base.key]


@dataclass
class ExperimentSeries:
    name: str = "experiment_series"
    entries: list[SeriesEntry] = field(default_factory=list)
    comparison: ComparisonSpec = field(default_factory=ComparisonSpec)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __len__(self): return len(self.entries)
    def __iter__(self): return iter(self.entries)
    def __getitem__(self, key):
        if isinstance(key, int): return self.entries[key]
        return next(e for e in self.entries if e.key == key)

    def add_result(self, key: str, result, spec: ExperimentSpec | None = None, **attrs):
        if any(e.key == key for e in self.entries):
            raise ValueError(f"Duplicate series key {key!r}")
        if spec is None:
            raw = result.metadata.get("experiment_spec") if hasattr(result, "metadata") else None
            if raw is None:
                raise ValueError("ExperimentResult does not contain experiment_spec metadata; pass spec explicitly")
            spec = ExperimentSpec.from_dict(raw)
        entry = SeriesEntry(key=key, result=result, spec=spec, **attrs)
        if self.entries:
            report = validate_compatibility(self.entries[0].spec, spec, self.comparison)
            if not report.compatible:
                fields = ", ".join(i.field for i in report.errors)
                raise ValueError(f"Series entry {key!r} is incompatible with baseline on: {fields}")
        self.entries.append(entry)
        return entry

    def add_experiment(self, key: str, experiment, **attrs):
        spec = ExperimentSpec.from_experiment(experiment)
        return self.add_result(key, experiment.run(), spec=spec, **attrs)

    def compatibility_matrix(self):
        out = {}
        for i, a in enumerate(self.entries):
            for j, b in enumerate(self.entries):
                if j <= i: continue
                out[(a.key, b.key)] = validate_compatibility(a.spec, b.spec, self.comparison)
        return out

    def longitudinal(self, baseline: str | None = None):
        if not self.entries:
            raise ValueError("ExperimentSeries is empty")
        return LongitudinalResult(list(self.entries), baseline or self.entries[0].key, self.comparison)

    @classmethod
    def run_checkpoints(cls, checkpoints: Iterable[Any], model_loader, experiment_factory, *, name="checkpoint_series", key_fn=None, time_fn=None, comparison=None):
        series = cls(name=name, comparison=comparison or ComparisonSpec())
        for i, checkpoint in enumerate(checkpoints):
            model = model_loader(checkpoint)
            experiment = experiment_factory(model, checkpoint)
            key = str(key_fn(checkpoint) if key_fn else checkpoint)
            t = time_fn(checkpoint) if time_fn else i
            series.add_experiment(key, experiment, time=t, checkpoint=str(checkpoint))
        return series
