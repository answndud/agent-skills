---
name: test-plan
description: Use only when the user explicitly asks for a test plan, test cases, testing strategy, validation routine, coverage gap analysis, or Korean requests like "테스트 계획", "테스트 케이스", "검증 루틴", or "어떤 테스트 짜야 해?". This skill produces a repository-grounded test planning report by default and does not write tests or edit files unless the user explicitly asks to reflect the plan in docs/PLAN.md. Do not use for normal implementation, repo-review, simplify, dev-loop execution, harness setup, PRD/TRD/ADR writing, or one-off explanations.
---

# Test Plan

## Purpose

Use this skill to design tests and validation before or after a feature, fix, refactor, or release step.

Default behavior is read-only planning. Produce a test planning report grounded in the repository's actual code, test structure, and commands. Do not implement tests by default.

## Activation Rules

Use this skill only when the user explicitly asks for test planning, such as:

- "테스트 계획"
- "테스트 케이스"
- "검증 루틴"
- "어떤 테스트 짜야 해?"
- "test plan"
- "testing strategy"
- "coverage gap"
- "what tests should I add?"

Do not use this skill for:

- normal feature or bug implementation
- repository review requests
- simplify or refactor cleanup
- autonomous development loops
- PLAN/PROGRESS/COMPLETED harness setup
- PRD/TRD/ADR document writing
- broad quality audits without a test-planning request

## Default Target

Default target is the current worktree diff.

Start by inspecting:

1. `git status --short`
2. `git diff --stat`
3. `git diff --staged --stat`, when staged changes exist
4. `git diff`
5. `git diff --staged`, when staged changes exist

Use `git status --short` to identify relevant untracked files. Untracked files do not appear in `git diff`; read only new source, test, docs, config, or example files that clearly belong to the current change.

When both staged and unstaged changes exist, treat them together as the user's effective change for planning. If the same file has staged and unstaged edits, mention the split state when it affects confidence or when the final committed change may differ from the current worktree.

If the user specifies a feature, file, directory, module, issue, PR, commit range, or manual scope, use that explicit scope instead of the default diff.

If there is no diff and no explicit target, produce a small report saying there is no concrete target and state what input would be needed.

## Repository Context

Read only enough context to design useful tests:

- `AGENTS.md`, if present
- `docs/PLAN.md` and `docs/PROGRESS.md`, if present, as read-only task context
- package, build, test, and lint configuration
- CI workflow files when relevant
- existing tests, fixtures, mocks, examples, and snapshots adjacent to the target
- source entrypoints, routes, CLI commands, API handlers, schemas, or public interfaces touched by the target

Use `rg --files` for fast discovery. Do not deeply audit the entire project unless the user explicitly asks for a broad test strategy.

Do not invent frameworks, commands, or conventions. If the repo does not reveal a test command or framework, mark it as `확인 필요`.

## Planning Heuristics

Design tests around observable behavior and risk:

- changed public API, CLI output, config shape, schema, or user-visible behavior
- edge cases, invalid input, empty state, boundaries, and failure paths
- security, authorization, trust boundaries, data loss, and unsafe side effects
- compatibility and migration-sensitive behavior
- async, concurrency, IO, network, browser, or external service boundaries
- regressions implied by the diff or task context

Recommend only relevant levels:

- unit
- integration
- CLI/API/browser/e2e
- smoke
- regression
- snapshot or golden output, only when the repo already uses that style or the output contract justifies it

Prefer the smallest test that gives confidence. Do not require e2e tests when unit or integration tests cover the risk better.

## Report Format

Use Korean by default unless the repository or user clearly uses another language. Keep code, paths, command names, and identifiers in their original form.

Produce this shape:

```md
## Test Plan Report

### Target
- Scope:
- Evidence:

### Behavior And Risk Summary
- ...

### Recommended Test Cases
| Priority | Level | Case | Acceptance / Risk Covered | Suggested Location |
|---|---|---|---|---|
| P1 | unit/integration/... | ... | ... | ... |

### Execution Order
1. ...

### Fixtures / Mocks / Data
- ...

### Verification Commands
- `command`: what it proves

### Coverage Gaps / Residual Risk
- ...

### Acceptance / Risk Coverage
- Requirement or risk: covered by test case(s) ...

### PLAN.md Reflection
- Recommended: yes/no
- Suggested PLAN item, if useful:
```

Prioritize test cases:

- `P1`: must-have coverage for likely regressions or important behavior.
- `P2`: important edge cases or integration coverage.
- `P3`: nice-to-have confidence or broader coverage.

Keep the report actionable. Avoid generic testing advice.

At the end, ask whether the user wants the plan reflected in `docs/PLAN.md` when that would be useful.

## Optional PLAN.md Reflection

Do not edit files by default.

If the user explicitly asks to reflect the plan in `docs/PLAN.md`:

1. Re-check `git status --short`.
2. Read `AGENTS.md`, `docs/PLAN.md`, and `docs/PROGRESS.md` if present.
3. Look for an equivalent active roadmap if `docs/PLAN.md` is missing or the repo clearly documents another workflow, such as `docs/tasks.md`, `docs/status/*`, `business/**`, or repo-specific planning docs.
4. Preserve the existing harness style, headings, active/pending structure, and language.
5. Before editing, check the target planning file's status. If it is modified, staged, or untracked with unrelated user changes, merge conservatively only when safe; otherwise stop and ask for direction.
6. Add only test-planning work items derived from the report.
7. Do not update `docs/PROGRESS.md` or `docs/COMPLETED.md` unless the user explicitly asks.
8. Do not implement tests.

If there is no `docs/PLAN.md` and no clear equivalent active roadmap, do not create a harness from this skill. Tell the user to use the project harness skill or ask explicitly for PLAN creation.

## Safety Boundaries

Do not:

- implement tests or production code
- add dependencies
- change expected outputs, snapshots, public examples, README instructions, or user-facing behavior descriptions
- run formatters or codegen that rewrite tracked files
- run migrations
- commit, push, tag, release, or deploy
- call live external systems unless the user explicitly asks
- update `docs/PLAN.md` unless the user explicitly asks after seeing the report
- update `docs/PROGRESS.md` or `docs/COMPLETED.md` unless explicitly asked

Do not run verification commands by default. This skill's default output is a plan, not executed validation. Run a local, non-mutating command only when the user explicitly asks, or when a quick command is necessary to identify the repository's real test command or framework for an accurate plan.

If a command needs production credentials, remote writes, billing systems, destructive migrations, or live external systems, list it as blocked/risky instead of running it.

## Final Response

Default final response is the test plan report.

If no concrete target exists, say so clearly and list the smallest useful target the user can provide.

If `docs/PLAN.md` was updated by explicit user request, include:

- changed file
- inserted or updated PLAN item summary
- verification not run, unless a non-mutating check was relevant
