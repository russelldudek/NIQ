# Candidate Campaign Site Audit

State: **building**

This audit covers the candidate vision site only. The broader application campaign is not yet complete because the resume, cover letter, interview brief, standalone entry plan PDFs, and protected external deployment have not yet been produced.

## Candidate vision contract

- Company/role context: passed
- Why the role matters now: passed
- Central operating tensions: passed
- Candidate thesis: passed
- Role-specific operating model: passed
- Decision/metric clarity: passed
- Verified career evidence: passed
- First 180 days: passed
- Transferability/objection handling: passed with strength-first framing
- Executive discovery questions: passed

## Brand

- Official NIQ color tokens: passed
- Typography evidence and substitute decision: passed
- Independent-candidate distinction: passed
- Official logo/wordmark: **blocked for this development commit** because the official Brandfolder binary asset could be identified but not retrieved by the current execution environment. The site uses a clearly typeset NIQ identifier rather than recreating the logo. Replace with the official local asset before protected external release.

## Experience and interaction

- Role-derived 3D depth narrative: passed
- Desktop scroll moves through depth rather than vertically translating page sections: passed
- Idle scene settling: passed; 180 ms idle detection resolves to the nearest scene over 820 ms, with a 1050 ms final-scene arrival
- User interruption: passed; wheel, touch, pointer, and navigation-key intent cancels an in-flight settle immediately
- Closing hero: passed; the executive-question scene now hands off to a separate full-screen final statement and contact action
- Meaningful scenario interaction: passed
- Smart starting state: passed
- Reset-equivalent baseline available through Balanced market scenario: passed
- Contextual comparison integrity: passed; scenario values are explicitly illustrative
- Value before ask: passed
- Cost-of-inaction framing: passed without coercive language
- Keyboard-operable controls: passed
- Reduced-motion semantic equivalent: passed

## Responsive QA

Rendered with Chromium:

- 1440 × 900: passed, zero horizontal overflow
- 1280 × 800: passed, zero horizontal overflow
- 768 × 1024: passed, zero horizontal overflow
- 390 × 844: passed, zero horizontal overflow
- 320 × 800: passed, zero horizontal overflow
- Browser console errors: 0 across tested viewports
- Reduced-motion layout: passed
- Scenario final-state synchronization: passed
- Closing-scene navigation and exact final settlement: passed
- `qa/scene_regression.py`: passed (closing scene, idle snap, user cancellation, reduced-motion behavior)

## Evidence integrity

- No NIQ internal source mix, vendor economics, workforce count, or cost-out target is asserted.
- Public NIQ metrics are linked to public company sources.
- Candidate hypotheses are labeled as candidate hypotheses.
- Candidate career evidence is limited to verified/user-confirmed claims.

## Candidate-facing confidentiality

- No private campaign-building system name appears in shipped HTML, CSS, JS, Markdown, filenames or metadata.
- No source repository link is exposed in the candidate website.
- The confidential candidate brief itself is not committed.

## Release status

The candidate vision site is ready for development publication to `main` as a **building** campaign. It is not yet eligible to be classified as a complete application campaign.

## User-directed correction record

Observed defect: the depth journey ended on the executive-question page rather than resolving into a deliberate closing hero, and free scrolling could stop with a scene slightly out of focus instead of fully settled.

Why prior QA missed it: the earlier checks verified scene visibility, depth motion, navigation, responsive bounds, and interaction state, but did not treat idle landing position or the narrative endpoint as explicit regression requirements.

Approved correction: preserve free depth scrolling while the user is moving, then after 180 ms of inactivity ease the camera to the nearest scene. Standard settling lasts 820 ms; the final closing scene deliberately arrives over 1050 ms. Any new wheel, touch, pointer, or navigation-key intent cancels the active settle. Mobile and reduced-motion modes retain natural scrolling with no auto-snap. A new eighth scene provides a quiet closing hero that reprises the thesis and advances to direct contact.

Regression assertion added: `qa/scene_regression.py` verifies eight scenes and navigation states, exact idle settlement, immediate cancellation of in-flight snapping, and no auto-snap under reduced motion.

Prior visual and motion proof: invalidated by this material correction and re-run across 1440 × 900, 1280 × 800, 768 × 1024, 390 × 844, 320 × 800, and reduced-motion states.
