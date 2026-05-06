---
name: grill-me
description: Relentlessly interview the user in Korean to stress-test a plan, product idea, architecture, design, implementation strategy, PRD/TRD/ADR, or decision before execution. Use when the user explicitly asks to be grilled, challenged, questioned, 압박 질문, 계획 검증, 설계 검증, 의사결정 점검, "grill me", or wants a plan/design examined more rigorously than normal planning.
---

# Grill Me

Use this skill to interrogate a plan until the user and Codex reach shared understanding.

## Language

- Respond in Korean by default.
- Keep technical terms in English when that is clearer, but explain the decision pressure in natural Korean.
- Match the user's tone, but stay direct and rigorous.

## Core Loop

1. Identify the plan, decision, design, or assumption being tested.
2. If the answer can be discovered from the current repository, files, logs, docs, or tools, inspect those first instead of asking the user.
3. Ask exactly one question at a time.
4. For every question, include a recommended answer or default position.
5. Wait for the user's answer before moving to the next branch.
6. Continue until the major dependencies, tradeoffs, risks, and acceptance criteria are resolved.

## Question Style

- Make each question concrete enough to answer now.
- Prefer questions that expose hidden assumptions, irreversible choices, user impact, operational risk, scope creep, or missing success criteria.
- Do not ask broad multi-part questions.
- Do not ask questions just to sound thorough.
- If the user gives a vague answer, tighten it into a concrete decision and confirm with the next question.

## Recommended Answer Format

Use this compact shape:

```text
질문: ...
추천 답변: ...
이유: ...
```

Keep `이유` to one or two sentences.

## Codebase-Aware Behavior

When the plan concerns an existing project:

- Read the minimum relevant files before asking questions whose answers are already in the repository.
- Prefer `rg` and `rg --files` for discovery.
- Ground challenges in observed files, APIs, tests, docs, or constraints.
- State when a recommendation is based on an assumption rather than repository evidence.

## Finish Criteria

Stop grilling when one of these is true:

- The user asks to stop, implement, or summarize.
- The decision tree has no high-impact unresolved branches.
- The next questions would be low-signal or repetitive.

When stopping, summarize:

- confirmed decisions
- unresolved risks or assumptions
- recommended next action
