---
name: tdd
description: Apply test-driven development with a red-green-refactor loop for features, bug fixes, and behavior changes. Use when the user asks for TDD, test-first development, red-green-refactor, 테스트 먼저, 테스트 주도 개발, integration tests, or wants behavior implemented through tests before code. Default to Korean output for Korean users.
---

# Test-Driven Development

Use this skill to implement behavior one verified slice at a time.

## Language

- Respond in Korean by default.
- Use project terminology and existing test vocabulary.
- Keep test names and descriptions behavior-oriented.

## Core Principle

Tests should verify observable behavior through public interfaces, not implementation details.

Good tests:

- exercise real code paths through public APIs or user-facing flows
- describe what the system does
- survive internal refactors
- fail when behavior breaks

Bad tests:

- mock internal collaborators unnecessarily
- test private methods
- assert internal call order or data shape without user-visible meaning
- fail after harmless refactors

## Avoid Horizontal TDD

Do not write all tests first and then all implementation.

Use vertical tracer bullets:

```text
RED -> GREEN: one behavior test -> minimal implementation
RED -> GREEN: next behavior test -> minimal implementation
RED -> GREEN: next behavior test -> minimal implementation
```

Each cycle should teach the next cycle.

## Planning

Before writing tests:

1. Read `AGENTS.md` if present.
2. Inspect existing tests, public interfaces, and relevant implementation.
3. Respect ADRs and existing domain vocabulary.
4. Identify the public interface or user-facing flow under test.
5. List the important behaviors to test, not implementation steps.
6. Confirm with the user only when interface shape, priority, or expected behavior is ambiguous enough to change the implementation.

Focus on critical paths and complex logic. Do not try to test every edge case by default.

## Red-Green Loop

For each behavior:

1. `RED`: write exactly one failing test for one observable behavior.
2. Run the narrowest relevant test command and confirm the expected failure.
3. `GREEN`: write the minimum code needed to pass that test.
4. Run the same test and confirm it passes.
5. Repeat for the next behavior.

Rules:

- One test at a time.
- Do not anticipate future tests with speculative code.
- Do not refactor while red.
- Prefer integration-style tests unless the repository's established test pattern points elsewhere.
- Mock only at external boundaries such as network, time, filesystem, payment providers, email, or third-party services.

## Refactor

After all current tests pass:

1. Look for duplication, unclear names, and shallow modules.
2. Deepen modules when complexity can move behind a smaller interface.
3. Keep behavior unchanged.
4. Run tests after each meaningful refactor step.

## Per-Cycle Checklist

Use this checklist internally:

- The test describes behavior, not implementation.
- The test uses a public interface or user-facing flow.
- The test would survive an internal refactor.
- The implementation is minimal for this test.
- No speculative feature was added.
- The relevant tests were run.

## Reporting

When reporting progress, include:

- current behavior slice
- RED result
- GREEN result
- remaining behaviors
- any tests not run and why
