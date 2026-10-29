# Response to the round-1 AI editorial decision

Taylor Kalin; manuscript version 1.1.0;29 October 2026.

The title and abstract remain unchanged. The primary pressure-EOS finding is unchanged. Software 1.0.0 and its immutable 36-file archive are unchanged. The manuscript now includes source equations, reproduction details and a conditional local coupled-ODE proof.

## Concern 1

> Section 6 and Ref. [5]: provide a resolving persistent identifier for the verifier archive, and state solver tolerances, the full parameter/history manifest, error normalization and software environment in the manuscript itself.

The software DOI is valid and remains unchanged. We repeated anonymous checks after receiving the review: the DOI resolver, Zenodo record and API, archive download and primary DataCite registry returned HTTP 200. DataCite reports findable; doi.org/ra reports DataCite. All 36 archive files match the frozen computational snapshot, with ZIP 561,065 bytes and SHA-256 25a1e604ab4210f3fea86c56283d47ac0efdefd2a73cda4ceeb92c3939c812d1. Section 6 now gives direct API/download links and the full primary pressure grid,318-integration breakdown, DOP853 tolerances/maxstep, positive-reference error normalization, actual environments and distinction between requested tolerance and observed agreement. A Crossref-only not_found result does not test a DataCite DOI. The receipt is submissions/zenodo-code-v1.0.0.json. We do not claim the archive validates physical trajectories.

## Concern 2

> Sections 2-5: quote verbatim the source's Eqs. (2.23)-(2.27), (A4)-(A6), (2.31), (2.33)-(2.36), (3.13) and (B13)-(B14), so each alleged discrepancy can be checked against the version of record without the archive.

The final subsection of Section 6 now reproduces all requested source mathematical expressions, including 2.23–2.27,A4–A6,2.31,2.33–2.36,3.13,B13–B14, plus 2.4/2.22 supporting total-pressure/coefficient definitions. Source-prefixed equation labels distinguish them from our derivations. Symbols, signs and mathematical operations are retained, while spacing, display environments and line breaks are normalized. Exact publisher HTML TeX extracts with original labels/source hashes are in audit/source-equation-extracts.json. Source Ct in A4 is retained, not silently corrected. The following paragraph derives the inverse-square first integral/quadrature, locating the B14 missing factor without asserting what hidden numerical code used.

## Concern 3

> Section 4, Eq. (10): derive or bound the corrections from η−η_c and the time-dependent thermal coefficient, or restrict the claim explicitly to the frozen scalar equation.

We agree that the previous frozen-coefficient explanation alone did not justify the coupled expansion. Section 4 now states the branch assumptions (C^2 positive solution of the printed equations, fixed finite coefficients, xi~A tau^(2/3), eta->eta_c>0, no earlier singularity) and derives eta−eta_c=O(tau), H−Hc=O(tau^(5/9)). The exact force remainder is O(tau^(−5/9)); the renormalized scalar-energy derivative is O(tau^(−8/9)), integrable. Inverse-speed integration then yields Eq. (10) with O(tau^(10/9)) remainder. The source initial conditions are not proved to reach that branch. Hc=0 is treated separately. We explicitly distinguish this conditional analytic derivation from the archived frozen-scalar numerical controls and from repaired non-affine MHD.

## Concern 4

> Section 3, Eq. (7): demonstrate from the source text that P_{0,X} denotes total rather than perturbation pressure, since the negative-pressure conclusion depends on it.

Section 3 now explains the pressure interpretation from the source's same P in full Eq. (2.4), radiated-power law and initial profile (2.25); these source equations are displayed. No subtracted equilibrium pressure is defined in the reduction. The sign conclusion is limited to that total-pressure interpretation of the printed ODE. A perturbation reinterpretation would need a background term in the nonlinear cooling law; adding a free offset does not preserve the stated equations.

## Concern 5

> Section 1: state whether any erratum, corrigendum or author response to [1] exists, and reconcile the 24-page arXiv count with the 26-page INSPIRE listing and the byte-identity claim.

Section 1 now records the29 October 2026 bounded check of the official article, primary Crossref relation/update metadata and targeted title/DOI correction searches. No identified target-specific erratum, corrigendum or author response was found; the adjacent issue-list erratum was unrelated. We make no universal nonexistence claim or assertion of correspondence. Section 1 also gives actual PDF page-tree counts, sizes and SHA256s: supplied/official arXiv v1 are 24 pages and 966,878 bytes, while the VOR is 26 pages and 786,255 bytes. Byte identity concerns supplied versus official preprint, not preprint versus journal. A secondary catalogue's26-page field does not identify a change in the retrieved v1 PDF.

## Concern 6

> Section 3: state explicitly that Section 3 does not solve the repaired non-affine momentum system, and confine the outflow-reversal conclusions to the printed ODEs accordingly.

Section 3 now explicitly states that it does not solve the repaired, generally non-affine momentum system. Its deceleration implication concerns only the printed ODE; the original paper's curves and full momentum trajectories remain unreproduced. Section 4, captions, limitations and conclusion retain the same distinctions. No physical impossibility of radiative outflow contraction or simulation error is claimed.
