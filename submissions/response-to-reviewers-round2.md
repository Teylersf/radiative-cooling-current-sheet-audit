# Response to the round-2 AI editorial decision

Taylor Kalin; manuscript version 1.1.1; 29 October 2026.

The analytic findings, title, abstract and scientific software version 1.0.0 are unchanged. This is a text-only revision: supplementary controls are fully specified and linked to public pinned mirrors, and the prior-work interpretation is clarified. Standard citations now also credit the NumPy, SciPy and Matplotlib libraries actually used; no original scientific text was trimmed.

## Concern 1

> Section 6 and Ref. [5]: supply an archive identifier or mirror that resolves independently of the author's own assertions, or state explicitly that the 4,096-state, 150-digit and steady-branch control counts are supplementary and not load-bearing for any conclusion.

Section 6 now explicitly labels the 4,096-state, 150-digit and steady-branch numerical counts supplementary and not load-bearing for any conclusion. The analytic claims follow from the displayed equations and conditional derivations. Reference [5] adds six direct public mirrors (three programs and their three JSON receipts) pinned to the unchanged computational commit. We independently fetched all six without authentication and verified exact bytes against that commit; submissions/round2-control-mirror-verification.json records the URLs and hashes. The software DOI 10.5281/zenodo.23780790 remains valid and unchanged; we do not replace it or claim a new archive version as a response to the review registry limitation.

## Concern 2

> Section 6: specify in the text the seeding, ranges and sign criterion for the 4,096 Eq. (7) outflow states and the parameter sets for the 150-digit and 24-case steady-identity checks, which are currently deferred to 'scripts and raw receipts'.

Section 6 now specifies the PCG64 seed, sequential uniform draws, transformations, zero-pressure overwrite, gamma and strict acceleration-sign test, as well as the two negative-pressure controls. It also gives the 150-digit precision, quadrature orders, cumulative-history parameters and all six endpoint powers, fixed leading-coefficient parameter, all three frozen scalar (H, energy) cases, all eight xi values, regularizing substitution and numerical comparison criteria. The full 24-case steady grid, nine clock cases, six rational sign cases and four domain tuples are stated in the text. These are the parameters in the original immutable code and receipts; no program, numerical output or tolerance was changed or newly run.

## Concern 3

> Section 5: correct the statement that Uzdensky and McKinney Section 4.1 'derive a bremsstrahlung instability condition'; the cited excerpt gives the evolutionary condition α<1+β, which bremsstrahlung fails (Reviewer 1 question).

We have separated the two arguments in the primary reference. In Uzdensky and McKinney Section 4.1, Eq. (57), alpha < 1 + beta_T is first obtained as an evolutionary-accessibility condition. On the following page they independently test the derivative of Qrad/Qohm with compression and obtain the same inequality as their thermal-stability condition, explicitly describing the bremsstrahlung branch as unstable. Section 5 now names both steps and distinguishes their cooling exponent beta_T from our upstream plasma beta. We retain the limitation that neither fixed-closure criterion transfers unchanged to the target's variable-length branch. This clarification follows the complete primary Section 4.1, rather than treating the evolutionary excerpt alone as a thermal-stability derivation.
