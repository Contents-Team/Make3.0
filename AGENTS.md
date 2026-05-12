# AGENTS.md

이 저장소에서 Claude Code, Cursor, Aider 등 AI 에이전트가 따를 작업 규약.

## Purpose

AI 에이전트가 컨트리뷰터로서 일관된 품질로 변경을 제출하도록 한다.

## Read This First

1. `README.md` — 프로젝트 개요
2. `doc/PRODUCT.md` — 무엇을 만들고 있는지·왜
3. `doc/ARCHITECTURE.md` — 시스템 구조
4. `doc/adr/` — 결정 이력
5. `doc/DEVELOPING.md` — 로컬 셋업

## Repo Map

| 경로 | 내용 |
|---|---|
| `src/` | 애플리케이션 코드 |
| `tests/` | 테스트 |
| `doc/` | 내부 dev/ops 문서 |
| `docs/` | 외부 사용자 문서 |
| `.github/` | CI·PR/Issue 템플릿 |

## Dev Setup

`doc/DEVELOPING.md` 참조.

## Core Engineering Rules

- 변경 범위 최소화 — 요청된 작업만
- 테스트 우선
- 타입 안전 — `any` 회피
- 에러 처리는 시스템 경계(외부 API, 사용자 입력)에서만
- 주석 최소화
- 디자인 패턴 이름은 영문 그대로 (`Repository Pattern`, `CQRS`, `Saga`)

## Database Change Workflow

1. 마이그레이션 파일 추가 (`migrations/NNNN-<slug>.sql`)
2. 다운(롤백) 스크립트 필수
3. `doc/DATABASE.md` 스키마 섹션 업데이트
4. 대규모 변경 시 ADR 추가

## Verification Before Hand-off

PR 제출 전:

- [ ] 빌드 통과
- [ ] 단위 테스트 통과
- [ ] 린트 통과
- [ ] 타입체크 통과
- [ ] 관련 문서 업데이트
- [ ] `CHANGELOG.md` `Unreleased` 섹션 추가

## Pull Request Requirements

- 템플릿 모든 필드 채움
- 1 PR = 1 책임
- `Model Used` 명시

## Definition of Done

1. 의도대로 동작 (수동 확인)
2. 자동 검사 통과
3. 문서 동기화
4. 메인테이너 1명 이상 승인
5. CI green

## Never Do This

- `LICENSE`, `SECURITY.md` 자동 수정 금지
- `doc/adr/` 기존 ADR 본문 수정 금지 (supersede ADR 새로 추가)
- 비밀 (`.env`, 키) 커밋 금지
- `--no-verify`, `--force` 등 검사 우회 금지