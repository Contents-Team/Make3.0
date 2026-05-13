# MAKE_FORMAT

> `.make` 파일 구조 분석과 에셋 네이밍 규칙. VIRNECT 의 `Make` 콘텐츠 패키지 포맷.

## Overview

`.make` 는 **glTF 2.0 Binary (GLB)** 컨테이너 + VIRNECT 커스텀 확장(`VNT_*`) 의 조합. 표준 glTF 뷰어로 열면 3D 씬은 보이지만, AR 타겟·이벤트·오디오 트리거 같은 인터랙션 정보는 VNT 확장 안에 있어 일반 뷰어는 무시한다.

### Container

```
[ 12-byte GLB header ]  magic="glTF" version=2 totalLength=N
[ Chunk 1: JSON      ]  length, type="JSON", glTF document
[ Chunk 2: BIN       ]  length, type="BIN\0", buffers (geometry + 임베디드 이미지)
```

분석된 샘플:
- `Template_260403.make` — 2.1 MB, Unity 6000.0.59f2 URP 익스포트
- `Make Templete_20260512.make` — 7.1 MB, "Virnect Scene Generator" 생성

## glTF Top-level Keys

표준 glTF 2.0 — `asset`, `scene`, `scenes`, `nodes`, `meshes`, `materials`, `textures`, `images`, `samplers`, `accessors`, `bufferViews`, `buffers`, `animations`, `extensionsUsed`, `extensions`, `extras`.

## VNT Extension Catalog

| Extension | 위치 | 역할 |
|---|---|---|
| `VNT_NodeProperty` | node | 노드 컴포넌트 메타 (Scene/Audio/Image 등) |
| `VNT_MediaResource` | node | `extras.media[]` 배열 인덱스 참조 |
| `VNT_Event` | node | 이벤트 트리거 + 액션 체인 |
| `VNT_Animation` | root | 애니메이션 메타 |
| `VNT_Settings_Target` | root | AR 타겟 설정 (이미지·크기) |
| `VNT_Settings_Environment` | root | 환경(조명·배경) 설정 |
| `VNT_Settings_GlobalOverlay` | root | UI 글로벌 오버레이 |
| `VNT_ExternalResources` | root | 외부 리소스 카탈로그 (UUID + OriginPath) |

### VNT_NodeProperty Components

`VNT_NodeProperty` 아래에 `VIRNECT.Components.<Name>` 형태로 컴포넌트 클래스가 박힘. 관찰된 종류:

| Component | 필드 |
|---|---|
| `SceneRoot` | 마커 (필드 없음) |
| `SceneComponent` | `EnableSceneInfo`, `SceneTitle`, `SceneDetail` |
| `AudioComponent` | `ResourceKey` (UUID), `Volume`, `Loop`, `Active`, `Billboard`, `CanMove` |

(추정 — 미관찰): `ImageComponent`, `VideoComponent`, `Model3DComponent`, `TextComponent` 등 동일 패턴.

### VNT_ExternalResources Schema

```jsonc
{
  "NodeID": 18,
  "ResourceItems": [
    {
      "ResourceID": "25b10b16-7d7d-4d5b-be40-d2416294ab71",  // UUID v4
      "ResourceType": 4,                                     // 아래 enum
      "OriginPath": "C:\\Users\\...\\file.mp3",              // 익스포트 시점 절대경로
      "Thumbnail": 3,                                        // texture index
      "accessor": 27,                                        // (optional)
      "texture": 59                                          // (optional)
    }
  ]
}
```

### ResourceType Enum (관찰값)

| Value | 추정 의미 | 확장자 |
|---|---|---|
| `1` | Image | `.png`, `.jpg` |
| `4` | Audio | `.mp3`, `.wav` |
| `2` (추정) | Video | `.mp4` |
| `3` (추정) | Model3D | `.glb`, `.gltf` |

> 실측 후 확정 필요. F2 의 모든 ResourceItems 가 `ResourceType: 1` (이미지) 였음.

## Asset Embedding

| 타입 | 저장 방식 | 참조 방법 |
|---|---|---|
| 3D 메시 | GLB BIN 청크에 임베드 | `accessor` → `bufferView` → `buffer` |
| 이미지 (PNG/JPG) | GLB BIN 청크에 임베드 | `image.bufferView` + `mimeType` |
| 오디오 (MP3/WAV) | 외부 참조 | `extras.media[].ResourceID` + `extension` |
| 비디오 (MP4) | 외부 참조 (추정) | 동일 패턴 |

```jsonc
"extras": {
  "media": [
    { "ResourceID": "25b10b16-...", "AccessorId": 0, "extension": ".mp3" }
  ]
}
```

## Naming Rules v4

> **목적**: **개발자와 AI 에이전트 모두** 가 `.make` 콘텐츠의 이름만 보고 (a) 종류·확장자, (b) 소속 자산, (c) 역할·상태를 즉시 알 수 있어야 한다. **그리고** 이 자가설명을 위해 사람이 손으로 머티리얼·애니메이션·중간 노드 수백 개를 명명하는 비용은 발생하지 않아야 한다.
>
> v1: 단일 문자 prefix + NN 순번 + 영문 강제. v2: 3-Layer Identity 도입했으나 prefix 선택화로 자가설명 손실. v3: 자가설명 강제 (mandatory prefix + namespace + suffix vocab). v4: prefix 정책은 v3 유지 + **Tier 책임 분리** — 사용자는 Tier A 만 명명, 시스템이 Tier C 자동 파생.

## Tier Responsibility Matrix (v4 신규)

자가설명적 이름은 모든 자산에 필요하지만, **누가 그 이름을 만드는가** 는 Tier 에 따라 다르다.

| Tier | 예 | Prefix | 누가 입력? | 사용자 부담 |
|---|---|---|---|---|
| **A** (user-uploaded) | image, audio, video, 3D model 원본 | **필수 (`img_`, `aud_`, `vid_`, `mdl_`)** | 사용자가 슬러그 입력 → 툴이 prefix 자동 부착 | 슬러그만 (`gnb__active`) |
| **B** (user-composed) | scene, step, group container | **필수 (`scn_`, `nod_`)** | 사용자가 의미 부여, 툴이 prefix 부착 | hierarchy 설계 |
| **C** (system-derived) | material, animation clip, intermediate mesh node, texture obj | **필수 (`mat_`, `anm_`, `tex_`)** | **시스템이 source 이름 mirror 로 자동 생성** | **0** |
| **System reserved** | `SceneRoot`, `TargetManager`, `EnvironmentSetting`, `GlobalOverlaySettings`, `ContentsRoot`, `ResourceCacheRoot` | (예외, prefix 없음) | VNT 예약 | — |

### 왜 Tier C 도 prefix 필요한가 (에이전트 가독성)

사용자가 머티리얼 패널을 직접 안 본다 해도, **다음 컨텍스트에서는 이름이 단독 노출**된다:

1. 로그/에러 메시지 (`Failed to load: mat_gnb__active`)
2. VNT 확장의 cross-reference (string ResourceKey 등)
3. grep 검색 (`grep '^mat_'` 로 머티리얼만 필터)
4. AI 에이전트가 raw JSON 또는 단편을 받음 (배열 context 잃음)
5. 다국어 코드베이스에서 패턴 매칭

이름에서 prefix 가 빠지면 **컨텍스트 없이는 정체 불명**. 따라서 prefix 는 모든 Tier 에 유지. 단 Tier C 는 사람이 만들지 않고 시스템이 mirror.

## System Auto-Derivation (Tier C)

사용자가 Tier A 자산을 업로드하면 시스템이 다음 규칙으로 Tier C 이름 자동 생성.

### Derivation Rules

```
사용자 업로드 파일:   GNB_Active.png
                         │
                         ▼ (1) 정규화: 공백 제거, lowercase, 확장자 분리
이미지 슬러그:           gnb_active  (또는 가족명 구조라면 gnb__active)
                         │
                         ▼ (2) Tier A prefix 부착
images[].name:           img_gnb__active
                         │
         ┌───────────────┼───────────────┬─────────────────┐
         ▼               ▼               ▼                 ▼
   materials:      textures:      mesh nodes:        VNT_ExternalResources:
   mat_gnb__active tex_gnb__active mesh_gnb__active   ResourceID = <UUID>
                                                      (source: img_gnb__active)
```

### Mirror Algorithm

```
def auto_derive(source_name: str, target_kind: str) -> str:
    """
    source_name:  Tier A 이름 (예: 'img_gnb__active')
    target_kind:  'mat' | 'tex' | 'mesh' | 'anm' | ...
    """
    # source 의 kind prefix 제거
    body = source_name.split('_', 1)[1]  # 'gnb__active'
    # target prefix 부착
    return f"{target_kind}_{body}"  # 'mat_gnb__active'
```

### Animation 자동 파생 (특수 케이스)

애니메이션은 단일 source 가 아니라 **채널 타겟** 으로 의미가 결정됨.

```
def derive_animation_name(animation_obj: dict, nodes: list) -> str:
    # animations[].channels[].target.node 분석
    target_nodes = [nodes[ch['target']['node']]['name'] for ch in animation_obj['channels']]
    primary_target = most_common(target_nodes)  # 가장 많이 변경되는 노드
    # primary_target 의 prefix 제거 후 anm_ 부착
    body = primary_target.split('_', 1)[1]
    return f"anm_{body}"  # 'anm_laptop' (laptop 의 transform 을 주로 변경)

    # 액션 추정 (translation/rotation/scale 변화량)
    # 가능하면 action suffix 추가: anm_laptop__open, anm_laptop__rotate
```

### 1:N 케이스 처리

한 source 가 여러 Tier C 객체를 생성할 때 (예: 동일 이미지가 albedo + normal map 으로 쓰이면):

```
source:              tex_laptop__screen
파생 1 (material):   mat_laptop__screen
파생 2 (mesh):       mesh_laptop__screen  ← UI quad 또는 surface
파생 3 (사용처):     없음 (텍스처 자체는 source)

albedo vs normal 같은 채널 분기:
tex_laptop__screen_albedo, tex_laptop__screen_normal  ← 채널 suffix vocab 적용
```

### 핵심 원칙: 3-Layer Identity

모든 에셋·노드는 다음 **3개 식별자**를 가진다. 책임이 다르고 변경 가능성이 다르다.

| Layer | 필드 | 변경 | 글자 | 책임 |
|---|---|---|---|---|
| **ID** | `ResourceID` / glTF index | **불변** | UUID v4 (ASCII) | machine join key. 코드·DB·외부 참조의 진실 |
| **Name** | `node.name`, `image.name`, etc. | 변경 가능 | ASCII `lower_snake_case` | 사람·도구가 grep·diff·정렬할 때 쓰는 식별자 |
| **DisplayTitle** | `SceneTitle`, `VNT_*` extras | 자유 변경 | Unicode (한국어 OK) | 사용자 화면에 노출되는 텍스트. i18n 가능 |

**Source of truth**: ID. Name 이 바뀌어도 ID 는 그대로. ID 만 외부 참조에 쓰고, Name 은 작업 편의용, DisplayTitle 은 사용자 대면.

### ResourceID

- **포맷**: `UUID v4` (`xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx`, 소문자, 하이픈)
- **불변·전역 유일**
- **중복 감지**: 동일 에셋은 콘텐츠 해시(SHA-256 등) 기반으로 dedup → 동일 ID 재사용. 새 파일이면 새 UUID.

### Name (Identifier) — 자가설명 강제

ASCII 기반 식별자. **Kind prefix 는 필수**. v2 의 "VNT 필드가 분류 담당" 정당화는 실무에서 무효 — 개발자는 IDE·scene graph·grep 에서 이름만 보기 때문.

**구조**:

```
<kind>_<asset>[__<component>][_<channel|state>]
└─3자─┘ └────slug────┘ └──suffix vocab──┘
```

- **`<kind>`** (필수, 3자) — 아래 Kind Prefix 표
- **`<asset>`** (필수) — 자산 식별 슬러그 (`laptop`, `engine_block`, `btn_start`)
- **`__<component>`** (선택, 이중 언더스코어) — 부모 자산의 자식·부위 (`__screen`, `__keyboard`)
- **`_<channel|state>`** (선택, 단일 언더스코어 suffix) — Texture 채널·UI 상태 vocab

**규칙**:
- 정규식: `^[a-z][a-z0-9_]*$`
- 최대 64자
- 이중 언더스코어 `__` 는 부모-자식 경계 전용 (다른 곳 사용 금지)
- 순번(`01`, `02`...) 박지 않음. 순서가 의미 있으면 별도 `order: 10` 필드

**유일성 scope**:
- `ResourceID`: **글로벌 유일** (전체 파일)
- `node.name`: 같은 부모 아래에서만 유일 (glTF 스펙)
- `image.name` / `material.name`: 의미적 권장 (ID 가 식별 담당)

### Kind Prefix Table (필수, 3-letter)

| Prefix | 의미 | 예상 확장자 | 저장 위치 |
|---|---|---|---|
| `mdl_` | 3D Model (mesh/node) | `.glb` | GLB BIN |
| `mat_` | Material | (논리 단위) | glTF `materials[]` |
| `tex_` | Texture (3D 입력) | `.png .jpg` | GLB BIN |
| `img_` | UI Image (2D 레이어) | `.png .jpg .webp` | GLB BIN |
| `aud_` | Audio | `.mp3 .wav` | external (`extras.media[]`) |
| `vid_` | Video | `.mp4 .webm` | external |
| `anm_` | Animation clip | (논리 단위) | glTF `animations[]` |
| `evt_` | Event trigger | (논리 단위) | `VNT_Event` |
| `scn_` | Scene container | (논리 단위) | scene root |
| `nod_` | Generic group | (논리 단위) | empty transform |

3-letter 이유: 단일 문자 모호성 (`M` = Model? Material? Mesh?) 제거. `mdl` vs `mat` 처럼 두 번째 글자로 확정.

### Texture Channel Suffix Vocabulary

| Suffix | 의미 |
|---|---|
| `_albedo` | Base color / diffuse |
| `_normal` | Normal map |
| `_roughness` | Roughness |
| `_metallic` | Metallic |
| `_ao` | Ambient occlusion |
| `_emissive` | Emissive |
| `_height` | Height / displacement |
| `_opacity` | Alpha mask |
| `_orm` | Occlusion-Roughness-Metallic 합성 |

### UI Image State Suffix Vocabulary

| Suffix | 의미 |
|---|---|
| `_default` | 기본 |
| `_hover` | 마우스 오버 |
| `_pressed` | 눌림 |
| `_active` | 활성화됨 |
| `_disabled` | 비활성화 |
| `_focused` | 포커스 |

### Asset Namespace 예시 — 노트북 3D 모델

```
mdl_laptop                        ← 루트 모델 노드 (.glb)
├── mdl_laptop__screen            ← sub-mesh
├── mdl_laptop__keyboard
├── mdl_laptop__hinge
└── mdl_laptop__body

mat_laptop__screen                ← 화면 머티리얼
mat_laptop__body_metal            ← 본체 메탈
mat_laptop__keyboard_plastic      ← 키보드 플라스틱

tex_laptop__screen_albedo         ← 화면 base color
tex_laptop__screen_emissive       ← 화면 발광
tex_laptop__body_albedo
tex_laptop__body_normal
tex_laptop__body_roughness
tex_laptop__body_metallic
tex_laptop__keyboard_albedo

anm_laptop__open                  ← 노트북 열기
anm_laptop__close
```

**`mat_laptop__body_metal` 해석 (이름만으로)**:
- `mat_` → 머티리얼
- `laptop` → 노트북 모델 소속
- `body` → 본체 부위
- `metal` → 메탈 변형 (다른 변형이 있을 수 있음 — `_plastic`, `_glass` 등)

### 한국어·고유명사 정책

| 상황 | 규칙 |
|---|---|
| Name (identifier) | ASCII 기본. `mdl_notebook`, `mat_button` |
| 한국어 고유명사 | 로마자 표기 + **용어집 (`doc/GLOSSARY.md`)** 등록 필수<br>예: `mdl_hangang_bridge` → glossary "한강대교" |
| DisplayTitle (사용자 화면) | Unicode 자유 — 한국어, 이모지 OK |

용어집은 `mdl_*`, `img_*`, `aud_*` 등에서 사용된 모든 로마자 슬러그 → 한국어 정식 명칭 매핑 보관.

### DisplayTitle (User-facing)

- 위치: `VNT_NodeProperty.VIRNECT.Components.SceneComponent.SceneTitle` 등 컴포넌트 안의 `*Title` `*Detail` `*Label` 필드
- 정규식: 제어문자 (`-`) 만 금지, 나머지 자유
- 한국어·이모지 OK
- i18n: locale 별 분기 가능 (확장 권장 — `SceneTitle.ko`, `SceneTitle.en`)

**예시**: `"엔진 점검 시작"`, `"Step 1 — Diagnose"`, `"마지막 문장을 재생합니다."`

### Material (Definition vs Instance)

Unity 등 엔진의 instance 사슬은 **runtime 복사본** — 별도 이름 필요 없음.

- **Definition** (source material) — 한 번만 명명: `unlit_opaque_button`, `lit_metal_steel`
- **Instance** — 익스포트 시 인스턴스 표기 제거. 동일 정의 참조하면 같은 이름으로 직렬화하거나, 인스턴스 명시 필요시 `_inst<index>` (예: `unlit_opaque_button_inst003`)

### Animation

- 정규식: Name 규칙 동일
- 형식 권장: `<target>_<action>` (kind prefix 불필요 — 애니메이션 컨테이너 자체가 종류)
- 예시: `logo_fade_in`, `camera_dolly_in`, `door_open`
- Unity 기본값 (`new Clip`) 금지

### Mesh

- 노드명과 동일 규칙
- **파일 확장자 노드명에 넣지 말 것** — 현재 안티패턴: `Logox4.png` 가 메시명. 정정: `logo_x4`

### OriginPath (보안·이식성 정책)

작성자 PC 의 로컬 경로 누설 방지.

| 단계 | 정책 |
|---|---|
| **로컬 작업본** | OriginPath 보존 OK (round-trip · 재임포트용) |
| **공유/배포본** | 익스포트 파이프라인에서 다음 변환:<br>① `C:\Users\<유저명>` → `<HOME>` 치환<br>② `<HOME>/Downloads/work/Projects/<프로젝트>` → `<PROJECT_ROOT>` 치환<br>③ 사용자명·식별 정보 스크럽 |
| **외부 배포본** | OriginPath 필드 완전 제거. ResourceID 만 유지 |

## v3 → v4 보강 근거 — "에이전트도 읽는다 + 사용자 노동 절감"

v3 는 자가설명을 강제하면서 **명명 비용** 을 고려 못 했음. 사용자 지적 2개로 노출:

1. UI 가족명 (`gnb`, `lnb`, `btn`) 이 이미 분류 함의 → prefix 가 redundant 길이만 증가? (반박: agent context 에서는 여전히 필요)
2. 사용자가 안 만지는 시스템 객체 (material, animation, intermediate node) 까지 사람이 명명할 필요는 없음 → 그러나 **에이전트는 읽어야 함** → 이름은 있되 자동 생성

**v4 합의**: prefix 정책 (v3) 유지 + **이름 입력 책임을 Tier 로 분리**.

| v3 | v4 |
|---|---|
| 모든 263 머티리얼을 손으로 의미 부여 | 시스템이 source mirror 로 자동 생성 (사람 0 작업) |
| 모든 7 애니메이션을 손으로 의미 부여 | 채널 타겟 분석으로 자동 파생 |
| 사용자 명명 부담: ~660 항목 | 사용자 명명 부담: ~192 항목 (Tier A·B 만, ~70% 감소) |

**유지**: 모든 이름은 여전히 kind prefix 보유 (자가설명). 에이전트가 단독 이름만 받아도 종류 파악 가능.

## v2 → v3 보강 근거 — "이름만 봐도 알 수 있다" 목적

v2 의 "Kind prefix 선택화" 가 실무 목적과 충돌. v3 보강 매핑:

| # | v2 의 결함 | v3 보강 |
|---|---|---|
| 1 | Kind prefix 선택화 → 이름만으로 종류 파악 불가 | 3-letter prefix 필수 (`mdl_`, `mat_`, `tex_`, `img_`, `aud_` 등) |
| 2 | Material 이 어떤 모델 소속인지 이름에 없음 | `<asset>__<component>` namespace — `mat_laptop__screen` |
| 3 | Texture (3D 입력) vs UI Image 미구분 | `tex_` vs `img_` prefix 분리 |
| 4 | Texture 채널 (albedo/normal/...) 표현 없음 | Channel suffix vocab — `_albedo`, `_normal`, `_roughness` ... |
| 5 | 파일 확장자 추론 불가 | Kind prefix → 확장자 매핑 표 명문화 |
| 6 | UI image 상태 (default/hover/pressed) 미규정 | State suffix vocab — `_default`, `_hover`, `_pressed` ... |
| 7 | ASCII 강제가 한국어 고유명사 자가설명 해침 | 로마자 + 용어집 (`doc/GLOSSARY.md`) 정책 |

**핵심 트레이드오프 인정**: v3 는 의도적으로 **VNT type 필드와 prefix 의 이중 인코딩**을 허용. v2 에서 "이중 인코딩 = 동기화 비용" 으로 비판했으나, 실무에서 개발자는 **JSON 메타필드 안 보고 이름만** 읽는 상황이 압도적으로 많음. 자가설명 가치가 동기화 비용을 능가.

## v1 → v2 보강 근거

v1 규칙의 8가지 허점과 보강 매핑 (역사적 기록):

| # | v1 허점 | v2 보강 |
|---|---|---|
| 1 | 단일 문자 prefix (`M` = Model? Material?) 모호 | Kind prefix 선택화. VNT type 필드가 이미 분류 |
| 2 | `<NN>` 2자리 — 실측 142개 vs 최대 100 | 순번 자체 제거. 필요 시 별도 `order: 10` (10단위) |
| 3 | 순번 renumber 캐스케이드 | 순번 제거 → 삭제·삽입 자유. 정렬은 `order` 필드 |
| 4 | Name vs ID 권위 불명 | 3-layer 분리 (ID / Name / DisplayTitle), source of truth = ID |
| 5 | 영문 강제 → 한국 사용자 대면 문구 손실 | DisplayTitle 은 Unicode 자유. Name 만 ASCII |
| 6 | Material instance·definition 미구분 | Definition 명명, instance 표기 제거 또는 `_inst<idx>` |
| 7 | 유일성 scope 불명 | ID=global, name=parent-local (glTF 스펙 따름) |
| 8 | 단일 정규식이 표시명까지 ASCII 강제 | identifier 정규식 + display 정규식 분리 |

**메타 보강**: prefix 시스템 over-engineering 의심 → VNT 의 `VIRNECT.Components.*` 가 이미 카테고리 역할. Name 에 prefix 박는 건 **이중 인코딩** → 선택화로 완화.

## 권장 파일 레이아웃 (Origin 디렉토리)

`.make` 익스포트 전 원본 작업 폴더 구조 권장:

```
<project>/
├── 2d/                      # 이미지 에셋 (.png .jpg .webp)
│   ├── ui/                  # 버튼·아이콘·HUD
│   ├── logo/                # 로고·브랜드
│   └── background/          # 배경 이미지
├── 3d/                      # 3D 에셋 (.glb .gltf .fbx)
│   ├── models/
│   └── textures/
├── audio/                   # 오디오 (.mp3 .wav)
│   ├── narration/           # 더빙·내레이션
│   ├── sfx/                 # 효과음
│   └── bgm/                 # 배경음악
├── video/                   # 동영상 (.mp4 .webm)
└── scene/                   # 씬 정의·메타
    └── *.make
```

각 폴더 안 파일명은 `<category>_<slug-en>_<NN>.<ext>` 권장:
- `audio/narration/narr_intro_01.mp3`
- `2d/ui/btn_start_default.png`
- `3d/models/m_engine_block_01.glb`

## 안티패턴 요약 (현재 샘플에서 관찰된 것)

| 문제 | 위치 | 위험 |
|---|---|---|
| 한글 + 공백 노드명 | F1 `nodes[]`, `meshes[]` | cross-platform 이슈, 검색·diff 어려움 |
| 파일 확장자가 노드명에 포함 | F2 `"Logox4.png"`, `"btn_start.png"` 가 노드명 | 메시·이미지 구분 어려움 |
| Unity 인스턴스 사슬 머티리얼명 | F2 모든 머티리얼 | 디버깅·검색 불가 |
| 기본 애니메이션명 | F1·F2 모두 | 어떤 애니메이션인지 식별 불가 |
| 절대경로 OriginPath 박제 | `VNT_ExternalResources` | 정보 누설·이식성↓ |
| ResourceID 와 노드명 불일치 | F1 mp3 노드 | 매핑 추적 어려움 |

## Validation Checklist (`.make` 익스포트 전, v2)

### Identifier (Name) 검증
- [ ] 모든 ASCII `name` 필드가 정규식 `^[a-z][a-z0-9_]*$` + 64자 이하 통과
- [ ] 모든 name 이 **Kind prefix** (`mdl_`/`mat_`/`tex_`/`img_`/`aud_`/`vid_`/`anm_`/`evt_`/`scn_`/`nod_`) 로 시작 — Tier C 포함 (시스템 자동 생성이라도 prefix 유지)
- [ ] 자식·부위 표현 시 **이중 언더스코어** `__` 사용 (`mdl_laptop__screen`)
- [ ] Texture 는 채널 suffix (`_albedo`/`_normal`/...) 명시
- [ ] UI Image 다중 상태는 state suffix (`_default`/`_hover`/...) 명시
- [ ] 노드명은 부모 노드 안에서 유일 (sibling 중복 0건)
- [ ] 파일 확장자 (`.png`, `.jpg`, `.mp3`, `.glb`) 가 `name` 에 포함되지 않음
- [ ] 한국어 고유명사가 로마자 슬러그로 사용된 경우 `doc/GLOSSARY.md` 에 등록됨

### Tier 분리 검증 (v4 신규)
- [ ] **Tier A** (이미지·오디오·비디오·3D 모델 원본): 사용자가 슬러그 입력, 툴이 prefix 부착
- [ ] **Tier B** (씬·스텝·그룹 컨테이너): 사용자가 의미 부여, 툴이 prefix 부착
- [ ] **Tier C** (머티리얼·애니메이션·중간 mesh 노드): 시스템이 source 이름 mirror 로 자동 생성. 사람 입력 없음
- [ ] Tier C 객체의 이름이 source Tier A/B 이름과 **derivation 규칙** 으로 연결되는지 확인 (예: `img_gnb__active` → `mat_gnb__active`)
- [ ] 애니메이션 이름이 채널 타겟 분석으로 파생되었는지 (`anm_<primary_target_body>`)

### ID 검증
- [ ] 모든 `ResourceID` 가 UUID v4 포맷 (소문자 + 하이픈)
- [ ] `ResourceID` 가 파일 전체에서 글로벌 유일
- [ ] 동일 콘텐츠 해시는 동일 `ResourceID` 재사용 (중복 임베딩 0건)

### Material/Animation 검증
- [ ] 머티리얼명에 `(Instance)` 사슬 없음
- [ ] 머티리얼 definition 만 의미 있는 이름, instance 는 `_inst<idx>` 또는 무명
- [ ] 애니메이션명에 `new Clip` 등 엔진 기본값 없음
- [ ] 애니메이션명이 `<target>_<action>` 패턴 (Unicode prose 금지)

### DisplayTitle 검증
- [ ] DisplayTitle 필드에 제어문자 없음
- [ ] (i18n 사용 시) `<title>.ko` / `<title>.en` 둘 다 존재하거나 fallback 명시

### Path/Privacy 검증
- [ ] 공유/배포본의 `OriginPath` 에 `C:\Users\`, `/home/`, `/Users/` 같은 사용자 홈 경로 없음
- [ ] 작성자 식별 정보 (사용자명, 이메일) 의 `extras` 누설 없음

## References

- glTF 2.0 spec: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
- GLB binary format: https://github.com/KhronosGroup/glTF/blob/main/specifications/2.0/Specification.adoc#binary-gltf-layout
- VNT extensions: 내부 문서 — TODO: 작성·링크

## Sample Inspection Snippets

전체 JSON 청크 추출 (PowerShell):

```powershell
$bytes = [System.IO.File]::ReadAllBytes('path/to/file.make')
$chunkLen = [BitConverter]::ToUInt32($bytes, 12)
$json = [System.Text.Encoding]::UTF8.GetString($bytes, 20, $chunkLen).TrimEnd([char]0,' ')
$json | Out-File 'file.json' -Encoding UTF8
```

`jq` 로 외부 리소스만 추출:

```bash
jq '.extensions.VNT_ExternalResources.ResourceItems[] | {ResourceID, ResourceType, OriginPath}' file.json
```
