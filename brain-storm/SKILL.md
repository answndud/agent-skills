---
name: brain-storm
description: Use only when the user explicitly asks to brainstorm repository-grounded ideas, future features, product improvements, next opportunities, or to clean up brainstorm notes. This skill scans the current codebase, proposes 3-5 grounded ideas, and saves only user-selected ideas under brain-storm/. Do not use for normal coding, dev-loop execution, PRD/TRD/ADR writing, repo-review, or one-off explanations.
---

# Brain Storm

## Purpose

Use this skill before specs, planning, or implementation to explore what could be built or improved next.

This skill is for idea discovery and backlog hygiene. It does not implement code, write PRD/TRD/ADR documents, run development loops, or make commitments that an idea will be built.

## Activation Rules

Use this skill only when the user explicitly asks for ideation or brainstorm cleanup, such as:

- "아이디어 브레인스토밍"
- "다음 기능 아이디어"
- "개선점 발굴"
- "future opportunities"
- "brainstorm notes 정리"
- "이미 구현된 아이디어 찾아줘"
- "brain-storm 해줘"

Do not use this skill for:

- normal coding requests
- `dev-loop` or autonomous implementation loops
- PRD/TRD/ADR document writing
- repository code review
- release notes or changelog writing
- UI prototype generation
- one-off explanations that are not ideation requests

## Modes

Use the mode that matches the request:

- `Brainstorm Mode`: scan the repository, propose 3-5 grounded ideas, then save only the ideas the user selects.
- `Cleanup Mode`: inspect existing `brain-storm/**/*.md` notes, detect implemented candidates, and delete only files the user explicitly approves.

## Principles

- Explore before proposing.
- Diverge before converging: propose varied ideas, not one narrow path.
- Ground every idea in repository evidence.
- One meaningful idea gets one markdown file.
- Prefer actionable ideas over vague product wishes.
- Treat generated ideas as backlog candidates, not approved requirements.
- Delete brainstorm notes only with explicit user approval.

## Repository Scan

Before proposing ideas, inspect enough context to understand the project:

1. `README.md`, if present.
2. `AGENTS.md`, if present.
3. Existing project docs when present:
   - `docs/PRD.md`
   - `docs/TRD.md`
   - `docs/ADR.md`
   - `docs/PLAN.md`
   - `docs/PROGRESS.md`
   - relevant docs discovered with `rg --files docs`, selected by filename, heading, or relation to the request
4. Existing brainstorm notes:
   - `brain-storm/**/*.md`
5. Manifest and config files when present:
   - `package.json`
   - `pyproject.toml`
   - `go.mod`
   - `Cargo.toml`
   - `Makefile`
   - `justfile`
6. Source entrypoints, tests, examples, routes, CLI files, or UI surfaces by using `rg --files` and reading only relevant files.

Do not deeply audit the whole codebase or bulk-read all of `docs/**`. Gather enough to understand product direction, current capabilities, obvious gaps, and constraints.

If the repository is too early or too ambiguous, still propose ideas, but clearly mark assumptions and open questions.

## Directory Rules

Ideas live under the project root `brain-storm/` directory.

Allowed paths:

- `brain-storm/{idea-slug}.md`
- `brain-storm/{domain}/{idea-slug}.md`

Only one nested level is allowed under `brain-storm/`.

Do not create UI prototype folders such as:

- `brain-storm/previews/`
- `brain-storm/design/`

Use lowercase-with-hyphens filenames. For Korean titles, preserve meaning in an English slug or a safe romanized slug.

## Brainstorm Mode

### Step 1: Propose Ideas

Generate 3-5 ideas based on the repository scan.

For each idea, present:

- `Title`
- `Description`: 1-2 sentences
- `Why now`: repository-grounded motivation
- `Complexity`: Low / Medium / High
- `Evidence`: relevant files, docs, modules, routes, CLI commands, or tests
- `Quick sketch`: optional ASCII flow, system sketch, or screen sketch of 3-8 lines

Ideas should be varied in type and scope, such as:

- new capability
- UX or developer-experience improvement
- reliability or safety improvement
- workflow automation
- documentation or onboarding improvement

Ask the user which ideas to save. Do not write idea files before selection unless the user explicitly requests automatic saving.

### Step 2: Deduplicate

For each selected idea:

1. Extract 3-5 key nouns from the title and description.
2. Search existing `brain-storm/**/*.md` for those keywords.
3. Derive the intended slug and exact target path.
4. Check whether the exact target path already exists.
5. If a duplicate, near-duplicate, or exact path conflict exists, ask whether to update the existing file, create a new file with a distinct slug, or skip.
6. Never overwrite a user-authored idea silently.

### Step 3: Save Selected Ideas

Before writing files:

1. Run `git status --short` when the repository is a git worktree.
2. Check whether the target `brain-storm/` files are modified, staged, or untracked.
3. Do not overwrite unrelated user changes. If a target file has existing changes that are not clearly part of this selected idea, stop and ask for direction.
4. If the exact target path exists, update it only after explicit user selection; otherwise choose a new slug or skip.

Create each selected idea file using this structure:

```md
# Idea Title

## Metadata

- Status: candidate
- Created: YYYY-MM-DD
- Source Request: short summary of the user request that led to this idea
- Last Reviewed: YYYY-MM-DD

## Summary

1-2 sentence summary.

## Motivation

Why this matters now, with repository evidence.

## Repository Evidence

- `path/or/symbol`: what it shows

## Proposed Approach

- 3-7 bullets, no code snippets unless needed for clarity.

## Acceptance Criteria

- Observable criteria for judging whether the idea is implemented.

## Complexity

Low / Medium / High, with a one-sentence reason.

## Sketch

```text
Optional ASCII flow, system sketch, or screen sketch.
```

## Open Questions

- 1-3 unresolved product or technical questions.

## Next Step

Recommended next action, such as PRD/TRD/ADR refinement, PLAN entry, or dev-loop milestone.
```

## Cleanup Mode

Use cleanup mode for requests such as:

- "brain-storm 정리"
- "이미 구현된 아이디어 찾아줘"
- "오래된 brainstorm notes 정리"

Steps:

1. List `brain-storm/**/*.md`.
2. For each idea, read title, summary, proposed approach, and acceptance criteria.
3. Extract implementation indicators such as component names, routes, CLI commands, API endpoints, model names, docs, or user-visible behavior.
4. Search source, docs, tests, and examples while excluding generated, vendor, cache, and build output paths.
5. Mark an idea as an implemented candidate only when multiple evidence points clearly match the described functionality.
6. Present candidates with evidence before taking action.
7. Delete only files the user explicitly approves.

Default cleanup search excludes:

- `brain-storm/`
- `.git/`
- `node_modules/`
- `dist/`
- `build/`
- `.next/`
- `coverage/`
- `.venv/`
- `venv/`
- `target/`
- `vendor/`
- generated snapshots or other obvious generated artifacts

Before deleting files:

1. Run `git status --short` when the repository is a git worktree.
2. Confirm each approved file is inside `brain-storm/`.
3. Do not delete modified, staged, or untracked brainstorm files unless the user explicitly approved that exact path after seeing its status.

In non-interactive mode, do not delete files. Report candidates only.

Never delete files outside `brain-storm/`.

## Safety Boundaries

Do not:

- implement code
- add dependencies
- write or edit PRD/TRD/ADR documents
- update `docs/PLAN.md`, `docs/PROGRESS.md`, or `docs/COMPLETED.md`
- create UI prototypes or preview HTML
- create `brain-storm/previews/` or `brain-storm/design/`
- run migrations or codegen
- run formatters that rewrite tracked files
- commit, push, tag, release, or deploy
- delete brainstorm files without explicit user approval
- treat saved ideas as approved requirements

## Final Report

For Brainstorm Mode, include:

```md
## Brain Storm Report

| Field | Value |
|---|---|
| Ideas Proposed | {count} |
| Ideas Saved | {count} |

### Proposed Ideas

- Title — Complexity — saved/skipped

### Saved Files

- `brain-storm/...`

### Suggested Next Steps

- Refine an idea with `$prd-trd-adr`
- Add selected work to `docs/PLAN.md` with `$plan-progress-completed`
- Run a bounded implementation loop with `$dev-loop`
```

For Cleanup Mode, include:

```md
## Brain Storm Cleanup Report

| Field | Value |
|---|---|
| Notes Reviewed | {count} |
| Implemented Candidates | {count} |
| Deleted | {count} |

### Candidates

- `brain-storm/...`: evidence summary
```

If no files are written or deleted, say so clearly.
