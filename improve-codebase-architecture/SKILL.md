---
name: improve-codebase-architecture
description: Find architecture improvement and refactoring opportunities in a codebase, especially deep module opportunities that improve testability, locality, maintainability, and AI navigability. Use when the user asks to improve architecture, 아키텍처 개선, 구조 개선, 리팩터링 후보 찾기, 코드베이스 구조 점검, make code more testable, consolidate tightly-coupled modules, or find deepening opportunities. Default to Korean output for Korean users.
---

# Improve Codebase Architecture

Use this skill to surface architectural friction and propose deepening opportunities.

## Language

- Respond in Korean by default.
- Keep architecture terms in English when they are clearer, but define and use them consistently.
- Ground every recommendation in observed repository evidence.

## Architecture Vocabulary

Use these terms consistently:

- `Module`: anything with an interface and implementation, such as a function, class, package, feature slice, or subsystem.
- `Interface`: everything a caller must know to use a module, including types, invariants, errors, ordering, and configuration.
- `Implementation`: the code inside the module.
- `Depth`: leverage at the interface. A deep module hides a lot of behavior behind a small stable interface.
- `Shallow module`: a module whose interface is nearly as complex as its implementation.
- `Seam`: where an interface lives and behavior can be changed without editing all callers.
- `Adapter`: a concrete implementation behind a seam.
- `Leverage`: what callers gain from module depth.
- `Locality`: what maintainers gain when related change, bugs, and knowledge are concentrated in one place.

## Principles

- The interface is the test surface.
- One adapter usually means a hypothetical seam; two adapters often mean a real seam.
- Use the deletion test: if deleting a module makes complexity vanish, it was likely pass-through. If deleting it pushes complexity into many callers, it was earning its keep.
- Prefer deepening existing concepts over inventing architecture labels.
- Respect existing ADRs and documented project decisions.

## Exploration

Before proposing candidates:

1. Read `AGENTS.md` if present.
2. Read domain vocabulary or context docs when present:
   - `CONTEXT.md`
   - `docs/ADR.md`
   - `docs/adr/**`
   - `docs/PRD.md`
   - `docs/TRD.md`
   - `docs/PLAN.md`
3. Inspect package/config and relevant source/test files with `rg` or `rg --files`.
4. Note where understanding one concept requires bouncing across many small modules.
5. Note where testing requires internal mocks, private knowledge, or awkward setup.
6. Note tightly coupled modules that leak decisions across their interfaces.

Do not perform a broad rewrite during exploration. Gather enough context to identify high-value candidates.

## Candidate Output

Present a numbered list of deepening opportunities.

For each candidate include:

- `Files`: relevant files or modules
- `Problem`: why the current architecture creates friction
- `Solution`: plain-language description of what would change
- `Benefits`: locality, leverage, testability, and maintainability gains
- `ADR impact`: whether it respects or conflicts with existing decisions
- `Confidence`: High / Medium / Low

Do not propose final interfaces in the first pass. Ask which candidate the user wants to explore.

## Grilling Loop

When the user selects a candidate, ask one architecture question at a time.

Resolve:

- the domain concept the module should represent
- what belongs behind the interface
- what callers should no longer know
- which adapters are real versus hypothetical
- what tests should survive internal refactors
- what migration path keeps behavior stable

If a new durable domain term emerges and the repository has `CONTEXT.md`, offer to update it. If the user rejects a candidate for a durable architectural reason, offer to record an ADR only when that reason would help future reviews avoid repeating the same suggestion.

## Implementation Boundary

This skill primarily proposes and sharpens architecture work.

Implement changes only when the user explicitly asks to apply a selected candidate. When implementing, keep the first patch narrow, behavior-preserving where possible, and verified by tests focused on public behavior.
