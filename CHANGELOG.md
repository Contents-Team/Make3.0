# Changelog

이 파일의 모든 주요 변경은 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 형식을 따르며, 버전은 [Semantic Versioning](https://semver.org/spec/v2.0.0.html) 을 사용합니다.

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.1.3] - 2026-05-12

### Changed
- `doc/MAKE_FORMAT.md` 네이밍 규칙 v3 → v4 보강 — **Tier 책임 분리**
  - 핵심 인사이트 2개 통합:
    1. 사용자 지적: "사용자가 편집할 수 없는 머티리얼/노드/애니메이션 등에 대한 네이밍은 불필요"
    2. 추가 제약: "사용자도 보지만 에이전트도 읽고 파악할 줄 알아야 함"
  - 합의: prefix 정책 (v3) 유지 + **이름 입력 책임을 Tier 로 분리**
  - **Tier Responsibility Matrix** 신설 — Tier A/B/C/System reserved 4 단계
    - Tier A (user-uploaded): 사용자 슬러그 + 툴 prefix 자동 부착
    - Tier B (user-composed): 사용자 의미 + 툴 prefix 자동 부착
    - Tier C (system-derived): **시스템 자동 mirror, 사람 입력 없음**
    - System reserved: VNT 예약어 (`SceneRoot` 등)
  - **System Auto-Derivation** 섹션 신설 — Tier C 자동 파생 알고리즘
    - 일반 mirror: source name 의 prefix 만 교체 (`img_gnb__active` → `mat_gnb__active`)
    - 애니메이션 특수: 채널 타겟 분석으로 primary target 추출
    - 1:N 케이스: 채널/상태 suffix 로 분기
  - 사용자 명명 작업량: v3 ~660 항목 → v4 ~192 항목 (약 70% 감소)
  - 검증 체크리스트에 Tier 분리 항목 5개 추가

### Added
- `doc/MAKE_FORMAT.md` 의 ``Tier Responsibility Matrix`` + ``System Auto-Derivation`` 섹션
- `doc/plans/HANDOFF.md` — 다음 세션 이어받기용 컨텍스트·열린 질문 인덱스

## [0.1.2] - 2026-05-12

### Changed
- `doc/MAKE_FORMAT.md` 네이밍 규칙 v2 → v3 보강 — **자가설명 강화**
  - **목적 명문화**: "이름만 봐도 (a) 파일 종류·확장자, (b) 소속 자산, (c) 역할·상태 즉시 파악" 을 최우선 목적으로 선언
  - v2 의 "Kind prefix 선택화" 결정 번복 → **3-letter prefix 필수** (`mdl_`/`mat_`/`tex_`/`img_`/`aud_`/`vid_`/`anm_`/`evt_`/`scn_`/`nod_`)
  - 단일 문자 모호성 (`M` = Model? Material?) 은 3자로 해소
  - **Asset Namespace** 도입 — `<asset>__<component>` (이중 언더스코어) 로 부모-자식 표현
  - **Texture 채널 vocab** — `_albedo`, `_normal`, `_roughness`, `_metallic`, `_ao`, `_emissive` 등 9종
  - **UI Image 상태 vocab** — `_default`, `_hover`, `_pressed`, `_active`, `_disabled`, `_focused` 6종
  - **Texture vs UI Image 분리** — 둘 다 PNG지만 `tex_` (3D 머티리얼 입력) vs `img_` (2D 레이어) 로 구분
  - **확장자 추론 매핑 표** — prefix 별 예상 확장자 명문화
  - **한국어·고유명사 정책** — 로마자 슬러그 + `doc/GLOSSARY.md` 등록 의무화
  - **이중 인코딩 트레이드오프 인정** — v2 의 "VNT 필드와 중복" 비판 번복: 자가설명 가치가 동기화 비용을 능가

### Added
- `doc/GLOSSARY.md` — 로마자 슬러그 ↔ 한국어 정식 명칭 매핑. v3 네이밍 정책 의무 부속 문서
- `doc/MAKE_FORMAT.md` 검증 체크리스트에 v3 항목 추가:
  - Kind prefix 시작 검증
  - 이중 언더스코어 namespace 검증
  - Texture/UI 상태 suffix 검증
  - GLOSSARY 등록 검증

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
