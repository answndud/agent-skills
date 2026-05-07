---
name: pre-mortem
description: Run a repository-grounded pre-mortem for the current project or app by assuming it failed after launch and finding loopholes, weak assumptions, missing safeguards, operational risks, UX/product gaps, security/data risks, test gaps, and proper fixes. Use when the user asks for pre-mortem, premortem, 사전 부검, 실패 시나리오, loopholes, proper fixes, 100% confidence check, "이 앱에 확신이 있나요", "출시 전 리스크 점검", "보완점 찾아줘", or wants Codex to challenge an app/project before release. Default to Korean output for Korean users.
---

# Pre-Mortem

Use this skill to challenge a project before it fails. Assume the app launched and something went wrong, then use repository evidence to find why.

## Operating Rules

- Default to Korean for Korean users.
- Inspect the current repository before judging. Use code, docs, configs, tests, schemas, routes, environment examples, CI, deployment files, and package scripts as evidence.
- Prioritize evidence-backed risks over generic advice.
- Mark speculation clearly when evidence is incomplete.
- Do not claim 100% confidence. State what would be needed to raise confidence.
- Do not edit files unless the user explicitly asks to implement fixes after the pre-mortem.
- If the current directory is not a project or there is no repository evidence, say so and ask for the correct project path.

## Risk Lenses

Review the project through these lenses when applicable:

- product fit and core user flow failure
- UX confusion, empty states, error states, onboarding, mobile behavior, accessibility
- authentication, authorization, roles, session handling, privacy
- data integrity, migrations, backups, deletion, idempotency, race conditions
- payments, billing, quotas, abuse, fraud, rate limits
- API contracts, validation, error handling, retries, timeouts
- security, secret handling, dependency exposure, unsafe inputs
- performance, scalability, caching, large data, cold starts
- deployment, environment variables, CI/CD, rollback, observability
- tests, fixtures, smoke tests, monitoring, alerting, runbooks
- maintainability, ownership boundaries, hidden coupling, risky manual steps

Skip irrelevant lenses, but say which important lens could not be assessed and why.

## Workflow

1. Map the project quickly:
   - identify stack, app type, entry points, package scripts, tests, docs, deployment/config files
   - identify critical user journeys and critical backend/data flows
2. Ask: "If this app failed after launch, what are the most plausible causes?"
3. Build a risk register. Each risk must include:
   - `Risk`: concise failure scenario
   - `Loophole`: the missing safeguard, weak assumption, or gap
   - `Evidence`: file, command output, docs, config, or "추정" if not directly proven
   - `Impact`: user/business/technical damage if it happens
   - `Likelihood`: High, Medium, Low, or Unknown
   - `Proper Fix`: concrete fix, not vague advice
   - `Verification`: test, command, monitoring check, or manual scenario to prove the fix
   - `Priority`: P0, P1, P2, or P3
4. Separate proven issues from uncertain risks.
5. End with the smallest high-leverage fix sequence.

## Output Format

Use this structure:

```markdown
## Confidence

- 현재 확신도: High/Medium/Low
- 100% 확신할 수 없는 이유:
- 확신을 높이려면 필요한 추가 근거:

## Executive Summary

- 가장 위험한 실패 시나리오:
- 가장 먼저 고칠 항목:
- 출시/배포 전 막아야 할 항목:

## Risk Register

| Priority | Risk | Loophole | Evidence | Impact | Likelihood | Proper Fix | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Unverified Assumptions

- 코드/문서 근거가 부족하지만 확인해야 하는 가정:

## Recommended Fix Sequence

1. P0/P1 fix:
2. Verification command:
3. Follow-up:
```

## Useful User Commands

These are examples of user requests that should trigger this skill:

```text
$pre-mortem 이 프로젝트가 출시 후 실패했다고 가정하고 pre-mortem 해주세요.
100% 확신할 수 없는 모든 loophole, proper fixes, impact, likelihood, evidence, verification command, early warning signal을 찾아주세요.
추측은 추측이라고 표시하고, 코드/문서 근거가 있는 항목을 우선하세요.
```

```text
$pre-mortem 이 앱을 운영자 관점에서 의심하세요.
보안, 데이터 손실, 결제/권한, 배포, UX 이탈, 성능, 테스트 공백, 운영 모니터링, 장애 복구 관점에서 실패 시나리오를 찾고 proper fix를 제안하세요.
```

```text
$pre-mortem 이 앱에 100% 확신과 자신감이 있나요?
그렇지 않다면 모든 loopholes, proper fixes, verification commands, early warning signals를 찾아주세요.
```
