"""Bounded algebra controls for the source normalization and steady-state model.

No ODE/PIC simulation, network, source-code execution or manuscript generation.
These checks test source-stated identities and conditional scaling formulas.
"""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import math
import platform

ROOT = Path(__file__).resolve().parents[1]


def clock_case(gamma_y, gamma=5/3, cbar=2.0, rho=3.0,
               pressure=4.0, a=2.0, b=0.5):
    inverse_energy_cooling_time = cbar*rho**(a-b)*pressure**(b-1)
    tau_u = 1/inverse_energy_cooling_time
    tau_p_over_q = (gamma-1)*tau_u
    tau_out = 1/gamma_y
    r_from_source_2_33_and_2_34 = tau_out/tau_u
    r_printed_2_35 = inverse_energy_cooling_time*gamma_y
    r_pressure_convention = tau_out/tau_p_over_q
    ratio = r_printed_2_35/r_from_source_2_33_and_2_34
    assert math.isclose(ratio, gamma_y**2, rel_tol=2e-15)
    assert math.isclose(tau_p_over_q/tau_u, gamma-1, rel_tol=2e-15)
    return dict(a=a, b=b, Cbar=cbar, rho=rho, pressure=pressure,
                Gamma_y0=gamma_y, tau_internal_energy=tau_u,
                tau_pressure_over_radiated_power=tau_p_over_q,
                tau_out=tau_out, R_from_displayed_times=r_from_source_2_33_and_2_34,
                R_printed_2_35=r_printed_2_35,
                printed_to_displayed_time_ratio=ratio,
                R_using_pressure_over_power_convention=r_pressure_convention)


def real_rational_power(base, exponent):
    """Use the real odd-root branch; return None if no real value exists."""
    if base < 0 and exponent.denominator % 2 == 0:
        return None
    magnitude = abs(base)**float(exponent)
    return (-magnitude if base < 0 and exponent.numerator % 2 else magnitude)


def tilde_sign_case(b, gamma=5/3, cbar=2.0):
    assert isinstance(b, Fraction) and b != 1
    exponent = Fraction(1)/(1-b)
    source_definition_base = (gamma-1)*float(1-b)*cbar
    # Substitute the source's own printed 2.35 into printed 2.36.
    converted_base = (gamma-1)*float(b-1)*cbar
    row = dict(b=float(b), b_rational=str(b),
               exponent=float(exponent), exponent_rational=str(exponent),
               base_from_2_27=source_definition_base,
               base_from_2_36_after_own_2_35=converted_base)
    expected = real_rational_power(source_definition_base, exponent)
    printed = real_rational_power(converted_base, exponent)
    row["tilde_from_2_27"] = expected
    if printed is not None:
        row.update(tilde_from_2_27=expected,
                   tilde_from_2_36_after_own_2_35=printed,
                   ratio=printed/expected,
                   real_branch_note=(
                       "Integer power or explicitly chosen real odd-root branch."))
    else:
        row["tilde_from_2_36_after_own_2_35"] = None
        row["real_branch_note"] = (
            "Negative base with an even-denominator reduced rational exponent: "
            "no real power value. This is not replaced by a complex coefficient.")
    return row


def sp_case(a, b, beta, cal_r, s_system, gamma=5/3):
    """Compare independently assembled displayed 4.7--4.16 relations.

    This uses the common order-one prefactor chosen by the printed scaling
    equations. It does not certify exact coefficients or thermal stability.
    """
    kappa = (gamma-1)/gamma**1.5
    compression = 1+beta
    length_power = (kappa/cal_r*beta**(b-1.5)
                    /(1+beta)**b*compression**(b-a+1))
    length_time = (kappa/cal_r*beta**(b-1.5)
                   /(1+beta)**(b-1)*compression**(b-a))
    length_4_11 = kappa/cal_r*beta**(b-1.5)/(1+beta)**(a-1)
    inflow_from_continuity_and_ohm = math.sqrt(
        compression/(s_system*length_power))
    inflow_4_12 = (math.sqrt(cal_r/kappa)
                   *beta**((1.5-b)/2)*(1+beta)**(a/2)
                   /math.sqrt(s_system))
    thickness_from_ohm = 1/(s_system*inflow_from_continuity_and_ohm)
    thickness_4_13 = (math.sqrt(kappa/cal_r)
                      *beta**((b-1.5)/2)*(1+beta)**(-a/2)
                      /math.sqrt(s_system))
    for left, right in [(length_power, length_time),
                        (length_power, length_4_11),
                        (inflow_from_continuity_and_ohm, inflow_4_12),
                        (thickness_from_ohm, thickness_4_13)]:
        assert math.isclose(left, right, rel_tol=3e-14)
    closure = inflow_from_continuity_and_ohm*length_power
    assert math.isclose(closure, compression*thickness_from_ohm,
                        rel_tol=3e-14)
    row = dict(a=a, b=b, beta_in=beta, calR=cal_r, S_system=s_system,
               kappa=kappa, A=compression, L_over_Lsystem=length_power,
               vin_over_VA=inflow_from_continuity_and_ohm,
               delta_over_Lsystem=thickness_from_ohm,
               delta_over_L=thickness_from_ohm/length_power,
               rate_over_classical_system_SP=(
                   inflow_from_continuity_and_ohm*math.sqrt(s_system)),
               fits_system=length_power<1,
               sub_Alfvenic_inflow=inflow_from_continuity_and_ohm<1,
               aspect_ratio_below_0_1=thickness_from_ohm/length_power<0.1)
    if a == 2 and b == 0.5:
        length_explicit = kappa/(cal_r*beta*(1+beta))
        enhancement_explicit = math.sqrt(cal_r/kappa*beta*(1+beta)**2)
        thin_explicit = math.sqrt(cal_r*beta/(kappa*s_system))
        assert math.isclose(length_power, length_explicit, rel_tol=3e-14)
        assert math.isclose(row["rate_over_classical_system_SP"],
                            enhancement_explicit, rel_tol=3e-14)
        assert math.isclose(row["delta_over_L"], thin_explicit, rel_tol=3e-14)
        row["brems_domain_bounds"] = dict(
            calR_for_L_below_system=kappa/(beta*(1+beta)),
            calR_for_rate_above_system_SP=kappa/(beta*(1+beta)**2),
            calR_at_delta_equals_L=kappa*s_system/beta,
            calR_at_vin_equals_VA=kappa*s_system/(beta*(1+beta)**2))
    return row


def main():
    clocks = [clock_case(g, a=a, b=b)
              for a, b in [(2.0, 0.5), (1.2, 0.4), (3.0, -0.5)]
              for g in (0.5, 1.0, 2.0)]
    signs = [tilde_sign_case(b) for b in
             (Fraction(0), Fraction(1, 2), Fraction(1, 3),
              Fraction(-1, 2), Fraction(2, 3), Fraction(3, 4))]
    assert signs[0]["ratio"] == -1
    assert signs[1]["ratio"] == 1
    assert signs[2]["tilde_from_2_36_after_own_2_35"] is None
    assert signs[3]["ratio"] == 1
    assert signs[4]["ratio"] == -1
    assert signs[5]["ratio"] == 1
    gamma = 5/3
    beta = 2.0
    sound_to_alfven = math.sqrt(gamma*beta/2)
    coefficient_from_first_2_38 = gamma*sound_to_alfven
    coefficient_printed_last_2_38 = math.sqrt(gamma*beta)
    coefficient_ratio = (coefficient_from_first_2_38
                         /coefficient_printed_last_2_38)
    assert math.isclose(coefficient_ratio, gamma/math.sqrt(2), rel_tol=2e-15)
    cases = [sp_case(a, b, beta, cal_r, 1e8)
             for a, b in [(2.0, 0.5), (1.2, 0.4), (3.0, -0.5)]
             for beta in (0.01, 0.1, 1.0, 10.0)
             for cal_r in (10.0, 100.0)]
    domains = [sp_case(2.0, 0.5, 1e-6, 100.0, 1e8),
               sp_case(2.0, 0.5, 1.0, 100.0, 1e8),
               sp_case(2.0, 0.5, 1.0, 1e10, 1e6),
               sp_case(2.0, 0.5, 100.0, 10.0, 1e7)]
    assert domains[0]["L_over_Lsystem"] > 1000
    assert domains[0]["rate_over_classical_system_SP"] < 1
    assert domains[1]["fits_system"] and domains[1]["sub_Alfvenic_inflow"]
    assert domains[1]["delta_over_L"] < 0.01
    assert domains[2]["vin_over_VA"] > 1 and domains[2]["delta_over_L"] > 1
    assert domains[3]["delta_over_L"] < 0.1 and domains[3]["vin_over_VA"] > 1
    report = dict(
        schema_version=1,
        scope=("Independent bounded normalization/algebra controls only; "
               "source assumptions are conditional, no ODE/PIC rerun."),
        source_arxiv_id="2508.13081v1",
        source_journal_doi="10.1017/S0022377825100949",
        source_journal_pdf_sha256=(
            "1e47de8f1bbdb554c26efe029b13127cdbf4464fe6599721b64129f86b22150e"),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        runtime=dict(python=platform.python_version(),
                     implementation=platform.python_implementation(),
                     dependencies="Python standard library only"),
        cooling_clock_cases=clocks,
        tilde_definition_sign_cases=signs,
        sound_Alfven_normalization=dict(
            assumed_beta="8*pi*P/B^2",
            gamma=gamma, beta=beta,
            cs_over_VA=sound_to_alfven,
            gamma_cs_over_VA=coefficient_from_first_2_38,
            printed_sqrt_gamma_beta=coefficient_printed_last_2_38,
            exact_to_printed_ratio=coefficient_ratio,
            interpretation=("Order-one coefficient/convention check, not a "
                            "refutation of the beta-half-power scaling.")),
        steady_state_scaling_positive_control=dict(
            cases=len(cases), all_identities_pass=True,
            retained_assumptions=[
                "Nearly uniform layer density, A=rhoX/rhoin~rhoout/rhoin",
                "Alfvenic outflow with its order-one factor suppressed",
                "Continuity and Ohm-law balances",
                "Local ohmic-radiative power balance",
                "Outflow-time/cooling-time closure",
                "Common order-one coefficients as in displayed 4.7/4.9"]),
        domain_cases=domains,
        exclusions=[
            "No claim that the posted figures use incorrect Gamma or units",
            "No universal invalidity claim from an unspecified temperature unit",
            "No physical prediction for formal cases outside sheet assumptions",
            "A positive stationary scaling is not a thermal stability proof",
            "No manuscript, publication, credentials or original source mutation"])
    output_path = ROOT/"results"/"independent-steady-state.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps({"clock_controls": "pass",
                      "tilde_sign_controls": "pass",
                      "SP_scaling_controls": len(cases),
                      "domain_cases": len(domains),
                      "heavy_physics_runs": 0}))


if __name__ == "__main__":
    main()
