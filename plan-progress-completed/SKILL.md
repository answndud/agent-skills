---
name: plan-progress-completed
description: Use only when the user explicitly asks to install, update, or improve a PLAN/PROGRESS/COMPLETED project harness, 작업 상태 문서, 세션 재개 문서, 초기 하네스, or 작업 중단/재개 가능하게 문서 세팅. This skill creates or reconciles docs/PLAN.md, docs/PROGRESS.md, docs/COMPLETED.md, and compact AGENTS.md rules after inspecting project context. Do not use for normal coding, one-off edits, autonomous development loops, release loops, or manual step-by-step coding requests.
---

# Plan Progress Completed

## Purpose

Use this skill to install or reconcile a project state harness that lets a future session continue work without guessing:

- `docs/PLAN.md`: active roadmap only
- `docs/PROGRESS.md`: current incomplete state only
- `docs/COMPLETED.md`: append-only archive of completed work
- compact `AGENTS.md` rules that explain how those documents are used

This skill sets up durable task state. It does not run an autonomous development loop and does not implement product features.

## Activation Rules

Use this skill only when the user explicitly asks for a project state harness, such as:

- "PLAN/PROGRESS/COMPLETED 하네스 만들어줘"
- "작업 상태 문서 세팅"
- "세션 재개 문서 만들어줘"
- "초기 하네스 적용"
- "작업 중단/재개 가능하게 문서 세팅"
- "plan-progress-completed 적용"
- "이 하네스 수준을 높여줘"

Do not use this skill for:

- normal coding requests
- one-off documentation edits
- feature implementation
- autonomous completion loops
- release loops
- reviews that do not ask for harness installation or improvement

## Startup Inspection

Before editing, inspect enough repository context to make the harness useful, not just syntactically present:

1. `AGENTS.md`, if it exists.
2. `README.md`, if it exists.
3. Whether `docs/` exists.
4. Whether these files already exist:
   - `docs/PLAN.md`
   - `docs/PROGRESS.md`
   - `docs/COMPLETED.md`
5. Existing product, technical, or policy docs when present:
   - `docs/product/**`
   - `docs/architecture.md`
   - `docs/development-workflow.md`
   - `docs/testing-and-validation.md`
   - `docs/domain-context.md`
   - `docs/prd*`, `docs/trd*`, `docs/adr*`
   - `business/**`
   - `PRODUCT.md`, `DESIGN.md`
6. Build, package, validation, and CI entry points when present:
   - `package.json`
   - `pyproject.toml`
   - `Cargo.toml`
   - `go.mod`
   - `Makefile`
   - `justfile`
   - `.github/workflows/**`

Use fast file discovery such as `rg --files` when possible. Do not deeply audit the whole codebase; gather enough to identify project purpose, important docs, obvious verification commands, and current harness state.

If files already exist, preserve user content and merge conservatively. Do not overwrite or delete existing document history.

## Quality Target

The output should be closer to a practical handoff harness than an empty boilerplate.

For an existing project, reflect what can be safely inferred:

- project purpose or current milestone
- important documents to read first
- current active/pending work, if already documented
- known blockers, if already documented
- obvious verification commands from package or project config
- archive rules and handoff expectations

For an empty or very early project, keep the structure minimal and mark unknowns honestly. Do not invent product requirements or implementation plans.

## Output Files

Create missing files only:

- `docs/PLAN.md`
- `docs/PROGRESS.md`
- `docs/COMPLETED.md`

Update `AGENTS.md` with a short "작업 상태 문서" section. Keep detailed operating rules in the docs templates, not in `AGENTS.md`.

Do not create project-specific PRD, TRD, ADR, skills, MCP config, subagents, hooks, release files, or extra documentation unless the user explicitly asks.

## AGENTS.md Rules

Add or reconcile compact rules with this meaning:

- New sessions or agents read `docs/PLAN.md` and `docs/PROGRESS.md` before work.
- `docs/COMPLETED.md` is an archive and not required startup reading.
- Scope, priority, and new feature changes are recorded in `docs/PLAN.md` before implementation.
- Meaningful implementation, documentation changes, verification, blockers, and interruptions are recorded in `docs/PROGRESS.md`.
- Completed work is archived to `docs/COMPLETED.md`, then removed from active docs.
- `docs/COMPLETED.md` is append-only, time-ordered, and uses continuous numbers for new harnesses.
- `docs/PLAN.md` and `docs/PROGRESS.md` must not retain completed work.
- When no active work remains, active docs show a single clear `현재 active 작업 없음` state.
- Keep code and documentation aligned in the same task.
- Verification commands and results are recorded in `docs/PROGRESS.md`.

When the project already has richer `AGENTS.md` guidance, preserve it. If useful and still compact, add:

- "먼저 볼 파일" for project onboarding.
- A short document map.
- The normal validation commands or where to find them.

## PLAN.md Template

Use Korean by default unless the repository clearly uses another language.

Prefer this shape for new harnesses:

```md
# PLAN.md

기준일: YYYY-MM-DD
목표: <프로젝트 목적 또는 현재 목표를 한 문장으로 적는다. 모르면 `확인 필요`로 둔다.>

## 문서 규칙
- 이 문서는 active roadmap만 유지한다.
- 완료된 작업은 [COMPLETED.md](./COMPLETED.md)에 archive한 뒤 여기서 바로 삭제한다.
- 세션 시작 시 기본으로 읽는 문서는 `PLAN.md`, `PROGRESS.md`, 그리고 `AGENTS.md`다.
- active 문서에는 완료된 작업을 남기지 않는다.
- 모든 active 작업이 끝나면 작업 본문은 전부 삭제하고 `현재 active 작업 없음`만 남긴다.

## 범위 원칙
- <확인된 프로젝트 우선순위나 범위 원칙을 적는다. 없으면 `확인 필요`로 둔다.>

## 현재 우선순위
현재 active 작업 없음

## Active Plan
현재 active 작업 없음

## 다음 실행 순서
현재 active 작업 없음
```

When there is active or pending work, use one small story per item:

```md
### 작업 제목

상태: `pending` | `in_progress` | `blocked`

- 목표:
- 범위:
- 제외:
- 완료 기준:
- 검증:
- 다음 액션:
```

Keep completed work out of `PLAN.md`. If no active work remains, collapse active sections to a single visible `현재 active 작업 없음` state rather than repeating it under every heading.

## PROGRESS.md Template

```md
# PROGRESS.md

기준일: YYYY-MM-DD

## 문서 규칙
- 이 문서는 active 상태, blocker, 최근 검증, 다음 액션만 유지한다.
- 작업이 완료되면 최종 상태와 검증 결과를 [COMPLETED.md](./COMPLETED.md)로 이동하고, active 문서에서는 바로 삭제한다.
- 작업이 모두 끝나면 완료 항목을 archive로 넘긴 뒤 active 본문은 전부 삭제한다.
- 모든 active 작업이 끝난 최종 상태는 `현재 active 작업 없음`만 남긴다.

현재 active 작업 없음
```

When work is active or blocked, use this shape:

```md
## 현재 상태 스냅샷
- 현재 작업:
- 상태:
- 변경/탐색한 파일:

## 열린 blocker
- 없음

## 직전 검증
- 실행 안 함: 이유

## 다음 액션
1. ...

## Archive Pointer
- 과거 맥락이 필요할 때만 [COMPLETED.md](./COMPLETED.md)를 확인한다.
```

`PROGRESS.md` should let a fresh session continue immediately. Include failed commands and blockers plainly; do not hide incomplete state.

## COMPLETED.md Template

````md
# COMPLETED.md

완료된 작업을 시간 오름차순으로 축적하는 append-only archive다. 새 세션 시작 시 필수로 읽지 않는다.

## 운영 규칙
- 완료 항목은 문서 맨 아래에 append한다.
- 번호는 `001`, `002`, `003`처럼 연속 번호를 사용하고 재사용하지 않는다.
- 오래된 작업이 위, 최신 작업이 아래에 오도록 유지한다.
- `docs/PLAN.md`, `docs/PROGRESS.md`에서 제거한 완료 기록을 복기 가능한 수준으로 정리한다.
- raw copy/paste dump가 아니라 사람이 다시 읽기 좋은 요약형 기록으로 작성한다.
- 명백한 오타 수정 외에는 기존 완료 항목의 의미를 바꾸지 않는다.

## 항목 포맷

```md
## 001: 작업 제목

- 완료일: YYYY-MM-DD
- 배경:
- 변경 내용:
- 코드/문서:
- 검증:
- 결과:
- 남은 리스크:
```

## Archive

아직 완료 archive 없음.
````

If an existing project already uses a date-based or otherwise consistent archive format, preserve that format instead of renumbering old entries. For new harnesses, use the numbered format above.

## Merge Policy

When existing harness files are present:

- Do not overwrite them wholesale.
- Preserve archive entries.
- Preserve active work and blockers.
- Do not renumber existing completed entries.
- Do not force this exact template when the existing structure is equivalent or richer.
- Add missing operational rules only when clearly absent.
- If the existing structure conflicts with this skill, make the smallest compatible edit and mention the difference in the final response.

## Safety Boundaries

Do not:

- commit, push, tag, release, or deploy unless the user explicitly asks
- run destructive commands
- delete existing docs history
- move completed archive entries
- renumber existing completed entries
- install unrelated tools
- turn this harness into an autonomous development loop
- invent product decisions, credentials, production status, or validation results

## Verification

After installation or reconciliation:

1. Show the changed paths.
2. Verify all required files exist.
3. Inspect the first sections of `AGENTS.md`, `PLAN.md`, `PROGRESS.md`, and `COMPLETED.md`.
4. Confirm `AGENTS.md` stayed compact.
5. Confirm active-none state is not repeated noisily across many sections.
6. Run the repository's normal tests only if the harness change is in a repository and the command is obvious.

If tests are not run, state why.

## Final Response

Keep the response concise:

- created or updated files
- whether existing content was preserved
- context inspected
- verification performed
- any remaining manual follow-up
