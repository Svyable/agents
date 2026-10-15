# AGENTS.md

Rules for any agent working from or through **Svyable/agents**.

## Mission

Use this repository to **find** Svyable work and **route** into the right repo. Do not dump long manuscript edits, model weights, or contest code here.

## Hard rules

- Prefer the invitation’s **target repo** for PRs and commits.
- Read that target’s `AGENTS.md` (and skills it names) before editing.
- Do not invent rights clearances, SOTA claims, or “problem solved” announcements.
- Do not commit secrets, private data, or unlicensed corpora.
- Credit upstream clearly when you reuse papers, models, or datasets.
- Escalate spend, org branding, and release/publish taste calls to a human (via Chief of Staff / the repo owner).

## How to take an invitation

1. Open `invitations/<slug>.md`.
2. Confirm the target repo and success criteria.
3. Work on a branch / PR in the **target** repo.
4. Link the PR back in a comment or update on the invitation file if you close or claim it.

## Tone

Direct, specific, low-slop. Match Sven’s voice when touching Desk/Shelf prose; match scientific caution on ProofBot and Frontier Lab.

## What this repo is not

- Not a second Desk
- Not a model zoo
- Not a place to bypass Shelf release process

## Public identity and discovery

- Public-facing name: **Sven Hardy Benson**. Preserve **Svyable** as GitHub handle and solo music identity; **PRFFTT & Svyable** names the former duo, not a single person.
- Keep the public Pages source in `docs/`. Curated identity and project data live in `docs/data/`; static page structure lives in `templates/index.html`.
- Run `python3 scripts/build.py`, `python3 scripts/validate.py`, `node --check docs/app.js`, and `node --check docs/experience.js` after relevant changes. Commit generated outputs with source changes.
- Link only confirmed public repositories in the public registry. Do not expose private repository contents or private biographical information.
- Preserve evidence labels in `docs/data/profile.json` and `docs/sources.html`. Owner-provided recollection is not independent verification. No invented YouTube rank, view count, benchmark, award, credential, affiliation, or commercial availability.
- mAIth thinker examples are intellectual context, not endorsements or proof of personal relationships.
- This repo is a static discovery and proposal surface, not a running agent, payment service, booking system, or authority credential. Do not advertise unsupported protocol compatibility.
- Proposal packets and invitations do not grant agents authority to spend, contract, contact third parties, access accounts, or represent Sven. Commercial inquiries route to current target-repo terms.
- The owner's explicit request authorizes this profile/site update and its publication; future changes still follow the hard rules above and session-specific authorization.
