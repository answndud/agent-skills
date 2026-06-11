---
name: simplify
description: Use only when the user explicitly asks to simplify, clean up, refactor, make code more readable, reduce duplication, improve naming, or do a commit-before cleanup pass, including Korean requests like "커밋 전 정리", "리팩터링", or "코드 단순화". This skill directly performs behavior-preserving cleanup on a concrete diff/scope. Do not use for normal implementation, repo-review, test planning, Codex /goal execution, harness setup, PRD/TRD/ADR writing, migrations, dependency changes, releases, or broad architecture rewrites.
---

# Simplify

Execution skill for small, behavior-preserving cleanup.

Use this after a feature, fix, or task works and the user wants the code made easier to read or maintain. This skill edits files; it is not a review report and not a test-planning skill.

## Activation

Use only for explicit cleanup/simplification requests:

- `simplify`, `clean up`, `refactor`
- `make this readable`, `reduce duplication`, `improve naming`
- `커밋 전 정리`, `리팩터링`, `코드 단순화`

Do not use for normal implementation, read-only review, test planning, autonomous loops, PLAN/DONE harness setup, PRD/TRD/ADR writing, dependency changes, migrations, releases, deployment work, or broad architecture rewrites.

## Target

Default target is the current worktree diff.

Inspect:

1. `git status --short`
2. `git diff --stat`
3. `git diff`
4. staged diff/stat when staged changes exist
5. relevant untracked files

If the user specifies files, directories, symbols, commits, or another scope, use that. If there is no diff and no target, say there is nothing to simplify.

Read `AGENTS.md` and `docs/PLAN.md` only for constraints/current task context. Read `docs/DONE.md` only when past completed context matters. Do not update task-state docs unless explicitly asked.

## Allowed Cleanup

Prefer existing repository style, helpers, APIs, parsers, and module boundaries.

Allowed:

- remove duplication, dead code, debug leftovers, stale comments, redundant checks
- simplify branches, nesting, naming, imports, and private/internal helpers
- reuse existing local utilities
- tighten tests, fixtures, docs, or examples for readability
- extract a helper only for clear duplication or meaningful complexity
- split or move small private code only when locality clearly improves

Forbidden unless explicitly requested:

- observable behavior changes
- public API, CLI output, schema, config format, persisted data, error message, snapshot, expected output, README instruction, or user-facing behavior changes
- dependency changes
- broad rewrites or large file moves
- rewriting formatters/codegen
- commits, pushes, deploys, live external systems

If a cleanup might change behavior, report it as deferred instead of applying it.

## Edit Guard

Before editing, re-check `git status --short`.

- Avoid unrelated modified, staged, or untracked files.
- Preserve staged/unstaged split where practical.
- If a file has mixed unrelated edits, edit only safe relevant hunks or stop.
- Do not stage files unless explicitly asked.
- Keep the diff small enough to review.

## Verification

Run the narrowest relevant non-mutating verification when practical:

- focused tests
- typecheck
- lint check that does not rewrite files
- build
- smoke check

If verification cannot run, state why. If post-cleanup verification fails and the failure is new or unclear, revert only your cleanup for the risky hunk/file and report blocked.

Never hide behavior drift by updating tests, snapshots, expected output, or docs to match a new result.

## Final Response

Use Korean by default.

If completed:

```text
SIMPLIFY_COMPLETE

- Simplified:
- Deferred:
- Verification:
- Changed Files:
```

If blocked:

```text
SIMPLIFY_BLOCKED

- 중단 이유:
- 위험 근거:
- 필요한 결정:
- 마지막 검증:
```

Keep it concise. Do not create a commit.
