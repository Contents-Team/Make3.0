# Build 관찰 — Make 3.1.0.8

> 기준 버전: **3.1.0.8** · 분석일: **2026-07-01**
> **성격: 빌드 산출물에서 실행 없이 관찰한 표면 정보** (메타데이터 판독). 손으로 다듬은 규칙 SSOT
> [`doc/MAKE_FORMAT.md`](../MAKE_FORMAT.md) 와 구분한다 — 여기 관찰을 규칙 본문에 반영할지는 **사람 승인** 후.
> 원시 데이터: [`versions/3.1.0.8.virnect-api.json`](../../versions/3.1.0.8.virnect-api.json).

## 빌드 메타

| 항목 | 값 |
|---|---|
| 제품 버전 | `3.1.0.8` (globalgamemanagers) |
| Unity | `6000.3.11f1` (Mono, 비-IL2CPP) |
| 추출 | `MakeInstaller_3.1.0.8.exe` (NSIS) → 7-Zip 무설치 추출, **미실행** |
| 최상위 실행/모듈 | `Make.exe`, `MakeFileWatcher.exe`, `UnityCrashHandler64.exe`, `UnityPlayer.dll` |
| 최상위 폴더 | `Make_Data`, `MonoBleedingEdge`, `D3D12`, `Docs`, `Icons`, `Make_BurstDebugInformation_DoNotShip` |
| 컴포넌트 정의 어셈블리 | **`Make_Data/Managed/VIRNECT_Extension.dll`** (`VIRNECT.Components.*`) + `Assembly-CSharp.dll`(에디터) |

> **핵심 발견**: `.make`의 `VNT_NodeProperty` 에 박히는 `VIRNECT.Components.<Name>` 런타임 클래스는
> `Assembly-CSharp.dll` 이 아니라 **`VIRNECT_Extension.dll`** 에 정의돼 있다. (MAKE_FORMAT.md 가 "추정/미관찰"로
> 남긴 컴포넌트들이 여기서 실측 확인됨.)

## VIRNECT.Components 카탈로그 (실측 58종, 필드 포함)

### 노드 컴포넌트 (Node components)
`SceneRoot`, `SceneComponent`, `ScreenComponent`, `ObjectComponent`, `VisualComponent`,
`ImageComponent`, `VideoComponent`, `TextComponent`, `AudioComponent`, `MeshComponent`,
`MaterialComponent`, `ShapeComponent`, `SocketComponent`, `TargetPreviewComponent`(3.1.0.8 신규)
- `ScreenTransformComponent` — `Anchor`, `AnchorPosition`
- `AnimationComponent` — `AnimationIDTables`, `Clips`
- `EventComponent` — `EventItems`
- `DataComponent` — `Interval`, `Loop`, `RequestOnAwake` (3.1.0.8 신규군)
- `RestApiComponent` — `RequestDatas` (3.1.0.8 신규)
- `UserDataComponent` — `UserDatas`
- 인터페이스/마커: `IAssetComponent`, `IGroupComponent`, `IPlayerComponent`, `RequireUnityComponent`1`

### 이벤트 시스템
- `EventItem` — `TriggerTarget`, `EventTrigger`, `PlaybackEndID`, `PlaybackEndTime`, `ActionItems`
- `ActionItem` — `Target`, `EventAction`, `Delay`, `PropertyModification`
- `EventTrigger` (enum) — `OnEnable`, `Tap`, `DoubleTap`, `PressStart`, `PressEnd`, `CollisionEnter`, `CollisionExit`, `PlaybackEnd`, `OnDisable`
- `EventAction` (enum) — `MoveScene`, `Play`, `PlayPause`, `PlayStop`, `Pause`, `Stop`, `Show`, `Hide`, `OpenURL`, `SetUp`, `OpenContent`

### 애니메이션
- `AnimationIDTable` — `Clip`, `Identifier` · `MakeRuntimeAnimationClip` — `Identifier`
- `ClipCurveData` — `CurveDataType`, `NodeObject`, `PropertyName`, `Curve`, `ComponentType`
- `ClipCurveDataType` (enum) — `None`, `Node`, `Component`, `Property` · `AnimationPropertyEvent`

### 앵커 / 트랜스폼
- `Anchor` (enum, 9) — `LeftTop`…`RightBottom` · `AnchorDirection` (enum) — `Left/Center/Right/Top/Middle/Bottom` · `AnchorExtension`
- `TransformComponent` · `AxisFlags` (enum) — `X`, `Y`, `Z`

### 속성 변경(PropertyModification) 계열
- `PropertyModification`, `SetPropertyModification`(`ModifiableProperty`), `StringPropertyModification`,
  `ContentPropertyModification`(`ContentQueryType`), `PlayPropertyModification`
- `ModifiableProperty` (enum) — `None`, `Text`, `Position`, `EulerAngles`, `Scale`, `Color`, `Resource`
- `GroupType` (enum) — `Scene`, `Target`, `Global`, `Screen`, `SceneGroup`, `Node`

### REST API / 데이터 바인딩 (3.1.0.8 신규 서브시스템)
- `RestAPIData` — `Method`, `DomainAddress`, `EndPoint`, `Headers`, `Params`, `PostRawData`, `Subscribers`
- `RestAPISubscriber` — `Filter`, `ResponseHandler` · `ResponseHandler` — `Comparison`, `ActionItems`
- `ComparisonCondition` — `Type`, `CompareValue` · `ComparisonType` (enum) — `GreaterThan`/`LessThan`/`Equal`/`NotEqual`/`GreaterThanOrEqual`/`LessThanOrEqual`/`Contains`
- `RequestMethod` (enum) — `GET`, `POST_RAW`, `POST_FORM` · `DataFormat` (enum) — `JSON`, `XML`, `ETC`
- `UserData`(`Subscribers`), `UserDataSubscriber`(`Value`), `Subscriber`, `KeyValueData`(`Key`,`Value`), `ParamData`, `HeaderData`

## 기타 VIRNECT 네임스페이스 (참고)
`VIRNECT.MakeEditor.Manager`(21), `VITNECT.MakeEditor.Binding.Adapters`(12, 원문 오탈자 `VITNECT`),
`VITNECT.MakeEditor.ViewModels`(9), `VirnectGLTF`/`VirnectGLTF.Plugins`(glTF import/export — `DataComponent*Plugin` 3.1.0.8 신규),
`VIRNECT.Net.Training.Endpoints`(Healthcheck/Image/Model3d/QR), `VirnectNetworkLibrary.*`.

## MAKE_FORMAT.md 로 승격 후보 (사람 승인 게이트)
- "추정/미관찰"로 남은 컴포넌트(`ImageComponent`·`VideoComponent`·`Model3D(=ObjectComponent?)`·`TextComponent`) → **실측 확인**.
- `VNT_NodeProperty` 컴포넌트 정의처를 `VIRNECT_Extension.dll` 로 명시.
- 위 승격은 규칙 SSOT 변경이므로 사람이 검토 후 별도 커밋.
