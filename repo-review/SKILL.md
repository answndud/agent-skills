---
name: repo-review
description: Use only when the user explicitly asks to review code or repository changes, such as "리뷰해줘", "코드리뷰", "변경사항 점검", "merge 전 점검", "diff 리뷰", "PR 리뷰", or "review this diff". This skill reviews the current worktree diff by default and reports findings first. Do not use for normal coding, autonomous development loops, harness setup, PRD/TRD/ADR writing, or one-off explanations.
---

# Repo Review

## Purpose

Use this skill to review repository changes for bugs, regressions, security risks, contract drift, missing tests, and documentation drift.

Default mode is review-only. Do not edit files unless the user explicitly asks to fix or modify the issues in the same request.

## Activation Rules

Use this skill only when the user explicitly asks for a review, such as:

- "리뷰해줘"
- "코드리뷰 해줘"
- "변경사항 점검"
- "merge 전 점검"
- "diff 리뷰"
- "PR 리뷰"
- "review this diff"

Do not use this skill for:

- normal implementation requests
- broad refactors
- autonomous development loops
- PLAN/PROGRESS/COMPLETED harness setup
- PRD/TRD/ADR document writing
- release notes or changelog writing
- one-off explanations that are not review requests

## Review Target

Default target is the current worktree diff.

Start with:

1. `git status --short`
2. `git diff --stat`
3. `git diff --staged --stat`, when staged changes exist
4. `git diff`
5. `git diff --staged`, when staged changes exist

Use `git status --short` to identify untracked files (`??`). Untracked files do not appear in `git diff`; read and review relevant new source, docs, config, and test files directly.

When both staged and unstaged changes exist, review them together as the user's effective change. If the same file has both staged and unstaged edits, call out the split state when it affects review confidence or the likely final patch.

If the user specifies a PR, branch, commit, base/head range, or path subset, review that explicit target instead.

If there is no diff and no explicit target, say there is nothing to review and suggest the exact target needed.

## Context To Read

Read only enough context to evaluate the diff:

- `AGENTS.md`, if present
- `docs/PLAN.md` and `docs/PROGRESS.md`, if present, for current task intent and recent verification only
- package, config, test, schema, or public interface files touched by or adjacent to the diff
- existing tests covering the changed behavior
- relevant untracked files reported by `git status --short`

`docs/PLAN.md` and `docs/PROGRESS.md` are read-only context for this skill. Do not update them unless the user explicitly asks.

For generated, binary, lockfile, snapshot, or very large diffs, summarize the artifact change and focus detailed review on the source-of-truth files. Still flag unexpected artifact drift, missing generated updates, or lockfile changes that do not match dependency changes.

## Review Priorities

Prioritize findings in this order:

1. Bugs and behavioral regressions.
2. Security, authorization, privacy, data-loss, and destructive-operation risks.
3. Public API, CLI, schema, output, or compatibility drift.
4. Missing or inadequate tests for changed behavior.
5. Documentation drift when docs and behavior now disagree.
6. Maintainability risks that are likely to cause concrete future defects.

Avoid low-signal comments:

- style preferences without correctness impact
- broad refactor suggestions unrelated to the diff
- praise, cheerleading, or generic summaries
- speculative findings without evidence

If uncertain, state the assumption or open question instead of presenting it as a finding.

## Severity

Use priority labels consistently:

- `P0`: data loss, security incident, full build/deploy failure, or critical outage.
- `P1`: major feature regression, auth/permission failure, broken public contract, or high-probability runtime failure.
- `P2`: edge-case bug, missing test, documentation or contract drift, or meaningful maintainability risk.
- `P3`: low-impact improvement with a concrete benefit.

Findings should be ordered by severity, then confidence.

## Output Format

Lead with findings.

When there are line-specific findings, use Codex inline review directives:

```text
::code-comment{title="[P1] Short issue title" body="Explain the concrete risk and why this diff causes it." file="/absolute/path/to/file" start=10 end=12 priority=1 confidence=0.85}
```

Keep line ranges tight. Use absolute file paths when possible.

After inline findings, include concise text sections:

- `Findings`: say "발견한 문제 없음" when there are no findings.
- `Open Questions / Assumptions`: only if they affect the review.
- `Test Gaps / Residual Risk`: mention tests not run or coverage still missing.
- `Change Summary`: short secondary context, not the lead.

For simple no-issue reviews, keep the final answer short.

## Fix Policy

Default behavior is review-only.

If the user explicitly asks to fix issues in the same request:

1. Present findings first.
2. Re-check `git status --short` before editing.
3. Identify the files that need edits and avoid unrelated modified files unless the fix requires them and the interaction is understood.
4. Make the smallest safe changes needed to address accepted or obvious issues.
5. Run relevant verification when available.
6. Do not broaden scope beyond the reviewed diff.

Never fix by running destructive commands or reverting unrelated user changes.

## Safety Boundaries

Do not:

- run formatters or codegen that rewrite tracked files during review-only mode
- update `docs/PLAN.md`, `docs/PROGRESS.md`, or `docs/COMPLETED.md` unless explicitly asked
- create or update PRD/TRD/ADR documents
- start an autonomous development loop
- commit, push, tag, release, or deploy
- call live external systems unless the user explicitly asks and the review target requires it
- infer secrets, credentials, billing behavior, or production state without evidence

Tests, builds, typechecks, lint checks, and smoke checks may be run when they do not rewrite tracked files and are relevant to the review. If a command cannot be run, state why.

## Review Checklist

When reviewing, consider:

- Does the changed behavior still satisfy the intended task?
- Could this fail at runtime for common inputs?
- Are authorization, ownership, trust boundaries, and sensitive data handled correctly?
- Did a public contract, CLI output, schema, config format, or API response change without compatible handling?
- Are failure paths and edge cases covered?
- Are tests updated for the behavior that changed?
- Are docs, examples, README, or generated reports now stale?
- Are there unrelated changes mixed into the diff?

## Final Response

Use Korean by default unless the repository or user clearly uses another language. Keep code, paths, command names, and identifiers in their original form.

Preferred response shape:

```md
Findings
- ...

Open Questions / Assumptions
- ...

Test Gaps / Residual Risk
- ...

Change Summary
- ...
```

Omit empty sections except `Findings`.
