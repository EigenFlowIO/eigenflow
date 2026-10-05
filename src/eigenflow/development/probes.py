from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping
import json
from .specs import probe_fingerprint


@dataclass
class ProbeSuite:
    """Versioned collection of probe populations assigned experimental roles."""
    populations: dict[str, Any]
    name: str = "probe_suite"
    version: str = "1"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.populations:
            raise ValueError("ProbeSuite requires at least one population")
        if len(set(self.populations)) != len(self.populations):
            raise ValueError("ProbeSuite role names must be unique")

    def __getitem__(self, role: str):
        return self.populations[role]

    @property
    def roles(self):
        return list(self.populations)

    @property
    def fingerprint(self) -> str:
        payload = {
            "name": self.name,
            "version": self.version,
            "roles": {k: probe_fingerprint(v) for k, v in sorted(self.populations.items())},
            "metadata": self.metadata,
        }
        return sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()

    def manifest(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "fingerprint": self.fingerprint,
            "metadata": self.metadata,
            "populations": {
                role: {
                    "name": pop.name,
                    "count": len(pop.samples),
                    "fingerprint": probe_fingerprint(pop),
                    "ids": pop.ids,
                    "metadata": pop.metadata,
                    "design": pop.design,
                }
                for role, pop in self.populations.items()
            },
        }

    def save_manifest(self, path):
        p = Path(path)
        if p.suffix:
            p.parent.mkdir(parents=True, exist_ok=True)
            target = p
        else:
            p.mkdir(parents=True, exist_ok=True)
            target = p / "probe_suite.json"
        target.write_text(json.dumps(self.manifest(), indent=2, default=str))
        return target
