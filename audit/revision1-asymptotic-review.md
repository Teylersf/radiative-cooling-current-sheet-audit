# Round-1 review: local bounds for the thermal correction

## Decision and scope

The editor's and reviewer 2's objection is justified for the explanation
currently supplied with manuscript Section 4, Eq. (10). A calculation for a
frozen scalar equation is not, by itself, a derivation of an expansion of
the coupled printed equations. In particular, convergence of eta to a
constant alone gives no rate and does not suffice to freeze the leading
inverse-square coefficient at subleading order.

The omission can nevertheless be bounded **using the source's printed
coupled ODE**. On the explicitly conditional finite-positive-eta,
inverse-square-collapse branch described below, the coupled eta equation
forces eta-eta_c=O(tau); the evolving thermal coefficient differs from its
limit by O(tau^(5/9)). Neither change precedes the nonzero limiting thermal
coefficient's tau^(8/9) correction. An energy argument gives a remainder,
rather than relying on formal differentiation of an asymptotic ansatz.

This result concerns the equations as printed, which independently use an
incorrect pressure construction. It is not an existence theorem for their
initial data, a solution of repaired non-affine radiative MHD, a physical
collapse prediction, or a reproduction of any source trajectory. The
published numerical verifier integrates frozen scalar controls only; those
checks do not numerically test the coupled remainder bounds proved here.
No canonical paper, program or result has been edited in this review.

## Exact reviewed concern and source equations

The current status receipt for owned paper `p_EE9ZliH1d9MufihL` records
round-1 `major_revision`. Reviewer 2 says:

> Section 4 states Eq. (10) after freezing the outflow scale but does not
> derive bounds on the omitted time-dependent outflow and thermal-coefficient
> terms, so its validity as an expansion of the coupled printed equations is
> not established.

The editor explicitly permits either deriving/bounding the corrections or
restricting the claim to the frozen scalar equation. This note addresses
that item only, not the other requested archival, quotation and provenance
repairs.

The target's VOR Eq. (2.31), p.7, together with Eq. (2.29), becomes, for
a=2, b=1/2 and gamma=5/3,

$$
\ddot\xi=-\frac{\eta}{\xi^2}+\frac1\eta
-H(t)\xi^{-5/3},\qquad
\ddot\eta=\frac1\xi-\frac{\xi}{\eta^2}
-\frac{H(t)}\eta\xi^{-2/3},\qquad
\dot I=(\xi\eta)^{-2/3},
$$

where

$$
H(t)=P_{0,X}\eta(t)^{-2/3}\bigl(\widetilde C I(t)^2-1\bigr).
$$

The positive term in the first equation is **1/eta**, not xi/eta^2.
The source's Appendix B first freezes eta and simplifies its forces before
obtaining its scalar first integral and quadrature, Eqs. (B11)-(B14), p.23.
The separate leading-amplitude factor-of-two check against (B14) is
unaffected by the present remainder issue.

## A conditional local statement for the coupled printed ODE

Assume a classical solution on a left neighborhood of a finite t_c with:

1. xi(t)>0 and eta(t)>0; I is the cumulative integral from a regular earlier
   time, with no prior singularity;
2. fixed finite P_{0,X} and tilde C, not a simultaneous infinite-cooling
   limit;
3. tau=t_c-t, xi(t)~A tau^(2/3) with A>0, and eta(t)->eta_c>0.

These are assumptions on a branch if it exists. They do not assert that
the original initial conditions reach that branch. Under these hypotheses,

$$
A^3=\frac{9\eta_c}{2},\qquad
I_c-I(t)\sim\frac95(A\eta_c)^{-2/3}\tau^{5/9},
\qquad 0<I_c<\infty.
$$

Moreover,

$$
\dot\eta(t)\longrightarrow v_c\in\mathbb R,\qquad
\eta(t)=\eta_c-v_c\tau+O(\tau^{4/3}),\qquad
H(t)-H_c=O(\tau^{5/9}),
$$

with H_c=P_{0,X} eta_c^(-2/3)(tilde C I_c^2-1). Consequently

$$
\ddot\xi=-\eta_c\xi^{-2}-H_c\xi^{-5/3}+R(t),
\qquad R(t)=O(\tau^{-5/9}).
$$

In particular R=o(tau^(-10/9)), the order of the nonzero H_c force.
The first subleading term is therefore

$$
\boxed{\displaystyle
\xi=A\tau^{2/3}+\frac{81}{44}H_cA^{-5/3}\tau^{8/9}
+O(\tau^{10/9}) .}
$$

When H_c is nonzero, this is genuinely the first correction on that branch.
The big-O constant need not be uniform as H_c approaches zero or another
parameter varies. No inference about a finite observation window follows
without such uniformity.

### Proof of the coefficient bounds

The integrand is (A eta_c)^(-2/3) tau^(-4/9)(1+o(1)); its endpoint is
integrable and has the tail just given. Thus I and H are bounded. The eta
equation gives

$$
\ddot\eta=O(\tau^{-2/3})+O(\tau^{-4/9})+O(\tau^{2/3})
=O(\tau^{-2/3}).
$$

Since tau^(-2/3) is integrable, dot eta has a finite endpoint limit, its
difference from that limit is O(tau^(1/3)), and a second integration gives
eta=eta_c-v_c tau+O(tau^(4/3)). The smooth dependence of H on positive
eta and finite I then gives H-H_c=O(tau)+O(tau^(5/9)). This establishes the
claimed bound without assuming an eta convergence rate in advance.

The first equation has
ddot xi=-eta_c A^(-2) tau^(-4/3)(1+o(1)); integration implies
dot xi=-3 eta_c A^(-2) tau^(-1/3)(1+o(1)). Comparing its integral with the
assumed xi asymptotic gives A^3=9 eta_c/2 and, in particular,
dot xi=O(tau^(-1/3)). The remainder is exactly

$$
R=-(\eta-\eta_c)\xi^{-2}
-(H-H_c)\xi^{-5/3}+\frac1\eta.
$$

The three respective bounds are O(tau^(-1/3)), O(tau^(-5/9)), and O(1).
Their total is the stated O(tau^(-5/9)).

### Energy argument: the omitted force cannot change the first correction

Define a renormalized scalar energy, **not a conserved energy of the full
MHD system**,

$$
\mathscr E(t)=\frac12\dot\xi^2-\frac{\eta_c}{\xi}
-\frac32H_c\xi^{-2/3}.
$$

The exact equations give dot mathscr E=dot xi R. Its magnitude is
O(tau^(-8/9)), which is integrable. Hence

$$
\mathscr E(t)=\mathscr E_c+O(\tau^{1/9}),\qquad
\dot\xi^2=\frac{2\eta_c}{\xi}+3H_c\xi^{-2/3}
+2\mathscr E_c+O(\xi^{1/6}).
$$

The solution is strictly decreasing sufficiently near the endpoint, so
xi can be used as a local variable. Expanding the positive inverse speed
and integrating from zero yields

$$
\tau=\frac{2\xi^{3/2}}{3\sqrt{2\eta_c}}
\left[1-\frac{27H_c}{44\eta_c}\xi^{1/3}
+O(\xi^{2/3})\right].
$$

Inverting this expression gives the boxed expansion with its remainder.
Equivalently, for m=8/9 the linearized balance has
m(m-1)-4/9=-44/81, giving D_1=(81/44)H_c A^(-5/3).
The energy argument also controls the free endpoint-time/energy modes;
one does not obtain the expansion merely by twice differentiating a
leading-order equivalence.

### Cancellation and the special scalar-energy correction

If H_c=0, the sharper energy expansion gives

$$
\xi=A\tau^{2/3}
+\frac{\mathscr E_c A^2}{5\eta_c}\tau^{4/3}
+O(\tau^{13/9}).
$$

Thus 4/3 can be the first correction if the limiting thermal coefficient
cancels and mathscr E_c is nonzero. If it also vanishes, further terms must
be examined. It is incorrect to promote 4/3 as a generic first thermal
correction for nonzero H_c. Conversely, simply asserting that H_c=0 does
not justify deleting a still time-dependent H(t) at every later order.

## Why convergence alone would fail

If eta(t) were an arbitrary imposed coefficient with only eta->eta_c,
the conclusion would not follow. For example eta-eta_c proportional to
tau^delta with 0<delta<2/9 would change the inverse-square force at order
tau^(delta-4/3). Its induced correction has power 2/3+delta, earlier than
8/9. Such a prescribed history does **not** satisfy the eta equation and
its integrable-acceleration bound on the branch considered above. This
counterargument is why the coupled equation and the branch assumptions
must appear in the revision.

## Exact proposed replacement for manuscript Section 4

Replace the paragraph beginning "Retaining a generic finite net thermal
coefficient" and the paragraph after Eq. (10) with the following. A short
appendix should supply the energy proof above; otherwise use the narrower
fallback below instead.

> A conditional local check can also retain the coupling to eta. Consider
> a C^2 positive branch of the **printed** Eqs. (2.29) and (2.31), with
> fixed finite coefficients, no earlier singularity, xi~A tau^(2/3) and
> eta->eta_c>0. This assumes a branch if it exists; it does not establish
> one for the source initial data. Let
> H(t)=P_{0,X} eta(t)^(-2/3)(tilde C I(t)^2-1) and H_c=lim H(t).
> The eta equation gives ddot eta=O(tau^(-2/3)), hence
> eta-eta_c=O(tau), while the cumulative-integral tail gives
> H-H_c=O(tau^(5/9)). Therefore
> ddot xi=-eta_c xi^(-2)-H_c xi^(-5/3)+O(tau^(-5/9)).
> The omitted force is later than the nonzero H_c term. Integrating the
> associated scalar-energy identity gives
>
> xi=A tau^(2/3)+D_1 tau^(8/9)+O(tau^(10/9)),
> A^3=9 eta_c/2, D_1=(81/44)H_c A^(-5/3).
>
> This is the first correction only for H_c nonzero. When H_c=0, a
> nonzero limiting scalar-energy constant instead yields a tau^(4/3)
> correction; further cancellations require further analysis. These local
> results concern the printed ODE, not repaired thermodynamics, physical
> collapse or a reconstruction of the original curves. The archived
> scalar quadrature controls test frozen coefficients; they do not
> numerically evolve or independently validate this coupled local branch.

### Minimal fallback if no coupled proof is included

> For a **separate frozen-coefficient scalar control only**, let
> ddot xi=-eta_c xi^(-2)-H_c xi^(-5/3), where eta_c>0 and H_c are constants.
> Its scalar first integral yields Eq. (10) when H_c is nonzero, and a
> free scalar-energy tau^(4/3) correction when H_c=0. This calculation
> illustrates the sensitivity to a retained thermal coefficient; it is
> not asserted as an expansion of the coupled source equations. No bounds
> on their omitted time-dependent terms are inferred from that control.

Under that fallback, remove or narrow any statement calling 8/9 the
generic coupled-equation correction. The cumulative-integral and leading
coefficient findings do not depend on retaining Eq. (10), so dropping the
secondary expansion would not weaken the principal pressure/EOS critique.

## Recommended response to reviewer 2/editor

> We agree that the previous frozen-coefficient explanation did not by
> itself justify an expansion of the coupled equations. We now state the
> local branch hypotheses explicitly and bound both omitted coefficients
> using the printed coupled eta and cumulative-integral equations. They
> imply eta-eta_c=O(tau) and H-H_c=O(tau^(5/9)), giving a force remainder
> O(tau^(-5/9)). The derivative of a renormalized scalar energy is then
> integrable, which yields Eq. (10) with remainder O(tau^(10/9)) when H_c
> is nonzero. We distinguish this conditional analytic statement from
> the archived frozen-scalar numerical controls and do not claim that the
> source initial conditions reach the branch or that it solves repaired
> radiative MHD. The cancellation case is stated separately.

Use this response only if the proof/qualifications are actually added.
If the fallback is chosen, say instead that Eq. (10) has been explicitly
restricted to the frozen scalar equation.

## Verification and evidence boundary

The exponent bookkeeping was independently checked with exact rational
arithmetic: remainder exponents -1/3 and -5/9 are both later than -10/9;
energy derivative exponent -8/9 is integrable; and
(8/9)(-1/9)-4/9=-44/81. No new integration or simulation is required for
this proof. The existing scalar calculation remains unchanged. The exact
source equation was read from the cached publisher-math extraction,
`journal-math-tex.json` entry138, and the source Appendix B expressions
from entries591-624 and following, in addition to the already completed
full-edition source review.
