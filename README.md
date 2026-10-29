# Thermodynamic consistency and closure limits of radiatively cooled X-point collapse

**Author: Taylor Kalin** · [taylorkalin.com](https://taylorkalin.com) · [ORCID](https://orcid.org/0009-0003-9000-9315)

This is the computational evidence for a mathematical comment on
[Chowdhry and Loureiro, JPP91, E148](https://doi.org/10.1017/S0022377825100949)
and [arXiv:2508.13081v1](https://arxiv.org/abs/2508.13081v1). Both complete
editions were read. The checks concern the printed energy equation, affine
closure, positive pressure, endpoint limits and steady-layer assumptions.

The principal finding is a nonlinear pressure-integration error. The corrected
scalar initial-value solution generally no longer has the common parabolic
spatial factor used to derive two global scale-factor equations. Separate
positive-pressure and cumulative-integral checks qualify the source's
outflow-reversal and strict endpoint interpretations. The displayed modified
Sweet-Parker algebra passes its own balances; domain restrictions and thermal
stability are separate questions.

Read the [complete mathematical comment](paper/manuscript.md),
[13-page PDF](paper/main.pdf) and
[verified public release](https://github.com/Teylersf/radiative-cooling-current-sheet-audit/releases/tag/v1.1.1).
The [published software archive](https://doi.org/10.5281/zenodo.23780790)
freezes 36 computational files at commit
`8a4e64cc032cb0c57bb621b200903b0c0f0706c2`. The live README now adds
manuscript links; the archived README and computational files remain preserved
at that pin. [Publication status](submissions/publication-status.json) distinguishes
public preprints, software publication, venue submissions and acceptance.

Manuscript 1.1.1 includes 18 exact source-equation extracts, a conditional coupled-ODE
remainder proof, full numerical protocol, and direct DataCite/archive checks.
The complete supplementary control grids and proper numerical-library citations are included. The original computational software remains 1.0.0. [Response to AI editorial
review](submissions/response-to-reviewers-round1.md) documents each change.
The preprint is also available on [AiraXiv](https://airaxiv.com/papers/view/2610.0118/).

[Attribution clarification](LICENSE_CLARIFICATION.md) corrects a copied title
in the frozen software license line; Taylor Kalin's ownership and license
terms remain the same.

These are original scalar and algebraic calculations, not a full MHD/PIC
simulation or a reconstruction of the source's plotted trajectories. They do
not prove physical radiative contraction is impossible. Underspecified
temperature/composition conventions are not labelled a verified coefficient
error. The journal's added applicability caveats and corrected preprint
notation are credited in [SOURCE.md](SOURCE.md).

## Reproduce

From a compatible Python environment, run:

```text
python experiments/calculate_examples.py
python experiments/verify_pressure_independently.py
python experiments/verify_asymptotics_independently.py
python experiments/verify_steady_state_independently.py
```

The producer uses NumPy and Matplotlib. The direct scalar pressure verifier
uses SciPy DOP853 plus independent mpmath quadrature. The asymptotic and
steady-state verifiers use the standard library. [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
records the two actual environments, controls, tolerances and provenance
adaptations. [requirements.txt](requirements.txt) provides pinned library
versions for a combined environment; the tested runs did not share one
interpreter. No source PDFs, network connection, GPU or private account is
needed for the scientific programs. Run without Python's `-O` flag.

The numerical programs write deterministic JSON/CSV outputs and three
original figures. Source hashes identify inspected editions; offline programs
explicitly read those as recorded provenance rather than pretending to hash
absent PDFs. Original independent scratch-run receipts are preserved separately
from the portable runs. A computational manifest binds the published files.

Taylor Kalin self-funds this work. AI tools assisted with retrieval, derivation,
code, cross-checks and drafting; computational independence is not independent
human peer review. The source authors and institutions have not endorsed this
comment. Original code is [MIT licensed](LICENSE-CODE); original audit text and
figures are [CC BY4.0](LICENSE-MANUSCRIPT). Third-party source material retains
its own rights.
