"""Original deterministic scalar examples; not a coupled MHD simulation.

The pressure law is tested on prescribed Jacobians. The cumulative-integral
and steady-layer examples test separate printed model assumptions.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import platform

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
GAMMA = 5/3


def positive_pressure(P0, I, J=1., b=.5, kappa=1.):
    """EOS solution before thermal extinction, with kappa=Cbar*rho0^(a-b)."""
    P0, I, J = np.asarray(P0), np.asarray(I), np.asarray(J)
    if np.any(P0 <= 0) or np.any(J <= 0) or np.any(I < 0) or kappa < 0:
        raise ValueError('Positive initial pressure and volume required')
    if b == 1:
        return P0*np.exp(-kappa*I)/J**GAMMA
    branch = P0**(1-b) - (1-b)*kappa*I
    if np.any(branch <= 0):
        raise ValueError('Stop at the positive branch boundary; no continuation')
    return branch**(1/(1-b))/J**GAMMA


def steady_case(beta, R, S, gamma=GAMMA):
    """Use source's displayed order-one SP conventions, not exact dynamics."""
    c = (gamma-1)/gamma**1.5
    A = 1+beta
    length = c/(R*beta*A)
    enhancement = math.sqrt(R*beta*A*A/c)
    delta_sys = 1/(enhancement*math.sqrt(S))
    aspect = delta_sys/length
    vin = enhancement/math.sqrt(S)
    return dict(beta=beta,calR=R,S=S,compression=A,length_over_system=length,
        rate_enhancement_over_incompressible_SP=enhancement,
        vin_over_VA=vin,delta_over_L=aspect,
        layer_fits_system=length<1,enhanced_relative_to_baseline=enhancement>1,
        thin_at_threshold_point1=aspect<.1,subAlfvenic=vin<1,
        continuity_relative_residual=abs(vin*length-A*delta_sys)/(A*delta_sys),
        ohms_law_relative_residual=abs(vin-1/(S*delta_sys))/vin)


def csv_write(name, rows):
    with (ROOT/'results'/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def main():
    if not __debug__:
        raise RuntimeError('Run without -O so validation assertions remain active')
    for d in ['results','figures']:
        (ROOT/d).mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,
        'xtick.labelsize':11,'ytick.labelsize':11,
        'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':150,
        'savefig.dpi':210,'axes.grid':True,'grid.alpha':.2})

    # Direct elementary counterexample: J=1, rho0=1, b=1/2, kappa=1.
    # The printed form uses a finite coefficient A=1/4 here. That choice is
    # illustrative; its zero initial derivative is independent of finite A.
    times=np.linspace(0,1.2,241)
    exact=positive_pressure(1.,times)
    printed=1-times*times/4
    exact_derivative=-1+times/2
    printed_derivative=-times/2
    exact_residual=exact_derivative+np.sqrt(exact)
    printed_residual=printed_derivative+np.sqrt(printed)
    assert np.max(abs(exact_residual))<3e-16
    assert exact_derivative[0]==-1 and printed_derivative[0]==0
    rows=[dict(time=float(t),correct_pressure=float(e),printed_form_pressure=float(p),
        correct_EOS_residual=float(er),printed_EOS_residual=float(pr))
        for t,e,p,er,pr in zip(times,exact,printed,exact_residual,printed_residual)]
    csv_write('isochoric-pressure.csv',rows)

    radius=np.linspace(0,1.15,241)
    P0=1-radius**2/2
    profile=positive_pressure(P0,.5)
    force_multiplier=1-.25/np.sqrt(P0)
    assert np.all(profile>0) and np.all(force_multiplier>0)
    assert np.ptp(force_multiplier)>.1
    # Scalar EOS flow preserves ordering; no negative continuation is plotted.
    assert np.all(np.diff(profile)<0)
    csv_write('pressure-profile.csv',[dict(radius=float(r),initial_pressure=float(p),
        cooled_pressure=float(v),gradient_multiplier=float(m))
        for r,p,v,m in zip(radius,P0,profile,force_multiplier)])
    fig,axs=plt.subplots(1,2,figsize=(10,3.8),layout='constrained')
    axs[0].plot(times,exact,label='EOS solution',color='#164e63',lw=2)
    axs[0].plot(times,printed,'--',label=r'Printed form, $A=1/4$',color='#b45309',lw=2)
    axs[0].set(xlabel='Prescribed isochoric time',ylabel='Pressure',
        title=r'(a) $P_0=1$, $\kappa=1$, $b=1/2$')
    axs[0].legend(fontsize=11)
    axs[1].plot(radius,P0,label='Initial parabola',color='#64748b')
    axs[1].plot(radius,profile,label='EOS solution at t=0.5',color='#164e63',lw=2)
    axs[1].plot(radius,.75**2*P0,'--',label='Rescaled parabola, same center',color='#b45309')
    axs[1].set(xlabel='Initial-label radius',ylabel='Pressure',title='(b) Positive branch retains center maximum')
    axs[1].legend(fontsize=11)
    fig.savefig(ROOT/'figures/pressure-and-profile.png'); plt.close(fig)

    # Prescribed xi=tau^alpha, eta=1, tc=1. They do not solve momentum.
    taus=np.logspace(-1,-24,240)
    integral_rows=[]
    fig,axs=plt.subplots(1,2,figsize=(10,3.6),layout='constrained')
    for alpha,color in [(2/3,'#164e63'),(1.,'#b45309')]:
        p=2*alpha/3
        Ic=1/(1-p)
        tail=taus**(1-p)/(1-p)
        integral=Ic-tail
        ratio=.1*integral**2*taus**(alpha/3)
        assert np.all(integral>0) and np.all(.1*integral**2<1)
        assert ratio[-1]<ratio[0]
        for tau,i,ta,ra in zip(taus,integral,tail,ratio):
            integral_rows.append(dict(alpha=alpha,tau=float(tau),integral=float(i),
                Ic=Ic,tail=float(ta),cooling_magnetic_ratio=float(ra)))
        axs[0].loglog(taus,integral,color=color,label=rf'$I$, $\alpha={alpha:.3g}$')
        axs[0].loglog(taus,tail,'--',color=color,label=rf'$I_c-I$, $\alpha={alpha:.3g}$')
        axs[1].loglog(taus,ratio,color=color,label=rf'$\alpha={alpha:.3g}$')
    axs[0].set(xlabel=r'Remaining time $\tau$',ylabel='Cumulative integral / tail',title='(a) The tail vanishes; the integral does not')
    axs[1].set(xlabel=r'Remaining time $\tau$',ylabel='Printed cooling / magnetic force',title=r'(b) Fixed $\widetilde C=0.1$, $P_{0,X}=1$')
    for ax in axs:
        ax.invert_xaxis(); ax.legend(fontsize=11)
    fig.savefig(ROOT/'figures/cumulative-integral.png'); plt.close(fig)
    csv_write('cumulative-integral.csv',integral_rows)

    cases=[steady_case(1,100,1e8),steady_case(1e-6,100,1e8),
           steady_case(1,1e10,1e8),steady_case(10,100,1e8)]
    assert cases[0]['layer_fits_system'] and cases[0]['subAlfvenic']
    assert not cases[1]['layer_fits_system'] and not cases[1]['enhanced_relative_to_baseline']
    assert not cases[2]['subAlfvenic'] and not cases[2]['thin_at_threshold_point1']
    for row in cases:
        assert row['continuity_relative_residual']<1e-14
        assert row['ohms_law_relative_residual']<1e-14
    csv_write('steady-branch-cases.csv',cases)
    betas=np.logspace(-7,2,400)
    Rs=np.logspace(-2,10,400)
    bb,rr=np.meshgrid(betas,Rs)
    c=(GAMMA-1)/GAMMA**1.5
    fits=rr>c/(bb*(1+bb))
    thin=rr<c*1e8*.01/bb
    sub=rr<c*1e8/(bb*(1+bb)**2)
    valid=(fits&thin&sub).astype(float)
    fig,ax=plt.subplots(figsize=(7.8,4.2),layout='constrained')
    ax.pcolormesh(bb,rr,valid,cmap=matplotlib.colors.ListedColormap(['#f1f5f9','#a5d8ce']),shading='auto',rasterized=True)
    ax.loglog(betas,c/(betas*(1+betas)),label='Layer fits system',color='#164e63')
    ax.loglog(betas,c*1e8*.01/betas,'--',label=r'$\delta/L=0.1$',color='#7c3aed')
    ax.loglog(betas,c*1e8/(betas*(1+betas)**2),':',label=r'$v_{in}/V_A=1$',color='#b45309')
    ax.set(xlabel=r'Upstream $\beta$',ylabel=r'Source cooling parameter $\mathcal{R}$',
        xscale='log',yscale='log',ylim=(1e-2,1e10),title=r'Necessary geometric/rate checks, $S_{sys}=10^8$')
    ax.legend(fontsize=11,loc='lower left')
    fig.savefig(ROOT/'figures/steady-branch-domain.png'); plt.close(fig)

    result=dict(schema_version=1,status='pass',scope='Prescribed scalar EOS, printed asymptotic forces and algebraic SP balances; no full MHD or source trajectory reproduction.',
        environment=dict(python=platform.python_version(),numpy=np.__version__,matplotlib=matplotlib.__version__),
        producer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        isochoric=dict(P0=1,b=.5,kappa=1,printed_A=.25,
            correct_initial_derivative=-1,printed_initial_derivative=0,
            max_correct_residual=float(max(abs(exact_residual))),
            pressure_at_time1=dict(correct=.25,printed=.75)),
        positive_profile=dict(time=.5,min_pressure=float(profile.min()),
            min_gradient_multiplier=float(force_multiplier.min()),max_gradient_multiplier=float(force_multiplier.max()),
            center_stays_maximum=True,exact_parabolic_rescaling=False),
        cumulative_histories=[dict(alpha=a,Ic=1/(1-2*a/3),tail_exponent=1-2*a/3,
            force_ratio_exponent=a/3) for a in [2/3,1]],
        steady_branch_cases=cases,thinness_plot_threshold=.1,
        independence='Separate high-precision verifiers neither import this producer nor use its CSV outputs as their mathematical reference.')
    (ROOT/'results/examples.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':'pass','figures':3,'steady_cases':len(cases),
        'correct_initial_derivative':-1,'printed_initial_derivative':0,
        'valid_case_enhancement':cases[0]['rate_enhancement_over_incompressible_SP']}))


if __name__=='__main__':
    main()
