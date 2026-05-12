---
name: bounty-radar
description: Score and triage paid open-source bounty, bug bounty, micro-task, and grant-like earning candidates before Codex claims, comments, opens PRs, or submits work. Use when the user asks to find money-making repos, bounty candidates, paid tasks, next earning opportunities, "다음 주제", "제출할만한 repo", "돈 벌 후보", or when Codex must avoid duplicate/overcrowded/assignment-gated bounty submissions.
---

# Bounty Radar

## Purpose

Use this skill to turn open-ended bounty hunting into a repeatable gate: discover candidates, verify the public record, score risk, and decide `submit_now`, `claim_first`, `hold`, or `reject`.

This skill does not guarantee payment and does not bypass maintainer rules. It is a pre-submission harness.

## Inputs

Accept any mix of:

- A user request such as "다음 주제 찾으세요" or "돈 벌 수 있는 repo 찾아줘".
- A candidate issue, PR, repo, bounty board URL, platform task, or copied bounty text.
- Existing project docs such as `README.md`, `docs/PROGRESS.md`, `AGENTS.md`.

If the task is about current bounty availability, recent repo activity, prices, assignments, comments, PR state, or platform listings, browse or use GitHub/official APIs instead of relying on memory.

## Workflow

1. Read local guardrails first:
   - `AGENTS.md`
   - `README.md`
   - `docs/PROGRESS.md`
   - `docs/PLAN.md` when present
2. Build a candidate list from public sources or user-provided links.
3. For each candidate, verify:
   - reward amount or credible payout path
   - issue state and creation/update dates
   - maintainer activity and acceptance criteria
   - existing claims, assignees, competing PRs, and direct duplicates
   - assignment, `/start`, verification-answer, KYC, manual QA, video, hardware, or private disclosure gates
   - whether the repo/source is already overused in the current project
4. Score candidates with `scripts/score_candidates.py` when you have structured fields.
5. Classify each candidate:
   - `submit_now`: clear reward path, no gate, low duplication, scoped fix, verification possible.
   - `claim_first`: promising but assignment/verification gate exists; comment with codebase-specific proof before PR.
   - `hold`: possible payout but blocked by gas, credentials, hardware, maintainer reply, private triage, or uncertain reward.
   - `reject`: closed/rewarded/stale, overcrowded, duplicate PR, vague reward, high legal/ToS risk, anti-AI/manual-only, or too broad.
6. Before any public action, present the top candidate and the exact proposed public comment/PR plan unless the user already gave clear approval for that class of action.
7. After action, update `README.md` and `docs/PROGRESS.md` if the current project uses those files.

## Hard Gates

Reject by default when any of these are true:

- Same repo already has a current submission from this project and the user did not explicitly approve another.
- Existing claim/comment/PR count for the same scope is 3 or more.
- Issue is closed, already rewarded, stale with no maintainer activity, or internally reserved.
- Assignment or verification is required and Codex has not been assigned.
- Maintainer says not to create PRs, rejects AI-generated submissions, or requires manual-only proof Codex cannot provide.
- Task requires unlawful access, captcha bypass, credential theft, payment abuse, harassment, or serious legal risk.
- Reward path is only aspirational, unspecified, or lower than the user's minimum.
- Local verification is impossible within the intended work window and no credible manual proof can be produced.

Hold rather than reject when:

- Private disclosure is the correct route.
- A small funding/gas/onboarding blocker prevents claim but deliverable is ready.
- A maintainer assignment is likely but not granted yet.
- The candidate is promising but needs deeper codebase reproduction.

## Scoring Rubric

Use a 0-100 score. Prefer lower-risk expected value over headline reward size.

- Reward clarity: 0-20
- Freshness and maintainer activity: 0-15
- Low duplication and low claim crowding: 0-20
- Scope and implementation fit: 0-15
- Verification feasibility: 0-15
- Source/repo diversification: 0-10
- Reputation/legal safety: 0-5

Apply penalties:

- `-25`: assignment required and not assigned
- `-25`: 3 or more competing claims/PRs in the same scope
- `-20`: reward path unclear or stale
- `-20`: manual hardware/video/KYC dependency blocks Codex
- `-30`: serious legal, ToS, or anti-AI risk
- `-15`: same repo/source already used recently

Suggested thresholds:

- `80+`: strong `submit_now` if no hard gate.
- `65-79`: `claim_first` or short reproduction before action.
- `45-64`: `hold`; only proceed if alternatives are worse.
- `<45`: `reject`.

## Required Output

For exploration, output a compact table:

| Candidate | Reward | State | Crowding | Gate | Score | Decision | Rationale |
|---|---:|---|---:|---|---:|---|---|

Then provide:

- `Top pick`: one candidate or `none`.
- `Next action`: exact command/repo/action/comment class.
- `Public action draft`: only if a claim/comment/PR is recommended.
- `Reject log`: brief notes for rejected candidates, suitable for `docs/PROGRESS.md`.

## Public Action Rules

- Never open PRs for assignment-gated bounties before assignment.
- Never post payout details, private payment information, or secrets publicly.
- Do not mention "AI macro" or batch automation in maintainer-facing text.
- Make public comments specific to the codebase, not generic "I want to work on this".
- Prefer one high-quality submission per repo/source.
- For private security reports, keep exploit detail out of public issues and PRs until maintainer triage.

## Script

Use `scripts/score_candidates.py` to score JSON candidates when useful:

```bash
python3 /path/to/bounty-radar/scripts/score_candidates.py candidates.json
```

Input is a JSON array. Each candidate may include:

```json
{
  "name": "owner/repo#123",
  "reward_clarity": 18,
  "freshness": 12,
  "low_crowding": 15,
  "scope_fit": 12,
  "verification": 14,
  "diversification": 8,
  "safety": 5,
  "assignment_unassigned": false,
  "crowded": false,
  "unclear_reward": false,
  "manual_blocker": false,
  "legal_or_ai_risk": false,
  "same_repo_recent": false
}
```

The script prints a Markdown table with score and suggested decision.
