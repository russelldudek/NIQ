# Candidate Vision Site Audit

State: **building**

This audit covers the candidate vision site only. The broader application campaign remains incomplete because the two-page resume, one-page cover letter, interview thesis brief, printable entry-plan artifacts, official NIQ mark, and protected external deployment remain outstanding.

## Argument and visitor journey

- Company/role context: passed
- Why the role matters now: passed
- Central operating tensions: passed
- Tactical empathy before prescription: passed
- Candidate thesis: passed
- Role-specific operating model: passed
- Honest cost of inaction: passed
- Verified transfer evidence: passed
- First 180 days: passed
- Executive discovery questions: passed
- Value before ask: passed
- Final CTA advances the argument: passed — `Pressure-test the model`

## Visual experience

- One dominant hero thesis: passed
- Signature hero visual: passed — six source planes resolving to one trusted signal
- Full-page visual pacing: passed across all eight scenes
- Depth-based desktop navigation: passed
- Nonlinear optical depth of field: passed
- Magnetic scene settlement: passed
- Sparse Signal Corridor background: passed
- Scroll-responsive signal streaking: passed
- Rest-state twinkling: passed; deliberately low amplitude
- Final-scene visual closure: passed; signal field fades down rather than competing with the CTA
- Mobile semantic equivalent: passed — source and portfolio systems recompose rather than preserving desktop 3D geometry
- Reduced-motion equivalent: passed — static field, no blur, no auto-snap, no motion-dependent access

## Interaction and psychology

- Smart starting state: passed — Balanced market
- Explicit reset to baseline: passed
- Meaningful participation: passed
- Scenario state transaction: passed
- Qualitative comparison integrity: passed — no unsupported source-mix percentages
- Human authority remains explicit: passed
- Decision load: passed
- Dark-pattern review: passed

## Responsive and runtime QA

Fresh Chromium regression suite: **7 / 7 passed**.

Verified viewports:
- 1440 × 900
- 1280 × 800
- 768 × 1024
- 390 × 844
- 320 × 800

Checks include:
- zero horizontal overflow;
- no browser console warnings/errors in tested views;
- eight-scene narrative and closing CTA;
- signal canvas initialization;
- qualitative portfolio state synchronization and reset;
- depth blur at intermediate positions and `blur(0)` at settlement;
- exact idle snap to the nearest scene;
- user interruption of an in-flight snap;
- mobile removal of depth blur and desktop navigation;
- reduced-motion removal of auto-snap and depth blur.

## Evidence integrity

- No NIQ internal source mix is asserted.
- No unverified NIQ workforce count, vendor economics, cost target, savings target, or quality threshold is asserted.
- Public NIQ metrics link to authoritative public company sources.
- Candidate interpretation is labeled as a candidate read.
- Career evidence remains within verified claim strength.

## Brand

- Official NIQ color tokens: passed
- Typography evidence and substitute decision: passed
- Independent-candidate distinction: passed
- Official logo/wordmark: **blocked for development**. The official media-kit asset has not yet been locally retrieved. The site uses a typeset NIQ identifier rather than recreating the mark.

## Candidate-facing confidentiality

- No internal campaign-system name appears in shipped HTML, CSS, JavaScript, Markdown, filenames, or metadata.
- No campaign source-control URL is exposed in the candidate website.
- The confidential role brief is not committed.

## Material redesign record — Signal Corridor

Observed issue: the prior site was technically strong but several scenes still read as an executive dashboard — repeated cards, fact tiles, and UI readouts competed with the single-pass argument.

Approved direction: rebuild the experience so each scene leaves one memorable idea. Preserve the depth engine, optical focus, and magnetic settlement; replace dashboard-like structures with spatial typography, adversarial tension pairs, a qualitative Source Portfolio, evidence words, a three-stage entry plan, and a no-oriented closing question. Add a sparse twinkling signal field that responds to scroll velocity without turning the site into a space theme.

Key copy decisions:
- `The Full View starts at the source.`
- `Protect the knowledge. Change the mechanism.`
- `Rebalance the portfolio. Don’t replace the field.`
- `See the economics. Prove the choices. Earn the right to scale.`
- `Pressure-test the model.`

Prior visual proof is invalidated by this material redesign. Fresh render and regression evidence is required before any later completion classification.
