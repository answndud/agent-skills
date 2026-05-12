---
name: plan-progress-completed
description: Use only when the user explicitly asks to install, update, or improve a PLAN/PROGRESS/COMPLETED project harness, 작업 상태 문서, 세션 재개 문서, 초기 하네스, or 작업 중단/재개 가능 문서 세팅. This skill creates or reconciles docs/PLAN.md, docs/PROGRESS.md, docs/COMPLETED.md, and compact AGENTS.md rules after inspecting project context. Do not use for normal coding, one-off edits, autonomous development loops, release loops, or manual step-by-step coding requests.
---

# Plan Progress Completed

## Purpose

Install or reconcile a small project state harness that lets a future session resume work without guessing.

The harness uses four documents:

- `AGENTS.md`: operating rules for agents and sessions
- `docs/PLAN.md`: active roadmap and intended work
- `docs/PROGRESS.md`: current resumable state
- `docs/COMPLETED.md`: append-only archive of completed work

The state documents must stay short. They are not policy manuals.

Core model:

```text
AGENTS.md     = 사용 규칙
PLAN.md       = 앞으로 할 일
PROGRESS.md   = 지금 어디서 멈췄는지
COMPLETED.md  = 끝난 일의 archive
```

This skill sets up durable task state. It does not implement product features, run an autonomous loop, or perform release work.

---

## Activation Rules

Use this skill only when the user explicitly asks for a project state harness, such as:

- "PLAN/PROGRESS/COMPLETED 하네스 만들어줘"
- "작업 상태 문서 세팅"
- "세션 재개 문서 만들어줘"
- "초기 하네스 적용"
- "작업 중단/재개 가능하게 문서 세팅"
- "plan-progress-completed 적용"
- "이 하네스 수준을 높여줘"
- "작업 상태 문서 정리해줘"

Do not use this skill for:

- normal coding requests
- one-off documentation edits
- feature implementation
- autonomous completion loops
- release loops
- code reviews that do not ask for harness installation or improvement
- manual step-by-step coding tasks

---

## Startup Inspection

Before editing, inspect enough repository context to make the harness useful, not merely present.

Inspect, when present:

1. `AGENTS.md`
2. `README.md`
3. Whether `docs/` exists
4. Whether these files already exist:
   - `docs/PLAN.md`
   - `docs/PROGRESS.md`
   - `docs/COMPLETED.md`
5. Existing product, technical, or policy docs:
   - `docs/product/**`
   - `docs/architecture.md`
   - `docs/development-workflow.md`
   - `docs/testing-and-validation.md`
   - `docs/domain-context.md`
   - `docs/prd*`
   - `docs/trd*`
   - `docs/adr*`
   - `business/**`
   - `PRODUCT.md`
   - `DESIGN.md`
6. Build, package, validation, and CI entry points:
   - `package.json`
   - `pyproject.toml`
   - `Cargo.toml`
   - `go.mod`
   - `Makefile`
   - `justfile`
   - `.github/workflows/**`

Use fast file discovery such as `rg --files` when available.

Do not deeply audit the whole codebase. Gather only enough to identify:

- project purpose
- important documents to read first
- obvious current milestone or active work
- known blockers, if already documented
- obvious verification commands
- existing harness state

If files already exist, preserve user content and merge conservatively. Do not overwrite or delete document history.

---

## Quality Target

The result should be a practical handoff harness, not empty boilerplate.

For an existing project, safely reflect:

- project purpose or current milestone
- important documents to read first
- current active or pending work, if already documented
- known blockers, if already documented
- obvious verification commands from project config
- archive and handoff expectations

For an empty or very early project:

- keep the documents minimal
- mark unknowns honestly
- do not invent product requirements
- do not invent implementation plans
- do not invent validation results

---

## Output Files

Create missing files only:

- `docs/PLAN.md`
- `docs/PROGRESS.md`
- `docs/COMPLETED.md`

Update `AGENTS.md` with a compact `작업 상태 문서` section.

Do not create any of the following unless the user explicitly asks:

- PRD
- TRD
- ADR
- skills
- MCP config
- subagents
- hooks
- release files
- extra documentation outside this harness

---

## Document Design Rules

The generated state documents must be small.

Rules belong primarily in:

- this skill
- `AGENTS.md`

State belongs in:

- `PLAN.md`
- `PROGRESS.md`
- `COMPLETED.md`

Avoid putting long operating rules inside the state documents.

### Active-none State

When no active work remains:

- `PLAN.md` should clearly show `현재 active 작업 없음`
- `PROGRESS.md` should clearly show `현재 active 작업 없음`
- Do not repeat that phrase under many sections
- Do not keep completed work in active documents

### Language

Use Korean by default unless the repository clearly uses another language.

---

## AGENTS.md Rules

Add or reconcile a compact section with this meaning.

Preferred section:

```md
## 작업 상태 문서

- 새 세션은 작업 전 `docs/PLAN.md`와 `docs/PROGRESS.md`를 읽는다.
- `docs/COMPLETED.md`는 완료 archive이며, 과거 맥락이 필요할 때만 읽는다.
- 범위, 우선순위, 신규 작업은 `docs/PLAN.md`에 기록한다.
- 진행 상태, 변경 파일, 검증 결과, blocker, 다음 액션은 `docs/PROGRESS.md`에 기록한다.
- 완료된 작업은 `docs/COMPLETED.md`에 append한 뒤 active 문서에서 제거한다.
- active 작업이 없으면 `PLAN.md`와 `PROGRESS.md`는 `현재 active 작업 없음`만 명확히 표시한다.
- 코드와 문서 변경은 같은 작업 단위 안에서 정렬한다.
```

When the project already has richer `AGENTS.md` guidance:

- preserve existing guidance
- add only missing state-document rules
- keep the new section compact
- do not duplicate existing rules

If useful and still compact, also add:

- `먼저 볼 파일`
- short document map
- normal validation commands or where to find them

Do not turn `AGENTS.md` into a long process manual.

---

## PLAN.md Template

`PLAN.md` contains only active roadmap and intended work.

For a new harness with no active work:

```md
## PLAN.md

목표: 확인 필요

### 범위/원칙

- 확인 필요

### Active

현재 active 작업 없음
```

For active or pending work:

```md
## PLAN.md

목표: <프로젝트 또는 현재 마일스톤 목표>

### 범위/원칙

- <확인된 범위 원칙>
- <확인된 우선순위>

### Active

#### <작업 제목>
- 상태: `pending` | `in_progress` | `blocked`
- 목표:
- 완료 기준:
- 다음 액션:
```

Optional fields may be added only when useful:

```md
- 제외:
- 검증:
- 관련 문서:
```

Do not keep completed work in `PLAN.md`.

When all active work is done, collapse active content to:

```md
현재 active 작업 없음
```

---

## PROGRESS.md Template

`PROGRESS.md` contains only the current resumable state.

For a new harness with no active work:

```md
## PROGRESS.md

현재 active 작업 없음
```

For active or blocked work:

```md
## PROGRESS.md

### 현재 상태

- 작업:
- 상태:
- 변경/탐색한 파일:
- blocker:
- 직전 검증:
- 다음 액션:
```

Guidelines:

- Keep this file short.
- Do not use it as an ever-growing logbook.
- Include failed commands and blockers plainly.
- Include the next action clearly enough for a fresh session to continue.
- When a task is completed, move the final summary and verification result to `COMPLETED.md`, then remove it from `PROGRESS.md`.
- If no active work remains, leave only a clear `현재 active 작업 없음` state.

---

## COMPLETED.md Template

`COMPLETED.md` is an append-only archive.

For a new harness:

```md
## COMPLETED.md

완료된 작업의 append-only archive다. 새 세션 시작 시 필수로 읽지 않는다.

## Archive

아직 완료 archive 없음.
```

When a task is completed, append a compact entry:

```md
#### 001: <작업 제목>

- 완료일: YYYY-MM-DD
- 요약:
- 변경:
- 검증:
- 남은 리스크:
```

Optional fields may be added only when useful:

```md
- 배경:
- 관련 파일:
- 후속 작업:
```

Archive rules:

- For new harnesses, use continuous numbers such as `001`, `002`, `003`.
- Append new entries at the bottom.
- Keep older work above newer work.
- Do not renumber existing entries.
- Do not move existing archive entries.
- Do not rewrite the meaning of existing completed entries.
- If an existing project already uses a date-based or otherwise consistent archive format, preserve that format instead of forcing numbered entries.

---

## Merge Policy

When existing harness files are present:

- do not overwrite them wholesale
- preserve active work
- preserve blockers
- preserve archive entries
- preserve existing numbering or date-based archive format
- do not renumber completed entries
- do not move completed entries
- do not delete document history
- do not force this exact template when the existing structure is equivalent or richer
- add only missing operational rules
- make the smallest compatible edit when structures conflict

If the existing structure conflicts with this skill, preserve user content first and mention the difference in the final response.

---

## Safety Boundaries

Do not:

- commit, push, tag, release, or deploy unless the user explicitly asks
- run destructive commands
- delete existing docs history
- move completed archive entries
- renumber existing completed entries
- install unrelated tools
- create unrelated project documents
- turn this harness into an autonomous development loop
- invent product decisions
- invent credentials
- invent production status
- invent validation results

---

## Verification

After installation or reconciliation:

1. Show changed paths.
2. Verify required files exist:
   - `docs/PLAN.md`
   - `docs/PROGRESS.md`
   - `docs/COMPLETED.md`
   - `AGENTS.md`
3. Inspect the first sections of:
   - `AGENTS.md`
   - `docs/PLAN.md`
   - `docs/PROGRESS.md`
   - `docs/COMPLETED.md`
4. Confirm `AGENTS.md` stayed compact.
5. Confirm `PLAN.md` and `PROGRESS.md` do not repeat active-none state noisily.
6. Confirm completed work is not retained in active documents.
7. Run normal repository tests only if:
   - the harness change is inside a repository, and
   - the command is obvious, and
   - running it is safe and proportionate.

If tests are not run, state why.

---

## Final Response

Keep the final response concise.

Include:

- created or updated files
- whether existing content was preserved
- context inspected
- verification performed
- whether tests were run
- any remaining manual follow-up

Do not include long copies of the generated files unless the user asks.
