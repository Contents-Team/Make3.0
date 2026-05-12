# Contributing Guide

이 프로젝트에 기여해 주셔서 감사합니다.

## Two Paths to Get Your PR Accepted

### Path 1: Small, Focused Changes (Fastest)

작은 버그 수정, 오타, 단일 함수 개선 등.

1. Fork & branch (예: `fix/login-redirect`)
2. 변경 + 테스트 추가
3. PR — 템플릿 채움
4. CI green 확인

### Path 2: Bigger or Impactful Changes

새 기능, 아키텍처 변경, 외부 API 추가 등.

1. 먼저 Issue로 의도 공유
2. 메인테이너 ack 후 작업 시작
3. `doc/plans/` 에 진행 계획 기록
4. 큰 결정은 `doc/adr/` 로 ADR 추가
5. PR — 위 문서들 링크

## PR Requirements

### Use the PR Template

`.github/PULL_REQUEST_TEMPLATE.md` 모든 체크박스 채움.

### Tests Must Pass

- 단위 테스트 추가/업데이트
- 기존 테스트 회귀 없음
- CI green 필수

### Model Used (Required, AI-assisted)

PR 본문에 사용한 AI 모델 명시 (예: `Claude Opus 4.7`, `Cursor + Claude Sonnet 4.6`).

## Feature Contributions

- 제품 비전 (`doc/PRODUCT.md`) 부합 확인
- 기존 아키텍처 (`doc/ARCHITECTURE.md`) 와 충돌 없는지

## General Rules

- Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`)
- 1 PR = 1 책임
- 비밀 (`.env`, 키) 커밋 금지

## Writing a Good PR Message

- **Why** 중심
- 관련 Issue 링크
- 스크린샷/로그 (UI 또는 디버깅 컨텍스트)