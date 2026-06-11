---
name: repo-review
description: Use only when the user explicitly asks to review code or repository changes, inspect risks, find missing tests, produce a test plan, or suggest validation for a concrete diff/scope. Triggers include "리뷰해줘", "코드리뷰", "변경사항 점검", "merge 전 점검", "diff 리뷰", "PR 리뷰", "테스트 계획", "테스트 케이스", "검증 루틴", "coverage gap", "testing strategy", or "review this diff". This skill is read-only by default and reports findings, test gaps, and validation recommendations. Do not use for normal coding, cleanup/refactor execution, autonomous development loops, harness setup, PRD/TRD/ADR writing, or one-off explanations.
---

# Repo Review

Read-only judgment for repository changes.

Use this skill to review a concrete diff, PR, commit range, module, or feature scope for:

- bugs and regressions
- security, authorization, privacy, data-loss, or destructive-operation risks
- public API, CLI, schema, config, output, or compatibility drift
- missing tests, weak coverage, and needed validation
- documentation drift
- maintainability risks likely to cause defects

Default mode is read-only. Do not edit files unless the user explicitly asks to fix issues in the same request.

## Activation

Use for explicit review or test-planning requests against code/repository context:

- `리뷰`, `코드리뷰`, `변경사항 점검`, `merge 전 점검`, `diff 리뷰`, `PR 리뷰`
- `테스트 계획`, `테스트 케이스`, `검증 루틴`, `어떤 테스트 짜야 해?`
- `review this diff`, `testing strategy`, `coverage gap`, `validation plan`

Do not use for normal implementation, behavior-preserving cleanup, broad refactors, autonomous loops, PLAN/DONE harness setup, PRD/TRD/ADR writing, release notes, or one-off explanations.

## Target

Default target is the current worktree diff.

Inspect:

1. `git status --short`
2. `git diff --stat`
3. `git diff`
4. staged diff/stat when staged changes exist
5. relevant untracked files

If the user specifies a PR, branch, commit range, base/head, paths, module, or feature, review that target. If there is no concrete target, say what target is needed.

## Context

Read only enough context to evaluate the target:

- `AGENTS.md`
- `docs/PLAN.md` for active task intent
- `docs/DONE.md` only when historical context matters
- adjacent package/config/test/schema/public interface files
- tests, fixtures, mocks, examples, snapshots, CI, or validation commands near the target

Treat PLAN/DONE as read-only unless explicitly asked to update them.

For generated, binary, lockfile, snapshot, or huge diffs, summarize the artifact and review source-of-truth files.

## Review Priorities

Order findings by severity and confidence:

- `P0`: data loss, security incident, full build/deploy failure, critical outage
- `P1`: major regression, auth/permission failure, broken public contract, high-probability runtime failure
- `P2`: edge-case bug, missing test, docs/contract drift, meaningful maintainability risk
- `P3`: low-impact improvement with concrete benefit

Avoid style-only comments, broad unrelated refactors, praise, and speculative findings without evidence.

## Test Planning

When the user asks for test cases, validation strategy, coverage gaps, or when the review finds untested risk, include concrete recommendations:

- high-risk behavior to cover
- test cases by `P1/P2/P3`
- suggested test level: unit, integration, API/CLI/browser/e2e, smoke, regression, snapshot/golden only when justified
- suggested test location based on existing repo conventions
- verification commands and what each proves
- residual risk if tests are not run or no framework is visible

Do not implement tests unless explicitly asked.

## Output

Lead with findings. For line-specific issues, use Codex inline comments:

```text
::code-comment{title="[P1] Short issue title" body="Explain the concrete risk and why this diff causes it." file="/absolute/path/to/file" start=10 end=12 priority=1}
```

Then include concise sections as needed:

- `Findings`: say `발견한 문제 없음` when there are none
- `Test Gaps / Validation Plan`: include concrete test cases or commands when relevant
- `Open Questions / Assumptions`: only when they affect confidence
- `Change Summary`: short secondary context

Omit empty sections except `Findings`.

## Fix Policy

If the user asks to fix:

1. Present findings first.
2. Re-check `git status --short`.
3. Make the smallest safe changes.
4. Avoid unrelated modified files.
5. Run relevant verification when available.
6. Do not broaden scope beyond the reviewed target.

Never use destructive commands or revert unrelated user changes.

## Boundaries

Do not commit, push, tag, release, deploy, create PRD/TRD/ADR, update PLAN/DONE, run rewriting formatters/codegen, or call live external systems unless explicitly asked.

Non-mutating tests, builds, typechecks, lint checks, and smoke checks may be run when relevant. If a command cannot be run, state why.
