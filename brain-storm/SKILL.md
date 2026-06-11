---
name: brain-storm
description: Use only when the user explicitly asks to brainstorm repository-grounded ideas, future features, product improvements, next opportunities, or to clean up brainstorm notes. This skill scans the current codebase, proposes 3-5 grounded ideas, and saves only user-selected ideas under brain-storm/. Do not use for normal coding, Codex /goal execution, PRD/TRD/ADR writing, repo-review, or one-off explanations.
---

# Brain Storm

Generate repository-grounded product or engineering ideas. Default behavior is read-only: propose ideas first, save only after the user selects them.

## Activation

Use only for explicit brainstorming or idea-management requests, such as:

- "브레인스토밍"
- "아이디어 내줘"
- "다음 기능 후보"
- "개선 아이디어"
- "brainstorm"
- "future features"
- "clean up brainstorm notes"

Do not use for normal implementation, code review, PRD/TRD/ADR writing, plan-done harness setup, Codex `/goal` execution, or one-off explanations.

## Modes

- `brainstorm`: default. Inspect the repo lightly and propose 3-5 ideas.
- `save`: only after the user chooses ideas to save.
- `cleanup`: only when the user explicitly asks to review or prune `brain-storm/` notes.

## Repository Scan

Gather enough context to ground ideas without auditing the whole repo.

Prefer:

- `README.md`, `AGENTS.md`
- `docs/PLAN.md`
- `docs/DONE.md`, only when past completed context matters
- PRD/TRD/ADR/product docs when present
- package/build config
- top-level source structure and main entrypoints
- existing tests or TODOs when obviously relevant

Use `rg --files`. Avoid bulk-reading all docs or source files.

## Idea Quality

Good ideas should be:

- grounded in visible repo evidence
- useful to the product, user workflow, reliability, testability, or maintainability
- small enough to become a PRD, issue, PLAN entry, or scoped Codex `/goal`
- explicit about uncertainty and required user decisions

Do not invent unsupported product strategy, business facts, user data, or architecture.

## Brainstorm Output

Return 3-5 candidates in Korean by default:

```md
## Brain Storm Report

### 1. <idea title>
- 요약:
- 근거:
- 기대 효과:
- 구현 범위:
- 리스크/확인 필요:
- 다음 액션:
```

Ask which ideas to save. Do not write files before selection unless the user explicitly requested automatic saving.

## Saving Ideas

Save selected ideas under `brain-storm/`.

File naming:

```text
YYYY-MM-DD-slug.md
```

Saved note shape:

```md
# <Idea Title>

## Metadata
- Date:
- Status: idea
- Source:

## Summary

## Repository Evidence

## Proposed Approach

## Acceptance Criteria

## Risks / Open Questions

## Next Step
```

Before writing, check `git status --short` and never overwrite a user-authored note silently.

## Cleanup Mode

Cleanup is preview-first.

1. List `brain-storm/` files and git status.
2. Identify likely stale, duplicate, empty, or obsolete notes.
3. Show a keep/delete/update recommendation.
4. Delete or rewrite files only after explicit user confirmation.

Never delete files outside `brain-storm/`.

## Boundaries

Do not:

- implement code
- create PRD/TRD/ADR unless explicitly asked
- update `docs/PLAN.md` or `docs/DONE.md` unless explicitly asked
- create prototype folders
- delete notes without confirmation
- claim repo-wide certainty from a light scan

## Suggested Next Steps

When useful, suggest one of:

- refine an idea with `$to-prd` or `$prd-trd-adr`
- break it into tickets with `$to-issues`
- add selected work to `docs/PLAN.md` with `$plan-done`
- start a scoped Codex `/goal` with explicit acceptance criteria
