# NIQ Candidate Vision — Development Audit

Campaign state: **building**

## Current design system

The candidate vision uses a depth-based **Signal Corridor** rather than ordinary vertical section scrolling. Desktop movement advances through eight role-specific planes; magnetic settlement brings the nearest plane into exact alignment; optical blur makes the departing plane fall out of focus; and a sparse signal field stretches subtly with scroll velocity before becoming quiet again at rest.

The argument remains:

**The Full View starts at the source.**

**Protect the knowledge. Change the mechanism.**

The site uses qualitative source roles — `PRIMARY`, `SUPPORTING`, `EXCEPTION`, `SUNSET` — rather than percentage-like source bars, and holds four invariants constant: trust, coverage, local intelligence, economics.

## User-directed visual composition correction

### Observed defect

Russell rejected the prior Signal Corridor render after direct visual review. The spatial mechanics were interesting, but the page composition was not at the same level: the hero type was grotesquely oversized, the source graphic read as overlapping translucent boxes, later scenes mixed unrelated box geometries, and text scale/alignment varied enough that the experience felt generic rather than executive-grade.

### Why prior QA missed it

The earlier proof verified scene count, state synchronization, depth blur, snap behavior, reduced motion, viewport overflow, and console health. Those checks did not constrain headline scale, hero line count, hero-copy versus visual separation, equal-column geometry, or the visual consistency of later sections. Structural correctness passed while perceived craft failed.

### Rejected execution

- oversized hero headline breaking into visually awkward lines;
- stacked horizontal source rectangles around `TRUSTED SIGNAL`;
- circular scene buttons competing with the content;
- bento-style company-moment cards;
- boxed scenario/source rows with inconsistent edge geometry;
- evidence and 180-day content using different alignment systems;
- tablet still forced through the desktop 3D renderer;
- 320-pixel tension rows exceeding the viewport.

### Approved correction

- force the hero into exactly three deliberate lines: `The Full View` / `starts at the` / `source.`;
- make `source.` the NIQ-blue visual anchor and cap desktop hero type below 70 px;
- replace the stacked-box hero graphic with a progressive source corridor of narrow vertical planes converging on one `TRUSTED SIGNAL` plane;
- convert the scene navigator to a quiet vertical index with small active-point indication;
- replace the company-moment bento with one aligned four-metric rail;
- convert the tactical-empathy scene to a shared axis system with an aligned three-part closing argument;
- convert the portfolio model to open source rails and left-edge active states rather than boxed cards;
- convert transfer evidence to one four-column proof rail and the entry plan to one three-column 30 / 90 / 180 runway;
- convert the question scene to three equal aligned columns;
- use the semantic vertical composition at tablet width as well as mobile rather than squeezing the depth renderer into 768 px;
- remove narrow-phone overflow and hide illegible micro-labels inside the mobile source corridor;
- retain the subtle signal field, magnetic snap, depth blur, tactical-empathy argument, qualitative portfolio interaction, and pressure-test CTA.

## Fresh QA evidence

- Scene regression: **5 / 5 tests passed** after the visual correction.
- Desktop hero uses exactly three explicit headline lines; rendered desktop font size is approximately 67.7 px and total headline height is below 200 px.
- Hero copy and source visual remain spatially separated at 1440 × 900.
- Transfer-evidence columns resolve to equal top alignment and equal width.
- 30 / 90 / 180 milestones resolve to equal top alignment.
- Qualitative scenario selection remains atomic across source roles, readouts, and `aria-pressed` state.
- Intermediate depth state still produces optical blur; the sampled departing scene measured `blur(3.73px)` and the arriving scene `blur(6.96px)` before magnetic settlement returned to the nearest exact scene.
- Render checks at 1440 × 900, 1280 × 800, 768 × 1024, 390 × 844, and 320 × 800 returned **zero horizontal overflow** and **zero console warnings/errors**.
- Tablet, mobile, and reduced-motion states use static semantic composition rather than 3D scene travel; reduced-motion filters resolve to `none`.
- 320-pixel hero remains three lines, stays below 44 px rendered type, and fits without overflow.
- Desktop screenshots were visually reviewed for the hero, tactical-empathy scene, portfolio model, evidence rail, entry plan, question rail, and final CTA.

## UX psychology status

- Smart starting state: passed — Balanced market is a labeled illustrative default.
- Honest orientation: passed — scene position reflects real content; no fake completion percentage.
- Value before ask: passed — contact actions appear only at the end of the argument.
- Meaningful participation: passed — market context changes the source posture and decision readout.
- Honest cost of inaction: passed — the site acknowledges what field-heavy collection protects as well as what it costs.
- Contextual comparison integrity: passed — no source percentage, maturity score, or unsupported improvement claim is shown.
- Dark-pattern review: passed — the no-oriented CTA invites a working session without scarcity, shame, or coercion.

## Remaining completion blockers

- official NIQ logo/wordmark asset still needs to be locally committed and rendered before Brand Fidelity can pass;
- exactly two-page resume and exactly one-page cover letter remain outstanding;
- interview thesis brief and printable entry-plan artifacts remain outstanding;
- protected external deployment remains outstanding;
- live exact-head verification remains outstanding.

Do not classify the campaign as complete until the complete application artifact set, official identity asset, protected deployment, exact-head live verification, print/PDF contracts, and final canonical audit all pass.
