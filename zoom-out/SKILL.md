---
name: zoom-out
description: Step back from unfamiliar or tangled code and explain the bigger picture before implementation. Use when the user asks to zoom out, 큰 그림 보기, 상위 구조 파악, 코드 흐름 지도, module map, caller map, architecture overview, or how a section fits into the broader codebase. Default to Korean output for Korean users.
---

# Zoom Out

Use this skill to move one layer up in abstraction before changing code. The goal is orientation, not implementation.

## Workflow

1. Identify the user's focus area: file, module, feature, bug, flow, or vague code region.
2. Inspect only the relevant repository evidence needed to map the area:
   - nearby files and directories
   - imports and exports
   - callers and callees
   - tests and fixtures
   - docs, route definitions, schemas, or config when they explain the domain
3. Explain the bigger picture using the project's own domain vocabulary.
4. Report uncertainty explicitly when evidence is incomplete.
5. Do not edit files unless the user separately asks for implementation after the map is delivered.

## Output Shape

Default to Korean for Korean users.

Include:

- **한 줄 요약**: 이 영역이 시스템에서 맡는 역할.
- **구조 지도**: 관련 모듈, 파일, 데이터 흐름, 호출 관계.
- **핵심 용어**: 코드에서 쓰는 도메인 용어와 의미.
- **작업 전 주의점**: 변경 시 깨지기 쉬운 경계, 테스트 포인트, 숨은 coupling.
- **다음 단계**: 구현, 진단, 리팩터링, 테스트 중 무엇을 먼저 해야 하는지 추천.

Keep it concise. Prefer a useful mental model over exhaustive file-by-file commentary.
