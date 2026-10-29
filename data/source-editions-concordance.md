# Source-edition preflight: radiative cooling, arXiv 2508.13081

Checked 29 October 2026. The complete supplied 24-page preprint and complete 26-page journal version of record were read, including their appendices, captions and references. Selected journal pages 1, 5, 7, 13 and 21 were also inspected visually. This is a provenance and substantive edition comparison, not a completed scientific audit or an exhaustive character-level diff.

## Identity and retrieval

The supplied file is **Current sheet formation under radiative cooling**, by **Simran Chowdhry and Nuno F. Loureiro**. It is byte-identical to the [official arXiv:2508.13081v1 PDF](https://arxiv.org/pdf/2508.13081v1): **24 pages, 966,878 bytes**, SHA-256 **49dd1f97967345a7c22825158758ab1ed49529abd27c717ee2bdbc6ef7c40c0c**. The official history examined lists only v1, submitted **18 August 2025 at 16:53:34 UTC**. The preprint's “under consideration” heading does not describe the later publication state.

The version of record is **Journal of Plasma Physics 91(6), E148 (2025)**, [DOI 10.1017/S0022377825100949](https://doi.org/10.1017/S0022377825100949). The [official Cambridge article](https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/current-sheet-formation-under-radiative-cooling/25F7006FAF380BAA0F24E9DE86FFA274) and [official PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/25F7006FAF380BAA0F24E9DE86FFA274/S0022377825100949a.pdf/current-sheet-formation-under-radiative-cooling.pdf) returned ordinary HTTP 200. The PDF contains **26 pages, 786,255 bytes**, SHA-256 **1e47de8f1bbdb554c26efe029b13127cdbf4464fe6599721b64129f86b22150e**. No human challenge, browser access, credentials or challenge circumvention was needed.

The journal records receipt on **18 August**, revision received **22 September**, acceptance **25 September**, and online publication **7 November 2025**. Its issue is December 2025. The publisher PDF explicitly states **CC BY 4.0**; the arXiv PDF metadata also identifies this license. Primary Crossref registration metadata independently confirms the journal citation, author ORCIDs, publication dates and license.

The [official arXiv source archive](https://arxiv.org/src/2508.13081v1) has **507,143 bytes**, SHA-256 **aefd7e6d7854a42965afdd39cc327e51104c65bce2fbf3d9448f8e36449ff2b6**. Five regular members were safely extracted: paper.tex, paper.bbl, jpp.cls, 00README.json and a six-page Illustrator graphics PDF. The manuscript includes the first five graphic pages. No numerical program, notebook, simulation input deck or tabulated numerical array is supplied in that archive. The TeX SHA-256 is **46af1a05cfd0d1842d53d4dd28da0987f6875072c325c2e6255d4f75474efe7c**. Nothing in the source archive was executed.

## Confirmed edition differences

| Item | Preprint | Journal |
| --- | --- | --- |
| Continuity expression | p.5, Eq.(2.14), TeX lines 167–170, omits an equality | p.5, Eq.(2.14), explicitly ends with =0 |
| Asymptotic flow-rate notation | p.10, Eq.(3.1), uses gamma and delta | p.10, Eq.(3.1), uses Gamma_x and Gamma_y; the xi, density and current exponents remain |
| Magnetic-flux definition | p.4 after Eq.(2.12), TeX line 155, uses z-hat cross grad-perp psi | p.5 after Eq.(2.12), PDF and publisher HTML show a dot product and add psi = −A_z |
| Cooling-law scope | Shorter parameterization discussion on p.3 | New footnote 1 on p.3 discusses fitted exponents beyond bremsstrahlung and a slowly varying beta requirement for field-dependent mechanisms |
| Crab-Nebula scope | p.8 gives an astrophysical example | New footnote 3 on p.9 explicitly requires relativistic corrections for a detailed application |
| Conclusion | p.19 describes the MHD starting point and future verification | p.20 explicitly says Newtonian MHD, discusses non-MHD extensions and cites qualitative agreement with existing radiative PIC results |
| Abstract bibliography | p.1 cites Uzdensky and McKinney (2011) | p.1 prints 1962, while its own body and p.25 bibliography identify that work as 2011 |

The flux-symbol difference is confirmed in both journal PDF pixels and the publisher's public TeX-math HTML text. It does not show what operation any numerical implementation used. Likewise, the restored continuity equality and flow-rate symbols should not be described as errors still present in the final article.

The journal's added applicability caveats and external PIC comparison deserve explicit credit. Numerical verification of the model in this paper is still described as future work. An external qualitative comparison is not a deposited reproduction of these particular ODE calculations.

## Retained source assertions and useful locators

The core equation numbering remains substantially the same across editions. The following are exact source-location correspondences for a later audit, **not adjudicated error findings**:

| Topic | Preprint pages | Journal pages | Equations |
| --- | --- | --- | --- |
| Base MHD and cooling law | 3 | 3 | 2.1–2.4 |
| Lagrangian field mappings | 3–4 | 4 | 2.5–2.11 |
| X-point setup and similarity equations | 4–5 | 5–6 | 2.12–2.20 |
| Cooled pressure, parabolic profile and coupled ODEs | 6–7 | 6–7 | 2.21–2.31 |
| Cooling/outflow times and cooling parameter | 7–8 | 8–9 | 2.32–2.38 |
| Weak-cooling asymptotics | 10–12 | 10–13 | 3.1–3.7 |
| Strong-cooling asymptotics | 12 | 13 | 3.8–3.12 |
| Critical cooling estimate | 13–14 | 14–15 | 3.13 |
| Modified Sweet–Parker model | 15–17 | 16–19 | 4.1–4.16 |
| Pressure derivation | 19–20 | 20–21 | A1–A6 |
| Weak-cooling ODE, quadrature and correction | 20–22 | 21–23 | B1–B14 |

Both editions retain the pressure representation with C1 and C2 and the source assertion that “the choice of C2(x0,y0) is unconstrained,” followed by the selected parabolic pressure profile. The final printed expressions in Eqs.(2.24), (2.26), (2.28) and Appendix A should therefore be checked directly, rather than presumed repaired during publication.

Both editions also retain the cooling-strength formulas (2.32)–(2.36), the strong-cooling exponent alpha approximately 1 in (3.11)–(3.12), the nearby eta much less than xi wording, and the steady-state compression/length/rate/thickness claims (4.10)–(4.16). Their mathematical validity has not been decided by this preflight. No corrected model, new simulation, author intent or historical execution identity is claimed.

All five figure numbers keep their topics: preprint pages **9, 10, 11, 13, 14** correspond to journal pages **10, 11, 12, 14, 15**. This is a topic/locator mapping, not a claim of byte-identical figures or numerically identical curves.

## Corrections, data and evidence boundaries

The primary Crossref record has an empty relation object and no update-to/updated-by entry. Four targeted correction/erratum searches found no target-specific notice. The readable official article did not reveal an actual code/data repository or deposit link; generic publisher navigation and unrelated errata were excluded. These are bounded checks, not proof that no correction or external data exists.

The supporting correction/deposit check is correction-and-deposit-check.json. The exact fetch URLs, dates, status codes and hashes are in primary-fetch-receipts.json. Publisher TeX-math span text is preserved in journal-math-tex.json; it is extracted public HTML, not a retrieved journal-author TeX archive.

The full text files are supplied-full-text.txt and journal-vor-full-text.txt, with individually numbered page files. Original source PDFs remain working evidence in this scratch area. Public-safe provenance contains stable official URLs, relative evidence basenames and hashes, without credentials, signed query strings or private network information.
