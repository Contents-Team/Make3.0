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

## Naming Rules (권장)

현재 샘플에서 발견된 안티패턴과 권장 규칙.

### ResourceID

- **포맷**: `UUID v4` (`8-4-4-4-12`, 소문자, 하이픈 포함)
- **불변**: 한 번 발급되면 변경 금지. 노드명·파일명이 바뀌어도 ResourceID 는 유지.
- **재사용**: 동일 에셋은 동일 ResourceID 공유 (중복 임베딩 방지).

### Node Name

| 노드 종류 | 규칙 | 예시 |
|---|---|---|
| 시스템 노드 | `PascalCase`, VNT 예약어 | `SceneRoot`, `EnvironmentSetting`, `TargetManager`, `GlobalOverlaySettings` |
| Scene 단위 | `S<NN>_<slug-en>` | `S01_Intro`, `S02_Diagnose` |
| Audio | `A<NN>_<slug-en>` | `A01_OpeningNarration` |
| Image | `I<NN>_<slug-en>` | `I01_BackgroundLogo` |
| Video | `V<NN>_<slug-en>` | `V01_TutorialClip` |
| 3D Model | `M<NN>_<slug-en>` | `M01_Engine`, `M02_DashPanel` |
| Text/Caption | `T<NN>_<slug-en>` | `T01_Title` |
| Event/Trigger | `E<NN>_<slug-en>` | `E01_OnStart` |

> `<NN>` = 2자리 0-padded 순번 (정렬·재배열 편의). `<slug-en>` = 영문 `kebab` 또는 `PascalCase`, 공백·한글 금지.

### Image Asset Name (image[].name)

- **현재 안티패턴**: `"1. Default"`, `"Type=audio"`, 한글, 공백 — 일관성 없음.
- **권장**: `<purpose>_<variant>` 또는 ResourceID 그대로.
  - `logo_primary`, `btn_start_default`, `btn_start_pressed`
  - `gnb_active`, `gnb_default`, `gnb_disabled`

### Material Name

- **현재 안티패턴**: `"UnlitOpaque (Instance) (Instance) (Instance) (Instance) (Instance) (Instance)"` — Unity 인스턴싱 아티팩트. 거의 모든 머티리얼이 동일 이름 사슬.
- **권장**: `<base>_<usage>_<NN>` — 인스턴스 표기 제거.
  - `UnlitOpaque_Logo_01`, `UnlitOpaque_Button_02`

### Animation Name

- **현재 안티패턴**: `"new Clip"`, `"new Clip1"`, `"new Clip2"` — Unity 기본값.
- **권장**: `Anim_<target>_<action>` — 무엇이·어떻게 움직이는지.
  - `Anim_Logo_FadeIn`, `Anim_Camera_DollyIn`, `Anim_Door_Open`

### Mesh Name

- **현재 안티패턴**: 한글 prose ("첫번째 문장을 재생합니다."), 또는 파일명 그대로 ("Logox4.png" — 메시인데 이미지 확장자).
- **권장**: 노드명과 동일 규칙. 메시-이미지 혼동 금지.

### OriginPath (보안·이식성)

- **현재 안티패턴**: 절대경로 박제 — `C:\Users\VIRNECT\Downloads\...`, `C:\Users\VIRNECT\Desktop\test\templete\...`. 작성자 PC 의 로컬 디렉토리 구조가 그대로 노출.
- **권장**:
  - 절대경로 제거 또는 익명화 (`<workspace>/...`).
  - 파일명만 유지하거나 ResourceID 만 보관 (OriginPath 는 디버그용 옵션).
  - 익스포트 시 작성자 식별 정보(`Username`) 자동 스크럽.

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

## Validation Checklist (`.make` 익스포트 전)

- [ ] 모든 노드명 `^[A-Za-z][A-Za-z0-9_]*$` 정규식 통과
- [ ] 모든 ResourceID 가 UUID v4 포맷
- [ ] 모든 머티리얼명에 `(Instance)` 미포함
- [ ] 모든 애니메이션명이 `Anim_` 접두 + 의미 있는 슬러그
- [ ] `OriginPath` 에 사용자 홈 디렉토리 경로 미포함
- [ ] 이미지 `name` 과 파일 확장자 분리
- [ ] 동일 에셋이 중복 ResourceID 로 임베드되지 않음

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
