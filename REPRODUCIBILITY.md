# Reproducibility and limits

The scientific package is offline and CPU-only. It contains original scalar
calculations and independent checks, not original-author numerical analysis or
a full MHD/PIC run. Source PDF and TeX files are retained in a separate local
cache, not included in the archive as the author's work.

## Actual environments and commands

The plotting producer was run with CPython3.12.14, NumPy2.3.5 and
Matplotlib3.11.2. The independent pressure verifier was run separately with
CPython3.13.7, NumPy2.2.1, SciPy1.17.1 and mpmath1.3.0. Both standard-library
verifiers ran under CPython3.13.7. These environment differences are deliberate
provenance, not an assertion that a single combined environment was tested.

The root requirements file pins a compatible combined package set. Numerical
tolerances govern reproducibility across environments. Figure bytes may change
with fonts or Matplotlib versions; neither bitwise portability nor physical
accuracy follows from deterministic calculations.

Run the four commands in README in ordinary Python, without `-O`. The producer
writes `results/examples.json`, four CSV tables and three PNG figures. Its
constant-volume pressure example has P0=kappa=1,b=1/2; its coefficient1/4 for
the competing printed form is an explicitly declared illustration, not a fit to
an original figure. Its positive radial profile stops before any label's
extinction. The cumulative examples impose xi=tau^alpha,eta=1 only to test
the integral. The SP shading imposes three necessary geometric/rate checks,
not all assumptions or a thermal stability test.

## Independent checks

- `verify_pressure_independently.py` directly integrates the original scalar
  pressure equation with DOP853, rtol2e-12, atol2e-14, maxstep0.025. Independent
  65-digit quadrature supplies the Bernoulli/exponential reference. The run
  contains318 scalar integrations and80 primary reference cases across four
  Jacobian histories and five b values. Numerical gradient differences check
  spatial nonclosure. The b0 calibrated form and b1 exponential are positive
  controls. Seeded4096-state acceleration checks illustrate an exact sign
  implication; sampling alone is not its proof.
- `verify_asymptotics_independently.py` uses 150-digit Decimal arithmetic and
  independently constructed48/96-point Gauss-Legendre quadratures. It checks
  cumulative versus tail integrals, the fixed-coefficient force-ratio limit,
  leading collapse coefficient and reduced-scalar subleading corrections.
  Its imposed histories and frozen-coefficient reduced equations are not
  claimed to be global solutions for the original paper's initial data.
- `verify_steady_state_independently.py` checks nine initial-clock examples,
  six explicitly classified rational real-power cases,24 parameter cases
  satisfying multiple SP identities and four domain examples. It does not
  introduce a length dynamics or stability eigenvalue.

None imports the plotting producer. Each records its own script digest.
Original scratch-run JSON files are retained under `data/` without rewriting
their self-hashes or calling them new runs. Separate portability receipts list
the limited path/output and provenance adaptations. Source metadata hash checks
verify the provenance record, not the absent source PDFs themselves.

## Scope controls

Pressure evolution assumes common positive J and uniform initial density;
ordering holds while both compared labels have positive pressure. Exact affine
closure failure does not preclude a declared local approximation. The printed
outflow sign proof assumes0<xi<eta and positive P0X. The cumulative limit uses
fixed finite coefficients and eta tending to a finite positive limit. A joint
large-cooling limit, a finite fitting window or collapsing eta is not excluded.

The SP expressions use the source's displayed, approximate order-one
conventions. Layer fit, thinness and slow inflow are necessary consistency
checks and do not establish a stable physically realized layer. Strong cooling,
optical thinness, collisional validity and other applicability requirements
remain additional conditions.
