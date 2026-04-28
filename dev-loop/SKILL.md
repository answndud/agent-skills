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

These are default paths, not hard requirements. If the repository already has equivalent active roadmap, progress log, or completed archive documents, use and preserve the existing structure instead of creating duplicates. Examples include `docs/status/*`, `docs/tasks.md`, `business/**` workflow docs, or repo-specific active/archive docs named differently.

Startup:

1. Read `AGENTS.md` if it exists.
2. Read `docs/PLAN.md` if it exists.
3. Read `docs/PROGRESS.md` if it exists.
4. Look for equivalent roadmap/progress/archive docs if the default paths are missing or the repo clearly documents another workflow.
5. Do not read archive docs such as `docs/COMPLETED.md` by default.
6. Read archive docs only when past implementation context is necessary.

If active roadmap, progress log, or completed archive docs are missing, create the minimum task-specific harness only because the user requested this workflow for the current task. Use the repository's existing equivalent location if one is obvious; otherwise use the default `docs/PLAN.md`, `docs/PROGRESS.md`, and `docs/COMPLETED.md` paths. Inspect enough context first to make it useful:

- `README.md`, if present
- package or build config such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, or `justfile`
- existing product, technical, policy, or architecture docs when obvious
- CI workflow files when obvious

Do not invent product requirements. Mark unknowns as `확인 필요` or record the narrowest safe assumption.

When no active work remains and the selected task or milestone is complete, the active roadmap and progress log should visibly contain a single clear state:

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

If details are missing, make the narrowest safe assumption and record it in the progress log. Stop and ask only when ambiguity affects correctness, public API behavior, security, credentials, permissions, billing, production, user data, or destructive changes.

## PLAN.md Refill Policy

The active roadmap document is the loop's active queue. The agent must keep it populated with the next useful work until the selected task or milestone is complete or blocked.

Preserve the repository's existing heading style and terminology. Use names such as `In Progress`, `Active Plan`, and `Pending` only for a newly created default harness or when those headings already exist. If the repo uses headings such as `현재 우선순위`, `작업 목록`, `Next`, or `Backlog`, add or promote work inside that existing structure.

Before changing code:

1. If the user's requested task or milestone is not represented in the active roadmap, add it before implementation.
2. Break the task into the smallest reviewable stories that can move independently.
3. Put exactly one story in the repository's current/in-progress section.
4. Put known remaining stories in the repository's pending/backlog/next section.
5. Each story must include:
   - status: `pending`, `in_progress`, or `blocked`
   - goal
   - scope
   - non-goals
   - acceptance criteria
   - verification commands
   - next action

During the loop:

- Continue current work from the progress log first.
- Otherwise continue the current `in_progress` story from the active roadmap.
- Otherwise promote the highest-priority pending story.
- If active and pending work are empty but the selected task or milestone is not complete, synthesize the next smallest story from remaining acceptance criteria, failed verification, review findings, or documented gaps, then add it to the active roadmap before implementation.
- If new work is discovered, add only work required for the selected task or milestone. Put unrelated ideas into follow-up notes or leave them out.
- If the next story requires a product, architecture, security, auth, credential, billing, production, or data-loss decision, stop as blocked instead of guessing.

## Loop Algorithm

Repeat while useful work remains:

1. Read active state: `AGENTS.md`, the active roadmap, and the progress log.
2. Ensure the requested task is represented in the active roadmap; if not, add the task contract and first small story.
3. Select one coherent story using the PLAN refill policy.
4. Keep exactly one small story in the current/in-progress area.
5. Update the progress log before implementation with current state, changed files if known, blocker, verification plan, and next action.
6. Implement the smallest reviewable change that moves the story forward.
7. Keep code and documentation aligned in the same story.
8. Run relevant verification: tests, build, lint, typecheck, smoke checks, direct local execution, or repository-defined scripts.
9. Record commands and results in the progress log.
10. Review `git diff --stat` and relevant diffs for regressions, missing tests, public interface drift, output/schema drift, and documentation drift.
11. Compare the story against its acceptance criteria and verification results.
12. If the story is incomplete, update the active roadmap and progress log with the remaining work and continue.
13. If the story is complete, append a detailed entry to the completed archive.
14. Remove completed work from the active roadmap and progress log.
15. Add or promote the next story when the milestone still has unmet acceptance criteria.
16. Commit locally only if the user explicitly requested commits for this loop or repository instructions clearly require local commits. Before committing, re-check `git status --short`, identify exactly which files belong to this story, and do not commit unrelated modified, staged, or untracked files.
17. Continue until the selected task or milestone is complete, or stop as blocked.

## Document Rules

Active roadmap document:

- contains only current and future work
- includes goal, priority, in-progress story, pending stories, completion criteria, next execution order, and verification commands
- is updated before code when scope, priority, or next work changes
- is refilled automatically with the next required story while the selected task or milestone remains incomplete
- does not keep completed work

Progress log document:

- contains only the current incomplete state
- records current task, state summary, blocker, changed files, recent verification, failures, and next action
- is updated before implementation and after meaningful implementation, documentation changes, review, verification, or interruption
- does not keep completed history

Completed archive document:

- is append-only
- uses continuous numbering only inside that file when the repository already follows that convention
- keeps oldest entries above newest entries
- includes completion date, background, changes, code/docs touched, verification commands and results, final result, and remaining risks or follow-up work
- preserves the repository's existing archive style when it is already consistent

## Completion Criteria

Return `LOOP_COMPLETE` only when all are true:

- the user's selected task or milestone is satisfied
- active roadmap acceptance criteria are satisfied
- relevant verification passed, or inability to verify is explicitly documented with a reason
- self-review did not find unresolved regressions or missing required tests
- code and documentation are consistent
- completed work was appended to the completed archive
- completed work was removed from the active roadmap and progress log
- when no active work remains, active docs show `현재 active 작업 없음`

If any acceptance criterion remains unmet, add or promote the next story in the active roadmap and continue instead of returning `LOOP_COMPLETE`.

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

Verification should default to local and non-mutating commands. Do not run verification that requires production credentials, billing systems, remote writes, deploy-like side effects, destructive migrations, or live external systems unless the user explicitly asked for that action. If such verification is required, stop as blocked and record the required approval or credential.

If verification cannot be run, record the reason in the progress log.

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

When blocked, update the progress log with current state, blocker, evidence, last verification result, required decision, and suggested next action.

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
