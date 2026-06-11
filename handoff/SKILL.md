---
name: handoff
description: Create or consume a handoff when Codex needs to transfer working context from one session, agent, role, or context window to another with no reliable return path. Use when the user asks for a handoff, 인계, 작업 인수인계, session transfer, context transfer, continuation note, resume document, implementation handoff, planner-to-implementer handoff, AFK run setup, parallel-agent handoff, or asks to clear/compact/start fresh while preserving decisions and next steps.
---

# Handoff

Prepare a handoff so another Codex session can continue without access to the current chat. Treat it as a one-way transfer: the receiving session may not be able to ask the original session what was meant.

## Core Rule

Write only information that changes what the next agent should do. Omit generic summaries, praise, and broad background that can be rediscovered cheaply.

## When Creating A Handoff

1. Identify the receiver's job: implementer, reviewer, debugger, planner, parallel worker, or future continuation.
2. Read the current repository state before writing if files may have changed.
3. Capture concrete state, decisions, and remaining work.
4. Make the handoff self-contained enough that a fresh session can start from it.
5. When the user asks for a handoff, respond directly in chat.
6. Do not claim tests passed, commands ran, or files changed unless they actually did.

## Handoff Content

Include these sections when relevant:

- **Goal**: The user-visible objective and current definition of done.
- **Current State**: What has been completed, what is partially done, and what is intentionally untouched.
- **Key Decisions**: Chosen approach, rejected alternatives that matter, and constraints from the user.
- **Files And Entry Points**: Important files, commands, URLs, tickets, PRs, branches, or artifacts.
- **Known Problems**: Failing tests, uncertain assumptions, blockers, risks, or places that need verification.
- **Next Steps**: Ordered, actionable steps for the receiving session.
- **Validation**: Commands already run and their results, plus recommended checks still needed.

## Writing Style

- Be specific enough to execute, not just orient.
- Prefer file paths, function names, command names, and exact decisions over narrative.
- Preserve user constraints verbatim when they are important.
- Mark uncertainty explicitly with `Unknown`, `Assumption`, or `Needs verification`.
- Keep the handoff concise. A good default is one screen for small tasks and a structured page for larger work.

## Consuming A Handoff

When the user provides or points to a handoff:

1. Read the handoff first.
2. Verify current repository state before editing; handoffs can be stale.
3. Reconstruct the objective, constraints, and next step.
4. Continue from the handoff rather than restarting discovery unless the handoff is incomplete or contradicted by the repo.
5. Report any stale or conflicting handoff details before making dependent changes.

## Template

```markdown
# Handoff

## Goal

## Current State

## Key Decisions

## Files And Entry Points

## Known Problems

## Next Steps

## Validation
```
