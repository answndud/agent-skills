---
name: prd-trd-adr
description: Use only when the user explicitly asks to create, update, or reconcile repository-start documents such as PRD/TRD/ADR, 프로젝트 시작 문서, 제품 요구사항 문서, 기술 요구사항 문서, or 아키텍처 결정 기록. This skill writes or updates docs/PRD.md, docs/TRD.md, and docs/ADR.md from repository evidence. Do not use for normal coding, one-off documentation edits, Codex /goal execution, plan-done harness setup, or manual step-by-step coding requests.
---

# PRD TRD ADR

Create or reconcile repository-start documents for future AI coding sessions:

- `docs/PRD.md`: what the product is, who it serves, goals, scope, and acceptance criteria
- `docs/TRD.md`: how the system is currently built, contracts, constraints, risks, and verification
- `docs/ADR.md`: important technical decisions with repository evidence

Default to Korean unless the repository or user clearly requests another language. This skill is documentation-only.

## Activation

Use only when the user explicitly asks for PRD/TRD/ADR or repository-start documentation.

Do not use for normal coding, README-only edits, active task harness setup, autonomous loops, changelogs, or architecture brainstorming unless the user asks to write repository documents.

## Inspection

Gather enough evidence to avoid generic templates:

- `README.md`, `AGENTS.md`
- existing `docs/**`, `business/**`, `PRODUCT.md`, `DESIGN.md`
- package/build manifests and CI
- source entrypoints, tests, schemas, scripts, and public interfaces

Use `rg --files`. Do not deep-audit the whole codebase unless needed to ground the documents.

## Output Paths

Default targets:

- `docs/PRD.md`
- `docs/TRD.md`
- `docs/ADR.md`

Preserve equivalent existing paths instead of creating duplicates. If multiple plausible targets exist, ask before writing. Use `ADR.md`, not `ARD.md`.

If `AGENTS.md` exists, add only a short pointer when useful:

```md
- 프로젝트 시작 문서: `docs/PRD.md`, `docs/TRD.md`, `docs/ADR.md`
```

Do not create `AGENTS.md` only for this skill.

## Merge Policy

When documents already exist:

- preserve useful content
- do not overwrite wholesale
- correct stale content only with repository evidence
- mark uncertainty as `가정`, `오픈 질문`, `추론된 근거`, or `근거 유형: inferred`
- do not invent requirements, future architecture, or decision history

## Document Boundaries

- PRD: product/user perspective, goals, non-goals, scenarios, requirements, scope, success criteria, open questions
- TRD: implementation perspective, architecture, modules, data/API/CLI/event contracts, flows, errors, trust boundaries, operations, tests, verification, risks
- ADR: significant decisions such as framework/runtime, storage, API style, auth model, deployment model, migration strategy, state management, external integration, or test architecture

Avoid turning these into task lists, changelogs, release notes, ideal future architecture, copied code dumps, or command-output archives.

## ADR Rules

Record only decisions with repository evidence.

Each ADR entry should include:

- ID and title
- status: `accepted`, `superseded`, `proposed`, or `deprecated`
- date or `Date unknown`
- context
- decision
- alternatives considered
- consequences
- repository evidence
- evidence type: `explicit` or `inferred`
- open questions, if any

If reasoning is inferred from dependencies, structure, code, or scripts, label it clearly. Do not create fake history.

## Consistency Check

Before finalizing:

- PRD goals do not contradict TRD constraints
- important TRD technical choices are reflected in ADR
- ADR entries cite concrete evidence
- current implementation and intended future structure are separated
- uncertain claims are marked
- documents make sense without previous session context

## Boundaries

Do not implement code, add dependencies, run migrations/codegen, run rewriting formatters, create skill metadata, create extra helper docs, commit, push, tag, release, or deploy.

Do not write requirements or architecture claims without repository evidence.

## Verification

After editing:

1. Show changed paths.
2. Read the first section of each target document.
3. Verify target paths or preserved equivalents.
4. Check that `AGENTS.md`, if changed, received only a short pointer.
5. Search for accidental placeholders except explicit assumptions/open questions.

Run repository tests only when a normal validation command is obvious and proportionate. Otherwise state why tests were not run.

## Final Response

Keep it concise:

- created or updated documents
- context inspected
- existing documents preserved or not
- verification performed
- remaining assumptions or open questions
