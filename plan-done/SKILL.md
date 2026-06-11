---
name: plan-done
description: Install or reconcile a lightweight PLAN/DONE project state harness for Codex sessions. Use when the user asks to set up, update, simplify, or improve project state documents, 작업 상태 문서, 세션 재개 문서, 하네스, PLAN.md/DONE.md, or plan/done 관리.
---

# Plan Done

Use this skill to create or reconcile a small project state harness that helps future Codex sessions resume work from a single active plan and a short completion archive.

Core model:

```text
AGENTS.md   = agent operating rules
PLAN.md     = active, pending, blocked, and next work
DONE.md     = short append-only archive of completed and verified work
```

The harness uses only `docs/PLAN.md`, `docs/DONE.md`, and a compact `AGENTS.md` rule section.

## Principles

- Keep the state surface small.
- Make `docs/PLAN.md` the first and usually only state document a new session reads.
- Use `docs/DONE.md` only when historical context is needed or when appending completed work.
- Treat `docs/PLAN.md` active cleanup as the highest-priority completion update.
- Append to `docs/DONE.md` with a short entry, preferably five bullets or fewer.
- Do not keep completed work in `docs/PLAN.md`.
- Do not create PRD, TRD, ADR, README, scripts, references, assets, or extra documentation for this harness unless the user explicitly asks.

## Startup Inspection

Before editing, inspect enough repository context to make the harness useful.

Check, when present:

1. `AGENTS.md`
2. `README.md`
3. `docs/`
4. Existing state files:
   - `docs/PLAN.md`
   - `docs/DONE.md`
5. Important project docs:
   - `docs/product/**`
   - `docs/architecture*`
   - `docs/development*`
   - `docs/testing*`
   - `docs/prd*`
   - `docs/trd*`
   - `docs/adr*`
   - `PRODUCT.md`
   - `DESIGN.md`
6. Build and validation entry points:
   - `package.json`
   - `pyproject.toml`
   - `Cargo.toml`
   - `go.mod`
   - `Makefile`
   - `justfile`
   - `.github/workflows/**`

Use `rg --files` for discovery. Do not audit the whole codebase; gather only enough to identify project purpose, active work, likely validation commands, and existing harness state.

## Output Files

Create or reconcile only:

- `docs/PLAN.md`
- `docs/DONE.md`
- `AGENTS.md`

Never erase useful historical content without explicit user approval.

## PLAN.md Shape

`docs/PLAN.md` contains current and future work only.

Use this compact structure:

```md
# PLAN.md

## Goal

<current milestone or "현재 active 작업 없음">

## Active

### <task name>

- 상태: pending | in_progress | blocked
- 목표:
- 완료 기준:
- 다음 액션:
- 검증:
- 관련 파일:

## Backlog

- ...
```

When there is no active work, make that clear once. Do not fill the file with empty boilerplate.

## DONE.md Shape

`docs/DONE.md` is a short append-only archive. A new session does not read it by default.

Use this compact structure:

```md
# DONE.md

완료된 작업의 짧은 append-only archive다. 새 세션 시작 시 기본적으로 읽지 않는다.

## Archive

### YYYY-MM-DD - <task name>

- 요약:
- 변경:
- 검증:
- 결정:
- 후속:
```

Keep each entry to five bullets or fewer unless the user asks for a detailed handoff.

## Completion Rule

When pausing unfinished work, update the relevant Active task in `docs/PLAN.md` as a current snapshot, not a running log.

When a task is complete:

1. Remove it from `docs/PLAN.md` Active.
2. Append a short entry to `docs/DONE.md`.
3. Leave only still-active, blocked, or future work in `docs/PLAN.md`.

If context is running long and only one update can be trusted, update `docs/PLAN.md` first. A stale active plan is more damaging than a missing archive entry.

## AGENTS.md Rules

Add or reconcile a compact section like this:

```md
## 작업 상태 문서

- 새 세션은 작업 전 `docs/PLAN.md`만 먼저 읽는다.
- 과거 완료 맥락이 필요할 때만 `docs/DONE.md`를 읽는다.
- 신규/진행/blocked 작업은 `docs/PLAN.md`에 기록한다.
- 완료된 작업은 `docs/DONE.md`에 5줄 이하로 append한 뒤 `docs/PLAN.md`의 Active에서 제거한다.
- `docs/PLAN.md`는 현재와 미래만 담고, 완료 이력은 남기지 않는다.
- 코드 변경과 문서 업데이트는 같은 작업 단위에서 처리한다.
```

If the project already has richer `AGENTS.md` guidance, preserve it and add only missing state-document rules. Keep this section compact.

## Language

Use Korean by default unless the repository clearly uses another language.
