---
name: dev-loop
description: Use only when the user explicitly asks for a bounded autonomous development loop for a specific task, milestone, release, or completion target, including phrases like "끝까지 개발", "완성될 때까지 반복", "재귀 루프", "계획-개발-리뷰 루프", "v1 완성", or "milestone complete". Do not use for normal coding, small edits, one-off explanations, open-ended refactors, or step-by-step manual control.
---

# Dev Loop

## Purpose

Use this skill for one explicitly requested task or milestone that should be driven through repeated planning, implementation, review, verification, and archival until it is complete or blocked.

This is not a default repository workflow. Do not copy this full workflow into `AGENTS.md` and do not make it permanent repository policy unless the user explicitly asks.

## Activation Rules

Use this skill only when the user clearly asks for an autonomous completion loop, such as:

- "끝까지 개발"
- "완성될 때까지 반복"
- "재귀 루프"
- "계획-개발-리뷰 루프"
- "v1 완성"
- "milestone complete"
- "keep going until this feature is complete"

Do not use this skill for:

- normal coding requests
- small edits
- one-off explanations
- simple reviews
- broad refactors without a completion target
- tasks where the user wants manual step-by-step control

## Durable State

Prefer the repository's existing task harness:

- `docs/PLAN.md`: active roadmap only
- `docs/PROGRESS.md`: current incomplete state only
- `docs/COMPLETED.md`: append-only archive

Startup:

1. Read `AGENTS.md` if it exists.
2. Read `docs/PLAN.md` if it exists.
3. Read `docs/PROGRESS.md` if it exists.
4. Do not read `docs/COMPLETED.md` by default.
5. Read `docs/COMPLETED.md` only when past implementation context is necessary.

If `docs/PLAN.md` or `docs/PROGRESS.md` does not exist, create the minimum task-specific harness only because the user requested this workflow for the current task. Inspect enough context first to make it useful:

- `README.md`, if present
- package or build config such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, or `justfile`
- existing product, technical, policy, or architecture docs when obvious
- CI workflow files when obvious

Do not invent product requirements. Mark unknowns as `확인 필요` or record the narrowest safe assumption.

When no active work remains and the selected task or milestone is complete, `docs/PLAN.md` and `docs/PROGRESS.md` should visibly contain a single clear state:

```text
현재 active 작업 없음
```

## Task Contract

Before implementation, identify or record the contract for the selected task or milestone:

- task name
- goal
- scope
- non-goals
- acceptance criteria
- verification commands
- known risks
- human decisions required

If details are missing, make the narrowest safe assumption and record it in `docs/PROGRESS.md`. Stop and ask only when ambiguity affects correctness, public API behavior, security, credentials, permissions, billing, production, user data, or destructive changes.

## PLAN.md Refill Policy

`docs/PLAN.md` is the loop's active queue. The agent must keep it populated with the next useful work until the selected task or milestone is complete or blocked.

Before changing code:

1. If the user's requested task or milestone is not represented in `docs/PLAN.md`, add it before implementation.
2. Break the task into the smallest reviewable stories that can move independently.
3. Put exactly one story in `In Progress` or `Active Plan`.
4. Put known remaining stories in `Pending`.
5. Each story must include:
   - status: `pending`, `in_progress`, or `blocked`
   - goal
   - scope
   - non-goals
   - acceptance criteria
   - verification commands
   - next action

During the loop:

- Continue current work from `docs/PROGRESS.md` first.
- Otherwise continue the current `in_progress` story from `docs/PLAN.md`.
- Otherwise promote the highest-priority pending story.
- If active and pending work are empty but the selected task or milestone is not complete, synthesize the next smallest story from remaining acceptance criteria, failed verification, review findings, or documented gaps, then add it to `docs/PLAN.md` before implementation.
- If new work is discovered, add only work required for the selected task or milestone. Put unrelated ideas into follow-up notes or leave them out.
- If the next story requires a product, architecture, security, auth, credential, billing, production, or data-loss decision, stop as blocked instead of guessing.

## Loop Algorithm

Repeat while useful work remains:

1. Read active state: `AGENTS.md`, `docs/PLAN.md`, `docs/PROGRESS.md`.
2. Ensure the requested task is represented in `docs/PLAN.md`; if not, add the task contract and first small story.
3. Select one coherent story using the PLAN refill policy.
4. Keep exactly one small story in `In Progress` or `Active Plan`.
5. Update `docs/PROGRESS.md` before implementation with current state, changed files if known, blocker, verification plan, and next action.
6. Implement the smallest reviewable change that moves the story forward.
7. Keep code and documentation aligned in the same story.
8. Run relevant verification: tests, build, lint, typecheck, smoke checks, direct local execution, or repository-defined scripts.
9. Record commands and results in `docs/PROGRESS.md`.
10. Review `git diff --stat` and relevant diffs for regressions, missing tests, public interface drift, output/schema drift, and documentation drift.
11. Compare the story against its acceptance criteria and verification results.
12. If the story is incomplete, update `docs/PLAN.md` and `docs/PROGRESS.md` with the remaining work and continue.
13. If the story is complete, append a detailed entry to `docs/COMPLETED.md`.
14. Remove completed work from `docs/PLAN.md` and `docs/PROGRESS.md`.
15. Add or promote the next story when the milestone still has unmet acceptance criteria.
16. Commit locally only if the user explicitly requested commits for this loop or repository instructions clearly require local commits.
17. Continue until the selected task or milestone is complete, or stop as blocked.

## Document Rules

`docs/PLAN.md`:

- contains only current and future work
- includes goal, priority, in-progress story, pending stories, completion criteria, next execution order, and verification commands
- is updated before code when scope, priority, or next work changes
- is refilled automatically with the next required story while the selected task or milestone remains incomplete
- does not keep completed work

`docs/PROGRESS.md`:

- contains only the current incomplete state
- records current task, state summary, blocker, changed files, recent verification, failures, and next action
- is updated before implementation and after meaningful implementation, documentation changes, review, verification, or interruption
- does not keep completed history

`docs/COMPLETED.md`:

- is append-only
- uses continuous numbering only inside that file when the repository already follows that convention
- keeps oldest entries above newest entries
- includes completion date, background, changes, code/docs touched, verification commands and results, final result, and remaining risks or follow-up work
- preserves the repository's existing archive style when it is already consistent

## Completion Criteria

Return `LOOP_COMPLETE` only when all are true:

- the user's selected task or milestone is satisfied
- `docs/PLAN.md` acceptance criteria are satisfied
- relevant verification passed, or inability to verify is explicitly documented with a reason
- self-review did not find unresolved regressions or missing required tests
- code and documentation are consistent
- completed work was appended to `docs/COMPLETED.md`
- completed work was removed from `docs/PLAN.md` and `docs/PROGRESS.md`
- when no active work remains, active docs show `현재 active 작업 없음`

If any acceptance criterion remains unmet, add or promote the next story in `docs/PLAN.md` and continue instead of returning `LOOP_COMPLETE`.

## Safety Boundaries

Do not:

- turn this workflow into repository default policy
- copy this full workflow into `AGENTS.md`
- start unrelated features
- perform broad refactors unless required by the selected task
- add dependencies without clear justification
- change public APIs unless required by the task
- run destructive commands
- commit unless the user explicitly requested commits for this loop or repository instructions clearly require local commits
- run `git push`, push tags, publish releases, deploy, delete data, rotate credentials, or call live external systems unless the user explicitly asked for that action

## Verification Policy

Never mark work complete from self-review alone.

Prefer repository-defined verification commands. If none are obvious, inspect the package, build, and test config and choose the narrowest valid command.

If verification cannot be run, record the reason in `docs/PROGRESS.md`.

## Stop Conditions

Stop with `LOOP_BLOCKED` when:

- the same verification failure repeats 3 times
- a required product or architecture decision is ambiguous
- credentials, secrets, billing, production, user data, or live deployment are required
- the change could delete data or require destructive migration
- the task requires scope beyond the user's stated goal
- active documents conflict with repository state and cannot be reconciled safely
- continuing would require guessing about security, auth, permissions, money movement, or user data
- PLAN refill would require inventing product direction rather than deriving the next story from the selected task, acceptance criteria, verification failures, or review findings

When blocked, update `docs/PROGRESS.md` with current state, blocker, evidence, last verification result, required decision, and suggested next action.

## Final Response

End with exactly one status block when this skill is used for a development loop.

If active work remains but progress was made:

```text
LOOP_CONTINUE

- 이번에 완료한 일:
- 변경한 파일:
- 실행한 검증:
- 현재 남은 작업:
- 다음 루프에서 바로 할 일:
```

If the selected task or milestone is complete:

```text
LOOP_COMPLETE

- 완료 요약:
- 변경한 파일:
- 실행한 검증:
- COMPLETED.md archive 항목:
- 남은 리스크:
```

If blocked:

```text
LOOP_BLOCKED

- 중단 이유:
- 근거:
- 마지막 검증:
- 필요한 결정:
- 다음 액션:
```
