# Changelog

이 파일의 모든 주요 변경은 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 형식을 따르며, 버전은 [Semantic Versioning](https://semver.org/spec/v2.0.0.html) 을 사용합니다.

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.1.1] - 2026-05-12

### Changed
- `doc/MAKE_FORMAT.md` 네이밍 규칙 v1 → v2 보강 — 자기반박 8개 허점 분석 후 정정
  - **3-Layer Identity** 도입: `ID` (UUID, 불변, machine) / `Name` (ASCII slug, code) / `DisplayTitle` (Unicode, user-facing)
  - 단일 문자 prefix (`S/A/I/V/M/T/E`) → 선택적 풀워드 prefix. VNT type 필드 활용
  - 2자리 `<NN>` 순번 제거 (실측 142 이미지 vs 최대 100 충돌). 필요 시 별도 `order` 필드 (10단위)
  - 영문 강제 → identifier 만 ASCII, DisplayTitle 은 Unicode (한국어 OK) + i18n
  - Material instance vs definition 구분 명시
  - 유일성 scope 명시 — ID global, name parent-local
  - 정규식 분리 — identifier `^[a-z][a-z0-9_]*$` + display (제어문자만 금지)
  - OriginPath 정책 3단계화 — 로컬/공유/외부배포

### Removed
- v1 의 `<단일문자><NN>_<slug-en>` 노드명 권장 패턴 (over-engineering, scope·scaling 결함)

## [0.1.0] - 2026-05-12

### Added
- 프로젝트 문서 스켈레골 부트스트랩 — `doc-init service` 프로파일 (paperclip 패턴 기반)
  - 루트 메타: `README.md`, `LICENSE` (MIT), `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, `AGENTS.md`, `CHANGELOG.md`, `.gitignore`
  - 내부 문서 `doc/`: `ARCHITECTURE.md`, `DATABASE.md`, `DEPLOYMENT.md`, `DEVELOPING.md`, `PRODUCT.md`, `RELEASING.md`, `SPEC.md`, `TASKS.md` + `adr/`, `plans/`, `experimental/`
  - 외부 문서 `docs/`: `start/`, `guides/`, `api/`, `cli/`, `deploy/`, `assets/`, `docs.json` (Mintlify)
  - `.github/`: PR/Issue 템플릿 + `workflows/` placeholder
- ADR-0001 — 아키텍처 결정을 ADR 로 기록 (`Status: Accepted`)
- `doc/MAKE_FORMAT.md` — `.make` 파일 포맷 분석 + 에셋 네이밍 규칙
  - `.make` = glTF 2.0 GLB + VNT_* 커스텀 확장 식별
  - 8개 VNT 확장 카탈로그 (`VNT_NodeProperty`, `VNT_MediaResource`, `VNT_Event`, `VNT_Animation`, `VNT_Settings_Target/Environment/GlobalOverlay`, `VNT_ExternalResources`)
  - ResourceType enum 매핑, UUID v4 ResourceID 규칙
  - 에셋 타입별 네이밍 규칙 (`S/A/I/V/M/T/E<NN>_<slug-en>`)
  - 6개 안티패턴 + 7개 검증 체크리스트
