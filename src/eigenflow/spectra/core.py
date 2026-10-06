from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh, eigs
from scipy.linalg import subspace_angles
from scipy.optimize import linear_sum_assignment

VALID_COMPLEX_POLICIES = {"auto", "preserve", "modulus", "real", "phase", "imag", "error"}
DEFAULT_COMPLEX_ATOL = 1e-10
DEFAULT_COMPLEX_RTOL = 1e-8


@dataclass
class SpectralSnapshot:
    parameter: float
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray | None
    operator: str
    observables: dict = field(default_factory=dict)
    complex_policy: str = "auto"

    @property
    def real(self):
        return np.real(self.eigenvalues)

    @property
    def imag(self):
        return np.imag(self.eigenvalues)

    @property
    def modulus(self):
        return np.abs(self.eigenvalues)

    @property
    def phase(self):
        return np.angle(self.eigenvalues)


@dataclass
class SpectralTrajectory:
    snapshots: list[SpectralSnapshot]
    operator: str

    @property
    def parameters(self):
        return np.array([s.parameter for s in self.snapshots])


def validate_complex_policy(policy: str) -> str:
    if policy not in VALID_COMPLEX_POLICIES:
        raise ValueError(
            f"Unknown complex-spectrum policy {policy!r}; expected one of "
            f"{sorted(VALID_COMPLEX_POLICIES)}"
        )
    return policy


def complex_mask(vals, atol=DEFAULT_COMPLEX_ATOL, rtol=DEFAULT_COMPLEX_RTOL):
    vals = np.asarray(vals)
    if vals.size == 0:
        return np.zeros(vals.shape, dtype=bool)
    threshold = float(atol) + float(rtol) * np.abs(vals)
    return np.abs(np.imag(vals)) > threshold


def characterize_spectrum(vals, atol=DEFAULT_COMPLEX_ATOL, rtol=DEFAULT_COMPLEX_RTOL):
    vals = np.asarray(vals)
    mask = complex_mask(vals, atol=atol, rtol=rtol)
    n = int(vals.size)
    count = int(np.count_nonzero(mask))
    max_abs_imag = float(np.max(np.abs(np.imag(vals)))) if n else 0.0
    scale = float(np.max(np.maximum(1.0, np.abs(vals)))) if n else 1.0
    max_relative_imag = max_abs_imag / scale
    return {
        "complex_detected": bool(count),
        "complex_count": count,
        "complex_fraction": float(count / n) if n else 0.0,
        "max_abs_imag": max_abs_imag,
        "max_relative_imag": float(max_relative_imag),
        "complex_tolerance_abs": float(atol),
        "complex_tolerance_rel": float(rtol),
    }


def project_eigenvalues(vals, policy="auto", *, atol=DEFAULT_COMPLEX_ATOL, rtol=DEFAULT_COMPLEX_RTOL):
    """Return a scalar coordinate for an eigenvalue spectrum.

    ``auto`` behaves like ``real`` only when the spectrum is effectively real.
    ``auto`` and ``preserve`` return ``None`` for genuinely complex spectra,
    forcing callers to avoid inventing a scalar ordering.
    """
    policy = validate_complex_policy(policy)
    vals = np.asarray(vals)
    info = characterize_spectrum(vals, atol=atol, rtol=rtol)
    if policy == "error" and info["complex_detected"]:
        raise ValueError("Complex eigenvalues encountered under complex='error'.")
    if policy in {"auto", "preserve"}:
        if info["complex_detected"]:
            return None
        return np.real(vals)
    if policy == "modulus":
        return np.abs(vals)
    if policy == "real":
        return np.real(vals)
    if policy == "imag":
        return np.imag(vals)
    if policy == "phase":
        return np.angle(vals)
    raise AssertionError(policy)


def solve_spectrum(M, k=None, vectors=True, which=None):
    n = M.shape[0]
    if n == 0:
        return np.array([]), None
    symmetric = (
        (M - M.T.conjugate()).nnz == 0
        if sparse.issparse(M)
        else np.allclose(M, np.asarray(M).T.conjugate())
    )
    if n <= 128 or k is None or k >= n - 1:
        a = M.toarray() if sparse.issparse(M) else np.asarray(M)
        vals, vecs = np.linalg.eigh(a) if symmetric else np.linalg.eig(a)
        order = np.argsort(vals.real) if symmetric else np.argsort(np.abs(vals))
        vals = vals[order]
        vecs = vecs[:, order]
    else:
        kk = min(k, n - 2)
        if symmetric:
            which = which or "SM"
            vals, vecs = eigsh(M, k=kk, which=which)
            order = np.argsort(vals)
        else:
            # For a nonsymmetric operator, preserve complex eigenpairs.  Sparse
            # eigs uses magnitude-oriented selectors such as LM/SM rather than
            # the Hermitian-only eigsh path.
            which = which or "LM"
            vals, vecs = eigs(M, k=kk, which=which)
            order = np.argsort(np.abs(vals))
        vals = vals[order]
        vecs = vecs[:, order]
    return vals, (vecs if vectors else None)


def ipr(vecs):
    arr = np.asarray(vecs)
    return np.sum(np.abs(arr) ** 4, axis=0)


def spectral_entropy(vals):
    a = np.abs(vals)
    s = a.sum()
    if s == 0:
        return 0.0
    p = a / s
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


def effective_rank(vals):
    return float(np.exp(spectral_entropy(vals)))


def graph_energy(vals):
    return float(np.abs(vals).sum())


def spectral_gaps(vals, policy="auto", *, atol=DEFAULT_COMPLEX_ATOL, rtol=DEFAULT_COMPLEX_RTOL):
    projected = project_eigenvalues(vals, policy, atol=atol, rtol=rtol)
    if projected is None:
        return None
    projected = np.asarray(projected, dtype=float)
    if policy == "phase" and len(projected) > 1:
        ordered = np.sort((projected + 2 * np.pi) % (2 * np.pi))
        return np.diff(np.r_[ordered, ordered[0] + 2 * np.pi])
    return np.diff(np.sort(projected))


def eigenspace_overlap(V, W):
    if V is None or W is None:
        return None
    return np.abs(np.asarray(V).conjugate().T @ np.asarray(W))


def principal_angle_values(V, W):
    return subspace_angles(V, W)


def match_eigenvalues(previous, current):
    """Minimum-cost matching in the complex plane between two spectra.

    Returns pairs ``(previous_index, current_index)``.  Unequal-size spectra are
    supported; unmatched modes are deliberately left unmatched rather than
    inventing continuity.
    """
    previous = np.asarray(previous, dtype=complex)
    current = np.asarray(current, dtype=complex)
    if previous.size == 0 or current.size == 0:
        return []
    cost = np.abs(previous[:, None] - current[None, :])
    rows, cols = linear_sum_assignment(cost)
    return list(zip(rows.tolist(), cols.tolist()))


def matched_spectral_paths(trajectory: SpectralTrajectory, max_modes=None):
    """Track eigenvalues across snapshots using adjacent complex-plane matching.

    Paths are seeded from the first non-empty snapshot.  Mode births after the
    seed snapshot are not back-filled; this routine is intentionally conservative
    and primarily supports trajectory visualization/comparison.
    """
    snaps = trajectory.snapshots
    if not snaps:
        return np.empty((0, 0), dtype=complex)
    first = next((i for i, s in enumerate(snaps) if len(s.eigenvalues)), None)
    if first is None:
        return np.empty((len(snaps), 0), dtype=complex)
    seed = np.asarray(snaps[first].eigenvalues, dtype=complex)
    m = len(seed) if max_modes is None else min(len(seed), int(max_modes))
    # Prefer largest-modulus modes for a bounded display, but preserve stable
    # identities after seeding through complex-plane matching.
    seed_idx = np.argsort(np.abs(seed))[::-1][:m]
    paths = np.full((len(snaps), m), np.nan + 1j * np.nan, dtype=complex)
    paths[first, :] = seed[seed_idx]
    active_indices = seed_idx.tolist()
    prev_full = seed
    for t in range(first + 1, len(snaps)):
        cur = np.asarray(snaps[t].eigenvalues, dtype=complex)
        if cur.size == 0:
            active_indices = [None] * m
            prev_full = cur
            continue
        pairs = dict(match_eigenvalues(prev_full, cur))
        new_active = []
        for j, prev_idx in enumerate(active_indices):
            cur_idx = pairs.get(prev_idx) if prev_idx is not None else None
            if cur_idx is not None:
                paths[t, j] = cur[cur_idx]
            new_active.append(cur_idx)
        active_indices = new_active
        prev_full = cur
    return paths


def compare_spectral_snapshots(left: SpectralSnapshot, right: SpectralSnapshot, mode="policy"):
    """Compare two spectral snapshots without silently mixing complex semantics.

    ``mode='complex'`` compares matched raw eigenvalues in the complex plane.
    ``mode='policy'`` compares the scalar coordinate selected by each snapshot's
    declared policy and returns a structured incompatibility if those semantics
    differ for genuinely complex spectra.
    """
    if mode not in {"policy", "complex"}:
        raise ValueError("mode must be 'policy' or 'complex'")
    lv=np.asarray(left.eigenvalues,dtype=complex)
    rv=np.asarray(right.eigenvalues,dtype=complex)
    pairs=match_eigenvalues(lv,rv)
    if not pairs:
        return {"status":"ok","mode":mode,"matched_modes":0,"mean_distance":0.0,"max_distance":0.0}
    if mode == "complex":
        d=np.array([abs(lv[i]-rv[j]) for i,j in pairs],dtype=float)
        return {"status":"ok","mode":"complex","matched_modes":len(pairs),"mean_distance":float(d.mean()),"max_distance":float(d.max())}
    lp=_snapshot_policy_for_compare(left)
    rp=_snapshot_policy_for_compare(right)
    li=characterize_spectrum(lv)["complex_detected"]
    ri=characterize_spectrum(rv)["complex_detected"]
    if (li or ri) and lp != rp:
        return {
            "status":"incompatible",
            "reason":"complex_policy_mismatch",
            "left_policy":lp,
            "right_policy":rp,
            "message":"Scalar spectral comparison requires matching complex-spectrum policies; use mode='complex' for raw complex-plane comparison.",
        }
    lproj=project_eigenvalues(lv,lp)
    rproj=project_eigenvalues(rv,rp)
    if lproj is None or rproj is None:
        return {
            "status":"incompatible",
            "reason":"undeclared_complex_projection",
            "left_policy":lp,
            "right_policy":rp,
            "message":"Complex spectra were preserved without a scalar projection; use mode='complex' or select an explicit complex policy.",
        }
    d=np.array([abs(float(lproj[i])-float(rproj[j])) for i,j in pairs],dtype=float)
    return {"status":"ok","mode":"policy","policy":lp,"matched_modes":len(pairs),"mean_distance":float(d.mean()),"max_distance":float(d.max())}


def _snapshot_policy_for_compare(snapshot):
    return getattr(snapshot,"complex_policy",None) or snapshot.observables.get("complex_policy","auto")
