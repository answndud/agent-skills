---
name: to-prd
description: Turn the current Korean or English conversation context, repository understanding, plan, feature idea, or rough requirements into a PRD. Use when the user asks to create a PRD, PRD로 정리, 요구사항 문서화, 제품 요구사항 정리, spec 작성, or convert the current discussion into a product requirements document. Default to Korean output for Korean users.
---

# To PRD

Use this skill to synthesize what is already known into a PRD.

## Language

- Write in Korean by default.
- Preserve product, code, API, and domain terms in English when they are clearer.
- Use concise, implementation-ready Korean rather than marketing copy.

## Core Rule

Do not interview the user by default. Synthesize from:

- the current conversation
- files or docs the user provided
- repository context
- existing plans, ADRs, PRDs, issues, comments, or notes

Ask only when a missing answer would change the PRD's core scope, safety, data model, public API, billing, permissions, or destructive behavior.

## Repository Context

When working inside a project:

1. Read `AGENTS.md` if present.
2. Read existing product or planning docs when obvious:
   - `docs/PRD.md`
   - `docs/TRD.md`
   - `docs/ADR.md`
   - `docs/PLAN.md`
   - `docs/PROGRESS.md`
   - relevant files discovered with `rg --files docs`
3. Inspect package/config and relevant source entrypoints only enough to understand current behavior.
4. Use the project's domain vocabulary.
5. Respect existing ADRs and architecture decisions.

## Deep Module Pass

Before writing the PRD, identify major modules likely to be built or modified.

Prefer deep modules: modules that hide meaningful complexity behind a small, testable interface that should rarely change.

If module boundaries are uncertain, include them as `확인 필요` in the PRD instead of stopping.

## Output Target

If the user asks to publish to an issue tracker and the required tool is available, publish there and apply the project's normal triage label if known.

If no issue tracker is available or configured, create or present a Markdown PRD instead. Prefer the repository's existing PRD location if one exists; otherwise use a clear path such as `docs/PRD.md` only when the user asked for a file.

## PRD Template

Use this structure:

```markdown
# PRD: <feature or product area>

## Problem Statement
Describe the user's problem from the user's perspective.

## Solution
Describe the proposed solution from the user's perspective.

## Goals
- ...

## Non-Goals
- ...

## User Stories
1. As a <user>, I want <capability>, so that <outcome>.

## Implementation Decisions
- Modules to build or modify
- Interfaces or contracts to define
- Technical clarifications
- Architecture decisions
- Schema changes
- API contracts
- Specific product interactions

Do not include fragile file paths or code snippets unless the user explicitly wants an implementation plan.

## Testing Decisions
- What external behavior needs tests
- Which modules or flows should be tested
- Similar tests or prior art in the codebase
- What not to test because it is implementation detail

## Acceptance Criteria
- [ ] ...

## Out of Scope
- ...

## Open Questions
- ...

## Further Notes
- ...
```

## Quality Bar

- Make user stories extensive enough to cover the feature surface.
- Separate product requirements from implementation details.
- Mark assumptions explicitly.
- Keep the PRD actionable for later conversion into issues.
