---
name: simplify
description: Use only when the user explicitly asks to simplify, clean up, refactor, make code more readable, reduce duplication, improve naming, or do a commit-before cleanup pass, including Korean requests like "커밋 전 정리", "리팩터링", or "코드 단순화". This skill directly performs behavior-preserving cleanup on the current worktree diff by default. Do not use for normal implementation, repo-review, dev-loop execution, harness setup, PRD/TRD/ADR writing, or broad architecture rewrites.
---

# Simplify

## Purpose

Use this skill after a feature, fix, or task works, but before commit, to make the current change easier to read and maintain without changing observable behavior.

This is a cleanup/refactor skill, not a feature implementation skill and not a review-only skill. It may edit files directly, but only inside a behavior-preserving cleanup scope.

## Activation Rules

Use this skill only when the user explicitly asks for cleanup or simplification, such as:

- "simplify"
- "clean up"
- "refactor"
- "make this more readable"
- "reduce duplication"
- "improve naming"
- "reorganize this code"
- "커밋 전 정리"
- "리팩터링"
- "코드 단순화"

Do not use this skill for:

- normal feature or bug implementation
- repository review requests
- autonomous development loops
- PLAN/PROGRESS/COMPLETED harness setup
- PRD/TRD/ADR document writing
- broad architecture rewrites
- migrations, dependency changes, releases, or deployment work

## Default Target

Default target is the current worktree diff.

Start by inspecting:

1. `git status --short`
2. `git diff --stat`
3. `git diff --staged --stat`, when staged changes exist
4. `git diff`
5. `git diff --staged`, when staged changes exist

Use `git status --short` to identify relevant untracked files. Untracked files do not appear in `git diff`; read only new source, test, docs, config, or example files that clearly belong to the current change.

When staged changes exist, treat the index as user-owned state. If simplification touches an already staged file, preserve the staged/unstaged split when practical. If preserving the split is not practical, report that the file now has new unstaged cleanup changes and do not stage them automatically.

If the user specifies files, directories, symbols, a commit range, or another explicit scope, use that scope instead of the default diff.

If there is no diff and no explicit target, say there is nothing to simplify and ask for a target only if needed.

## Simplification Goals

Apply small, behavior-preserving changes that improve maintainability:

- remove duplicated logic
- remove unnecessary abstraction or indirection
- reduce excessive branching, nesting, or control flow noise
- improve unclear names when call sites can be updated safely
- remove dead code, debug leftovers, stale comments, or redundant checks
- reuse existing helpers, APIs, parsers, or framework conventions
- move small functions or constants only when it clearly improves locality
- clean tests, fixtures, docs, or examples only for naming, imports, structure, or readability

Prefer the repository's existing style, helpers, and module boundaries. Add a new abstraction only when it removes real duplication or complexity.

Do not change expected test outputs, snapshots, public examples, README instructions, or user-facing behavior descriptions as part of simplify. If those need to change, report the item as deferred because it may represent behavior or contract drift.

## Hard Boundaries

Do not:

- change observable behavior
- change public APIs, CLI flags, CLI output, schemas, config formats, or persisted data formats
- add or remove dependencies
- perform broad rewrites or large file moves
- optimize performance by changing semantics
- rewrite unrelated files
- revert user changes
- run destructive commands
- run formatters or codegen that rewrite tracked files unless the user explicitly asks
- commit, push, tag, release, or deploy
- call live external systems unless the user explicitly asks

If a cleanup would require one of these, do not apply it. Report it as deferred.

## Workflow

### 1. Understand Scope

Read enough surrounding code to know the intended behavior and existing patterns. For changed code, inspect adjacent tests, public interfaces, and helper modules when relevant.

Read `AGENTS.md` if it exists. If `docs/PLAN.md` or `docs/PROGRESS.md` exists, read it only as context for current task intent, relevant validation commands, and repo-specific constraints. Do not update task-state docs from this skill unless the user explicitly asks.

For generated, binary, lockfile, snapshot, or very large diffs, summarize the artifact change and focus edits on source-of-truth files. Do not hand-edit generated artifacts unless the repo clearly treats them as source.

### 2. Pre-Edit Guard

Before editing:

1. Re-check `git status --short`.
2. Identify the exact files this simplification may touch.
3. Avoid unrelated modified, staged, or untracked files.
4. If a target file has mixed unrelated user edits, edit only the relevant hunks when safe; otherwise stop and report `SIMPLIFY_BLOCKED`.
5. If staged and unstaged edits overlap in the same file, preserve the user's split state where possible and mention any confidence limits.
6. Do not run `git add` or otherwise stage files unless the user explicitly asks.

### 3. Edit

Make the smallest reviewable cleanup that improves the diff.

Allowed edits include:

- inline or remove needless wrappers
- extract a helper only for clear duplication
- rename local variables, private helpers, or internal functions for clarity
- replace ad hoc logic with existing local utilities
- simplify conditionals without changing edge-case behavior
- remove unreachable code or debug leftovers when evidence is clear
- tighten comments so they explain why, not what

When unsure whether behavior changes, do not edit that part.

### 4. Verify

Run the narrowest relevant local verification available:

- focused tests for touched behavior
- typecheck
- lint check that does not rewrite files
- build
- smoke check
- repository-defined non-mutating validation command

When practical, run the narrowest relevant baseline verification before editing. If baseline verification is too slow, unavailable, or not obvious, record that the pre-simplify baseline was not established.

Do not run verification that requires production credentials, billing systems, remote writes, deploy-like side effects, destructive migrations, or live external systems unless the user explicitly asked.

If formatter/codegen is necessary but would rewrite tracked files, report it instead of running it unless the user explicitly asked.

If verification cannot be run, state why.

After editing, run the same focused verification when practical. If post-simplify verification fails:

- If the baseline also failed the same way, report the existing failure and keep the cleanup only when the diff is clearly unrelated.
- If the failure is new or the cause is unclear, revert only your simplification changes for the risky hunk or file, then report `SIMPLIFY_BLOCKED`.
- Never hide a behavior change by updating tests, snapshots, expected output, or docs to match the new result.

### 5. Self-Review

Review `git diff --stat` and relevant diffs after editing.

Check specifically for:

- behavior drift
- public contract drift
- changed error messages or output formats
- unrelated churn
- formatting-only noise
- missing tests when logic was materially rearranged

If self-review finds a behavior risk, revert only your own simplification for that hunk or stop as blocked. Never revert unrelated user changes.

## Deferred Simplifications

Report cleanup candidates without applying them when they:

- might change behavior
- require public contract changes
- need a product or architecture decision
- require dependency changes
- are too broad for a commit-before cleanup pass
- need tests that are missing or cannot be run

Deferred items are suggestions, not completed work.

## Final Response

Use Korean by default unless the repository or user clearly uses another language. Keep code, paths, command names, and identifiers in their original form.

If cleanup completed, end with:

```text
SIMPLIFY_COMPLETE

- Simplified:
- Deferred:
- Verification:
- Changed Files:
```

If blocked, end with:

```text
SIMPLIFY_BLOCKED

- 중단 이유:
- 위험 근거:
- 필요한 결정:
- 마지막 검증:
```

Keep the response concise. Do not create a commit.
