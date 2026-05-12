# Make Templete_20260512.make — Renaming Proposal

- Status: Draft
- Date: 2026-05-12
- Author: HamIsBadass (Claude-assisted)

> v3 네이밍 규칙 (`doc/MAKE_FORMAT.md`) 을 실제 콘텐츠에 적용한 **제안서**. 원본 `.make` 파일은 수정하지 않음. 제안 채택 시 별도 마이그레이션 스크립트로 일괄 적용.

## Source File

- 경로: `C:\Users\VIRNECT\Downloads\Make Templete_20260512.make`
- 크기: 7.1 MB
- 생성기: `Virnect Scene Generator v1.0.1`
- 컨테이너: glTF 2.0 GLB

## Scope (실측 카운트)

| 항목 | 수 |
|---|---|
| scenes | 1 |
| nodes | 513 |
| meshes | 265 |
| materials | 263 |
| textures | 142 |
| images | 142 |
| animations | 7 |
| extensionsRequired | `KHR_materials_unlit` |

## 현재 안티패턴 감사

| 패턴 | 카운트 | 위치 | 심각도 |
|---|---|---|---|
| `.png` 확장자가 노드명에 포함 | 383 / 513 (75%) | `nodes[].name` | 🔴 High — Mesh/Image/UI 구분 불가 |
| 공백 포함 노드명 (`Text 1`, `Contents 1-1`) | 25 | `nodes[].name` | 🟡 Med — 식별자 부적격 |
| `UnlitOpaque (Instance) ...` 사슬 | 263 / 263 (100%) | `materials[].name` | 🔴 High — 식별 불가능 |
| 시퀀스 접미사 `X 2`, `X 3` (자동 생성) | 13 | `nodes[].name` | 🟡 Med — 의미 없는 중복 |
| Unity 기본 애니메이션명 `new Clip`, `new Clip1` | 7 / 7 (100%) | `animations[].name` | 🔴 High — 대상 불명 |
| Image name = UUID (식별자가 표시명) | 142 / 142 (100%) | `images[].name` | 🟢 Low — ID 로는 OK, 사람 가독성 ↓ |
| OriginPath 절대경로 누설 | 142+ | `VNT_ExternalResources` | 🟠 Med — `C:\Users\VIRNECT\Desktop\test\templete\2d\...` |

## Scene Hierarchy (실측)

```
[scene root] ContentsRoot
├── [0] EnvironmentSetting        (system)
├── [1] TargetManager             (system)
├── [2] GlobalOverlaySettings     (system)
├── [3] SceneRoot                 (VNT content container)
│   ├── [4] Start
│   ├── [9] Contents 1-1
│   ├── [47] Contents 1-2
│   ├── [85] Contents 1-3
│   ├── [123] Contents 2-1-1
│   ├── [166] Contents 2-1-2
│   ├── [209] Contents 2-2-1
│   ├── [247] Contents 3-1-1-1
│   ├── [295] Contents 3-1-1-2
│   ├── [343] Contents 3-2-1-1
│   ├── [391] Contents 3-2-2-1
│   └── [439] Contents 4
└── [508] ResourceCacheRoot       (rendered-out cache)
    ├── [509] A220-300_B738_KoreanAir_ final
    └── [511] 0016
```

콘텐츠 계층 의미 추정 (확인 필요): 챕터 > 레슨 > 스텝 > 서브스텝 의 4-레벨 학습 구조로 보임 (`3-1-1-2` = 챕터 3, 레슨 1, 스텝 1, 서브 2).

## Renaming Proposals

### 1. System / Reserved Nodes (변경 없음)

VNT 시스템 예약어. v3 도 그대로 유지.

| 현재 | 제안 | 비고 |
|---|---|---|
| `EnvironmentSetting` | `EnvironmentSetting` | 유지 |
| `TargetManager` | `TargetManager` | 유지 |
| `GlobalOverlaySettings` | `GlobalOverlaySettings` | 유지 |
| `SceneRoot` | `SceneRoot` | 유지 (`VNT.Components.SceneRoot` 마커) |
| `ContentsRoot` | `ContentsRoot` | scene 루트, 유지 |
| `ResourceCacheRoot` | `ResourceCacheRoot` | 유지 |

> 시스템 예약어는 v3 prefix 규칙의 예외. paperclip 도 동일 패턴 (`SceneRoot`).

### 2. Scene / Content Containers

`Contents X-Y-Z-W` 계층 → `scn_` prefix + namespace + 명시적 레벨 표기.

| 현재 | 제안 | 근거 |
|---|---|---|
| `Start` | `scn_start` | 오프닝 씬 |
| `Contents 1-1` | `scn_ch1__l1` | Chapter 1, Lesson 1 |
| `Contents 1-2` | `scn_ch1__l2` | |
| `Contents 1-3` | `scn_ch1__l3` | |
| `Contents 2-1-1` | `scn_ch2__l1__s1` | Chapter 2, Lesson 1, Step 1 |
| `Contents 2-1-2` | `scn_ch2__l1__s2` | |
| `Contents 2-2-1` | `scn_ch2__l2__s1` | |
| `Contents 3-1-1-1` | `scn_ch3__l1__s1__sub1` | 4-level |
| `Contents 3-1-1-2` | `scn_ch3__l1__s1__sub2` | |
| `Contents 3-2-1-1` | `scn_ch3__l2__s1__sub1` | |
| `Contents 3-2-2-1` | `scn_ch3__l2__s2__sub1` | |
| `Contents 4` | `scn_ch4` | 단일 챕터 |

> **확인 필요**: `Contents X-Y-Z-W` 의 실제 의미가 챕터/레슨/스텝/서브가 맞는지. 만약 다른 의미면 (예: 단원/주제/페이지/탭) slug 수정 필요.

> **대안**: 의미 불명 시 보수적으로 `scn_content__3_1_1_2` (숫자 보존, 의미 추정 회피)

### 3. UI Image Nodes (가장 큰 그룹 — 383개)

`.png` 확장자가 노드명에 박힌 케이스. `img_` prefix + (해당 시) state suffix.

#### 단일 상태 UI

| 현재 | 제안 | 비고 |
|---|---|---|
| `Logox4.png` | `img_logo_x4` | 로고 4배 변형 |
| `btn_start.png` | `img_btn_start__default` | 단일 상태인데 명시적으로 `_default` |
| `Tablet.png` | `img_tablet` | |
| `Tablet.png 3` | `img_tablet__variant3` | (시퀀스 접미사는 variant 로) |

#### 4-상태 UI 패밀리 (GNB, LNB)

GNB (Global Navigation Bar) 와 LNB (Local Navigation Bar) 가 각각 4상태 비트맵을 가짐.

| 현재 | 제안 |
|---|---|
| `GNB_Active.png` | `img_gnb__active` |
| `GNB_default.png` | `img_gnb__default` |
| `GNB_Disabled.png` | `img_gnb__disabled` |
| `GNB_Pressed.png` | `img_gnb__pressed` |
| `LNB_Active.png` | `img_lnb__active` |
| `LNB_default.png` | `img_lnb__default` |
| `LNB_Disabled.png` | `img_lnb__disabled` |
| `LNB_Pressed.png` | `img_lnb__pressed` |

> `gnb`, `lnb` 는 `doc/GLOSSARY.md` 에 등록 (Global/Local Navigation Bar).

### 4. UI Group Containers

`GNB_1`, `LNB_1-1` 등 그룹화 노드는 컨테이너 — `nod_` prefix.

| 현재 | 제안 |
|---|---|
| `GNB_1`, `GNB_2`, `GNB_3`, `GNB_4` | `nod_gnb_grp__1` ... `nod_gnb_grp__4` |
| `LNB_1-1`, `LNB_1-2`, `LNB_1-3` | `nod_lnb_grp__1_1`, `nod_lnb_grp__1_2`, `nod_lnb_grp__1_3` |
| `LNB_2-1`, `LNB_2-2`, ... | `nod_lnb_grp__2_1`, `nod_lnb_grp__2_2`, ... |

### 5. Text Nodes

`Text 1` 같은 텍스트 노드. v3 vocab 에 `txt_` 추가 제안 (현재 v3 는 `nod_` 로 분류). 

> **v3 규칙 보강 제안**: Kind Prefix Table 에 `txt_` (Text/Label 노드) 추가.

| 현재 | 제안 (v3 보강 후) | 대안 (v3 현행) |
|---|---|---|
| `Text 1` | `txt_<purpose>` (예: `txt_intro_title`) | `nod_text_1` |

> **확인 필요**: `Text 1` 의 표시 내용. 만약 "시작" 같은 짧은 라벨이면 `txt_label_start`, 본문이면 `txt_paragraph_intro`.

### 6. 3D Model Nodes (ResourceCacheRoot 안)

| 현재 | 제안 | 근거 |
|---|---|---|
| `A220-300_B738_KoreanAir_ final` | 분리 권장:<br>`mdl_aircraft_a220_300`<br>`mdl_aircraft_b738`<br>`mdl_livery_korean_air` | 항공기 2종 + 도장. 한 노드에 묶지 말고 sub-mesh 로 분리 |
| `0016` | `mdl_<purpose>__0016` 또는 `mdl_unknown__0016` | **의미 확인 필요**. 부품 번호로 추정 |

추정되는 자식 구조 (확인 후 적용):

```
mdl_aircraft_a220_300
├── mdl_aircraft_a220_300__fuselage    (동체)
├── mdl_aircraft_a220_300__wing_left
├── mdl_aircraft_a220_300__wing_right
├── mdl_aircraft_a220_300__tail
├── mdl_aircraft_a220_300__engine_left
├── mdl_aircraft_a220_300__engine_right
└── mdl_aircraft_a220_300__gear

mat_aircraft_a220_300__fuselage_paint
mat_aircraft_a220_300__metal_polish
mat_livery_korean_air__decal

tex_aircraft_a220_300__fuselage_albedo
tex_aircraft_a220_300__fuselage_normal
tex_aircraft_a220_300__fuselage_roughness
tex_livery_korean_air__decal_albedo
```

> **확인 필요**: 모델이 실제로 어떤 sub-mesh 를 갖는지 (현재 분석으로는 mesh 인덱스만 보임, 의미는 추정).

### 7. Materials (263개, 100% 안티패턴)

현재 모든 머티리얼이 `UnlitOpaque (Instance) (Instance) ...` 사슬. v3 정책: definition 만 명명, instance 는 사용 대상으로 명명.

**원인 분석**: Unity URP 의 `UnlitOpaque` 단일 정의가 142개 텍스처에 각각 인스턴스로 적용됨. instance 마다 다른 텍스처를 지칭하므로 **각 텍스처에 따른 머티리얼명** 부여가 자연스러움.

| 현재 (sample) | 제안 |
|---|---|
| `UnlitOpaque (Instance)` (texture index 0 사용) | `mat_logo_x4` |
| `UnlitOpaque (Instance) (Instance)` (texture index 1 사용) | `mat_btn_start__default` |
| `UnlitOpaque (Instance) (Instance) (Instance)` (texture index 2 사용) | `mat_tablet` |
| ... | ... |

**일괄 규칙**: 머티리얼이 단일 텍스처를 참조하면 `mat_<해당이미지슬러그>` 로 명명. Base material (`UnlitOpaque`) 자체는 `mat_unlit_opaque__base` 로 유지 (있다면).

### 8. Textures (142개)

현재 `image.name` 은 UUID. v3 의 ResourceID 정책상 UUID 는 적합하나, **사람 가독성**을 위해 ASCII slug 도 함께 권장. 단, `image.name` 은 한 값만 가능하므로 트레이드오프:

| 옵션 | image.name | image.uri 또는 extras |
|---|---|---|
| **A**: UUID 유지 | `6c34f19e-9d40-...` | `extras.slug: "tex_logo_x4_albedo"` 추가 |
| **B**: slug 사용 | `tex_logo_x4_albedo` | UUID 는 `ResourceID` 에만 보관 |

> **권장: 옵션 B** — `image.name` 은 사람이 읽고, ID join 은 `ResourceID` (별도 UUID 필드) 가 담당. 3-Layer Identity 원칙과 부합.

매핑 예시 (OriginPath 기반 추정):

| OriginPath | image.name (현재 UUID) | 제안 image.name |
|---|---|---|
| `2d/Logox4.png` | `6c34f19e-9d40-47a5-beb7-184b41bb19d5` | `tex_logo_x4_albedo` (또는 `img_logo_x4` if UI 용도) |
| `2d/btn_start.png` | `56d82d1a-75ed-4bf5-8cce-8a2df27af166` | `img_btn_start__default` |
| `2d/Tablet.png` | `aa0452b8-af43-4b15-a2cf-b2829e33a7df` | `img_tablet` |
| `2d/GNB_Active.png` | `548c19c8-24e9-498a-914b-b51c342ab68c` | `img_gnb__active` |
| `2d/GNB_default.png` | `896ba3cf-910c-4dc6-bb3b-77c778411c84` | `img_gnb__default` |
| `2d/GNB_Disabled.png` | `11f6dadb-4f61-47c6-af7c-77cfb208530e` | `img_gnb__disabled` |
| `2d/GNB_Pressed.png` | `39562a07-26a4-4ea7-9f1a-79a064e20ccd` | `img_gnb__pressed` |

> **OriginPath 가 모두 `2d/` 폴더에 있는 점** 으로 보아 모두 UI 이미지. 따라서 `img_` prefix 가 적절 (3D 머티리얼 입력이 아님).

### 9. Animations (7개, 100% Unity 기본값)

| 현재 | 제안 (대상 식별 필요) |
|---|---|
| `new Clip` | `anm_<target>_<action>` — TODO: `animations[].channels[].target.node` 확인 |
| `new Clip1` | 동일 |
| `new Clip2` | 동일 |
| `new Clip3` | 동일 |
| `new Clip4` | 동일 |
| `new Clip5` | 동일 |

> **확인 필요**: 각 animation 의 channels 가 어떤 노드를 타겟하는지. 타겟 노드명에서 액션 추정. 추가 분석 단계 필요.

## OriginPath 정리 제안

| 현재 | 제안 |
|---|---|
| `C:\Users\VIRNECT\Desktop\test\templete\2d\Logox4.png` | `<PROJECT_ROOT>/2d/Logox4.png` |
| `C:\Users\VIRNECT\Desktop\test\templete\2d\btn_start.png` | `<PROJECT_ROOT>/2d/btn_start.png` |
| ... | ... |

작성자 식별 (`VIRNECT` 유저명) + 로컬 경로 (`Desktop\test\templete`) 모두 `<PROJECT_ROOT>` 토큰으로 익명화.

## v3 규칙 보강 제안 (이번 분석에서 발견된 갭)

1. **`txt_` prefix 추가** — Text/Label 노드용. 현재 v3 의 `nod_` 로는 텍스트 노드를 명확히 못 표현.
2. **`grp` 또는 `_grp` 보조 토큰** — UI 컨테이너 그룹 표현 (`nod_gnb_grp__1`). 또는 단순히 `nod_<name>_<index>` 로 두고 컨벤션화.
3. **시퀀스 접미사 처리 규칙 명문화** — `Tablet.png 3` 같은 Unity 자동 생성 `X N` 접미사는 익스포트 단계에서 제거하거나 `__variant<N>` 으로 정규화.

## Open Questions

- [ ] `Contents X-Y-Z-W` 의 실제 의미 (챕터/레슨/스텝/서브가 맞는지)
- [ ] `Text 1` 의 표시 내용
- [ ] `0016` 의 정체 (부품 번호? 다른 식별자?)
- [ ] `A220-300_B738_KoreanAir_ final` 의 sub-mesh 실측 구조
- [ ] 7개 애니메이션 각각의 채널 타겟 노드
- [ ] `images[].name` UUID 와 `ResourceID` 의 관계 (동일? 별개?)

## Rollout

이 제안이 채택되면:

1. v3 규칙 보강 (`txt_` prefix 추가) → MAKE_FORMAT.md 패치
2. GLOSSARY.md 신규 슬러그 등록 (`gnb`, `lnb`, `ch`, `aircraft`, `livery`, `a220_300`, `b738`, `korean_air`)
3. Open Questions 답변 수집 → 본 제안 확정
4. 마이그레이션 스크립트 작성 (`scripts/migrate-make-naming.ps1` 또는 `.py`)
5. 백업 후 일괄 적용 → 검증 → 신규 `.make` 출력
6. 결과를 v0.2.0 으로 릴리스
