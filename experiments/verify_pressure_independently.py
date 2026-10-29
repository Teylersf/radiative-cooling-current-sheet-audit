"""Independent scalar thermodynamic checks; not a full MHD simulation.

SciPy integrates the stated pressure equation directly. Independently,
mpmath quadrature evaluates the closed form. No prior verifier is imported.
Recorded source hashes are provenance, not a claim to rehash absent PDFs.
Only the study results directory receives scientific output.
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import sys

import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "results"
RECORDED_SOURCES = [
    {"file": "journal-vor-S0022377825100949.pdf", "sha256": "1e47de8f1bbdb554c26efe029b13127cdbf4464fe6599721b64129f86b22150e"},
    {"file": "official-arxiv-2508.13081v1.pdf", "sha256": "49dd1f97967345a7c22825158758ab1ed49529abd27c717ee2bdbc6ef7c40c0c"},
    {"file": "arxiv-source-v1/paper.tex", "sha256": "46af1a05cfd0d1842d53d4dd28da0987f6875072c325c2e6255d4f75474efe7c"},
]
mp.mp.dps = 65
GAMMA = 5 / 3
GAMMA_MP = mp.mpf(5) / 3
A = 2
KAPPA = 0.12
END = 0.4
GRID = np.linspace(0, END, 17)
BS = [0, 0.25, 0.5, 0.75, 1]
RTOL, ATOL = 2e-12, 2e-14
PROFILES = {
    "isochoric": (0.0, 0.0),
    "compression": (-0.35, 0.0),
    "expansion": (0.4, 0.0),
    "changing_compression_rate": (-0.25, 0.3),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_provenance():
    """Read only recorded metadata; source PDF or TeX bytes are never needed."""
    metadata_path = ROOT / "data/source-editions.json"
    metadata = None
    metadata_hash = None
    if metadata_path.is_file():
        raw = metadata_path.read_bytes()
        metadata = json.loads(raw)
        metadata_hash = hashlib.sha256(raw).hexdigest()

    def leaves(value, path="$" ):
        if isinstance(value, dict):
            for key, child in value.items():
                yield from leaves(child, path + "." + str(key))
        elif isinstance(value, list):
            for i, child in enumerate(value):
                yield from leaves(child, path + "[" + str(i) + "]")
        elif isinstance(value, str):
            yield path, value

    fields = list(leaves(metadata)) if metadata is not None else []
    rows = []
    for row in RECORDED_SOURCES:
        matches = [path for path, value in fields if value == row["sha256"]]
        if metadata is not None and row["file"].endswith(".pdf") and not matches:
            raise ValueError("Source-editions metadata does not contain the recorded PDF hash: " + row["file"])
        rows.append({**row, "verification_semantics": "recorded provenance; source bytes not read or rehashed",
                     "record_source": "data/source-editions.json" if matches else "preserved original independent run receipt",
                     "matching_metadata_fields": matches})
    return {"sources": rows,
            "metadata": {"source_bytes_rehashed": False,
                         "metadata_file": "data/source-editions.json" if metadata is not None else None,
                         "metadata_sha256": metadata_hash,
                         "fallback_source_records_used": sum(not row["matching_metadata_fields"] for row in rows),
                         "note": "Source hashes identify previously verified editions; this offline numerical run makes no new assertion about unavailable PDF or TeX bytes."}}


def jacobian(name, t):
    h0, h1 = PROFILES[name]
    return np.exp(h0 * t + h1 * t * t), h0 + 2 * h1 * t


def jacobian_mp(name, t):
    h0, h1 = (mp.mpf(str(value)) for value in PROFILES[name])
    return mp.exp(h0 * t + h1 * t * t)


def rhs(name, rho0, b, kappa):
    def energy(t, pressure):
        J, H = jacobian(name, t)
        P = pressure[0]
        if P <= 0:
            raise RuntimeError("Control left the positive branch; do not evaluate fractional power")
        return [-GAMMA * H * P - kappa * (rho0 / J) ** (A - b) * P ** b]
    return energy


def integrate(name, P0, rho0, b, kappa=KAPPA):
    answer = solve_ivp(rhs(name, rho0, b, kappa), (0, END), [P0],
                       method="DOP853", t_eval=GRID, rtol=RTOL, atol=ATOL,
                       max_step=0.025)
    if not answer.success or answer.y.shape != (1, len(GRID)):
        raise RuntimeError("Direct pressure integration did not complete")
    if np.any(answer.y <= 0):
        raise RuntimeError("A selected control reached nonpositive pressure")
    return answer.y[0], answer.nfev


def integral_mp(name, b, t):
    b = mp.mpf(str(b))
    q = GAMMA_MP * (1 - b) + b - A
    return mp.quad(lambda u: jacobian_mp(name, u) ** q, [0, mp.mpf(str(t))])


def pressure_mp(name, P0, rho0, b, t, kappa=KAPPA, integral=None):
    P0, rho0, b, kappa, t = [mp.mpf(str(v)) for v in (P0, rho0, b, kappa, t)]
    J = jacobian_mp(name, t)
    I = integral_mp(name, b, t) if integral is None else integral
    if b == 1:
        Y = P0 * mp.exp(-kappa * rho0 ** (A - 1) * I)
        branch = mp.mpf(1)
    else:
        branch = P0 ** (1 - b) - (1 - b) * kappa * rho0 ** (A - b) * I
        if branch <= 0:
            raise RuntimeError("Closed form left its positive physical branch")
        Y = branch ** (1 / (1 - b))
    return Y / J ** GAMMA_MP, branch


def printed_pressure_mp(name, P0, b, t, C2_multiplier):
    """Printed two-function expression, C1=1 and C2=multiplier*P0."""
    P0, b, t, multiplier = [mp.mpf(str(v)) for v in (P0, b, t, C2_multiplier)]
    if b == 1:
        raise ValueError("Printed expression is undefined at b=1")
    I = integral_mp(name, b, t)
    tilde = ((GAMMA_MP - 1) * (1 - b) * mp.mpf(str(KAPPA))) ** (1 / (1 - b))
    return P0 * (1 - multiplier * tilde * I ** (1 / (1 - b))) / jacobian_mp(name, t) ** GAMMA_MP


def main():
    if sys.flags.optimize:
        raise RuntimeError("Run ordinary Python; optimized mode disables verification guards")
    # Independent evolution versus independent high-precision quadrature.
    integrals = {(name, b): [integral_mp(name, b, t) for t in GRID]
                 for name, b in itertools.product(PROFILES, BS)}
    grouped = defaultdict(lambda: {"case_count": 0, "maximum_absolute_error": 0.0,
                                   "maximum_relative_error": 0.0})
    min_pressure, min_branch, nfev, solves = math.inf, math.inf, 0, 0
    for name, b, P0, rho0 in itertools.product(PROFILES, BS, [0.8, 2.3], [0.7, 1.4]):
        numeric, count = integrate(name, P0, rho0, b)
        nfev += count
        solves += 1
        exact = []
        for t, I in zip(GRID, integrals[name, b]):
            value, branch = pressure_mp(name, P0, rho0, b, t, integral=I)
            exact.append(float(value))
            min_branch = min(min_branch, float(branch))
        exact = np.array(exact)
        absolute = float(np.max(np.abs(numeric - exact)))
        relative = float(np.max(np.abs(numeric - exact) / exact))
        assert relative < 5e-10
        row = grouped[name, b]
        row["case_count"] += 1
        row["maximum_absolute_error"] = max(row["maximum_absolute_error"], absolute)
        row["maximum_relative_error"] = max(row["maximum_relative_error"], relative)
        min_pressure = min(min_pressure, float(numeric.min()))

    # Same initial value for every finite C2; wrong initial cooling for b>0.
    wrong_initial = []
    for b in [0.25, 0.5, 0.75]:
        errors = []
        for H0, P0, rho0, multiplier in itertools.product([-0.35, 0, 0.4], [0.8, 2.3], [0.7, 1.4], [0, 0.1, 1, 3]):
            C1, C2 = 1.0, multiplier * P0
            assert P0 * C1 == P0
            m = 1 / (1 - b)
            assert m > 1 and np.isfinite(C2)
            printed = -GAMMA * H0 * P0  # derivative of I**m is0 at I=0
            required = printed - KAPPA * rho0 ** (A - b) * P0 ** b
            errors.append(abs(printed - required))
        assert min(errors) > 0
        wrong_initial.append({"b": b, "finite_C2_controls": len(errors),
                              "minimum_initial_derivative_error": min(errors),
                              "maximum_initial_derivative_error": max(errors)})

    # Differentiate the full printed expression at positive times, not only
    # its initial power law, and substitute into the original pressure law.
    printed_residuals = []
    for b, multiplier in itertools.product([0.25, 0.5, 0.75], [0.1, 1, 3]):
        residuals, differences = [], []
        for time in [0.05, 0.2, 0.4]:
            t = mp.mpf(str(time))
            P = printed_pressure_mp("changing_compression_rate", 1.7, b, t, multiplier)
            assert P > 0
            derivative = mp.diff(lambda u: printed_pressure_mp("changing_compression_rate", 1.7, b, u, multiplier), t)
            h0, h1 = [mp.mpf(str(v)) for v in PROFILES["changing_compression_rate"]]
            H = h0 + 2 * h1 * t
            rho = mp.mpf("1.1") / jacobian_mp("changing_compression_rate", t)
            eos_residual = derivative + GAMMA_MP * H * P + mp.mpf(str(KAPPA)) * rho ** (A - mp.mpf(str(b))) * P ** mp.mpf(str(b))
            reference = pressure_mp("changing_compression_rate", 1.7, 1.1, b, t)[0]
            residuals.append(float(abs(eos_residual)))
            differences.append(float(abs(P - reference)))
        assert max(residuals) > 1e-4 and max(differences) > 1e-4
        printed_residuals.append({"b": b, "C2_over_P0": multiplier, "positive_times_checked": 3,
                                  "maximum_absolute_original_EOS_residual": max(residuals),
                                  "maximum_pressure_difference_from_correct_solution": max(differences)})

    # A nontrivial positive control: b=0 can be calibrated, but C2 is fixed.
    b0_errors = []
    for name, P0, rho0 in itertools.product(PROFILES, [0.8, 2.3], [0.7, 1.4]):
        C2 = rho0 ** A / (GAMMA - 1)
        tilde = (GAMMA - 1) * KAPPA
        for t, I in zip(GRID, integrals[name, 0]):
            J, _ = jacobian(name, t)
            calibrated = (P0 - C2 * tilde * float(I)) / J ** GAMMA
            correct = float(pressure_mp(name, P0, rho0, 0, t, integral=I)[0])
            b0_errors.append(abs(calibrated - correct))
    assert max(b0_errors) < 2e-14

    # b->1 limit of the repaired expression is the exponential solution.
    limits = []
    for epsilon in [mp.mpf("0.001"), mp.mpf("0.000001"), mp.mpf("0.000000001")]:
        near = pressure_mp("changing_compression_rate", 2.3, 1.4, 1 - epsilon, END)[0]
        exact_b1 = pressure_mp("changing_compression_rate", 2.3, 1.4, 1, END)[0]
        limits.append({"one_minus_b": float(epsilon), "absolute_difference_from_b1": float(abs(near - exact_b1))})
    assert limits[2]["absolute_difference_from_b1"] < limits[1]["absolute_difference_from_b1"] < limits[0]["absolute_difference_from_b1"]

    # Independent scalar ODE trajectories preserve initial pressure ordering.
    ordering = []
    starts = np.linspace(0.4, 4, 11)
    for name, b in itertools.product(PROFILES, BS):
        values = []
        for P0 in starts:
            numeric, count = integrate(name, float(P0), 1, b)
            values.append(numeric)
            min_pressure = min(min_pressure, float(numeric.min()))
            nfev += count
            solves += 1
        separation = float(np.min(np.diff(np.stack(values), axis=0)))
        assert separation > 0
        ordering.append({"profile": name, "b": b, "initial_pressures": len(starts),
                         "sample_times": len(GRID), "minimum_adjacent_pressure_difference": separation})

    # Finite-difference gradients of independent ODE solutions versus mp.diff.
    # A prescribed affine flow fixes J; these flows are not claimed to solve
    # the momentum equation. Location-dependent force coefficients show why
    # a time-only affine acceleration cannot generally satisfy both laws.
    name, PX, rho0, kappa, x0, step = "changing_compression_rate", 4.0, 1.0, 0.6, 0.25, 1e-4
    xi = math.exp(-0.3 * END)
    J, _ = jacobian(name, END)
    gradient_rows, spreads = [], []
    for b in [0, 0.5, 1]:
        coefficients = []
        for y0 in [0, 0.4, 0.8]:
            profile = lambda x: PX * (1 - (x * x + y0 * y0) / 2)
            plus, cplus = integrate(name, profile(x0 + step), rho0, b, kappa)
            minus, cminus = integrate(name, profile(x0 - step), rho0, b, kappa)
            min_pressure = min(min_pressure, float(plus.min()), float(minus.min()))
            solves += 2
            nfev += cplus + cminus
            finite_difference = (plus[-1] - minus[-1]) / (2 * step)
            reference = float(mp.diff(lambda x: pressure_mp(name, PX * (1 - (x * x + mp.mpf(str(y0)) ** 2) / 2), rho0, b, END, kappa)[0], mp.mpf(str(x0))))
            error = abs(finite_difference - reference)
            assert error < 2e-7
            coefficient = -J / (rho0 * xi * x0) * finite_difference
            coefficients.append(float(coefficient))
            gradient_rows.append({"b": b, "x0": x0, "y0": y0,
                                  "gradient_from_direct_ODE_solutions": float(finite_difference),
                                  "gradient_from_mp_differentiation": reference,
                                  "absolute_error": float(error),
                                  "pressure_acceleration_over_x0": float(coefficient)})
        spread = max(coefficients) - min(coefficients)
        if b == 0.5:
            assert spread > 1e-3
        else:
            assert spread < 2e-7
        spreads.append({"b": b, "force_coefficient_location_spread": spread,
                        "affine_pressure_control": "fails_exact_global_closure" if b == 0.5 else "spatially_constant_special_case"})

    rng = np.random.default_rng(250813081)
    xi = np.exp(rng.uniform(-4, 0, 4096))
    eta = xi + np.exp(rng.uniform(-2, 1, 4096))
    PXs = np.exp(rng.uniform(-3, 2, 4096))
    theta = rng.uniform(0, 1, 4096)
    theta[0] = 0  # positive magnetic acceleration still survives at P=0
    accelerations = xi * (xi ** -2 - eta ** -2 + PXs * theta / (xi * eta) ** GAMMA)
    assert np.all(accelerations > 0)
    negatives = []
    for theta0 in [-0.1, -2.0]:
        pressure = theta0 / 0.5 ** GAMMA
        acceleration = 0.5 * (3 + pressure)
        negatives.append({"xi": 0.5, "eta": 1, "P0X": 1, "theta": theta0,
                          "central_pressure": pressure, "outflow_acceleration": acceleration})
    assert negatives[0]["outflow_acceleration"] > 0 and negatives[1]["outflow_acceleration"] < 0

    provenance = source_provenance()
    result = {
        "status": "pass", "schema_version": 1,
        "scope": "Independent scalar EOS integration and closure/positivity controls for the stated formulas; prescribed positive Jacobians, not a full MHD or reconnection simulation.",
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__, "mpmath": mp.__version__},
        "method": {"direct_ODE": "SciPy DOP853 pressure equation, not a transformed closed-form ODE", "rtol": RTOL, "atol": ATOL, "max_step": 0.025,
                   "reference": "mpmath65digit quadrature of J^q, followed by Bernoulli/exponential formula", "time_grid_points": len(GRID), "final_time": END, "random_generator": "NumPy PCG64 seed250813081"},
        "sources": provenance["sources"],
        "source_provenance": provenance["metadata"],
        "verifier_sha256": sha(Path(__file__)),
        "direct_integrations": solves, "ODE_function_evaluations": nfev,
        "positive_branch_minimum_pressure": min_pressure, "reference_controls_minimum_closed_form_branch_parameter": min_branch,
        "EOS_reference_controls": [{"profile": name, "b": b, **row} for (name, b), row in grouped.items()],
        "maximum_ODE_vs_reference_relative_error": max(row["maximum_relative_error"] for row in grouped.values()),
        "printed_C1_C2_initial_derivative_controls": wrong_initial,
        "printed_full_form_positive_time_residual_controls": printed_residuals,
        "printed_b1_status": "undefined at b=1; repaired exponential solution independently matches direct ODE",
        "b0_calibrated_C2_positive_control": {"C2_required": "rho0^a/(gamma-1) under the printed tilde convention", "maximum_absolute_error": max(b0_errors), "not_arbitrary": True},
        "b_to_one_limit_controls": limits,
        "pressure_order_controls": {"independent_profile_exponent_groups": len(ordering), "initial_pressures_per_group": len(starts), "all_ordered": True, "minimum_adjacent_pressure_difference": min(row["minimum_adjacent_pressure_difference"] for row in ordering)},
        "spatial_gradient_controls": gradient_rows, "force_coefficient_spreads": spreads,
        "outflow_positive_pressure_controls": {"states": len(accelerations), "assumptions": "0<xi<eta,P0X>0,theta>=0, printed finalODE", "minimum_acceleration": float(accelerations.min()), "all_strictly_positive": True,
                                                  "negative_pressure_is_not_sufficient_by_itself": negatives},
        "limits": ["Positive thermodynamic branch only; no square-root continuation through zero pressure.", "Pressure ordering assumes spatially uniform density and common J history.",
                   "Failure of exact affine closure does not preclude a declared local approximation or a different positive-pressure model.",
                   "Outflow implication is conditional on the displayed finalODE and xi<eta, not all possible cooled plasmas.",
                   "No hidden author-code identity, source numerical trajectory, physical spectrum, MHD dynamics, or full collapse times are reproduced."]}
    HERE.mkdir(parents=True, exist_ok=True)
    (HERE / "independent-pressure.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "scalar_ODE_integrations": solves,
                      "max_relative_error": result["maximum_ODE_vs_reference_relative_error"],
                      "max_spatial_gradient_error": max(row["absolute_error"] for row in gradient_rows),
                      "positive_outflow_states": len(accelerations), "result_file": "independent-pressure.json"}))


if __name__ == "__main__":
    main()
