---
name: plan-done
description: Create, update, simplify, or reconcile lightweight docs/PLAN.md and bounded docs/DONE.md project state files, including executable phase/slice plans, without turning PLAN.md into AGENTS.md. Use for 작업 상태 문서, 세션 재개 문서, PLAN.md/DONE.md 관리, phase decomposition, or cleanup of bloated plans.
---

# Plan Done

Use this skill to maintain a small project state harness:

```text
docs/PLAN.md = current/future work only, preferably as executable slices
docs/DONE.md = recent completed work only, latest 30 entries
AGENTS.md    = agent operating rules, only when explicitly requested
```

## Core Rule

`docs/PLAN.md` is not `AGENTS.md`.

Do not put these in `docs/PLAN.md`:

- agent operating rules
- commit/stage/push rules
- subagent rules
- broad tool usage policy
- long "correction" or postmortem sections
- generic safety philosophy
- repeated external-evidence disclaimers
- completed work history
- large status dashboards
- boilerplate that does not tell the next agent what to build next

If those rules are needed, they belong in `AGENTS.md`, and only if the user
explicitly asks to update AGENTS.md.

## Planning Principle

Write `docs/PLAN.md` for implementation, not contemplation.

When `다음 액션` is abstract, rewrite it into small executable slices. Each slice
must name likely edit files, concrete change, exact verification, observable
done condition, and one guardrail. Prefer one next delegated slice over a broad
phase handoff.

If active work exists, include exactly one `## Next` section at the top of
`docs/PLAN.md` so a low-cost implementation agent can start without scanning
the whole file. Do not include hidden reasoning, speculative alternatives,
pasted code, logs, diffs, or tutorial text.

## Startup Inspection

Read only enough context to write a useful active plan.

Usually inspect:

1. `AGENTS.md`
2. existing `docs/PLAN.md`
3. existing `docs/DONE.md` only if recent history is needed
4. important product/build files named by the user or obvious from the task
5. nearby tests/build files needed to make verification concrete

Use `rg --files` for discovery. Do not audit the whole repository unless the
user asked for a broad plan from scratch.

## Output Scope

Default editable files:

- `docs/PLAN.md`
- `docs/DONE.md`

Do not edit `AGENTS.md` unless the user explicitly asks for AGENTS.md or agent
operating rules.

Do not create PRD/TRD/ADR, README, scripts, references, assets, or extra docs
for this harness unless explicitly requested.

## PLAN.md Shape

Keep `docs/PLAN.md` compact and actionable.

Preferred structure:

```md
# PLAN.md

## Goal

<1-3 sentences about the current milestone and concrete finish state.>

## Next

- 위임: P<N>.<M>
- 목표:
- 파일:
- 검증:

## Active

### P<N> - <short concrete name>

- 상태: pending | in_progress | blocked
- 목표:
- 범위:
  - 수정:
  - 참조:
  - 보존:
- slices:
  1. P<N>.1 - <verb + object>
     - 파일:
     - 변경:
     - 검증:
     - 완료:
     - 금지:
- 검증:
- 완료:

## Backlog

- <optional future work, 3-10 bullets>
```

Add `## Acceptance Bar` after `## Goal` only when it prevents ambiguity about
"done". Keep it to 5-8 bullets.

Each Active item must be enough for the next agent to identify the edit files,
change, verification, and exit condition. For tiny tasks, use one slice and
keep `## Next` pointing at it.

Avoid vague verbs such as "정리한다", "개선한다", "보강한다", "검토한다",
or "반영한다". Prefer concrete verbs such as "add `<function>`", "extend
`<schema>` with `<field>`", "render `<state>` in `<component>`", or "add a
regression test for `<case>`".

If a verification command is unknown, write the smallest discovery action
instead of a vague placeholder:

```md
- 검증:
  - `rg -n "test|vitest|jest|npm run" package.json -g 'package.json'`
```

## Phase and Slice Size

A slice should usually edit 1-4 files. Split a phase if it touches more than 8
likely edit files or mixes unrelated domains such as schema, state wiring, UI,
persistence, network/runtime behavior, tests, release/docs, or security/public
claim wording.

Keep at most 3 active phases in `docs/PLAN.md` unless the user explicitly wants
a broader roadmap. Backlog is for future work, not hidden active work.

## Status Guidance

- `pending`: ready to work.
- `in_progress`: currently being worked.
- `blocked`: use only when no meaningful local/source action can continue.

Do not mark a task `blocked` merely because final public claims need external
evidence, credentials, device access, or release approval. If local prep can be
implemented, keep the task `pending` and make the completion criteria local.

## DONE.md Shape

`docs/DONE.md` is a bounded recent log. Keep only the latest 30 completed
entries and delete older entries instead of preserving them elsewhere. New
sessions should not need to read it by default.

Use:

```md
# DONE.md

최근 완료 작업 30개만 보관한다. 오래된 항목은 삭제한다.
새 세션 시작 시 기본적으로 읽지 않는다.

## Recent

### YYYY-MM-DD - <task name>

- 요약:
- 변경:
- 검증:
- 후속:
```

Keep each entry to five bullets or fewer unless the user asks for a detailed
handoff. Do not paste logs, diffs, or full command output.

When `docs/DONE.md` exceeds 30 entries, delete the oldest entries. Do not create
historical backup files, monthly logs, or replacement history files unless
explicitly requested.

## Completion Cleanup

When a task is complete:

1. Remove it from `docs/PLAN.md` Active.
2. Append a short entry to `docs/DONE.md`.
3. If `docs/DONE.md` has more than 30 entries, delete the oldest entries.
4. Update `## Next` to the next unfinished slice, or remove it if no active
   work remains.
5. Leave only current, pending, or genuinely blocked work in `docs/PLAN.md`.

When only a slice is complete but the phase remains active:

1. Remove the completed slice, or mark it done only if the user wants visible
   slice progress.
2. Keep `## Next` pointing at the next unfinished slice.
3. Do not create a running log.

When pausing unfinished work, update the relevant Active item as a current
snapshot. Do not leave a running log.

## Language

Use Korean by default unless the repository or user clearly prefers another
language.
