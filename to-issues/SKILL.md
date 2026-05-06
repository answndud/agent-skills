---
name: to-issues
description: Break a PRD, plan, spec, architecture note, feature idea, or current conversation into implementation issues using thin vertical tracer-bullet slices. Use when the user asks to create issues, 이슈로 쪼개기, 티켓 생성, 작업 분해, implementation tickets, or convert a PRD/spec/plan into independently implementable tasks. Default to Korean output for Korean users.
---

# To Issues

Use this skill to turn a plan or PRD into independently implementable issues.

## Language

- Write in Korean by default.
- Keep product, code, API, and domain terms in English when they are clearer.
- Use issue titles that are short and action-oriented.

## Source Material

Work from what is already available:

- current conversation
- PRD, plan, spec, ADR, or issue body supplied by the user
- repository docs and code
- existing issue tracker item, if the user provides a URL or issue number and a tool is available

If an issue reference is provided, fetch and read its body and relevant comments before drafting.

## Repository Context

If repository context is needed and not already known:

1. Read `AGENTS.md` if present.
2. Read relevant PRD/TRD/ADR/PLAN/PROGRESS docs.
3. Inspect only enough source and tests to understand current architecture and vocabulary.
4. Respect existing ADRs in the affected area.

## Slice Strategy

Break work into tracer-bullet vertical slices.

A good slice:

- delivers a narrow but complete path through all needed integration layers
- is demoable or verifiable on its own
- has clear acceptance criteria
- can be implemented and reviewed independently
- avoids being only a horizontal layer task such as "build database only" or "build UI only"

Prefer many thin slices over a few thick ones.

## HITL vs AFK

Mark each issue:

- `AFK`: can be implemented and merged without more human decisions.
- `HITL`: requires human interaction, such as product choice, architecture decision, design review, copy approval, security decision, billing decision, or credential access.

Prefer `AFK` where the plan already contains enough information.

## Draft First

Before publishing or writing files, present the proposed issue breakdown as a numbered list.

For each issue, include:

- `Title`
- `Type`: `HITL` or `AFK`
- `Blocked by`
- `User stories covered`, when the source material has user stories
- `Acceptance criteria`

Ask the user to approve the granularity and dependency order unless they explicitly asked for direct file output.

## Publishing

If the user asks to publish to an issue tracker and the required tool is available, create issues in dependency order so blockers can reference real issue identifiers.

If no issue tracker is available or configured, output Markdown issue drafts instead. Create files only when the user asks for files or the repository has an obvious issue-draft convention.

Do not close, modify, or archive any parent issue unless the user explicitly asks.

## Issue Body Template

Use this structure:

```markdown
## Parent
Reference the parent issue, PRD, or spec if one exists. Omit this section if none exists.

## What to build
Describe the end-to-end behavior of this vertical slice. Do not describe only one technical layer.

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by
None - can start immediately
```

## Quality Bar

- Keep each issue independently grabbable.
- Make dependencies explicit.
- Avoid file paths and code snippets unless needed for precision.
- Preserve the plan's product intent while making implementation work smaller and safer.
