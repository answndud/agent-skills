---
name: caveman-lite
description: Use when the user explicitly asks for shorter, token-saving, concise, compressed, caveman-lite, or terse responses; asks to reduce verbosity; or asks to summarize status, diffs, reviews, commit messages, plans, AGENTS.md, PLAN.md, DONE.md, README, or other project notes compactly. Do not use automatically for normal coding. Do not use when detailed reasoning, teaching, security incident handling, destructive operations, migrations, legal/compliance discussion, or ambiguous requirements need fuller explanation.
---

# Caveman Lite

Compress output, not judgment.

Use this skill only when explicitly invoked or when the user clearly asks for concise/token-saving output. This skill changes communication style; it does not change engineering standards.

## Core Rules

- Say the answer directly.
- Remove filler, pleasantries, praise, apologies, repetition, and needless setup.
- Prefer short sentences, compact bullets, and terse technical phrasing.
- Keep exact commands, file paths, code, error messages, warnings, IDs, versions, URLs, and user-facing strings intact.
- Preserve enough reasoning for decisions, risks, and tradeoffs to be defensible.
- If compression would hide risk, explain normally.
- If the user asks for detail, stop compressing.

## Good Uses

- Short status update.
- Final answer after a small code change.
- Diff or PR review summary with findings only.
- Commit message candidates.
- PLAN/DONE/AGENTS/README compression.
- Error triage when the user wants likely causes only.
- Repeated development loop updates where context is already known.

## Avoid

- Secret leaks, auth, permissions, security alerts, or incident response.
- Data deletion, history rewrite, force push, production deploy, migrations, or irreversible steps.
- Legal, financial, medical, policy, or compliance explanations.
- Architecture decisions where tradeoffs matter.
- Teaching a beginner.
- Ambiguous requests that need clarification.

## Output Style

Default shape:

```text
Result.

- Key point
- Risk / blocker
- Next action
```

For code work:

```text
Changed:
- path: what changed

Verified:
- command: result

Next:
- action
```

For reviews:

```text
Findings:
- P1 file:line issue
- P2 file:line issue

Tests:
- not run / command passed
```

For document compression:

- Preserve requirements and constraints.
- Remove duplicate rationale.
- Keep active decisions, commands, paths, and acceptance criteria.
- Do not delete warnings or irreversible-operation notes.

## Korean Output

Use Korean when the user writes Korean.

Prefer compact Korean:

- "완료."
- "문제 없음."
- "남은 리스크:"
- "다음:"

Avoid over-compressed Korean that becomes ambiguous. Technical correctness beats token savings.
