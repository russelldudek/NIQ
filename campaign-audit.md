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
