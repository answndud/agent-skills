# Global Skills Index

Updated: 2026-06-11

이 문서는 `/Users/alex/.agents/skills` 전역 스킬의 빠른 참조용 인덱스다.

주의:

- 이 파일은 안내 문서이며 스킬이 아니다.
- Codex가 스킬로 인식하는 대상은 각 하위 폴더의 `SKILL.md`다.
- 스킬을 직접 호출할 때는 `$skill-name` 형식을 사용한다.
- 스킬을 수정, 추가, 삭제하면 이 인덱스도 함께 갱신한다.

## brain-storm

- 용도: 저장소 근거 기반으로 다음 기능, 개선점, 제품 아이디어를 3-5개 제안하거나 `brain-storm/` 노트를 preview-first로 정리한다.
- 쓸 때: 브레인스토밍, 다음 기능 후보, 개선 아이디어, future opportunities, brainstorm notes 정리.
- 쓰지 않을 때: 바로 구현, 코드 리뷰, PRD/TRD/ADR 작성, PLAN/DONE 하네스, Codex `/goal` 실행.

## browser-extension-doctor

- 용도: 브라우저 확장 변경 직후 manifest, 권한, content/background 경계, messaging, storage, CSP, secret, store policy, browser compatibility를 점검한다.
- 쓸 때: Manifest V3, permissions, host_permissions, content script, background service worker, extension messaging, Chrome/Firefox 확장 품질 점검.
- 쓰지 않을 때: 일반 웹사이트 변경, 확장과 무관한 README/디자인-only 변경.

## caveman-lite

- 용도: 답변을 짧고 토큰 절약형으로 압축한다.
- 쓸 때: 짧은 상태 보고, diff/리뷰/커밋 메시지/PLAN/DONE/README 요약.
- 쓰지 않을 때: 보안 사고, 파괴적 작업, 마이그레이션, 법률/컴플라이언스, 모호한 요구사항.

## diagnose

- 용도: 어려운 버그, 실패 테스트, 오류, flaky behavior, 성능 회귀를 재현 루프부터 좁힌다.
- 쓸 때: diagnose, debug, 디버그, 진단, 원인 찾아줘, 테스트 실패, 성능 회귀.
- 쓰지 않을 때: 리뷰, 테스트 계획만 필요한 경우, 출시 전 리스크 점검.

## find-session

- 용도: 현재 live Codex 대화가 어떤 `~/.codex/sessions/**/rollout-*.jsonl` 파일인지 찾는다.
- 쓸 때: 현재 세션 JSONL 경로, thread id, session file 확인.
- 쓰지 않을 때: 세션 파일 수정, 삭제, 압축, cleanup.

## grill-me

- 용도: 계획, 설계, 구현 전략, PRD/TRD/ADR, 의사결정을 한국어로 한 질문씩 압박 검증한다.
- 쓸 때: grill me, 계획 검증, 설계 검증, 압박 질문, 의사결정 점검.
- 쓰지 않을 때: 바로 구현해야 하는 명확한 작업.

## handoff

- 용도: 세션, 에이전트, 역할, 컨텍스트 전환을 위한 인계문을 만들거나 소비한다.
- 쓸 때: handoff, 인계, 작업 인수인계, context transfer, continuation note, parallel-agent handoff.
- 쓰지 않을 때: 같은 세션에서 바로 계속할 수 있는 일반 작업.

## improve-codebase-architecture

- 용도: deep module 후보, 구조 개선, testability와 locality를 높일 리팩터링 기회를 찾는다.
- 쓸 때: 아키텍처 개선, 구조 개선, 리팩터링 후보, 코드베이스 구조 점검.
- 쓰지 않을 때: 즉시 구현할 작은 기능, 단순 cleanup, diff 리뷰.

## plan-done

- 용도: `docs/PLAN.md`, `docs/DONE.md`, `AGENTS.md` 기반의 가벼운 작업 상태 하네스를 설치/정리한다.
- 쓸 때: 작업 상태 문서, 세션 재개 문서, PLAN/DONE 관리, 하네스 설정.
- 쓰지 않을 때: 일반 코딩, PRD/TRD/ADR 작성, 코드 리뷰.

## prd-trd-adr

- 용도: 저장소 근거 기반으로 `docs/PRD.md`, `docs/TRD.md`, `docs/ADR.md`를 작성하거나 갱신한다.
- 쓸 때: PRD/TRD/ADR, 프로젝트 시작 문서, 제품/기술 요구사항 문서, 아키텍처 결정 기록.
- 쓰지 않을 때: 일반 코딩, README-only 수정, PLAN/DONE 하네스.

## pre-mortem

- 용도: 프로젝트가 출시 후 실패했다고 가정하고 리스크와 proper fix를 저장소 근거로 찾는다.
- 쓸 때: pre-mortem, 사전 부검, 실패 시나리오, loopholes, 출시 전 리스크 점검.
- 쓰지 않을 때: 이미 발생한 버그 진단, 현재 diff 코드 리뷰.

## repo-review

- 용도: concrete diff/scope를 read-only로 리뷰하고 버그, 리스크, 테스트 갭, 검증 전략을 제안한다.
- 쓸 때: 코드리뷰, 변경사항 점검, PR/diff 리뷰, 테스트 계획, 테스트 케이스, 검증 루틴, coverage gap.
- 쓰지 않을 때: 직접 cleanup/refactor 실행, 일반 구현, PRD/TRD/ADR 작성.

## session-cleanup

- 용도: `~/.codex/sessions`의 stale Codex session JSONL을 preview-first로 정리하면서 live Desktop 세션을 보호한다.
- 쓸 때: 세션 삭제 후보 보고서, keep/delete preview, 명시 확인 후 삭제.
- 쓰지 않을 때: JSONL 내용만 줄이고 싶을 때, 현재 열린 세션을 위험하게 건드리는 작업.

## simplify

- 용도: 이미 동작하는 변경을 behavior-preserving cleanup으로 직접 정리한다.
- 쓸 때: simplify, clean up, refactor, 커밋 전 정리, 코드 단순화.
- 쓰지 않을 때: read-only 리뷰, 테스트 계획, 기능 구현, public API 변경, 광범위한 아키텍처 rewrite.

## spring-boot-doctor

- 용도: Spring Boot 백엔드 변경 직후 diff 기반 품질 진단을 수행한다.
- 쓸 때: controller/service/repository/entity/security/JWT/session/Flyway/application.yml/Redis/Actuator/Docker/CI 변경 후, 백엔드 품질/운영 안정성 점검.
- 쓰지 않을 때: 순수 프론트엔드, 단순 README 문구, Spring Boot 런타임과 무관한 디자인 변경.

## tdd

- 용도: 기능, 버그 수정, 동작 변경을 test-first `RED -> GREEN -> REFACTOR` 사이클로 구현한다.
- 쓸 때: TDD, test-first, red-green-refactor, 테스트 먼저, 테스트 주도 개발.
- 쓰지 않을 때: 테스트 계획만 필요한 경우, 이미 구현된 변경 리뷰.

## to-issues

- 용도: PRD, plan, spec, architecture note, feature idea를 구현 가능한 vertical slice issue로 쪼갠다.
- 쓸 때: 이슈로 쪼개기, 티켓 생성, 작업 분해, implementation tickets.
- 쓰지 않을 때: PRD 자체 작성, 코드 구현, broad architecture review.

## to-prd

- 용도: 현재 대화, 저장소 이해, rough requirements, feature idea를 PRD로 합성한다.
- 쓸 때: PRD로 정리, 요구사항 문서화, 제품 요구사항 정리, spec 작성.
- 쓰지 않을 때: 여러 구현 issue로 분해해야 하는 경우, PRD/TRD/ADR 3종 문서가 필요한 경우.

## zoom-out

- 용도: 낯설거나 복잡한 코드 영역을 수정하기 전에 구조, 호출 관계, 도메인 용어를 설명한다.
- 쓸 때: zoom out, 큰 그림 보기, 상위 구조 파악, 코드 흐름 지도, module map, architecture overview.
- 쓰지 않을 때: 바로 구현해야 하는 명확한 작업.
