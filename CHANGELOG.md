# Changelog

> **범위: 이 레포의 문서(특히 `doc/MAKE_FORMAT.md` 의 `.make` 포맷·에셋 네이밍 규칙) 변경 이력.**
> Make **제품(설치파일/빌드) 버전별 기능 변경**은 별도 로그 [PRODUCT_CHANGELOG.md](./PRODUCT_CHANGELOG.md) 참조.

이 파일의 모든 주요 변경은 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 형식을 따르며, 버전은 [Semantic Versioning](https://semver.org/spec/v2.0.0.html) 을 사용합니다.

## [Unreleased]

### Added
- `PRODUCT_CHANGELOG.md` — Make 제품(설치파일/빌드) 버전별 기능 변경 로그 신설. 이 문서 변경 로그와 **별도 관리**. 베이스라인 `3.1.0.4` 항목 포함.
- `doc/UPDATE_WORKFLOW.md` — 팀원↔Claude 협업 규약(상황별 명령 예시·두 로그 구분·PR/승인 흐름).
- `doc/ONBOARDING.md` — 협업자 온보딩(접근·gh 인증·클론·Claude 연결) + main 브랜치 보호 규칙 요약.

### Changed
- `README.md` — TODO 플레이스홀더를 실제 레포 내용으로 채움(`.make` 포맷 = glTF GLB + `VNT_*`, 네이밍 v7, `doc/` 구조, Python 스크립트, 텔레메트리 없음 명시). 기존 섹션 구조 보존.
- `CHANGELOG.md` — 헤더에 범위 명시(문서/네이밍 변경 전용) + `PRODUCT_CHANGELOG.md` 교차 링크.

### Deprecated

### Removed

### Fixed

### Security
- `.gitignore` — PUBLIC 레포 보호: `*.make`·`*.pptx`·설치파일(`*.exe`/`*.zip`/`*.7z`/`*.msi`)·빌드 추출 스크래치(`_make3.0_builds/`) 무시 추가. 클라이언트 자료·바이너리 실수 커밋 방지.

## [0.1.6] - 2026-06-25

### Changed
- `doc/MAKE_FORMAT.md` 네이밍 규칙 v6 → v7 개정 — **3-Tier → 2-Tier 모델로 축소**
  - **T3 (System-Derived) 단계 삭제** — 머티리얼·중간 mesh·texture object 등 시스템 자동 생성 객체는 사용자 명명 대상에서 제외(시스템 자동 처리). 명명 모델은 **T1 (원본 파일) / T2 (Make Editor 인스턴스)** 두 단계로 축소
  - **약자 폐지 → 풀어쓰기**:
    - 상태: `_Def`/`_Prs`/`_On`/`_Off`/`_Sel` → `Default`(생략)/`Pressed`/`On`/`Off`/`Disabled`
    - 방향: `_L`/`_R`/`_U`/`_D`/`_CW`/`_CCW` → `Left`/`Right`/`Up`/`Down`/`Clockwise`/`AntiClockwise`
  - **도메인 약자 PascalCase 통일**: `GNB`/`BGM`/`SFX` → `Gnb`/`Bgm`/`Sfx` (3글자+ PascalCase, 2글자 `UI`/`TTS` 는 대문자 유지)
  - **영상 카테고리 5 → 2종**: `CUT`/`TUT`/`LOOP`/`INTRO`/`OUTRO` → `Info` (정보 전달 통합) / `Bgv` (배경 영상)
  - **애니메이션 효과 기반 재정의**: `<Target>_<Act>` 약자 패턴 → 효과 이름(`Bounce`/`ZoomIn`/`ZoomOut`/`Pop`/`Pulse`/`Spin`/`Slide`/`Flip`/`Fade`/`Highlight`). 대상 오브젝트명 제외, 속성 4종(`Position`/`Rotation`/`Scale`/`Color` — 3D 모델은 `Color` 불가)
  - **T2 토큰 구분 통일**: Family 약자 뒤에도 단일 `_` (`Gnb_01`, `Btn_Start`). 메인 내비 `Gnb`/`Snb`/`Bnb` 는 번호+상태로 구분(`Gnb_01_On`)
  - **숫자 경로 최대 3자리** (`Contents_3_1_1`), 이중 밑줄 `__` 제거
  - 상태 `Selected` 제거(`On` 과 기능 동일), `Disabled` 를 `Off` 와 구분해 부활

### Added
- `doc/MAKE_FORMAT.md` 의 `씬 하이어아키 (Scene Hierarchy)` 섹션 — 디바이스별(HMD = World 전용 / PC·Tablet = Models 만 World, 나머지 Screen) 빈 오브젝트 컨테이너 구조 표준
- `doc/MAKE_FORMAT.md` 의 `C# 컨벤션 대조 (Microsoft .NET)` 섹션 + 개선 제안
- 애니메이션 포함 3D 모델 접두사 `Ani_` (`Ani_Cupcake.fbx`)
- 음성 변환(TTS) 적용 텍스트 접두사 `TTS_`
- `Modal` 패밀리 (모달·팝업 창)
- `doc/assets/MakeNamingConvention_v7.xlsx` — 비개발자용 v7 네이밍 가이드 워크북 (Overview/T1/T2/Hierarchy/Animation/Vocab/Examples/Checklist/Anti-Patterns 9시트)

### Removed
- **3D 텍스처 명명 규칙 삭제** — PNG 는 UI 스프라이트 전용. Role 토큰(`ALB`/`NRM`/`RGH`/`MET`/`EMI`/`MSK`/`AO`)·텍스처 채널 suffix·`tex_` 일체 폐지
- `doc/assets/MakeNamingConvention_v6.xlsx` (v7 로 대체, git 히스토리에 보존)

### Fixed
- 오타 정정 (`Strat` → `Start`), 안티패턴 예시를 단일 이슈로 명확화

## [0.1.5] - 2026-05-13

### Changed
- `doc/MAKE_FORMAT.md` 네이밍 규칙 v5 → v6 보강 — **3-Tier 책임 모델로 재구성**
  - **실측 분석 기반** — `Make Templete_20260512.make` (513 노드) 의 안티패턴·실사용 vocab 추출
  - **Two-Layer (L1/L2) → Three-Tier (T1/T2/T3)** 재구조화
    - **T1** (Source Asset, filesystem): v5 L1 유지 — PascalCase + 확장자
    - **T2** (Instance, Make Editor visible, v6 신규): **kind prefix 폐지** — Make Editor 타입 아이콘이 종류 알려줌 → 인스턴스명 간결성 우선
    - **T3** (System-Derived, v4·v5 본문 유지): 머티리얼·중간 mesh 등 사용자 미편집 객체 — `lower_snake_case + prefix` 유지
  - **인스턴스 명명 정책 대전환** (T2):
    - kind prefix (`mdl_`/`img_`/`txt_` 등) 폐지
    - PascalCase + 단일 `_`
    - 이중 언더스코어 `__` 폐지 (트리 컨텍스트가 위계 표현)
    - 하이픈 **명시 금지**
    - 닫힌 sibling vocab(L/R/U/D, In/Out) 단문자 허용
  - **State Vocab 축약 (v6)**:
    - 3-letter PascalCase: `_Def`/`_Prs`/`_On`/`_Off`/`_Sel`
    - `_Hover`/`_Focused`/`_Highlight` 제거 (VR/터치 환경)
    - `Active/Disabled` → `On/Off` 통합 (시각 상태 우선, 의미 분기는 VNT 필드에서)
  - **Audio 카테고리 갱신**:
    - `BGM`/`SFX`/`NAR` 3종 (구 `VO` → `NAR`, `AMB` 제거)
    - 카테고리·description 사이 `_` 삽입 (`BGM_Tutorial_01.wav`)
  - **Video 카테고리 풀이 명문화**:
    - `CUT` (Cutscene), `TUT` (Tutorial), `LOOP`, `INTRO`, `OUTRO`
    - 동일하게 `_` 삽입 (`TUT_BatterySwap_Step01_01.mp4`)
  - **UI Family Vocab (v6 신규, 권장)**: `GNB`/`LNB`/`Btn`/`Nav`/`Pnl`/`Ico`/`Bg`/`Logo`/`Tip`/`Txt` 10종 — T2 인스턴스 인계 직관성
  - **Animation Naming (v6 신규)**:
    - prefix 폐지 (animations[] 배열 위치가 타입 선언)
    - `<Target>_<Act>[_<Dir>]` 패턴
    - Action vocab: `Rot`/`Scl`/`Mov`/`Clr`/`Op` + compound `ZI`/`ZO`/`FI`/`FO`/`Tx`/`Pop`
    - Direction vocab: `L`/`R`/`U`/`D`/`CW`/`CCW`
    - 다중 속성 결정론적 순서: `Rot → Scl → Mov → Clr → Op`
    - `^new Clip\d*$` 패턴 임포트 차단
  - **`_v<NN>` marker 정책 완화**: T1 옵션, T2 금지
  - 실측 파일 변환 예시 — 11개 Contents 페이지, 4-방향 회전 UI, 7개 default 애니메이션 매핑
  - 검증 체크리스트 T2·Animation 항목 12개 추가

### Added
- `doc/MAKE_FORMAT.md` 의 `Three-Tier Naming Model`, `T2 — Instance Naming`, `Animation Naming` 섹션
- `v5 → v6 보강 근거` 섹션 — 실측 갭 10개 + 자체 반박 4개

## [0.1.4] - 2026-05-13

### Changed
- `doc/MAKE_FORMAT.md` 네이밍 규칙 v4 → v5 보강 — **소스 에셋 파일시스템 레이어 추가**
  - 외부 제안 `Make Asset Naming Convention v0.5` (HamIsBadass, 2026-05-13) 검토·통합
  - 핵심 인사이트: v4 까지는 `.make` 내부 식별자(L2) 만 규정 — 임포트 직전 외부 소스 파일(FBX/PNG/WAV/MP4) 명명 규약 부재
  - **Two-Layer Naming Model** 신설:
    - L1 (Source Asset, filesystem): PascalCase + `_v<NN>` marker + 확장자
    - L2 (`.make` Internal): lower_snake_case + 3-letter kind prefix (구 v4 본문 유지)
  - **L1 → L2 Normalization** 매핑 명문화 — 임포트 파이프라인이 자동 수행
  - **Source Asset Filesystem Naming** 섹션 신설 (L1 본문):
    - Global Rules + `v` marker 로 Source vs Instance 구분
    - 타입별 규칙: FBX / PNG (Role 토큰 `ALB`/`NRM`/`Sprite` 등) / WAV·MP3 (카테고리 prefix `BGM`/`SFX`/`VO`/`AMB`) / MP4 (컨텍스트 prefix `CUT`/`TUT`/`LOOP`/`INTRO`/`OUTRO`) / Font
    - Hierarchy 규칙: 자식 부위 FBX 의 부모 이름 포함 의무
    - State 토큰 (`Open`/`Broken`/`Closed`/`Damaged`) 정의
  - **변경 타당성 분석 표** 추가 (v4 → v5 보강 근거) — 외부 제안 항목별 채택/부분채택 판정
  - 검증 체크리스트에 L1 항목 10개 추가
- 원본 외부 제안 파일을 `doc/experimental/2026-05-13-make-asset-naming-v0.5-source.md` 로 보존

### Added
- `doc/MAKE_FORMAT.md` 의 `Two-Layer Naming Model`, `L1 → L2 Normalization`, `Source Asset Filesystem Naming` 섹션
- `doc/experimental/2026-05-13-make-asset-naming-v0.5-source.md` — 통합 전 원본 제안서 아카이브

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
