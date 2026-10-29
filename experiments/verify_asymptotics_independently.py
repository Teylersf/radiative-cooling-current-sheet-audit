"""Deterministic scalar asymptotic checks, not a coupled-MHD simulation.

Standard-library Decimal arithmetic and independent Gauss-Legendre quadrature.
The source EOS is not repaired here: limits of its printed ODE are inspected.
"""
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib
import json
import math

if not __debug__:
    raise RuntimeError('Run ordinary Python without -O or PYTHONOPTIMIZE; verification assertions must remain enabled.')

ROOT = Path(__file__).resolve().parents[1]
D = Decimal


def power(x, exponent):
    return (x.ln()*exponent).exp()


def legendre(n, x):
    old, current = D(1), x
    for k in range(2, n+1):
        old, current = current, ((2*k-1)*x*current-(k-1)*old)/k
    derivative = n*(x*current-old)/(x*x-1)
    return current, derivative


def quadrature_nodes(n):
    nodes = []
    for i in range(1, n//2+1):
        x = D(str(math.cos(math.pi*(i-.25)/(n+.5))))
        for _ in range(20):
            p, derivative = legendre(n, x)
            delta = p/derivative
            x -= delta
            if abs(delta) < D('1e-140'):
                break
        p, derivative = legendre(n, x)
        assert abs(p) < D('1e-135')
        w = 2/((1-x*x)*derivative*derivative)
        nodes.extend([(-x, w), (x, w)])
    return sorted(nodes)


def integrate(fn, lo, hi, nodes):
    center, half = (hi+lo)/2, (hi-lo)/2
    return half*sum((w*fn(center+half*x) for x,w in nodes), D(0))


def text(x):
    return format(x, '.60g')


def main():
    with localcontext() as context:
        context.prec = 150
        small, large = quadrature_nodes(48), quadrature_nodes(96)
        assert abs(sum(w for _,w in large)-2) < D('1e-135')
        assert abs(integrate(lambda z:z**8,D(0),D(1),large)-D(1)/9) < D('1e-135')
        eta, A = D(2), D(1)
        cumulative = []
        largest_quad_difference = D(0)
        for alpha in (D(2)/3,D(1)):
            p = 2*alpha/3
            prefactor = power(eta*A,-D(2)/3)
            base_small = integrate(lambda v:power(v,-p),D('.5'),D(1),small)
            base_large = integrate(lambda v:power(v,-p),D('.5'),D(1),large)
            base_exact = (1-power(D('.5'),1-p))/(1-p)
            error = abs(base_large-base_small)/base_large
            largest_quad_difference=max(largest_quad_difference,error)
            assert error < D('1e-65')
            assert abs(base_large/base_exact-1) < D('1e-120')
            Ic = prefactor/(1-p)
            cooling_coefficient=D('.1')
            assert 1-cooling_coefficient*Ic**2>0
            r = power(D('.5'),1-p)
            for n in (10,20,40,80,160,320):
                tau = D(2)**(-n)
                xi = A*power(tau,alpha)
                # Independently integrate the power-law history by dyadic
                # panel scaling, using a quadrature-computed base panel.
                I_numeric = prefactor*base_large*(1-r**n)/(1-r)
                tail = Ic*power(tau,1-p)
                I_analytic = Ic-tail
                assert abs(I_numeric/I_analytic-1) < D('1e-120')
                # P0=1, C=.1 also keeps the printed pressure factor positive
                # for this imposed entire volume history. No flow is solved.
                ratio = cooling_coefficient*power(eta,-D(5)/3)*I_numeric**2*power(xi,D(1)/3)
                tail_ratio = cooling_coefficient*power(eta,-D(5)/3)*tail**2*power(xi,D(1)/3)
                normalized = ratio/power(tau,alpha/3)
                limit = cooling_coefficient*power(eta,-D(5)/3)*Ic**2*power(A,D(1)/3)
                cumulative.append({'alpha':text(alpha),'tau':text(tau),'xi':text(xi),
                    'I_quadrature':text(I_numeric),'Ic':text(Ic),'Ic_minus_I':text(tail),
                    'I_over_Ic':text(I_numeric/Ic),'cooling_coefficient':text(cooling_coefficient),
                    'limiting_printed_pressure_factor':text(1-cooling_coefficient*Ic**2),
                    'cooling_to_magnetic_ratio':text(ratio),
                    'discarded_constant_tail_only_ratio':text(tail_ratio),
                    'ratio_divided_by_tau_to_alpha_over_3':text(normalized),
                    'positive_limit_of_that_scaled_ratio':text(limit),
                    'cumulative_quadrature_relative_error':text(abs(I_numeric/I_analytic-1))})
            rows=cumulative[-6:]
            assert D(rows[-1]['cooling_to_magnetic_ratio']) < D(rows[0]['cooling_to_magnetic_ratio'])
            assert abs(D(rows[-1]['I_over_Ic'])-1) < D('1e-30')
        # Independent acceleration coefficient check of the actual leading
        # scalar force balance, not the printed time-inversion expression.
        eta=D(2); lead_power=D(2)/3
        right=power(9*eta/2,D(1)/3)
        printed=power(9*eta/4,D(1)/3)
        def acceleration_ratio(a):
            return (a*lead_power*(1-lead_power))/(eta/a**2)
        assert abs(acceleration_ratio(right)-1)<D('1e-135')
        assert abs(acceleration_ratio(printed)-D('.5'))<D('1e-135')
        leading={'eta_c':text(eta),'correct_A':text(right),'correct_A_cubed':'9*eta_c/2',
                 'printed_B14_A':text(printed),'printed_A_cubed':'9*eta_c/4',
                 'printed_acceleration_to_required_force_ratio':text(acceleration_ratio(printed))}
        scalar = []
        # Controlled reduced equation x''=-eta/x^2-H/x^(5/3).
        # Its exact energy integral gives xdot^2=2eta/x+3H/x^(2/3)+2E.
        # Integrate the inverse speed from zero to x after u=x*z^6,
        # which removes endpoint singularities from the numerical integral.
        for H,E in ((D(1),D('.7')),(D('-.5'),D('.7')),(D(0),D('.7'))):
            expected_power=D(8)/9 if H else D(4)/3
            expected_D=D(81)/44*H*power(right,-D(5)/3) if H else E/(5*eta)*right**2
            rows=[]
            for k in (3,6,9,12,18,24,36,48):
                x=D(10)**(-k)
                coeff=3*H/(2*eta)*power(x,D(1)/3)
                energy_coeff=E/eta*x
                def integrand(z):
                    denominator=1+coeff*z*z+energy_coeff*z**6
                    assert denominator>0
                    return z**8/denominator.sqrt()
                tau48=6*x*x.sqrt()/(2*eta).sqrt()*integrate(integrand,D(0),D(1),small)
                tau96=6*x*x.sqrt()/(2*eta).sqrt()*integrate(integrand,D(0),D(1),large)
                relative=abs(tau48/tau96-1)
                largest_quad_difference=max(largest_quad_difference,relative)
                assert relative<D('1e-65')
                delta=x-right*power(tau96,D(2)/3)
                amplitude=delta/power(tau96,expected_power)
                rows.append({'xi':text(x),'tau_from_scalar_energy_integral':text(tau96),
                    'xi_minus_leading_term':text(delta),'expected_correction_power':text(expected_power),
                    'scaled_correction_amplitude':text(amplitude),
                    'predicted_amplitude':text(expected_D),
                    'amplitude_relative_error':text(abs(amplitude/expected_D-1)),
                    '48_vs_96_point_quadrature_relative_difference':text(relative)})
            assert D(rows[-1]['amplitude_relative_error'])<D('1e-12')
            x1,x2=rows[-2:]
            slope=(abs(D(x2['xi_minus_leading_term']))/abs(D(x1['xi_minus_leading_term']))).ln()/(D(x2['tau_from_scalar_energy_integral'])/D(x1['tau_from_scalar_energy_integral'])).ln()
            assert abs(slope-expected_power)<D('1e-10')
            scalar.append({'eta_c':text(eta),'net_thermal_coefficient_H':text(H),'scalar_energy_E':text(E),
                'scope':'Frozen-coefficient scalar comparison, not the source coupled-flow solution.',
                'expected_first_correction_power':text(expected_power),
                'last_two_point_logarithmic_correction_slope':text(slope),'points':rows})
        result={'schema_version':1,'all_checks_passed':True,'producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'decimal_precision_digits':150,'quadrature':'Independent 48- and 96-point Gauss-Legendre nodes, computed in Decimal arithmetic.',
            'scope':'Conditional asymptotic consistency of the printed finite-eta scalar forces; no full MHD, corrected EOS evolution, source-code execution or figure reproduction.',
            'cumulative_integral_cases':cumulative,'leading_coefficient':leading,
            'scalar_energy_quadrature_checks':scalar,
            'maximum_48_vs_96_relative_quadrature_difference':text(largest_quad_difference),
            'source_locators':{'journal_doi':'10.1017/S0022377825100949','cumulative_integral':'Eq.(2.29), p.7; printed ODE Eq.(2.31), p.7',
                'weak_and_strong_asymptotics':'Eqs.(3.2)–(3.12), pp.11–13; Fig.4, p.14',
                'proposed_equal_order_threshold':'Eq.(3.13), p.15','leading_coefficient':'Appendix B, Eqs.(B11)–(B14), p.23'},
            'limits':['A finite-window cooling-dominated regime is not ruled out at a fixed large coefficient.',
                'The limiting argument requires eta_c>0; simultaneous two-axis collapse is outside its assumptions.',
                'The 8/9 correction is generic only when the net limiting thermal coefficient is nonzero; cancellations and energy constants change subleading behavior.',
                'The source pressure formula independently fails its primitive EOS; this check does not substitute a claimed solution of corrected physical equations.',
                'No physical universal asymptotic exponent, astrophysical transition or actual Figure4 fit has been measured.'],
            'new_MHD_or_PIC_simulations':0}
        p=ROOT/'results/independent-asymptotics.json'
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
        print(json.dumps({'all_checks_passed':True,'cumulative_cases':len(cumulative),'scalar_cases':len(scalar),
            'scalar_quadrature_points':sum(len(s['points']) for s in scalar),'maximum_quadrature_difference':text(largest_quad_difference),
            'receipt_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))


if __name__=='__main__':
    main()
