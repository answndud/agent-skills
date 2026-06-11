---
name: spring-boot-doctor
description: Run a Spring Boot quality diagnosis loop after backend feature work, bug fixes, refactors, or before commit/PR. Use for Spring Boot controller, service, repository, entity, QueryDSL, Spring Security, JWT/session/cookie/auth, Flyway migration, application.yml/properties/profile, DTO/request/response/validation, Redis/cache/session, observability/logging/metrics/actuator, Docker/CI/deployment, API contract, security, operations, or documentation-drift changes. Also use when the user asks for 점검, 리뷰, 품질, 보안, 운영 안정성, 리팩토링, Spring Boot Doctor, backend doctor, or post-change diagnosis on a Spring Boot project.
---

# Spring Boot Doctor

Run a focused post-change diagnosis loop for Spring Boot projects. Treat this as a second-pass reviewer after implementation, not as a generic best-practices note.

Default to Korean output for Korean users. Keep commands, paths, class names, severity labels, and verdict labels in English when clearer.

## Core Rule

Do not declare backend work complete immediately after edits. Inspect the diff, classify the changed surface, run proportionate verification, fix blocking issues when allowed, rerun relevant checks, and report residual risk.

## Scope

Use for changes touching:

- controllers, request/response DTOs, validation, exception handling, API paths, or OpenAPI docs
- service/domain logic, state transitions, idempotency, concurrency, permissions, tenant/role/resource ownership
- repositories, entities, QueryDSL, JPA mappings, transactions, fetch strategy, caching, Redis
- Spring Security, JWT, sessions, cookies, CORS, CSRF, OAuth, principals
- Flyway migrations, schema, indexes, constraints, seed/reference data
- `application*.yml`, profiles, Actuator, Prometheus, Swagger, Docker, CI, deployment, logging, metrics, runbooks

Skip for pure frontend, design/image-only, wording-only docs, or files unrelated to Spring Boot runtime behavior.

## Workflow

1. Detect project shape: build tool, modules, Java/Spring versions, profiles, migration tool, test tasks.
2. Inspect `git status --short`, relevant diff/stat, and changed files.
3. Classify the changed surface: `api`, `security`, `persistence`, `migration`, `domain`, `config-ops`, `observability`, `docs`.
4. Read nearby safety context, not only the diff. For example, API changes often require security config, exception handlers, services, DTOs, and tests.
5. Discover targeted tests adjacent to changed classes or by endpoint/domain keyword.
6. Pick the smallest meaningful verification command.
7. Run feasible local checks. If a check is skipped, record `not run` with the reason.
8. Apply the checklist below to the changed surface.
9. Fix P0/P1 issues unless the user requested report-only mode.
10. Rerun relevant verification after fixes and report score, verdict, commands, issues, fixes, and remaining risks.

## Verification

Prefer targeted commands before broad suites:

- Gradle: `./gradlew compileJava compileTestJava`, targeted `./gradlew test --tests '...'`, `./gradlew test`, `./gradlew integrationTest`, `./gradlew bootJar`
- Maven: `./mvnw -DskipTests compile test-compile`, targeted `./mvnw -Dtest=TestClass test`, `./mvnw test`, `./mvnw verify`
- Config/deploy: `docker compose config` when compose files changed

Rules:

- Run compile verification after Java/Kotlin backend changes when feasible.
- Run integration or context tests for controller, security, repository, QueryDSL, migration, or profile changes when available.
- Do not treat unrun checks as passed.
- Do not run production credentials, remote writes, destructive migrations, deploys, or billing systems unless explicitly requested.

## Checklist

Use only the relevant checks for the changed surface.

### API

- Request DTO validation and `@Valid` are present where needed.
- Controllers do not expose JPA entities directly.
- Response shape, error shape, status codes, pagination, sorting, filtering, and path/version conventions are intentional and tested or documented.
- Global exception handling remains stable and does not leak internals.

### Security

- AuthN/AuthZ is explicit and deny-by-default where practical.
- `permitAll`, CORS, CSRF, session/JWT/cookie settings are narrowly scoped and production-safe.
- Request-provided ids such as `userId`, `tenantId`, `accountId`, `resourceId`, or `organizationId` are ownership-checked.
- Secrets, tokens, passwords, private data, and credentials are not committed or logged.
- Swagger/OpenAPI, Actuator, Prometheus, H2 console, and admin endpoints are not unintentionally exposed in prod.

### Persistence

- Transactions live at service/application boundaries and use `readOnly = true` for read paths when appropriate.
- Lazy associations are not accessed outside transaction boundaries, especially with OSIV off.
- Fetch joins, projections, entity graphs, batching, and pagination/count queries avoid obvious N+1 or duplicate-row regressions.
- Bulk updates/deletes handle stale persistence context.
- Entity serialization, `toString`, equality, logs, and DTO mapping do not traverse unsafe lazy graphs.

### Migration

- Flyway naming and schema match entity/repository expectations.
- `NOT NULL`, `UNIQUE`, FK, enum, seed, and reference-data changes consider existing data.
- Destructive or large-table changes have backup/backfill/rollback or forward-fix reasoning.
- New joins/filters have relevant indexes when needed.
- Risky changes prefer expand-and-contract.

### Domain / Ops / Docs

- State transitions reject illegal states and handle duplicate requests where needed.
- Side effects such as audit logs, events, notifications, and cache invalidation remain intact.
- Logs/metrics include useful context without leaking sensitive data.
- Profile, env, deployment, API, migration, or runbook docs are updated when they are the project SSOT.
- `docs/PLAN.md` may be read for active context. Read or update `docs/DONE.md` only when completed context/archive work is explicitly relevant.

## Severity

- `P0`: compile/context/test failure, auth bypass, tenant/role/ownership escape, secret leak, prod dangerous exposure, destructive migration without safety, core data integrity break.
- `P1`: missing validation/transaction/test coverage for important changed behavior, risky query/migration/API contract/security/session/profile drift.
- `P2`: thin coverage, stale docs for non-critical behavior, weak logging, minor boundary or naming issue.
- `P3`: polish, wording, naming, small cleanup.

P0/P1 block completion unless the user asked for report-only mode.

## Health Score

Start at 100:

- P0: -25 each
- P1: -10 each
- P2: -4 each
- P3: -1 each

Caps:

- compile/context failure: max 49
- required test failure: max 59
- auth/tenant/secret/prod exposure: max 39
- destructive migration risk: max 49
- breaking API contract without docs/tests: max 69

Verdict:

- 90-100: Excellent
- 75-89: Good
- 60-74: Needs work
- 40-59: Risky
- 0-39: Critical

## Fix Policy

- Prefer narrow, evidence-backed fixes.
- Avoid broad rewrites.
- Fix P0/P1 before finalizing unless report-only was requested.
- Fix P2/P3 only when localized and low risk; otherwise report follow-up.
- Rerun relevant verification after fixes or state why it was not rerun.

## Final Report

Use this compact Korean shape:

```text
spring boot doctor

baseline score: <0-100 or baseline unavailable>
current score: <0-100> (<Excellent/Good/Needs work/Risky/Critical>)
regression: <delta or unknown>
변경 영역: <api/security/persistence/migration/domain/config-ops/observability/docs>
판정: <통과 | 차단 | 위험 동반 통과>

실행한 명령:
- <command>: <passed/failed/not run> <짧은 이유>

발견한 이슈:
- [P0/P1/P2/P3] <issue> | 근거: <file/command> | 조치: <fixed/follow-up>

적용한 수정:
- <없음 또는 목록>

남은 리스크:
- <없음 또는 목록>
```
