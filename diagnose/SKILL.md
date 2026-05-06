---
name: diagnose
description: Disciplined diagnosis loop for hard bugs, failing tests, broken behavior, errors, crashes, flaky behavior, and performance regressions. Use when the user says diagnose, debug, 디버그, 진단, 원인 찾아줘, something is broken/failing/throwing, a test fails, or performance regressed. Default to Korean output for Korean users.
---

# Diagnose

Use this skill for hard bugs where disciplined diagnosis matters more than quick guessing.

## Language

- Respond in Korean by default.
- Keep error messages, commands, symbols, and code identifiers exact.
- State evidence separately from hypotheses.

## Core Rule

Build a feedback loop first.

If there is a fast, deterministic, agent-runnable pass/fail signal for the bug, the cause can be found through bisection, hypothesis testing, and instrumentation. Without a loop, do not jump straight to a fix unless the user explicitly asks for a best-effort patch.

## Phase 1: Build Feedback Loop

Spend disproportionate effort here.

Try to construct the loop in roughly this order:

1. Failing test at the seam that reaches the bug: unit, integration, e2e, or existing regression test.
2. CLI invocation with fixture input and expected output.
3. HTTP/curl script against a running dev server.
4. Headless browser script with Playwright or Puppeteer, asserting DOM, console, network, or screenshot state.
5. Replay captured trace: request payload, event log, HAR, fixture, crash input, or production-like artifact.
6. Throwaway harness that exercises the bug path through a small entrypoint.
7. Property or fuzz loop for intermittent wrong output.
8. Bisection harness for regressions between commits, versions, datasets, or configs.
9. Differential loop comparing old versus new behavior.
10. Human-in-the-loop script only as a last resort, with structured steps and captured output.

Improve the loop itself:

- Make it faster by narrowing setup and scope.
- Make it sharper by asserting the user's exact symptom.
- Make it deterministic by pinning time, seeding randomness, isolating filesystem state, and freezing network dependencies.

For nondeterministic bugs, increase reproduction rate. Loop the trigger many times, add stress, parallelize, inject sleeps, or narrow timing windows until the failure rate is high enough to debug.

If no loop can be built, stop and report what was tried. Ask for the missing artifact or access, such as logs, HAR, core dump, screen recording with timestamps, repro environment, or permission to add temporary instrumentation.

## Phase 2: Reproduce

Run the loop and confirm:

- The failure matches the user's described bug, not a nearby different failure.
- The failure reproduces across multiple runs, or at a high enough rate for flaky bugs.
- The exact symptom is captured: error message, wrong output, timing, UI state, or failing assertion.

Do not proceed to fix until the bug is reproduced or the user explicitly accepts best-effort work.

## Phase 3: Hypothesize

Generate 3-5 ranked hypotheses before testing.

Each hypothesis must be falsifiable:

```text
If <cause> is the cause, then <probe/change> will make the bug disappear, move, or get worse.
```

Discard or sharpen any hypothesis that cannot predict an observable result.

Show the ranked list to the user when useful. Proceed with the best-ranked hypothesis if the user is unavailable and the next probe is safe.

## Phase 4: Instrument

Each probe must map to one hypothesis.

Rules:

- Change one variable at a time.
- Prefer debugger or REPL inspection when available.
- Add targeted logs only at boundaries that distinguish hypotheses.
- Tag temporary logs with a unique prefix such as `[DEBUG-a4f2]`.
- Never spray logs everywhere and grep blindly.

For performance regressions:

- Establish a baseline measurement first.
- Use timing harnesses, profiler output, query plans, browser performance traces, or benchmark commands.
- Measure before fixing.

## Phase 5: Fix And Regression Test

Write the regression test before the fix when there is a correct seam.

A correct seam exercises the real bug pattern as it occurs at the call site. If the available seam is too shallow and would give false confidence, document that as an architecture problem.

If a correct seam exists:

1. Turn the minimized repro into a failing test.
2. Watch it fail.
3. Apply the smallest fix.
4. Watch it pass.
5. Re-run the original Phase 1 feedback loop.

## Phase 6: Cleanup And Post-Mortem

Before declaring done:

- Re-run the original repro loop and confirm it no longer fails.
- Run the regression test or document why no correct seam exists.
- Remove all `[DEBUG-...]` instrumentation.
- Delete throwaway harnesses unless they became useful checked-in regression assets.
- Report the correct hypothesis and why the fix addresses it.

After the fix, ask what would have prevented the bug.

If the answer involves no good test seam, tangled callers, hidden coupling, or shallow modules, recommend using `improve-codebase-architecture` with the specific finding.
