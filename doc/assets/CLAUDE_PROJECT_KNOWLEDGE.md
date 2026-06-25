# Make3.0 — Project Knowledge Bundle

> 이 파일은 레포 문서를 하나로 묶은 **스냅샷**입니다. Claude.ai 프로젝트 지식에 이 파일을 업로드해 참조하세요. 레포가 갱신되면 `py scripts/build_project_knowledge.py` 재실행 후 이 파일을 다시 업로드하면 최신화됩니다.

| 항목 | 값 |
|---|---|
| Repo | https://github.com/Contents-Team/Make3.0.git |
| Commit | `000495f` |
| Commit date | 2026-06-25T20:57:49+09:00 |
| Bundle built | 2026-06-25T21:11:17+09:00 |
| Included docs | 4 |

## 포함 문서
- `README.md`
- `doc/MAKE_FORMAT.md`
- `doc/GLOSSARY.md`
- `CHANGELOG.md`


---

# ===== FILE: README.md =====

# Make3.0

> 한 줄 가치제안 — TODO: Make3.0 이 무엇이고, 누구의 어떤 문제를 푸는가.

## What is 

TODO: 1-2문단으로 핵심 가치 설명. 어떤 도메인의 어떤 문제를 풀고, 기존 대안과 무엇이 다른지.

## Features

- TODO: 핵심 기능 1
- TODO: 핵심 기능 2
- TODO: 핵심 기능 3

## Problems Make3.0 solves

- TODO: 사용자가 겪던 문제 1 → Make3.0 의 해결
- TODO: 문제 2 → 해결

## Quickstart

\\\ash
TODO: 3-5줄 안에 동작 확인 가능한 명령
\\\

이 레포는 `.make` 포맷·에셋 네이밍 규칙 문서를 다룹니다. 핵심은 [doc/MAKE_FORMAT.md](./doc/MAKE_FORMAT.md) 참조.

## FAQ

**Q. TODO**
A. TODO

**Q. 에셋 네이밍 규칙은?**
A. `doc/MAKE_FORMAT.md` 의 `Naming Rules` (현재 v7) 참조. 용어 매핑은 `doc/GLOSSARY.md`.

## Development

핵심 문서는 [doc/MAKE_FORMAT.md](./doc/MAKE_FORMAT.md) (포맷·네이밍 규칙) 와 [CHANGELOG.md](./CHANGELOG.md) 참조.

## Roadmap

분기별 마일스톤은 [ROADMAP.md](./ROADMAP.md) 참조.

## Contributing

기여 절차는 [CONTRIBUTING.md](./CONTRIBUTING.md). AI 에이전트는 [AGENTS.md](./AGENTS.md) 의 작업 규약을 먼저 읽을 것.

## Telemetry

TODO: 수집 항목·옵트아웃 방법. 수집 안 한다면 `없음`으로 명시.

## License

MIT — [LICENSE](./LICENSE)

---

# ===== FILE: doc/MAKE_FORMAT.md =====

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

## Naming Rules v7

> **목적**: **개발자, 사용자, AI 에이전트 모두** 가 `.make` 콘텐츠를 다룰 때, 각 컨텍스트(OS 파일 탐색기 / Make Editor UI / JSON·grep) 에 가장 적합한 명명 형식을 사용한다. UI 아이콘이 타입을 알려주는 컨텍스트에서는 prefix 를 제거해 간결성을 우선, 가독성을 위해 약자보다 **풀어쓰기**를 선호.
>
> v1: 단일 문자 prefix + NN 순번 + 영문 강제. v2: 3-Layer Identity 도입했으나 prefix 선택화로 자가설명 손실. v3: 자가설명 강제 (mandatory prefix + namespace + suffix vocab). v4: prefix 정책은 v3 유지 + **Tier 책임 분리** — 사용자는 Tier A 만 명명, 시스템이 Tier C 자동 파생. v5: **소스 에셋 파일시스템 레이어** 추가 — `.make` 내부 식별자와 외부 원본 파일 명명을 명시적으로 분리. v6: **3-Tier 책임 모델** 로 재구성 — T1 / T2 / T3. v7: **2-Tier 로 축소** — T3(시스템 파생) 삭제(시스템 자동 처리), 3D 텍스처 명명 규칙 삭제(PNG = UI 스프라이트 전용), **약자 폐지 → 풀어쓰기**(상태 `Pressed`/`On`/`Off`/`Disabled`, 방향 `Left`/`Right`/`Up`/`Down`), 도메인 약자 PascalCase(`Gnb`/`Bgm`/`Sfx`/`Info`), 영상 2종(`Info`/`Bgv`), 애니메이션 효과 기반(`Bounce`/`Spin`/...), 애니메이션 포함 모델 `Ani_` 접두사, TTS 텍스트 `TTS_` 접두사, 씬 하이어아키 표준·C# 대조표 신설.

## Two-Tier Naming Model (v7)

| Tier | 적용 대상 | 형식 | 사용자가 봄? | AI raw 입력? |
|---|---|---|---|---|
| **T1 — Source Asset (filesystem)** | 모델러/아티스트가 납품하는 원본 파일 (`.fbx`, `.png`, `.wav`, `.mp4`, `.ttf`) | **PascalCase** + 확장자 + 카테고리 토큰 (모호 타입만) + `_v<NN>` (옵션) | ✅ OS 파일 아이콘 보조 | ✅ filename 단독 전달 가능 |
| **T2 — Instance (Make Editor)** | `.make` 안의 사용자 직접 명명 노드 (씬·페이지·UI 그룹·이미지·3D 모델 등) | **PascalCase**, **kind prefix 없음**, 토큰은 단일 `_` 로 구분, 트리 컨텍스트 활용 | ✅ Make Editor 타입 아이콘 보조 | ❌ 보통 JSON 구조와 동반 |

> **T3(System-Derived) 폐지 (v7)**: 머티리얼·중간 mesh·texture object 등 사용자가 직접 명명하지 않는 객체는 **명명 규칙 대상에서 제외**한다. 시스템이 자동 생성·관리하며, 사용자·문서가 이름을 규정하지 않는다. (버전 독립 식별자 — `ResourceID`/`OriginPath`/`DisplayTitle` — 는 아래 `Format-Level Identifiers` 참조.)

**왜 컨텍스트별로 형식이 다른가**:
- T1: 모델러 도구(Blender/Maya/Photoshop) 산업 관례 + OS 파일 탐색기 가독성. 확장자가 타입을 선언.
- T2: Make Editor 트리 옆 타입 아이콘이 종류를 알려줌 → prefix redundant. 부모-자식 컨텍스트가 의미를 보강 → 자식 이름은 짧게.

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

## T1 — Source Asset Filesystem Naming (v7)

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
| 하이픈 금지 | `Contents_3_1_1` | `Contents_3-1-1-2` |
| 중복 타입 토큰 금지 | `GlassBottle_v01.fbx` | `GlassBottle_Mod_v01.fbx` |
| 숫자 경로 최대 3자리 | `Contents_3_1_1` | `Contents_3_1_1_2` |
| 이중 밑줄 `__` 금지 | `GlassBottle_Open` | `GlassBottle__Open` |
| 영문 전용 | `BatteryPack_v01` | `배터리팩_v01` |

> ⚠️ Version 히스토리 (`_v01`, `_v02`) 는 납품 전 WIP 관리용 (v6 부터 **옵션**). 최종 납품 에셋은 별도 합의 없으면 단일 깨끗한 버전만 유지.
> ⚠️ 이름은 PascalCase 로 붙이고(`GlassBottle`), 언더바 `_` 는 **구조 토큰(종류·이름·상태·번호·방향) 구분에만** 사용 (`GlassBottle_Open`, `Gnb_01`).

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

확장자 `.fbx` 가 타입을 선언. **이름에 타입 토큰 박지 말 것.** 애니메이션이 포함된 모델은 이름 앞에 접두사 **`Ani_`** 를 붙여 애니메이션 없는 모델과 구분 (v7). 애니메이션 없는 모델은 접두사 없이 그대로.

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
Ani_Cupcake_v01.fbx                     # 애니메이션 포함 모델 — 접두사 Ani_
```

#### L1.2 — Image — UI Sprite (`.png`, `.jpg`)

> **3D 텍스처 명명 규칙 폐지 (v7)**: PNG 는 **UI 스프라이트 전용**. ALB/NRM/RGH/MET/EMI/MSK/AO 같은 Role 토큰, 텍스처 채널 suffix, `tex_` 일체 삭제. (3D 모델 텍스처는 `.fbx`/`.glb` 에 임베드되어 시스템이 관리 — 사용자 명명 대상 아님.)

UI 스프라이트는 **Family + 이름 + 상태** 형식. 토큰마다 단일 `_` 로 구분. 상태는 기본(`Default`) 생략, 변형 상태만 표시. 방향은 풀어쓰기(`Left`/`Right`/`Up`/`Down`).

```
<Family>[_<Name>][_<Direction>][_<State>].png
```

```
Gnb_01_On.png
Btn_Navi_Left.png
Btn_Navi_Left_Pressed.png
Rotation_Up.png
Logo.png                      # Family 단독 OK
Tip.png
Pnl_Tablet.png
```

> PNG 스프라이트는 `v<NN>` 미사용 — 아트 에셋이며 버전 관리되는 소스 파일이 아니다. variant `<NN>` 으로 충분.

#### L1.3 — Audio (`.wav`, `.mp3`)

확장자가 타입 선언. 카테고리는 첫 토큰으로, description 과 `_` 로 구분. 카테고리 약자는 PascalCase (v7 — `Gnb_On` 패턴과 일관).

| Category | 풀이 | Meaning |
|---|---|---|
| `Bgm` | Background Music | 배경음악 |
| `Sfx` | Sound Effect | 효과음 (UI 클릭·완료음·경고 등) |
| `Nar` | Narration | 내레이션·더빙 (구 `VO`) |

```
<Category>_<Description>_<NN>.<ext>
```

```
Bgm_Tutorial_01.wav
Bgm_Boss_01.wav
Sfx_UI_Click_01.wav
Sfx_Complete_01.wav
Sfx_AlertWarning_01.wav
Nar_Intro_01.wav
Nar_Step_01.wav
```

> v5 의 `VO` 는 `Nar` 로, `AMB` 는 제거 (현재 사용처 없음 — 필요 시 향후 추가). v7 에서 약자 대소문자 `BGM`/`SFX`/`NAR` → `Bgm`/`Sfx`/`Nar` (PascalCase).

#### L1.4 — Video (`.mp4`)

확장자가 타입 선언. 카테고리는 첫 토큰, description 과 `_` 로 구분. **v7 에서 5종 → 2종으로 통합.**

| Category | 풀이 | Meaning |
|---|---|---|
| `Info` | Information | 설명·정보 전달용 (구 `CUT`/`TUT`/`INTRO`/`OUTRO` 통합) |
| `Bgv` | Background Video | 반복 재생되는 배경 영상 (구 `LOOP`) |

```
<Category>_<Description>_<NN>.mp4
```

```
Info_Assembly_01.mp4
Info_BatterySwap_Step01_01.mp4
Bgv_Workshop.mp4
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

씬 텍스트 객체는 T2 인스턴스 규칙을 따른다 (직관적 PascalCase 이름, 음성 변환 적용 시 접두사 `TTS_` — `T2 — Instance Naming` 참조).

### Hierarchy Rules — Parent & Child (L1)

#### Source Asset Delivery

자식 부위를 별도 FBX 로 납품할 때 **부모 이름을 반드시 포함** — 파일명만으로 AI·사람이 관계 파악 가능.

```
GlassBottle_v01.fbx          ← Parent
GlassBottle_Cap_v01.fbx      ← Child part of GlassBottle
GlassBottle_Label_v01.fbx    ← Child part of GlassBottle
```

#### Scene Object Hierarchy

Make Editor 안에서는 부모-자식 트리가 위계를 표현하므로 자식 이름은 짧게 (`Cap`). 이름 문자열만 외부로 전달할 때는 부모 이름을 포함해 자체 기술적으로:

| Case | Child name 형식 | 자체 기술 | 권장 용도 |
|---|---|---|---|
| **A** — 씬 트리를 AI 가 읽음 | `Cap` | ❌ 트리 필요 | Make 내부 동작 (T2 인스턴스) |
| **B** — AI 가 이름 문자열만 받음 | `GlassBottle_Cap` | ✅ 이름만으로 완전 | 파일 납품·외부 리뷰 (T1 소스) |

### Instance Rules (T1 외부 표기)

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

## T2 — Instance Naming (Make Editor visible, v7)

> Make Editor 트리에 노출되는 사용자 직접 명명 노드. 아이콘이 타입을 시각적으로 알려주므로 **kind prefix 폐지**. 부모-자식 트리 컨텍스트가 의미를 보강하므로 **자식 이름은 짧게**. v7 — 약자 대신 풀어쓰기, Family 약자 뒤에도 단일 `_`.

### Core Rules

| Rule | ✅ | ❌ |
|---|---|---|
| PascalCase 토큰 | `Btn_Start`, `Btn_Start_Pressed` | `btn_start`, `gnb_act` |
| Prefix 없음 (T2 한정) | `Cupcake` | `mdl_cupcake` |
| 토큰 사이 단일 `_` (Family 뒤에도) | `Contents_3_1_1`, `Gnb_01` | `Contents_3-1-1-2`, `Contents__3` |
| 숫자 경로 최대 3자리 | `Contents_3_1_1` | `Contents_3_1_1_2` |
| 확장자 없음 | `Logo_x4` | `Logo_x4.png` |
| 기본(Default) 상태 생략, 변형만 표시 | `Btn_Start` → `Btn_Start_Pressed` | `Btn_Start_Default` |
| 애니메이션 포함 3D 모델은 접두사 `Ani_` | `Ani_Cupcake` | `Cupcake` (애니메이션인데 표시 없음) |
| 닫힌 sibling vocab 은 방향 단어 OK | `RotationPanel/Left`, `…/Right` | (해당 부모 컨텍스트 외에선 사용 금지) |
| 자유 명명 sibling 은 의미 슬러그 | `Btn_Reset`, `Btn_ZoomIn` | `R`, `Z` (모호) |

### Syntax

```
<Family>_<Asset>[_<Direction>][_<State>]

Family    : UI Family Vocab (선택, 권장)
Asset     : 자산 슬러그 (PascalCase)
Direction : Direction Vocab (해당 시, 풀어쓰기)
State     : State Vocab (풀어쓰기, 기본 Default 는 생략)
```

### UI Family Vocab (v7, 권장)

T2 인스턴스명에서 family 토큰 사용을 권장 — 인계 시 직관성·범용성 확보. 메인 내비(`Gnb`/`Snb`/`Bnb`)는 이름 대신 **번호 + 상태**로 구분.

| Family | 의미 | Asset slug 필요? |
|---|---|---|
| `Gnb` | Global Navigation Bar (전체 메뉴바) | ❌ 번호로 구분 (`Gnb_01`, `Gnb_01_On`) |
| `Snb` | Side Navigation Bar (측면 메뉴바) | ❌ 번호로 구분 (`Snb_01`) |
| `Bnb` | Bottom Navigation Bar (하단 메뉴바) | ❌ 번호로 구분 (`Bnb_01`) |
| `Btn` | Button (generic) | ✅ |
| `Modal` | Modal / Popup (모달·팝업 창) | 이름 또는 용도 (`Modal_Exit`) |
| `Nav` | Navigation control (prev/next) | ❌ |
| `Pnl` | Panel / Background container | ❌ |
| `Ico` | Icon | ✅ |
| `Bg` | Background image | ❌ |
| `Logo` | Logo / Brand mark | ❌ |
| `Tip` | Tooltip | ❌ |
| `TTS_` | 음성 변환(TTS) 적용 텍스트 접두사 | TTS 적용 텍스트만 (`TTS_StartHeadline`). 일반·버튼 텍스트는 접두사 없이 직관적 PascalCase (`Start`) |

> **약자 대소문자 (v7)**: 3글자+ 도메인 약자는 PascalCase (`Gnb`/`Snb`/`Bnb`/`Bgm`/`Sfx`/`Nar`/`Info`). 2글자·널리 쓰는 약어(`UI`/`TTS`)는 대문자 유지.

### State Vocab (v7, 풀어쓰기)

VR/터치 환경 기준 — `Hover`·`Focused`·`Highlight` 삭제, `Active` 는 `On` 으로 통합. **기본(Default)은 접미사 생략**, 변형 상태만 뒤에 표시.

| Suffix | 상태 | 의미 |
|---|---|---|
| (없음) | Default | 기본 상태 (접미사 생략) |
| `_Pressed` | Pressed | 눌린 상태 |
| `_On` | On | 켜짐 / 활성 (토글) |
| `_Off` | Off | 꺼짐 / 비활성 (토글 · 상호작용 가능) |
| `_Disabled` | Disabled | 사용 불가 (상호작용 막힘 · 흐리게) |

> ⚠️ v7 에서 `Off` 와 `Disabled` 를 **구분** — `Off` 는 토글 꺼짐(상호작용 가능), `Disabled` 는 사용 불가(상호작용 막힘). `Selected` 는 `On` 과 기능 동일하여 제거.

### Direction Vocab (v7, 풀어쓰기)

방향 정보가 자산명 일부일 때 풀어쓰기 suffix.

| Suffix | 의미 |
|---|---|
| `_Left` | Left |
| `_Right` | Right |
| `_Up` | Up |
| `_Down` | Down |
| `_Clockwise` | Clockwise (회전 전용) |
| `_AntiClockwise` | Anti-clockwise (회전 전용) |

### 닫힌 Sibling Vocabulary — 방향 단어 허용 컨텍스트

부모 노드의 자식 sibling 이 닫힌 vocabulary(Left/Right/Up/Down, In/Out, Prev/Next) 로 완결되면 자식 이름은 방향 단어 단독 OK. AI 가 parent path 로 의미 합성 가능.

```
RotationPanel
├── Left           ← parent=RotationPanel 컨텍스트에서 "회전 왼쪽" 자명
├── Right
├── Up
└── Down
```

→ 단, sibling 이 자유 명명(Btn_Reset, Btn_ZoomIn 등) 으로 섞이면 방향 단독 금지 — 의미 슬러그 필요.

### Examples — 실측 파일(`Make Templete_20260512.make`) 변환

```
SceneRoot                       (예약, 유지)
├── Start
│   ├── Logo_x4                 ← Logox4.png
│   ├── StartHeadline           ← Text 1 (의미 부여; TTS 적용 시 TTS_StartHeadline)
│   ├── Btn_Start               ← btn_start.png
│   └── Pnl_Tablet              ← Tablet.png
├── Contents_1_1                ← Contents 1-1 (하이픈 → _)
│   ├── Gnb_01
│   │   ├── Gnb_01_On           ← GNB_Active.png
│   │   ├── Gnb_01              ← GNB_default.png (기본 상태 생략)
│   │   ├── Gnb_01_Disabled     ← GNB_Disabled.png
│   │   └── Gnb_01_Pressed
│   └── Snb_01_01
├── Contents_3_1_1              ← 위계, 하이픈 → _ (숫자 최대 3자리)
└── Contents_4
    ├── Stage_3D                ← '3D Model' (공백 제거)
    │   └── Ani_Cupcake         ← '0016' (애니메이션 포함; GLOSSARY: 0016 → Cupcake)
    ├── Pnl_Nav                 ← Navi.png
    │   ├── Btn_Navi_Left
    │   │   ├── Btn_Navi_Left           ← 기본 상태 생략
    │   │   ├── Btn_Navi_Left_Off
    │   │   └── Btn_Navi_Left_Pressed   (오타 Presssed 교정; 구 Highlight → Pressed)
    │   ├── Nav_Title
    │   ├── Nav_Page
    │   ├── Btn_Navi_Right
    │   └── Tip                 ← tooltip.png
    └── RotationPanel
        ├── Left                ← R_rotation 등, 방향 단어 단독 OK
        ├── Right
        ├── Up
        ├── Down
        ├── Btn_Reset
        ├── Btn_ZoomIn
        └── Btn_ZoomOut
```

## Animation Naming (v7)

애니메이션은 `animations[]` 배열에 위치 — **타입이 위치로 선언**되므로 prefix 없음. 이름은 대상 오브젝트와 무관하게 **'무엇이 어떻게 움직이는지'를 직관적 효과 이름**으로 짓는다 (v7 — 약어·대상 이름 미사용). 한 클립이 여러 속성을 동시에 변경 가능.

### 움직일 수 있는 속성 (4가지, 기술 기준)

| 속성 | 의미 | 3D 모델 적용 |
|---|---|---|
| `Position` | 위치 이동 | 가능 |
| `Rotation` | 회전 | 가능 |
| `Scale` | 크기 변화 | 가능 |
| `Color` | 색상 변화 | **불가 (UI·2D 전용)** |

### Syntax

```
<Effect>[_<Direction>]

Effect    : 직관적 효과 이름 (아래 vocab)
Direction : 방향이 필요하면 풀어쓰기 (_Left / _Right / _Up / _Down)
```

속성을 나열하지 않고, `Bounce`·`ZoomIn`·`Pop` 처럼 '어떤 애니메이션인지'가 바로 보이는 효과 이름을 쓴다. **대상 오브젝트 이름은 넣지 않는다.**

### Effect Vocab

| Effect | 느낌 / 동작 | 사용 속성 · 3D |
|---|---|---|
| `Bounce` | 통통 튀어오름 | Position+Scale · 3D 가능 |
| `ZoomIn` / `ZoomOut` | 확대 / 축소 | Scale · 3D 가능 |
| `Pop` | 팝 하고 나타남 | Scale · 3D 가능 |
| `Pulse` | 커졌다 작아지기 반복 | Scale · 3D 가능 |
| `Spin` | 빙글 회전 (방향 가능) | Rotation · 3D 가능 |
| `Slide` | 미끄러져 이동 (방향 가능) | Position · 3D 가능 |
| `Flip` | 뒤집기 (방향 가능) | Rotation · 3D 가능 |
| `Fade` | 서서히 나타남 / 사라짐 | Color/투명도 · 3D 불가 (UI·2D) |
| `Highlight` | 색으로 강조 | Color · 3D 불가 (UI·2D) |

### Examples — 실측 7개 애니메이션

| 현재 (default) | 채널·path | v7 (효과 기반) |
|---|---|---|
| `new Clip` (btn_start, scale) | scale | `Pop` |
| `new Clip` (3D Model, rotation) | rotation | `Spin_Left` |
| `new Clip1` (3D Model, rotation) | rotation | `Spin_Right` |
| `new Clip2` (3D Model, rotation) | rotation | `Spin_Up` |
| `new Clip3` (3D Model, rotation) | rotation | `Spin_Down` |
| `new Clip4` (3D Model, scale+translation) | scale+translation | `ZoomIn` |
| `new Clip5` (3D Model, scale) | scale | `ZoomOut` |

> `^new Clip\d*$` 패턴은 임포트 검증에서 차단 (Unity 기본값 누설 방지). `Color`(`Fade`/`Highlight`) 효과는 3D 모델에 사용 금지 — UI·2D 전용.

## Scene Hierarchy (v7)

> 빈 게임오브젝트(Empty)를 **"폴더 컨테이너"** 로 써서 오브젝트의 형태(증강 = 월드 공간 / 스크린 = UI 공간)별로 묶는다. ① AI·사람이 구조만 보고 빠르게 검색 ② 그룹 단위 접기/숨기기로 간편한 유지보수가 목표. 표준 템플릿이며, 쓰지 않는 컨테이너는 삭제하고 쓴다 (World·Screen 모두 접두사 없는 타입 컨테이너 방식 동일).

### 디바이스별 씬 트리

**HMD — World 전용 (모델·UI 모두 월드 공간)**

```
World_01                  장면 단위 (World_NN)
├── Models                3D 모델 (Ani_ 포함/미포함)   예: Ani_Cupcake
├── Gnb                   전역 내비                    예: Gnb_01_On
├── Snb                   측면 내비                    예: Snb_01_On
├── Bnb                   하단 내비                    예: Bnb_01_On
├── Modal                 모달·팝업                    예: Modal_Exit
├── Btn                   일반 버튼                    예: Btn_Start
└── Audio                 사운드 (Bgm·Sfx·Nar)         예: Bgm_Workshop
```

**PC · Tablet — Models 만 World, 나머지 Screen**

```
World_01                  3D 모델만 월드 공간
└── Models                3D 모델 (Ani_ 포함/미포함)   예: Ani_Cupcake
Screen_01                 UI·사운드 (스크린 공간)
├── Gnb / Snb / Bnb       내비                         예: Gnb_01_On
├── Modal                 모달·팝업                    예: Modal_Exit
├── Btn                   일반 버튼                    예: Btn_Start
└── Audio                 UI 사운드 · Nar(TTS 시 텍스트) 예: Sfx_Click_01, Nar_Intro_01
```

### 컨테이너 규칙

| 규칙 | 이유 |
|---|---|
| 최상위 컨테이너는 빈 오브젝트, Transform 원점(0,0,0)·Scale 1 고정 | 자식 오브젝트의 월드 좌표가 틀어지지 않도록 |
| 컨테이너 안 분류는 접두사 없이 패밀리/타입 이름 (`Models`, `Gnb`, `Audio`) · PascalCase | AI·검색이 형태와 종류를 바로 인식 |
| 그룹 안에 객체를 자식(child)으로 넣어 정리 → 접기/숨기기로 관리 | 씬이 커져도 한눈에 보고 빠르게 찾음 |
| 순수 정리용 빈 오브젝트에는 `EditorOnly` 태그 → 빌드에서 자동 제외 | 런타임 메모리·계층 영향 최소화 |
| 장면은 최상위 컨테이너 뒤 번호로 구분 (`World_01` / `Screen_01`) — 같은 번호 = 한 장면 | 이름만 보고 장면 파악, 월드·스크린을 같은 번호로 묶음 |

> 빈 부모 만들기: 선택 후 `Ctrl+Shift+G` (Mac `Cmd+Shift+G`). 단순 구분선(헤더) 빈 객체 아래 오브젝트는 자식이 아님 — 자식 중첩 시 좌표 틀어짐 주의. 본 표준은 '자식 컨테이너' 방식(원점 고정)을 채택.
> 출처: Unity Manual(Hierarchy), Unity Learn(Organizing your Scene), gamedevbeginner.com

## C# Convention Cross-reference (v7)

에셋·씬·파일 이름은 C# 식별자가 아니므로 전면 적용은 부적절하다. 그대로 전이되는 원칙(선명도·`__` 금지·단일문자 지양·PascalCase)은 따르고, 안 맞는 항목(`_` 구분자·패밀리 접두사)은 의도적 일탈로 이유를 명기한다. 출처: Microsoft Learn — C# 식별자 명명 규칙 / .NET 코딩 규칙.

| 항목 | 현재 컨벤션 | MS C# 규칙 | 판정 / 조치 |
|---|---|---|---|
| 기본 표기 | PascalCase | 형식·public 멤버 PascalCase | ✅ 일치 |
| 이중 밑줄 `__` | 자체 금지 | `__` 금지 (컴파일러 예약) | ✅ 준수 |
| 약어 `Btn`/`Nav` | 적극 사용 | 약어 지양·"간결성보다 선명도" | ⚠️ 의도적 일탈 — 에디터 표시명 축약, Vocab 용어집으로 완화 |
| 단일문자 방향 | v7 에서 풀어쓰기로 폐지 | 단일문자 금지 (루프 카운터만 예외) | ✅ 채택 — `Left`/`Right`/`Up`/`Down` |
| `_` 단어 구분자 | `Btn_Navi_Left_Pressed` | `_` 는 private 필드 접두사로만 | ⚠️ 자산·파일명엔 적합 / 코드 심볼은 무언더바 PascalCase |
| 약자 대소문자 (`GNB`/`BGM`) | → `Gnb`/`Bgm` (PascalCase) | 3글자+ 약어도 PascalCase | ✅ 채택 — 3글자+ PascalCase, 2글자(`UI`)는 대문자 유지 |

**개선 제안**:
1. 코드 경계 정의 — 카테고리(`Bgm`/`Sfx`/`Info`/`Bgv`)·애니메이션이 C# enum/직렬화 필드가 되는 지점엔 PascalCase 병행형 제공 (`AudioCategory.Bgm`).
2. 각 의도적 일탈 항목에 "이유" 한 줄 부착 (예: `_` 구분자는 에디터 가독성용).
3. 약자 대소문자 규칙 채택: 3글자+ PascalCase(`Gnb`/`Bgm`), 2글자 대문자(`UI`).

## Format-Level Identifiers (버전 독립)

> 아래는 명명 Tier 와 무관한 **포맷 레벨 식별자** — `.make` 파일 구조 자체의 속성으로, v7 에서도 유지. 시스템 자동 생성 객체(머티리얼·중간 mesh·texture object)는 v7 에서 명명 규칙 대상이 아니며, 시스템이 `ResourceID` 기반으로 관리한다.

### 핵심 원칙: 3-Layer Identity

모든 에셋·노드는 다음 **3개 식별자**를 가진다. 책임이 다르고 변경 가능성이 다르다.

| Layer | 필드 | 변경 | 글자 | 책임 |
|---|---|---|---|---|
| **ID** | `ResourceID` / glTF index | **불변** | UUID v4 (ASCII) | machine join key. 코드·DB·외부 참조의 진실 |
| **Name** | `node.name`, `image.name`, etc. | 변경 가능 | ASCII PascalCase (T2 규칙) | 사람·도구가 grep·diff·정렬할 때 쓰는 식별자 |
| **DisplayTitle** | `SceneTitle`, `VNT_*` extras | 자유 변경 | Unicode (한국어 OK) | 사용자 화면에 노출되는 텍스트. i18n 가능 |

**Source of truth**: ID. Name 이 바뀌어도 ID 는 그대로. ID 만 외부 참조에 쓰고, Name 은 작업 편의용, DisplayTitle 은 사용자 대면.

### ResourceID

- **포맷**: `UUID v4` (`xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx`, 소문자, 하이픈)
- **불변·전역 유일**
- **중복 감지**: 동일 에셋은 콘텐츠 해시(SHA-256 등) 기반으로 dedup → 동일 ID 재사용. 새 파일이면 새 UUID.

### Name (Identifier)

ASCII 기반 식별자. 사용자가 명명하는 노드는 T2 규칙(PascalCase) 을 따른다. 시스템 자동 생성 객체(머티리얼·중간 mesh·texture object)는 **v7 에서 명명 규칙 대상이 아니며**, 시스템이 `ResourceID` 기반으로 내부 식별자를 부여·관리한다 (사용자·문서가 prefix·채널 suffix 를 규정하지 않음).

**유일성 scope**:
- `ResourceID`: **글로벌 유일** (전체 파일)
- `node.name`: 같은 부모 아래에서만 유일 (glTF 스펙)
- `image.name` / `material.name`: 시스템 관리 (ID 가 식별 담당)

### 한국어·고유명사 정책

| 상황 | 규칙 |
|---|---|
| Name (identifier) | ASCII 기본. `Notebook`, `Btn_Start` |
| 한국어 고유명사 | 로마자 표기 + **용어집 (`doc/GLOSSARY.md`)** 등록 필수<br>예: `HangangBridge` → glossary "한강대교" |
| DisplayTitle (사용자 화면) | Unicode 자유 — 한국어, 이모지 OK |

용어집은 T1·T2 이름에서 사용된 모든 로마자 슬러그 → 한국어 정식 명칭 매핑을 보관.

### DisplayTitle (User-facing)

- 위치: `VNT_NodeProperty.VIRNECT.Components.SceneComponent.SceneTitle` 등 컴포넌트 안의 `*Title` `*Detail` `*Label` 필드
- 정규식: 제어문자 (`-`) 만 금지, 나머지 자유
- 한국어·이모지 OK
- i18n: locale 별 분기 가능 (확장 권장 — `SceneTitle.ko`, `SceneTitle.en`)

**예시**: `"엔진 점검 시작"`, `"Step 1 — Diagnose"`, `"마지막 문장을 재생합니다."`

> 머티리얼·애니메이션·중간 mesh 등 시스템 자동 생성 객체의 식별자는 v7 에서 사용자·문서 명명 대상이 아니다 (시스템이 자동 처리). 사용자가 명명하는 애니메이션 **표시 이름**은 위 `Animation Naming (v7)` 의 효과 기반 규칙을 따른다. 단, **파일 확장자를 노드명에 넣지 말 것** — 안티패턴 `Logox4.png` → `Logo_x4`.

### OriginPath (보안·이식성 정책)

작성자 PC 의 로컬 경로 누설 방지.

| 단계 | 정책 |
|---|---|
| **로컬 작업본** | OriginPath 보존 OK (round-trip · 재임포트용) |
| **공유/배포본** | 익스포트 파이프라인에서 다음 변환:<br>① `C:\Users\<유저명>` → `<HOME>` 치환<br>② `<HOME>/Downloads/work/Projects/<프로젝트>` → `<PROJECT_ROOT>` 치환<br>③ 사용자명·식별 정보 스크럽 |
| **외부 배포본** | OriginPath 필드 완전 제거. ResourceID 만 유지 |

## v6 → v7 보강 근거 — "단순화 + 가독성 + 실사용 정합"

v6 의 3-Tier·약자 체계가 실제 운영에서 과하다는 피드백 반영. 핵심: **사용자가 안 만지는 것은 규칙에서 빼고, 사람이 쓰는 것은 약자 대신 풀어쓴다.**

| # | v6 갭 | v7 보강 |
|---|---|---|
| 1 | T3(시스템 파생) 명명 규칙이 사용자·문서 부담만 늘림 (시스템이 자동 생성) | **T3 삭제 → 2-Tier**. 자동 생성 객체는 `ResourceID` 기반 시스템 관리 |
| 2 | 3D 텍스처 Role 토큰(`ALB`/`NRM`/...)·`tex_` 채널 — 사용자가 다루지 않음 | **3D 텍스처 명명 규칙 삭제**, PNG = UI 스프라이트 전용 |
| 3 | 약자(`_Def`/`_Prs`, `_L`/`_R`, `Rot`/`Scl`) 학습 비용·모호성 | **풀어쓰기** (`Pressed`/`On`/`Off`/`Disabled`, `Left`/`Right`/...) |
| 4 | `_On`/`_Off` 가 토글·가용성 두 의미 통합 → 디버깅 모호 | `Off`(토글 꺼짐) 와 `Disabled`(사용 불가) **분리** |
| 5 | `_Sel`(Selected) 가 `_On` 과 기능 중복 | `Selected` 제거 |
| 6 | 영상 5종(`CUT`/`TUT`/`LOOP`/`INTRO`/`OUTRO`) 과세분 | **2종** `Info`(정보 전달) / `Bgv`(배경 영상) |
| 7 | 애니메이션 `<Target>_<Act>_<Dir>` — 대상 이름 의존·약어 난해 | **효과 기반** (`Bounce`/`Spin`/`ZoomIn`/...), 대상 이름 제외, 속성 4종(`Position`/`Rotation`/`Scale`/`Color`) |
| 8 | 도메인 약자 대소문자 혼재 (`GNB`/`BGM`) | **3글자+ PascalCase** (`Gnb`/`Bgm`), 2글자(`UI`)만 대문자 |
| 9 | Family 약자 뒤 구분 불일치, 숫자 경로 길이 무제한 | Family 뒤에도 단일 `_`, **숫자 경로 최대 3자리**, `__` 제거 |
| 10 | 애니메이션 포함 모델·TTS 텍스트 구분 부재 | 접두사 **`Ani_`**(애니메이션 모델), **`TTS_`**(음성 변환 텍스트), `Modal` 패밀리 추가 |
| 11 | 씬 계층 구조·코드 컨벤션 정합 가이드 부재 | **씬 하이어아키 표준**(디바이스별) + **C# 대조표** 신설 |

**핵심 결정**: "자가설명을 모든 객체에 강제"(v3~v6) → **사용자가 실제로 다루는 객체에만 규칙 적용 + 약자 대신 풀어쓰기**. AI 가독성은 트리 컨텍스트·풀어쓴 단어로 충분히 확보.

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

각 폴더 안 파일명은 T1 규칙(PascalCase + 카테고리 토큰) 권장:
- `audio/narration/Nar_Intro_01.wav`
- `2d/ui/Btn_Start.png`
- `3d/models/EngineBlock_v01.fbx` (애니메이션 포함 시 `Ani_EngineBlock_v01.fbx`)

## 안티패턴 요약 (현재 샘플에서 관찰된 것)

| 문제 | 위치 | 위험 |
|---|---|---|
| 한글 + 공백 노드명 | F1 `nodes[]`, `meshes[]` | cross-platform 이슈, 검색·diff 어려움 |
| 파일 확장자가 노드명에 포함 | F2 `"Logox4.png"`, `"btn_start.png"` 가 노드명 | 메시·이미지 구분 어려움 |
| Unity 인스턴스 사슬 머티리얼명 | F2 모든 머티리얼 | 디버깅·검색 불가 |
| 기본 애니메이션명 | F1·F2 모두 | 어떤 애니메이션인지 식별 불가 |
| 절대경로 OriginPath 박제 | `VNT_ExternalResources` | 정보 누설·이식성↓ |
| ResourceID 와 노드명 불일치 | F1 mp3 노드 | 매핑 추적 어려움 |

## Validation Checklist (`.make` 익스포트 전, v7)

### T1 — Source Asset Filesystem 검증
- [ ] 파일명에 공백 없음, 구분자는 `_` 만 (**하이픈 0건**)
- [ ] 토큰별 PascalCase (`GlassBottle`, `BatteryPack`), kebab/snake/소문자 시작 없음
- [ ] 언더바 `_` 는 구조 토큰 구분에만, 이중 밑줄 `__` 0건
- [ ] 숫자 경로 최대 3자리 (`Contents_3_1_1`)
- [ ] Variant `_NN` 은 2자리 고정 (`_01`, `_02`), `_1`/`_001` 금지
- [ ] Version marker `_v<NN>` 는 옵션 — 사용 시 소스 파일에만, 인스턴스 표기에는 금지
- [ ] 확장자가 타입을 선언하는 경우 이름에 중복 타입 토큰 없음 (`_Mod_` 등 금지)
- [ ] 애니메이션 포함 3D 모델에 접두사 `Ani_` (`Ani_Cupcake_v01.fbx`)
- [ ] PNG 는 UI 스프라이트 전용 (3D 텍스처 Role 토큰·`tex_` 0건), `v<NN>` 미사용
- [ ] Audio 카테고리 (`Bgm`/`Sfx`/`Nar`) 가 첫 토큰, description 과 `_` 로 구분
- [ ] Video 카테고리 (`Info`/`Bgv`) 가 첫 토큰, description 과 `_` 로 구분
- [ ] 자식 부위 FBX 는 부모 이름을 파일명에 포함 (`GlassBottle_Cap_v01.fbx`)
- [ ] 영문 전용 — 한글 파일명 0건 (GLOSSARY 매핑 사용)

### T2 — Instance Naming 검증
- [ ] T2 인스턴스명에 kind prefix (`mdl_`/`img_`/`txt_`/`aud_` 등) **0건**
- [ ] 모든 인스턴스명이 PascalCase, 확장자 0건 (`*.png`/`.fbx` 박제 없음)
- [ ] 구분자는 단일 `_` 만 (이중 `__`·하이픈 0건), 숫자 경로 최대 3자리
- [ ] State suffix 는 v7 vocab (`_Pressed`/`_On`/`_Off`/`_Disabled`) 내 사용, 기본(Default)은 생략
- [ ] Direction suffix 는 v7 vocab (`_Left`/`_Right`/`_Up`/`_Down`/`_Clockwise`/`_AntiClockwise`) 풀어쓰기
- [ ] 방향 단어 단독 sibling (`Left`/`Right`/`Up`/`Down`) 은 닫힌 vocab 부모 컨텍스트에서만 사용
- [ ] UI Family vocab (`Gnb`/`Snb`/`Bnb`/`Btn`/`Modal`/`Nav`/`Pnl`/`Ico`/`Bg`/`Logo`/`Tip`) 권장 적용, 메인 내비는 번호+상태 (`Gnb_01_On`)
- [ ] 애니메이션 포함 3D 모델에 접두사 `Ani_`
- [ ] 텍스트 오브젝트는 직관적 이름, 음성 변환(TTS) 적용 시에만 접두사 `TTS_`

### Animation 검증
- [ ] 애니메이션명에 prefix·대상 오브젝트명 없음 — `<Effect>[_<Direction>]` 패턴
- [ ] Effect 토큰이 v7 vocab (`Bounce`/`ZoomIn`/`ZoomOut`/`Pop`/`Pulse`/`Spin`/`Slide`/`Flip`/`Fade`/`Highlight`) 내
- [ ] `Color`(`Fade`/`Highlight`) 효과를 3D 모델에 사용하지 않음 (UI·2D 전용)
- [ ] `^new Clip\d*$` 패턴 (Unity 기본값) **0건**

### ID 검증
- [ ] 모든 `ResourceID` 가 UUID v4 포맷 (소문자 + 하이픈)
- [ ] `ResourceID` 가 파일 전체에서 글로벌 유일
- [ ] 동일 콘텐츠 해시는 동일 `ResourceID` 재사용 (중복 임베딩 0건)
- [ ] 노드명은 부모 노드 안에서 유일 (sibling 중복 0건)
- [ ] 파일 확장자 (`.png`, `.fbx`, `.mp3`) 가 노드명에 포함되지 않음
- [ ] 한국어 고유명사가 로마자 슬러그로 사용된 경우 `doc/GLOSSARY.md` 에 등록됨

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


---

# ===== FILE: doc/GLOSSARY.md =====

# GLOSSARY

> `.make` 콘텐츠의 ASCII 식별자 (Name) 에 사용된 **로마자 슬러그 → 한국어 정식 명칭** 매핑. `doc/MAKE_FORMAT.md` 의 한국어·고유명사 정책에 따라 등록.

## How to Use

- 새 에셋 명명 시 한국어 고유명사가 슬러그에 들어가면 이 표에 한 줄 추가
- 코드 리뷰어는 이 표 확인해서 슬러그의 의미를 즉시 파악
- DisplayTitle (사용자 화면 텍스트) 은 자유 — 이 표 영향 받지 않음

## Format

```
| 슬러그 | 한국어 | 분류 | 비고 |
```

- **슬러그**: Name 에 쓰이는 `lower_snake_case` ASCII
- **한국어**: 정식 한국어 명칭
- **분류**: 어떤 종류의 에셋인지 (모델·UI·오디오 등)
- **비고**: 외래어 출처, 동의어, 사용 컨텍스트

## Glossary

| 슬러그 | 한국어 | 분류 | 비고 |
|---|---|---|---|
| `laptop` | 노트북 | 모델 | 예시 |
| `engine_block` | 엔진 블록 | 모델 | 예시 |
| `hangang_bridge` | 한강대교 | 모델 | 예시 (로마자 고유명사) |
| `btn_start` | 시작 버튼 | UI | 예시 |
| `gnb` | 전역 네비게이션 바 (Global Navigation Bar) | UI | 약어 통용 |
| TODO | TODO | TODO | TODO |

## Conventions for New Entries

1. **약어**: 통용되는 약어 (`gnb`, `cta`, `ui`) 는 그대로 쓰되 비고에 풀어쓰기
2. **외래어**: 한국어 음역보다 영어 원어 우선 (`laptop` > `notebook` 만약 노트북 의미)
3. **고유명사**: 로마자 표기 (Revised Romanization 권장 — `hangang` > `han-gang`)
4. **중복 슬러그**: 같은 슬러그가 다른 의미로 쓰이면 namespace 로 구분 — `mdl_screen` (모니터 화면) vs `mdl_laptop__screen` (노트북 화면)

## Reverse Index (Optional)

큰 프로젝트일 때 슬러그 검색 편의용 역방향 인덱스 추가 가능:

| 한국어 | 슬러그 |
|---|---|
| 노트북 | `laptop` |
| 엔진 블록 | `engine_block` |
| 한강대교 | `hangang_bridge` |
| 시작 버튼 | `btn_start` |


---

# ===== FILE: CHANGELOG.md =====

# Changelog

이 파일의 모든 주요 변경은 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 형식을 따르며, 버전은 [Semantic Versioning](https://semver.org/spec/v2.0.0.html) 을 사용합니다.

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

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
