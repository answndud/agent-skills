# Global Skills Index

이 문서는 `/Users/alex/.agents/skills` 전역 스킬의 빠른 참조용 인덱스다.

주의:

- 이 파일은 안내 문서이며 스킬이 아니다.
- Codex가 스킬로 인식하는 대상은 각 하위 폴더의 `SKILL.md`다.
- 스킬을 직접 호출할 때는 `$skill-name` 형식을 사용한다.

## brain-storm

- 용도: 현재 저장소를 근거로 다음 기능, 개선점, 제품 아이디어를 3-5개 발굴하고 사용자가 선택한 아이디어만 `brain-storm/` 아래에 저장한다.
- 쓸 때: "아이디어 브레인스토밍", "다음 기능 아이디어", "개선점 발굴", "future opportunities", "brain-storm 해줘".
- 쓰지 않을 때: 바로 구현, PRD/TRD/ADR 작성, 코드 리뷰, 자율 개발 루프, 단순 설명.
- 결과물: 저장소 근거가 붙은 아이디어 후보 목록, 선택 시 `brain-storm/**/*.md` 아이디어 파일.

## codex-session-slimmer

- 용도: `~/.codex/sessions`의 오래된 Codex session JSONL을 삭제하지 않고 직접 줄여 디스크 사용량을 줄인다.
- 쓸 때: 특정 `YYYY/MM` 또는 `YYYY/MM/DD` 세션 폴더가 너무 커서 rollout JSONL 내용을 보존 가능한 범위에서 슬림화하고 싶을 때.
- 쓰지 않을 때: 세션 파일 전체 삭제, 활성 세션 보호가 필요한 일반 cleanup, 별도 archive 생성.
- 결과물: 수정된 JSONL 파일, 파일별 before/after 크기와 어떤 필드를 줄였는지 보고.

## dev-loop

- 용도: 특정 작업이나 milestone을 계획, 구현, 검증, 리뷰, 완료 archive까지 반복해서 끝까지 밀어붙이는 자율 개발 루프다.
- 쓸 때: "끝까지 개발", "완성될 때까지 반복", "재귀 루프", "계획-개발-리뷰 루프", "v1 완성", "milestone complete".
- 쓰지 않을 때: 일반적인 작은 코드 수정, 단발 설명, 수동 단계별 진행, 범위가 열린 리팩터링.
- 결과물: 코드 변경, 검증 결과, `docs/PLAN.md`, `docs/PROGRESS.md`, `docs/COMPLETED.md` 상태 갱신.

## diagnose

- 용도: 어려운 버그, 실패 테스트, 오류, flaky behavior, 성능 회귀를 재현 루프부터 만들어 원인을 좁히고 고친다.
- 쓸 때: "diagnose", "debug", "디버그", "진단", "원인 찾아줘", "테스트가 실패해", "성능이 느려졌어".
- 쓰지 않을 때: 재현 없이 바로 best-effort patch만 원하는 단순 수정.
- 결과물: 재현 루프, 가설 목록, 계측 결과, 최소 수정, 회귀 테스트 또는 테스트 seam 부재 보고.

## find-session

- 용도: 현재 live Codex 대화가 어떤 `~/.codex/sessions/**/rollout-*.jsonl` 파일에 해당하는지 찾는다.
- 쓸 때: 현재 세션 JSONL 경로, `CODEX_THREAD_ID`, session file 확인이 필요할 때.
- 쓰지 않을 때: 세션 파일 수정, 삭제, 압축, cleanup.
- 결과물: 현재 thread id, 정확한 session file 경로, cwd, exact/fallback confidence.

## grill-me

- 용도: 계획, 설계, 구현 전략, PRD/TRD/ADR, 의사결정을 한국어로 한 질문씩 집요하게 검증한다.
- 쓸 때: "grill me", "계획 검증", "설계 검증", "압박 질문", "의사결정 점검".
- 쓰지 않을 때: 바로 구현해야 하는 명확한 작업, 질문 없이 문서로 정리해야 하는 경우.
- 결과물: 한 번에 하나의 질문, 추천 답변, 이유, 마지막에는 확정 결정과 남은 리스크 요약.

## improve-codebase-architecture

- 용도: 코드베이스에서 deep module 후보, 구조 개선, testability와 locality를 높일 리팩터링 기회를 찾는다.
- 쓸 때: "아키텍처 개선", "구조 개선", "리팩터링 후보 찾기", "코드베이스 구조 점검", "make code more testable".
- 쓰지 않을 때: 즉시 구현할 작은 기능, 단순 cleanup, diff 리뷰, TDD 구현.
- 결과물: 파일/모듈별 architecture friction, deepening opportunity 후보, 사용자 선택 후 설계 질문 루프.

## plan-progress-completed

- 용도: 프로젝트에 `PLAN.md`, `PROGRESS.md`, `COMPLETED.md` 작업 상태 하네스를 설치하거나 개선한다.
- 쓸 때: "PLAN/PROGRESS/COMPLETED 하네스", "작업 상태 문서 세팅", "세션 재개 문서", "작업 중단/재개 가능하게".
- 쓰지 않을 때: 일반 코딩, 자율 개발 루프 실행, PRD/TRD/ADR 작성, 단발 문서 수정.
- 결과물: `docs/PLAN.md`, `docs/PROGRESS.md`, `docs/COMPLETED.md`, 필요 시 compact `AGENTS.md` 규칙.

## pre-mortem

- 용도: 현재 프로젝트나 앱이 출시 후 실패했다고 가정하고 loophole, 약한 가정, 누락된 안전장치, proper fix를 저장소 근거 기반으로 찾는다.
- 쓸 때: "pre-mortem", "사전 부검", "실패 시나리오", "loopholes", "proper fixes", "100% 확신 있나요", "출시 전 리스크 점검", "보완점 찾아줘".
- 쓰지 않을 때: 이미 발생한 버그 원인 진단, 현재 diff 코드 리뷰, 순수 아키텍처 리팩터링 후보 탐색, 테스트 계획만 필요한 경우.
- 결과물: confidence 평가, executive summary, Risk Register, unverified assumptions, recommended fix sequence.

## prd-trd-adr

- 용도: 저장소 근거를 바탕으로 프로젝트 시작 문서인 PRD, TRD, ADR을 작성하거나 기존 문서와 reconcile한다.
- 쓸 때: "PRD/TRD/ADR 만들어줘", "프로젝트 시작 문서", "제품 요구사항 문서", "기술 요구사항 문서", "아키텍처 결정 기록".
- 쓰지 않을 때: 일반 코딩, 단발 README 수정, active task harness 설치, 자율 개발 루프.
- 결과물: `docs/PRD.md`, `docs/TRD.md`, `docs/ADR.md` 또는 기존 equivalent 문서 갱신.

## repo-review

- 용도: 현재 worktree diff 또는 지정된 diff/PR/커밋을 코드 리뷰 관점으로 점검한다.
- 쓸 때: "리뷰해줘", "코드리뷰", "변경사항 점검", "merge 전 점검", "diff 리뷰", "PR 리뷰".
- 쓰지 않을 때: 일반 구현 요청, cleanup/refactor 직접 수행, PRD/TRD/ADR 작성, 자율 개발 루프.
- 결과물: Findings 우선의 리뷰 결과, severity, open questions, test gaps, change summary. 기본은 review-only.

## session-cleanup

- 용도: `~/.codex/sessions`의 stale Codex session JSONL을 preview-first 방식으로 정리하되 live Desktop 세션과 사용자가 지정한 채팅을 보호한다.
- 쓸 때: 오래된 세션 삭제 후보 보고서, keep/delete preview, 명시적 확인 후 삭제가 필요할 때.
- 쓰지 않을 때: JSONL 내용만 줄이고 싶을 때, 현재 열린 세션을 위험하게 건드리는 작업.
- 결과물: 보호 세션 목록, 삭제 후보 목록, 확인 후 삭제 및 reclaimed space 보고.

## simplify

- 용도: 이미 동작하는 변경을 커밋 전 더 읽기 쉽고 유지보수 가능하게 behavior-preserving cleanup한다.
- 쓸 때: "simplify", "clean up", "refactor", "커밋 전 정리", "리팩터링", "코드 단순화".
- 쓰지 않을 때: 기능 구현, 버그 수정 자체, public API 변경, 광범위한 architecture rewrite, review-only 요청.
- 결과물: 작은 cleanup patch, 검증 결과, deferred simplification 후보.

## tdd

- 용도: 기능, 버그 수정, 동작 변경을 test-first 방식으로 `RED -> GREEN -> REFACTOR` 한 사이클씩 구현한다.
- 쓸 때: "TDD", "test-first", "red-green-refactor", "테스트 먼저", "테스트 주도 개발", "integration tests".
- 쓰지 않을 때: 테스트 계획만 필요한 경우, 이미 구현된 변경의 리뷰, 재현 루프가 필요한 어려운 버그 진단.
- 결과물: 한 번에 하나의 실패 테스트, 최소 구현, 통과 결과, 이후 refactor와 관련 테스트 실행 기록.

## test-plan

- 용도: 현재 diff, 기능, 모듈, 릴리스 단계에 대해 저장소 근거 기반 테스트 계획과 coverage gap을 만든다.
- 쓸 때: "테스트 계획", "테스트 케이스", "검증 루틴", "어떤 테스트 짜야 해?", "testing strategy", "coverage gap".
- 쓰지 않을 때: 실제 테스트 구현, 코드 리뷰, simplify, 자율 개발 루프, PRD/TRD/ADR 작성.
- 결과물: 우선순위별 test case 표, 실행 순서, fixture/mock/data, verification commands, coverage gaps.

## to-issues

- 용도: PRD, plan, spec, architecture note, feature idea를 구현 가능한 vertical slice issue로 쪼갠다.
- 쓸 때: "이슈로 쪼개기", "티켓 생성", "작업 분해", "implementation tickets", PRD/spec/plan을 issue로 전환.
- 쓰지 않을 때: PRD 자체 작성, 코드 구현, broad architecture review.
- 결과물: HITL/AFK로 표시된 issue breakdown, dependency order, acceptance criteria, 필요 시 issue draft.

## to-prd

- 용도: 현재 대화, 저장소 이해, rough requirements, feature idea를 PRD로 합성한다.
- 쓸 때: "PRD로 정리", "요구사항 문서화", "제품 요구사항 정리", "spec 작성", 현재 논의를 PRD로 만들기.
- 쓰지 않을 때: 여러 구현 issue로 분해해야 하는 경우, PRD/TRD/ADR 3종 프로젝트 시작 문서가 필요한 경우.
- 결과물: Problem Statement, Solution, User Stories, Implementation Decisions, Testing Decisions, Acceptance Criteria가 포함된 PRD.

## zoom-out

- 용도: 낯설거나 복잡한 코드 영역을 수정하기 전에 한 단계 위 추상화에서 구조, 호출 관계, 도메인 용어를 설명한다.
- 쓸 때: "zoom out", "큰 그림 보기", "상위 구조 파악", "코드 흐름 지도", "module map", "caller map", "architecture overview".
- 쓰지 않을 때: 바로 구현해야 하는 명확한 작업, 전체 코드베이스 아키텍처 개선 후보 탐색, 버그 원인 진단.
- 결과물: 한 줄 요약, 구조 지도, 핵심 용어, 작업 전 주의점, 다음 단계 추천.
