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

## Naming Rules v6

> **목적**: **개발자, 사용자, AI 에이전트 모두** 가 `.make` 콘텐츠를 다룰 때, 각 컨텍스트(OS 파일 탐색기 / Make Editor UI / JSON·grep) 에 가장 적합한 명명 형식을 사용한다. UI 아이콘이 타입을 알려주는 컨텍스트에서는 prefix 를 제거해 간결성을 우선, 이름 단독 노출 컨텍스트에서는 prefix 를 유지해 자가설명 보존.
>
> v1: 단일 문자 prefix + NN 순번 + 영문 강제. v2: 3-Layer Identity 도입했으나 prefix 선택화로 자가설명 손실. v3: 자가설명 강제 (mandatory prefix + namespace + suffix vocab). v4: prefix 정책은 v3 유지 + **Tier 책임 분리** — 사용자는 Tier A 만 명명, 시스템이 Tier C 자동 파생. v5: **소스 에셋 파일시스템 레이어** 추가 — `.make` 내부 식별자와 외부 원본 파일 명명을 명시적으로 분리. v6: **3-Tier 책임 모델** 로 재구성 — T1 (파일시스템 소스) / T2 (Make Editor 인스턴스, prefix 폐지·PascalCase·짧음) / T3 (시스템 파생, prefix 유지). 단일 `_` 통일, 하이픈 금지, state·action·direction vocab 축약.

## Three-Tier Naming Model (v6)

| Tier | 적용 대상 | 형식 | 사용자가 봄? | AI raw 입력? |
|---|---|---|---|---|
| **T1 — Source Asset (filesystem)** | 모델러/아티스트가 납품하는 원본 파일 (`.fbx`, `.png`, `.wav`, `.mp4`, `.ttf`) | **PascalCase** + 확장자 + 카테고리/Role 토큰 (모호 타입만) + `_v<NN>` (옵션) | ✅ OS 파일 아이콘 보조 | ✅ filename 단독 전달 가능 |
| **T2 — Instance (Make Editor)** | `.make` 안의 사용자 직접 명명 노드 (씬·페이지·UI 그룹·이미지·3D 모델 등) | **PascalCase**, **kind prefix 없음**, 단일 `_`, 트리 컨텍스트 활용 | ✅ Make Editor 타입 아이콘 보조 | ❌ 보통 JSON 구조와 동반 |
| **T3 — System-Derived** | 머티리얼·중간 mesh·texture object 등 사용자가 직접 명명 안 함 | **lower_snake_case** + 3-letter kind prefix (구 v4·v5 L2 본문) | △ 패널에서 간접 노출 | ✅ string cross-ref 단독 노출 빈도 높음 |

**왜 컨텍스트별로 형식이 다른가**:
- T1: 모델러 도구(Blender/Maya/Photoshop) 산업 관례 + OS 파일 탐색기 가독성. 확장자가 타입을 선언.
- T2: Make Editor 트리 옆 타입 아이콘이 종류를 알려줌 → prefix redundant. 부모-자식 컨텍스트가 의미를 보강 → 자식 이름은 짧게.
- T3: 사용자 미편집·AI grep·로그 단독 노출 빈도 높음 → prefix 보존이 비용 0, 가치 큼. 시스템 자동 파생이므로 사용자 명명 부담 없음.

### T1 → T2 Transform (Import-time)

```
Source file:        GlassBottle_Cap_v01.fbx           (T1, PascalCase + vNN + ext)
                         │
                         ▼ (1) 확장자 제거 (Make Editor 아이콘이 타입 알려줌)
                         ▼ (2) _v<NN> marker 제거 (버전은 ResourceID 로 추적)
                         ▼ (3) PascalCase 보존
Instance name:      GlassBottle_Cap                    (T2, 짧고 자연스러움)
```

State 토큰도 PascalCase 로 보존: `GlassBottle_Open_v01.fbx` → `GlassBottle_Open`.

T3 (머티리얼·중간 mesh) 는 별도 자동 파생 (Tier C 알고리즘) — 본문 후반 참조.

## T1 — Source Asset Filesystem Naming (v6)

> 모델러·아티스트가 납품 또는 작업 디렉토리에 두는 원본 파일 명명 규칙. `.make` 임포트 이전 단계.

### Design Principles

| 원칙 | 설명 |
|---|---|
| 공백 금지 | 공백은 CLI·툴 파이프라인을 깨뜨림 |
| 구분자 `_` 만 사용 | 하이픈·점·혼합 구분자 금지 |
| 토큰 내부는 PascalCase | `GlassBottle` (not `glassbottle` / `glass-bottle`) |
| 동의어 금지 | 한 개념당 한 용어 — 별칭 허용 안 함 |
| 최소 토큰 | 의미를 더하지 않는 토큰 제거. 확장자가 타입을 선언하면 이름에 타입 토큰 박지 말 것 |
| 영문만 | 한국어 파일명 금지 (GLOSSARY 매핑 사용) |

### Global Rules

| Rule | ✅ Correct | ❌ Incorrect |
|---|---|---|
| 공백 없음 | `GlassBottle_v01.fbx` | `Glass Bottle_v01.fbx` |
| 구분자 `_` | `GlassBottle_Cap_v01` | `GlassBottle-Cap-v01` |
| 토큰별 PascalCase | `BatteryPack` | `batterypack` / `battery_pack` |
| Variant 2자리 고정 | `_01`, `_02` | `_1`, `_001` |
| Version `v` + 2자리 (옵션) | `_v01`, `_v02` | `_V1`, `_ver01` |
| 하이픈 금지 | `Contents_3_1_1_2` | `Contents_3-1-1-2` |
| 중복 타입 토큰 금지 | `GlassBottle_v01.fbx` | `GlassBottle_MOD_v01.fbx` |
| 영문 전용 | `BatteryPack_v01` | `배터리팩_v01` |

> ⚠️ Version 히스토리 (`_v01`, `_v02`) 는 납품 전 WIP 관리용 (v6 에서 **옵션**). 최종 납품 에셋은 별도 합의 없으면 단일 깨끗한 버전만 유지.

### Source Asset vs Scene Instance (the `v` marker)

`.make` 씬 안에 동일 소스 에셋을 여러 번 배치할 수 있다. 각 배치는 독립 인스턴스 — 자체 이름·transform·이벤트 보유.

| Pattern | Meaning | Layer |
|---|---|---|
| `Name_v<NN>.<ext>` | Source Asset (원본 파일) | L1 — filesystem |
| `Name_<NN>` (확장자 없음) | Scene Instance Object | `.make` 내부 (legacy 표기) |
| `Name_<NN>.<ext>` | ❌ 모호 — 소스 파일인지 잘못 명명된 인스턴스인지 불명 |
| `Name_v<NN>` (확장자 없음) | ❌ 모호 — 소스처럼 보이는데 확장자가 없음 |

> Note: `.make` 내부 식별자의 권위 있는 형식은 L2 의 `mdl_glass_bottle` (snake_case + prefix). 위의 `Name_<NN>` 인스턴스 표기는 외부 도구 호환을 위한 보조 표현으로만 사용.

### Source Asset Syntax

```
<Name>[_State]_v<NN>.<ext>                            루트 파일
<ParentName>_<ChildName>[_State]_v<NN>.<ext>          자식 부위 파일 (분리 납품)
```

#### Token Definitions

| Token | Description | Format |
|---|---|---|
| `Name` | 자산 고유 식별자 | PascalCase |
| `ParentName` | 부모 자산명 (자식 부위에서) | PascalCase |
| `ChildName` | 부위·컴포넌트 명 | PascalCase |
| `State` | 형태 변형 (기본형과 다를 때만) | PascalCase (`Open`, `Broken`, `Closed`, `Damaged`) |
| `v<NN>` | 소스 에셋 버전 번호 | `v01`, `v02` |

### Per-Type Source Naming

#### L1.1 — 3D Model (`.fbx`)

확장자 `.fbx` 가 타입을 선언. **이름에 타입 토큰 박지 말 것.**

```
GlassBottle_v01.fbx
GlassBottle_v02.fbx
GlassBottle_Open_v01.fbx
GlassBottle_Broken_v01.fbx
GlassBottle_Cap_v01.fbx                 # 자식 부위 (분리 납품)
GlassBottle_Label_v01.fbx
BatteryPack_v01.fbx
BatteryPack_TopCover_v01.fbx
BatteryPack_Handle_v01.fbx
WorkshopTable_v01.fbx
WorkshopTable_Drawer_v01.fbx
```

#### L1.2 — Image / Texture (`.png`)

PNG 는 **Role/Descriptor 토큰이 필요한 유일한 타입**. UI 스프라이트와 3D 텍스처가 모두 PNG 라 확장자만으론 용도 분간 불가.

| Token | Meaning | Used for |
|---|---|---|
| `Sprite` | UI 이미지 (버튼·아이콘·패널·배경) | UI |
| `ALB` | Albedo / Base Color | 3D Texture |
| `NRM` | Normal Map | 3D Texture |
| `RGH` | Roughness Map | 3D Texture |
| `MET` | Metallic Map | 3D Texture |
| `EMI` | Emission Map | 3D Texture |
| `MSK` | Mask Map | 3D Texture |
| `AO` | Ambient Occlusion | 3D Texture |

```
<Name>_<Role>_<NN>.png                3D 텍스처
<UIElementName>_Sprite_<NN>.png       UI 스프라이트
```

```
GlassBottle_ALB_01.png
GlassBottle_NRM_01.png
GlassBottle_RGH_01.png
GlassBottle_MET_01.png
GlassBottle_Cap_ALB_01.png
BatteryPack_ALB_01.png
BatteryPack_EMI_01.png
PlayBtn_Sprite_01.png
CloseBtn_Sprite_01.png
WarningIcon_Sprite_01.png
StepCompleteIcon_Sprite_01.png
PanelBackground_Sprite_01.png
```

> ⚠️ PNG 텍스처는 `v<NN>` 미사용 — 아트 에셋이며 버전 관리되는 소스 파일이 아니다. variant `<NN>` 으로 충분.
> L2 변환 시 Role 토큰은 채널 suffix 로 매핑: `GlassBottle_ALB_01.png` → `tex_glass_bottle_albedo`, `PlayBtn_Sprite_01.png` → `img_play_btn_default`.

#### L1.3 — Audio (`.wav`, `.mp3`)

확장자가 타입 선언. 카테고리는 첫 토큰으로, description 과 `_` 로 구분 (v6 — `GNB_Active` 패턴과 일관).

| Category | 풀이 | Meaning |
|---|---|---|
| `BGM` | Background Music | 배경음악 |
| `SFX` | Sound Effect | 효과음 (UI 클릭·완료음·경고 등) |
| `NAR` | Narration | 내레이션·더빙 (구 `VO`) |

```
<Category>_<Description>_<NN>.<ext>
```

```
BGM_Tutorial_01.wav
BGM_Boss_01.wav
SFX_UI_Click_01.wav
SFX_StepComplete_01.wav
SFX_AlertWarning_01.wav
NAR_Intro_01.wav
NAR_Step01_Guide_01.wav
```

> v5 의 `VO` 는 `NAR` 로, `AMB` 는 제거 (현재 사용처 없음 — 필요 시 향후 추가).

#### L1.4 — Video (`.mp4`)

확장자가 타입 선언. 컨텍스트는 첫 토큰, description 과 `_` 로 구분.

| Category | 풀이 | Meaning |
|---|---|---|
| `CUT` | Cutscene | 시네마틱·서사 영상 클립 |
| `TUT` | Tutorial | 단계별 설명·튜토리얼 영상 |
| `LOOP` | Looping background video | 반복 재생 배경 영상 |
| `INTRO` | Intro sequence | 콘텐츠 진입 인트로 |
| `OUTRO` | Outro sequence | 콘텐츠 종료 아웃트로 |

```
<Category>_<Description>_<NN>.mp4
```

```
INTRO_Main_01.mp4
OUTRO_Credit_01.mp4
CUT_AssemblyStep01_01.mp4
TUT_BatterySwap_Step01_01.mp4
TUT_BatterySwap_Step02_01.mp4
LOOP_WorkshopBackground_01.mp4
```

#### L1.5 — Text / Font

폰트 파일은 공유 자원 — 콘텐츠 종속 아님. 인-콘텐츠 텍스트 객체(라벨·타이틀)는 파일이 아닌 씬 객체.

**Source Asset (Font File)**

```
<FontFamilyName>_<Weight>_<NN>.<ext>
```

```
NotoSansKR_Regular_01.ttf
NotoSansKR_Bold_01.ttf
Roboto_Medium_01.ttf
```

씬 텍스트 객체는 L2 규칙 (`txt_step_title` 또는 v4 의 `nod_step_title`) 을 따른다.

### Hierarchy Rules — Parent & Child (L1)

#### Source Asset Delivery

자식 부위를 별도 FBX 로 납품할 때 **부모 이름을 반드시 포함** — 파일명만으로 AI·사람이 관계 파악 가능.

```
GlassBottle_v01.fbx          ← Parent
GlassBottle_Cap_v01.fbx      ← Child part of GlassBottle
GlassBottle_Label_v01.fbx    ← Child part of GlassBottle
```

#### Scene Object Hierarchy (legacy 표기)

L2 의 `mdl_glass_bottle__cap` 표기를 권장하나, 외부 도구가 PascalCase 만 지원할 때의 대체 표기:

| Case | Child name 형식 | 자체 기술 | 권장 용도 |
|---|---|---|---|
| **A** — 씬 트리를 AI 가 읽음 | `Cap_01` | ❌ 트리 필요 | Make 내부 동작 |
| **B** — AI 가 이름 문자열만 받음 | `GlassBottle_01_Cap_01` | ✅ 이름만으로 완전 | 파일 납품·외부 리뷰 |

> **Make 3.0 권장**: 내부 정규화 후 L2 의 `mdl_glass_bottle__cap` 사용. Case A/B 는 외부 인터페이스 호환용.

### Instance Rules (L1 외부 표기)

#### Same source, multiple placements

```
Source:   GlassBottle_v01.fbx
Scene:    GlassBottle_01       ← 1st instance
          GlassBottle_02       ← 2nd instance
          GlassBottle_03       ← 3rd instance
```

#### Different state variants, multiple placements

```
Source (base):      GlassBottle_v01.fbx
Source (open lid):  GlassBottle_Open_v01.fbx
Scene:    GlassBottle_01          ← base, 1st
          GlassBottle_02          ← base, 2nd
          GlassBottle_Open_01     ← open, 1st
          GlassBottle_Open_02     ← open, 2nd
```

#### Collision check — instance number vs source version

| Name | Layer | Meaning |
|---|---|---|
| `GlassBottle_v01.fbx` | Source Asset | Version 1 of the original file |
| `GlassBottle_v02.fbx` | Source Asset | Version 2 — revised delivery |
| `GlassBottle_01` | Scene Instance | 1st placement in scene |
| `GlassBottle_02` | Scene Instance | 2nd placement in scene |

> `v` marker 가 소스와 인스턴스 레이어를 완전 분리. **명명 충돌 불가능.**

## T2 — Instance Naming (Make Editor visible, v6)

> Make Editor 트리에 노출되는 사용자 직접 명명 노드. 아이콘이 타입을 시각적으로 알려주므로 **kind prefix 폐지**. 부모-자식 트리 컨텍스트가 의미를 보강하므로 **자식 이름은 짧게**.

### Core Rules

| Rule | ✅ | ❌ |
|---|---|---|
| PascalCase 토큰 | `BtnStart`, `GNB_Act` | `btn_start`, `gnb_act` |
| Prefix 없음 (T2 한정) | `Cupcake` | `mdl_cupcake` |
| 단일 `_` 만 (하이픈·이중 `__` 금지) | `Contents_3_1_1_2` | `Contents_3-1-1-2`, `Contents__3` |
| 확장자 없음 | `Logo_x4` | `Logo_x4.png` |
| 닫힌 sibling vocab 은 단문자 OK | `RotationPanel/L`, `…/R` | (해당 부모 컨텍스트 외에선 사용 금지) |
| 자유 명명 sibling 은 의미 슬러그 | `BtnReset`, `BtnZoomIn` | `R`, `Z` (모호) |

### Syntax

```
<Family><Asset>[_<Direction>][_<State>]

Family    : UI Family Vocab (선택, 권장)
Asset    : 자산 슬러그 (PascalCase)
Direction : Direction Vocab (해당 시, 단문자)
State     : State Vocab (3-letter 축약)
```

### UI Family Vocab (v6, 권장)

T2 인스턴스명에서 family 토큰 사용을 권장 — 인계 시 직관성·범용성 확보.

| Family | 의미 | Asset slug 필요? |
|---|---|---|
| `GNB` | Global Navigation Bar | ❌ (단독 사용 OK) |
| `LNB` | Local Navigation Bar | ❌ |
| `Btn` | Button (generic) | ✅ |
| `Nav` | Navigation control (prev/next) | ❌ |
| `Pnl` | Panel / Background container | ❌ |
| `Ico` | Icon | ✅ |
| `Bg` | Background image | ❌ |
| `Logo` | Logo / Brand mark | ❌ |
| `Tip` | Tooltip | ❌ |
| `Txt` | Text / Label (T2 family 로만, prefix 아님) | ✅ |

### State Vocab (v6, 3-letter 축약)

VR/터치 환경 기준 — `Hover`·`Focused`·`Highlight` 삭제, `Active/Disabled` 를 `On/Off` 로 통합.

| Suffix | 풀이 | 의미 |
|---|---|---|
| `_Def` | Default | 기본 |
| `_Prs` | Pressed | 눌림 |
| `_On` | On (Active) | 활성/켜짐 |
| `_Off` | Off (Disabled) | 비활성/꺼짐 |
| `_Sel` | Selected | 선택됨 |

> ⚠️ `_On`/`_Off` 는 토글 상태(`btn_rotation_on/off`) 와 가용성(예전 `Active/Disabled`) 두 의미를 통합. 의미 분기가 필요한 경우는 VNT 컴포넌트 필드(`Enable` 등) 에서 처리하고, **이름은 시각 상태만** 표현.

### Direction Vocab (v6)

방향 정보가 자산명 일부일 때 단문자 suffix.

| Suffix | 의미 |
|---|---|
| `_L` | Left |
| `_R` | Right |
| `_U` | Up |
| `_D` | Down |
| `_CW` | Clockwise (회전 전용) |
| `_CCW` | Counter-clockwise |

### 닫힌 Sibling Vocabulary — 단문자 허용 컨텍스트

부모 노드의 자식 sibling 이 닫힌 vocabulary(L/R/U/D, In/Out, Prev/Next) 로 완결되면 자식 이름은 단문자 OK. AI 가 parent path 로 의미 합성 가능.

```
RotationPanel
├── L              ← parent=RotationPanel 컨텍스트에서 "회전 왼쪽" 자명
├── R
├── U
└── D
```

→ 단, sibling 이 자유 명명(BtnReset, BtnZoomIn 등) 으로 섞이면 단문자 금지 — 의미 슬러그 필요.

### Examples — 실측 파일(`Make Templete_20260512.make`) 변환

```
SceneRoot                       (예약, 유지)
├── Start
│   ├── Logo_x4                 ← Logox4.png
│   ├── StartHeadline           ← Text 1 (의미 부여)
│   ├── BtnStart                ← btn_start.png
│   └── PnlTablet               ← Tablet.png
├── Contents_1_1                ← Contents 1-1 (하이픈 → _)
│   ├── GNB_1
│   │   ├── GNB_On              ← GNB_Active.png
│   │   ├── GNB_Def
│   │   ├── GNB_Off             ← GNB_Disabled.png
│   │   └── GNB_Prs
│   └── LNB_1_1
├── Contents_3_1_1_2            ← 4단계 위계, 하이픈 → _
└── Contents_4
    ├── Stage_3D                ← '3D Model' (공백 제거)
    │   └── Cupcake             ← '0016' (GLOSSARY: 0016 → Cupcake)
    ├── PnlNav                  ← Navi.png
    │   ├── BtnNavi_L
    │   │   ├── BtnNavi_L_Def
    │   │   ├── BtnNavi_L_Off
    │   │   ├── BtnNavi_L_Prs   (오타 Presssed 교정)
    │   │   └── BtnNavi_L_Hl    (※ Highlight 는 v6 vocab 에서 제거 — 대체: _Prs)
    │   ├── NavTitle
    │   ├── NavPage
    │   ├── BtnNavi_R
    │   └── Tip                 ← tooltip.png
    └── RotationPanel
        ├── L                   ← R_rotation 의 R 등, 단문자 OK
        ├── R
        ├── U
        ├── D
        ├── BtnReset
        ├── BtnZoomIn
        └── BtnZoomOut
```

## Animation Naming (v6)

애니메이션은 `animations[]` 배열에 위치 — **타입이 위치로 선언**되므로 prefix 없음. 한 클립이 여러 속성 (rotation/scale/translation/color/opacity) 을 동시에 변경 가능.

### Syntax

```
<Target>_<Act1>[_<Dir1>][_<Act2>[_<Dir2>]]...

Target    : primary channel target 노드의 슬러그 (PascalCase)
Act       : Action Vocab (2~3-letter)
Dir       : Direction Vocab (해당 Act 가 방향성 있을 때)
```

여러 속성이 한 클립에 있으면 **결정론적 순서**: `Rot → Scl → Mov → Clr → Op`.

### Action Vocab

| Abbr | 풀이 | 채널 path |
|---|---|---|
| `Rot` | Rotate | rotation |
| `Scl` | Scale | scale |
| `Mov` | Move | translation |
| `Clr` | Color | material color / texture switch |
| `Op` | Opacity | alpha |

#### Compound short-forms (자주 쓰는 UX 패턴)

| Abbr | 풀이 | 채널 조합 |
|---|---|---|
| `ZI` | Zoom In | Scl + Mov (towards) |
| `ZO` | Zoom Out | Scl + Mov (away) |
| `FI` | Fade In | Op (0→1) |
| `FO` | Fade Out | Op (1→0) |
| `Tx` | Transform (full) | Rot + Scl + Mov |
| `Pop` | Pop (scale easing) | Scl with bounce |

> 정의되지 않은 2-letter action 토큰은 임포트 검증에서 에러 — 오타 보호.

### Examples — 실측 7개 애니메이션

| 현재 (default) | 채널·path | v6 |
|---|---|---|
| `new Clip` (btn_start, scale) | scale | `BtnStart_Scl` |
| `new Clip` (3D Model, rotation) | rotation | `Cupcake_Rot_L` |
| `new Clip1` (3D Model, rotation) | rotation | `Cupcake_Rot_R` |
| `new Clip2` (3D Model, rotation) | rotation | `Cupcake_Rot_U` |
| `new Clip3` (3D Model, rotation) | rotation | `Cupcake_Rot_D` |
| `new Clip4` (3D Model, scale+translation) | scale+translation | `Cupcake_ZI` |
| `new Clip5` (3D Model, scale) | scale | `Cupcake_ZO` |

다중 속성 예시:
- 회전 + 색상: `Cupcake_Rot_R_Clr`
- 스케일 + 페이드 인: `BtnStart_Scl_FI`
- 전체 변환 + 색상: `Cupcake_Tx_Clr`

> `^new Clip\d*$` 패턴은 임포트 검증에서 차단 (Unity 기본값 누설 방지).

## T3 — System-Derived Identifier (`.make` Internal, v4 본문 유지)

> 이하 v4·v5 본문은 **사용자가 직접 명명하지 않는** 객체(머티리얼·중간 mesh 노드·texture object) 에 적용. T2 사용자 인스턴스명은 위 "T2 — Instance Naming" 참조.

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

## v5 → v6 보강 근거 — "컨텍스트별 형식 분리 + 사용자 간결성"

v5 까지는 `.make` 내부 식별자 전체에 단일 형식 (lower_snake_case + kind prefix) 강제. 실측 (`Make Templete_20260512.make`, 513 노드 분석) 결과 다음 갭 노출:

| # | v5 갭 | v6 보강 |
|---|---|---|
| 1 | Make Editor UI 가 타입 아이콘 보유 → kind prefix 가 인스턴스명에서 redundant | **T2 인스턴스 prefix 폐지** (PascalCase + family vocab) |
| 2 | `__` 이중 언더스코어가 이름 길이 증가, 부모-자식 트리가 이미 위계 표현 | 단일 `_` 통일, 트리 컨텍스트 활용 |
| 3 | 하이픈(`Contents 3-1-1-2`) 과 `_` 혼용 — 구분자 정책 불명 | **하이픈 명시 금지**, `_` 만 |
| 4 | State 풀어쓰기 (`_default`/`_pressed`/...) 길이·일관성 부족 | 3-letter 축약 (`_Def`/`_Prs`/`_On`/`_Off`/`_Sel`) |
| 5 | `_hover`·`_focused`·`_highlight` 가 VR/터치 환경에 부재 | 제거 |
| 6 | Audio 카테고리·description 붙임 (`BGMTutorial`) — `GNB_Active` 패턴과 불일치 | `_` 삽입 (`BGM_Tutorial`) |
| 7 | 애니메이션 `anm_` prefix — animations[] 배열 위치가 이미 타입 선언 | prefix 폐지, `<Target>_<Act>_<Dir>` |
| 8 | 다중 속성 클립 (rotation+scale+translation) 명명 미규정 | property 순서 결정론적 (`Rot→Scl→Mov→Clr→Op`) |
| 9 | UI family (`GNB`/`LNB`) ad-hoc — 인계 직관성 부족 | 9종 vocab 권장 사용 |
| 10 | `_v<NN>` marker 필수 — 임포트 후 모든 인스턴스에서 무의미 | T1 옵션, T2 금지 |

**핵심 결정**: 단일 형식 정책 (v3~v5) → **컨텍스트별 형식 분리**. T1 (파일 탐색기) / T2 (Make Editor) / T3 (시스템 파생) 각각의 사용자·AI 노출 패턴이 다름 → 같은 규칙으로 묶을 가치 < 컨텍스트별 최적화 이득.

**자체 반박 (수용)**:
- `_On`/`_Off` 가 토글 상태와 가용성 두 의미 통합 — 디버깅 모호. 의미 분기는 VNT 컴포넌트 필드에서 처리.
- 단문자 sibling (`L`/`R`/`U`/`D`) 이 트리 컨텍스트 의존 — cross-ref 는 노드 인덱스 기반이므로 안전.
- `Contents_3_1_1_2` 가 vocab 부재로 외부 도구에서 위치 모호 — 외부 export 시 full path 권장.
- `ZI`/`ZO`/`FI`/`FO` 초기 학습 비용 — vocab 표 + 임포트 검증으로 보호.

## v4 → v5 보강 근거 — "소스 파일 레이어 명시"

v4 까지는 `.make` **내부** 식별자(L2) 만 규정. 외부 소스 파일(FBX/PNG/WAV/MP4) 이 어떤 형식으로 납품되어야 임포트 파이프라인이 깨끗하게 L2 로 변환할 수 있는지 미정의. 모델러·아티스트가 임의 명명 → 임포트 시 정규화 실패 또는 메타데이터 손실 위험.

v5 가 채택한 외부 명명 제안(`Make Asset Naming Convention v0.5`) 의 타당성 평가:

| 제안 항목 | 평가 | v5 채택 여부 |
|---|---|---|
| Source Asset vs Scene Instance 의 `v` marker 구분 | ✅ 타당 — 동일 디렉토리에서 소스/인스턴스 혼동 방지 | 채택 (L1 규칙) |
| PascalCase 토큰 | ✅ 타당 — 모델러 도구(Maya/Blender) 산업 관례, L2 와 분리됨 | 채택 (L1 한정) |
| `_NN` 2자리 variant 고정 | ⚠️ 부분 채택 — L1 파일시스템에서만 유효. L2 는 순번 금지(v4) 유지 | 채택 (L1 한정) |
| PNG Role 토큰 (`ALB`/`NRM`/`Sprite` 등) | ✅ 타당 — PNG 만 확장자로 용도 분간 불가 | 채택 (L1 한정), L2 변환표 추가 |
| Audio/Video 카테고리 prefix (`BGM`/`SFX`/`CUT`/`TUT`) | ✅ 타당 — 파일 탐색기 정렬·검색 효율 | 채택 (L1 한정) |
| State 토큰 (`Open`/`Broken`/`Closed`/`Damaged`) | ✅ 타당 — 형태 변형의 명시적 표현 | 채택, L2 의 `__<state>` 로 매핑 |
| 자식 부위에 부모 이름 포함 | ✅ 타당 — 파일명 자체기술 | 채택 (L1 한정) |
| Scene Instance Case A/B 권고 | ⚠️ 보조만 — L2 의 `mdl_*__*` 가 권위 표기 | 외부 인터페이스 호환용으로만 유지 |
| Kind prefix 부재 | ❌ L2 호환 안 됨 | L1 → L2 임포트 시 자동 부착 |
| `lower_snake_case` 미사용 | ❌ L2 호환 안 됨 | L1 → L2 임포트 시 자동 변환 |

**핵심 트레이드오프**: 두 레이어가 다른 형식을 쓰는 비용 < 각 레이어 고유 컨텍스트(파일 탐색기 vs 코드/JSON)에 맞춘 가독성 이득. 임포트 파이프라인이 결정론적 매핑(L1→L2 Normalization 섹션) 을 자동 수행하므로 이중 명명 부담은 없음.

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

## Validation Checklist (`.make` 익스포트 전, v6)

### T1 — Source Asset Filesystem 검증
- [ ] 파일명에 공백 없음, 구분자는 `_` 만 (**하이픈 0건**)
- [ ] 토큰별 PascalCase (`GlassBottle`, `BatteryPack`), kebab/snake/소문자 시작 없음
- [ ] Variant `_NN` 은 2자리 고정 (`_01`, `_02`), `_1`/`_001` 금지
- [ ] Version marker `_v<NN>` 는 옵션 (v6) — 사용 시 소스 파일에만, 인스턴스 표기에는 금지
- [ ] 확장자가 타입을 선언하는 경우 이름에 중복 타입 토큰 없음 (`_MOD_`, `_TEX_` 등 금지)
- [ ] PNG 는 Role 토큰 (`Sprite`/`ALB`/`NRM`/`RGH`/`MET`/`EMI`/`MSK`/`AO`) 필수, `v<NN>` 미사용
- [ ] Audio 카테고리 (`BGM`/`SFX`/`NAR`) 가 첫 토큰, description 과 `_` 로 구분
- [ ] Video 카테고리 (`CUT`/`TUT`/`LOOP`/`INTRO`/`OUTRO`) 가 첫 토큰, description 과 `_` 로 구분
- [ ] 자식 부위 FBX 는 부모 이름을 파일명에 포함 (`GlassBottle_Cap_v01.fbx`)
- [ ] 영문 전용 — 한글 파일명 0건 (GLOSSARY 매핑 사용)

### T2 — Instance Naming 검증 (v6 신규)
- [ ] T2 인스턴스명에 kind prefix (`mdl_`/`img_`/`txt_`/`aud_` 등) **0건**
- [ ] 모든 인스턴스명이 PascalCase, 확장자 0건 (`*.png`/`.fbx` 박제 없음)
- [ ] 구분자는 단일 `_` 만 (이중 `__`·하이픈 0건)
- [ ] State suffix 는 v6 vocab (`_Def`/`_Prs`/`_On`/`_Off`/`_Sel`) 내 사용
- [ ] Direction suffix 는 v6 vocab (`_L`/`_R`/`_U`/`_D`/`_CW`/`_CCW`) 내 사용
- [ ] 단문자 sibling (`L`/`R`/`U`/`D`) 은 닫힌 vocab 부모 컨텍스트에서만 사용
- [ ] UI Family vocab (`GNB`/`LNB`/`Btn`/`Nav`/`Pnl`/`Ico`/`Bg`/`Logo`/`Tip`/`Txt`) 권장 적용
- [ ] 4단계 위계는 `_` 로 평탄화 (`Contents_3_1_1_2`)

### Animation 검증 (v6 신규)
- [ ] 애니메이션명에 prefix 없음 — `<Target>_<Act>[_<Dir>]` 패턴
- [ ] Action 토큰이 v6 vocab (`Rot`/`Scl`/`Mov`/`Clr`/`Op` 또는 compound `ZI`/`ZO`/`FI`/`FO`/`Tx`/`Pop`) 내
- [ ] 다중 속성 클립의 토큰 순서가 결정론적 (`Rot → Scl → Mov → Clr → Op`)
- [ ] `^new Clip\d*$` 패턴 (Unity 기본값) **0건**

### L2 — Identifier (Name) 검증
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
