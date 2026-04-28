---
name: prd-trd-adr
description: Use only when the user explicitly asks to create, update, or reconcile repository-start documents such as PRD/TRD/ADR, 프로젝트 시작 문서, 제품 요구사항 문서, 기술 요구사항 문서, or 아키텍처 결정 기록. This skill writes or updates docs/PRD.md, docs/TRD.md, and docs/ADR.md from repository evidence. Do not use for normal coding, one-off documentation edits, dev-loop requests, plan-progress-completed harness setup, or manual step-by-step coding requests.
---

# PRD TRD ADR

## Purpose

Use this skill to create or reconcile repository-start documents that help a future AI coding agent understand:

- `docs/PRD.md`: what the project is, why it exists, who it serves, and what success means
- `docs/TRD.md`: how the current system is built, what contracts and constraints matter, and how to verify changes
- `docs/ADR.md`: important architectural decisions already reflected in the repository

Default output language is Korean unless the repository or user clearly requests another language.

This skill is documentation-only. It does not implement product features or run an autonomous development loop.

## Activation Rules

Use this skill only when the user explicitly asks for PRD/TRD/ADR or repository-start documentation, such as:

- "PRD/TRD/ADR 만들어줘"
- "프로젝트 시작 문서 작성"
- "제품 요구사항 문서 만들어줘"
- "기술 요구사항 문서 갱신"
- "아키텍처 결정 기록 정리"
- "docs/PRD.md, docs/TRD.md, docs/ADR.md 작성"

Do not use this skill for:

- normal coding requests
- one-off README or docs edits
- active task harness setup
- autonomous development loops
- release notes or changelog writing
- architecture brainstorming without a request to write repository documents

## Repository Inspection

Before editing, inspect enough repository evidence to avoid generic templates:

1. `README.md`, if present.
2. `AGENTS.md`, if present.
3. Existing docs:
   - `docs/**`
   - `business/**`
   - `PRODUCT.md`
   - `DESIGN.md`
4. Manifest and config files when present:
   - `package.json`
   - `pyproject.toml`
   - `Cargo.toml`
   - `go.mod`
   - `Makefile`
   - `justfile`
5. Source entrypoints, tests, schemas, scripts, and CI workflows by using `rg --files` and reading only the relevant files.

Do not perform a deep code audit unless the requested document cannot be grounded otherwise. Gather enough to identify project purpose, current implementation shape, interfaces, verification commands, and structural decisions.

## Output Paths

Default targets:

- `docs/PRD.md`
- `docs/TRD.md`
- `docs/ADR.md`

If an equivalent document already exists, preserve its path instead of creating a duplicate. Examples:

- `docs/prd.md`
- `docs/product/prd.md`
- `docs/technical/trd.md`
- `docs/adr.md`

If multiple plausible candidates exist and the correct target cannot be inferred safely, stop and ask the user to choose. Do not create both.

Use `ADR.md` for Architecture Decision Record. Do not create `ARD.md`.

## Merge Policy

When a target document already exists:

- Do not overwrite it wholesale.
- Preserve useful current content.
- Correct stale content only when repository evidence clearly contradicts it.
- Mark uncertainty as `가정`, `오픈 질문`, `추론된 근거`, or `근거 유형: inferred`.
- Do not invent requirements, future architecture, or decision history.

If `AGENTS.md` exists, add or reconcile only a short pointer such as:

```md
- 프로젝트 시작 문서: `docs/PRD.md`, `docs/TRD.md`, `docs/ADR.md`
```

Do not add long PRD/TRD/ADR operating rules to `AGENTS.md`. If `AGENTS.md` does not exist, do not create it only for this skill.

## Document Boundaries

Keep the three documents distinct:

- PRD is product-facing: what, why, who, scenarios, requirements, success criteria, scope.
- TRD is implementation-facing: current architecture, code organization, contracts, flows, risks, verification.
- ADR is decision-facing: important technical or architectural choices and their evidence.

Avoid turning any of them into:

- a task list
- a changelog
- a release note
- an ideal future architecture with no repository evidence
- a dump of copied code or command output

## PRD Requirements

The PRD target document must include:

- 프로젝트 요약
- 문제 정의
- 대상 사용자 / 운영자 / 이해관계자
- 목표
- 비목표
- 핵심 사용 시나리오 / 사용자 흐름
- 기능 요구사항
- 제약사항
- 수용 기준
- 성공 지표
- 범위 경계
- 오픈 질문 / 가정

Write from the product and user perspective. Keep low-level implementation detail out unless it is necessary to explain externally visible behavior.

## TRD Requirements

The TRD target document must include:

- 시스템 맥락
- 아키텍처 개요
- 주요 모듈 / 컴포넌트와 각 책임
- 디렉터리 및 코드 조직 구조
- 데이터 모델 / 저장소 / 스키마
- API 계약 / CLI 계약 / 이벤트 계약 / 외부 연동 경계
- 요청 / 작업 / 상태 흐름
- 에러 처리 및 실패 모드
- 보안 및 신뢰 경계
- 성능 / 확장성 / 운영 제약
- 관측성 / 로깅 / 모니터링 기대사항
- 테스트 전략
- 검증 명령
- 실행 / 배포 / 롤백 고려사항
- 알려진 기술 리스크
- 오픈 기술 질문

Also capture implementation rules that future agents should not casually break, such as stable interfaces, compatibility expectations, migration cautions, performance-sensitive paths, security-sensitive paths, and modules that require extra care.

Separate:

- 현재 구현
- 의도된 구조
- 아직 메워야 할 갭

## ADR Requirements

The ADR target document records only significant architectural or technical decisions that have repository evidence.

Good ADR candidates include framework/runtime choices, storage choices, API style, monolith/service boundary, background job strategy, auth model, state management, deployment model, migration strategy, test strategy tied to architecture, and external integration patterns.

Do not record trivial code style preferences or unsupported guesses.

Each ADR entry must include:

- ADR ID
- 제목
- 상태: `accepted`, `superseded`, `proposed`, or `deprecated`
- 날짜, or `Date unknown`
- 맥락
- 결정 내용
- 고려한 대안
- 결과 / 영향
- 저장소 내 근거
- 근거 유형: `explicit` or `inferred`
- 오픈 질문, if any

If the reasoning is inferred from dependencies, file structure, code, or scripts, label it as `추론된 근거` and `근거 유형: inferred`. Do not create fake history.

## Consistency Check

Before finalizing, check:

- PRD goals do not contradict TRD implementation constraints.
- TRD technical choices that are structurally important are represented in ADR.
- ADR entries have concrete repository evidence.
- Current implementation and intended future structure are clearly separated.
- Uncertain claims are marked as assumptions or open questions.
- The documents can be understood by a future AI coding agent without previous session context.

## Safety Boundaries

Do not:

- implement code
- add dependencies
- run migrations or codegen
- run formatters that rewrite files
- create target-repository `agents/openai.yaml`, `.agents/**`, or skill metadata files
- create extra references or helper docs unless the user explicitly asks
- commit, push, tag, release, or deploy
- write requirements or architecture claims without repository evidence

## Verification

After creating or reconciling documents:

1. Show changed paths.
2. Read the first section of each target document.
3. Verify the required document names or preserved equivalent paths.
4. Check that `AGENTS.md` changed only by a short pointer, if it changed.
5. Search the generated documents for obvious placeholders that should not remain except explicit `가정` or `오픈 질문`.

Run repository tests only if the document changes are in a repository and a normal validation command is obvious. If tests are not run, state why.

## Final Response

Keep the response concise:

- created or updated documents
- context inspected
- whether existing documents were preserved
- verification performed
- remaining assumptions or open questions
