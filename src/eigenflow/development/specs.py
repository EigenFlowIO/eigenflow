from __future__ import annotations
from dataclasses import dataclass, field, asdict, is_dataclass
from hashlib import sha256
from typing import Any, Mapping, Sequence
import json


def _simple(value: Any):
    if is_dataclass(value):
        return {k: _simple(v) for k, v in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(k): _simple(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_simple(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "name"):
        d = {"name": str(getattr(value, "name"))}
        if hasattr(value, "__dict__"):
            d.update({k: _simple(v) for k, v in vars(value).items() if not k.startswith("_") and k != "name"})
        return d
    return str(value)


def _analysis_spec(a: Any) -> dict[str, Any]:
    if isinstance(a, str):
        return {"name": a}
    name = getattr(a, "name", a.__class__.__name__)
    out = {"name": str(name)}
    if hasattr(a, "__dict__"):
        out["config"] = {k: _simple(v) for k, v in vars(a).items() if not k.startswith("_")}
    return out


def probe_fingerprint(probes) -> str:
    payload = {
        "name": probes.name,
        "ids": list(probes.ids),
        "metadata": probes.metadata,
        "design": _simple(getattr(probes, "design", {})),
    }
    raw = json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


@dataclass(frozen=True)
class ExperimentSpec:
    """Serializable description of the measurement contract of an experiment.

    The spec deliberately excludes the model object itself. It describes the probe
    population and measurement choices that must be controlled for a structural
    comparison to be meaningful.
    """
    probe_fingerprint: str
    probe_name: str
    probe_count: int
    probe_design: dict[str, Any] = field(default_factory=dict)
    sites: Any = "all"
    reducer: Any = "flatten"
    batch_size: int = 32
    metric: Any = "cosine"
    filtration: Any = "edge_density"
    analyses: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    preprocessing: Any = None
    measurement_metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_experiment(cls, experiment) -> "ExperimentSpec":
        ex = experiment.extraction
        return cls(
            probe_fingerprint=probe_fingerprint(experiment.probes),
            probe_name=experiment.probes.name,
            probe_count=len(experiment.probes.samples),
            probe_design=_simple(experiment.probes.design),
            sites=_simple(ex.sites),
            reducer=_simple(ex.reducer),
            batch_size=int(ex.batch_size),
            metric=_simple(experiment.metric),
            filtration=_simple(experiment.filtration),
            analyses=tuple(_analysis_spec(a) for a in experiment.analyses),
            preprocessing=_simple(getattr(experiment, "preprocessing", None)),
            measurement_metadata=_simple(getattr(experiment, "measurement_metadata", {})),
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ExperimentSpec":
        d = dict(data)
        d["analyses"] = tuple(d.get("analyses", ()))
        return cls(**d)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["analyses"] = list(self.analyses)
        return d

    @property
    def fingerprint(self) -> str:
        raw = json.dumps(self.to_dict(), sort_keys=True, default=str, separators=(",", ":")).encode()
        return sha256(raw).hexdigest()


@dataclass(frozen=True)
class ComparisonSpec:
    """Contract declaring which dimensions may vary in a comparison."""
    vary: tuple[str, ...] = ("model", "checkpoint", "time", "condition", "architecture", "run")
    require_same: tuple[str, ...] = (
        "probe_fingerprint", "sites", "reducer", "metric", "filtration", "analyses", "preprocessing"
    )
    allow_site_alignment: bool = False
    notes: str | None = None


@dataclass(frozen=True)
class CompatibilityIssue:
    field: str
    left: Any
    right: Any
    severity: str
    message: str


@dataclass
class CompatibilityReport:
    compatible: bool
    issues: list[CompatibilityIssue] = field(default_factory=list)
    controlled_differences: list[CompatibilityIssue] = field(default_factory=list)
    comparison_spec: ComparisonSpec = field(default_factory=ComparisonSpec)

    @property
    def errors(self):
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self):
        return [i for i in self.issues if i.severity == "warning"]

    def to_dict(self):
        return {
            "compatible": self.compatible,
            "issues": [asdict(i) for i in self.issues],
            "controlled_differences": [asdict(i) for i in self.controlled_differences],
            "comparison_spec": asdict(self.comparison_spec),
        }


def validate_compatibility(left: ExperimentSpec, right: ExperimentSpec, spec: ComparisonSpec | None = None) -> CompatibilityReport:
    spec = spec or ComparisonSpec()
    issues: list[CompatibilityIssue] = []
    controlled: list[CompatibilityIssue] = []
    l = left.to_dict(); r = right.to_dict()
    for field_name in spec.require_same:
        lv, rv = l.get(field_name), r.get(field_name)
        if lv != rv:
            severity = "warning" if field_name == "sites" and spec.allow_site_alignment else "error"
            issues.append(CompatibilityIssue(
                field_name, lv, rv, severity,
                f"Measurement field {field_name!r} differs between results."
            ))
    # Record all non-required differences to make intentional variation inspectable.
    for field_name in sorted(set(l) | set(r)):
        if field_name in spec.require_same:
            continue
        lv, rv = l.get(field_name), r.get(field_name)
        if lv != rv:
            controlled.append(CompatibilityIssue(field_name, lv, rv, "info", f"Controlled/declared difference in {field_name!r}."))
    return CompatibilityReport(not any(i.severity == "error" for i in issues), issues, controlled, spec)


@dataclass(frozen=True)
class SiteAlignment:
    """Explicit correspondence between sites in two results."""
    mapping: dict[str, str]
    strategy: str = "declared"
    notes: str | None = None

    @classmethod
    def exact(cls, left_sites: Sequence[str], right_sites: Sequence[str]) -> "SiteAlignment":
        common = [s for s in left_sites if s in set(right_sites)]
        return cls({s: s for s in common}, strategy="exact_name")

    @classmethod
    def normalized_depth(cls, left_sites: Sequence[str], right_sites: Sequence[str]) -> "SiteAlignment":
        left = list(left_sites); right = list(right_sites)
        if not left or not right:
            return cls({}, strategy="normalized_depth")
        mapping = {}
        for i, s in enumerate(left):
            t = 0.0 if len(left) == 1 else i / (len(left) - 1)
            j = round(t * (len(right) - 1))
            mapping[s] = right[j]
        return cls(mapping, strategy="normalized_depth", notes="Index-based normalized-depth alignment is approximate, not semantic equivalence.")
