# Product Changelog — Make (설치파일/빌드)

> **범위: VIRNECT `Make` 제품의 설치파일(빌드) 버전별 기능 추가/수정/삭제 기록.**
> 이 레포의 문서·네이밍 규칙 변경은 [CHANGELOG.md](./CHANGELOG.md) 참조 (별도 관리).
>
> **분석 근거**: 빌드 산출물 표면 — 파일 매니페스트(해시)·셰이더·씬·에셋 인벤토리 + C# 어셈블리
> (`Assembly-CSharp.dll` 등)의 공개 타입/메서드 표면(실행 없이 메타데이터 판독). 내부 로직만 바뀐
> 변경은 표면에 안 드러날 수 있음 — **"표면 기준 관찰"** 성격.
> **워크플로우**: 새 설치파일을 받으면 직전 버전과 diff → 여기에 버전·분석일과 함께 항목 추가.

## [3.1.0.8] — 분석일 2026-07-01 (직전: 3.1.0.7)

- **기준 빌드**: `MakeInstaller_3.1.0.8.exe` (Unity `6000.3.11f1`, Mono). clean 설치파일 추출(미실행).
- **비교 대상**: `MakeInstaller_3.1.0.7.exe`. 파일 331개로 동일(추가/삭제 없음), 코드 변경은
  `Assembly-CSharp.dll`(+7KB)·`VIRNECT_Extension.dll`(+8.5KB)에 집중. 상세 관찰 → [`doc/product/BUILD_3.1.0.8.md`](doc/product/BUILD_3.1.0.8.md).
- 근거: C# 타입/필드 표면 diff(컴파일러 자동생성 제외).

### Added
- **REST API / 데이터 바인딩 서브시스템** — `VIRNECT.Components`: `RestApiComponent`, `RestAPIData`,
  `RestAPISubscriber`, `ResponseHandler`, `ComparisonCondition`, `ComparisonType`(enum). 에디터:
  `RestAPIDataEditor`, `RequestInfo(Editor)`, `ResponseHandlerEditor`, `ComparisonConditionEditor`,
  `SubscribersDrawerEditor`, `SubscriberList`. → 콘텐츠가 외부 REST API를 호출/구독하고 응답 조건으로 액션 분기.
- **AR 타겟 프리뷰** — `VIRNECT.Components.TargetPreviewComponent` 신규.
- **glTF 데이터 컴포넌트 플러그인** — `VirnectGLTF.DataComponentExportPlugin` / `.Plugins.DataComponentImportPlugin`
  (= `.make` 저장/로드 시 DataComponent 직렬화 경로).
- 리스트 편집 UI — `ListEditorWithFooterButtons`, `ListEditorWithLabelAndAddButton`.

### Modified
- `VIRNECT.Components.RestAPISubscriber` — 필드 `+ResponseHandler`.
- `TargetManagerExtensionData` — 필드 `+TargetPreviewObjectID`.
- `VisualizationOptionType`(enum) — `+SceneLayout` (Skybox 와 All 사이).

### Removed
- `RequestDataDescriptor`/`RequestDataEditor`, `RequestDataList` 필드 비워짐 → `RequestInfo`/REST 서브시스템으로 대체.

> 3.1.0.7 및 이전(3.1.0.4 등) 스냅샷은 참고용. 3.1.0.4 는 MCP 주입 빌드(`MK-MakePC-MCP`)라 clean 제품
> diff 기준으로는 부적합 → clean 설치파일(3.1.0.7/3.1.0.8)만 비교에 사용.

<!--
항목 템플릿 (새 버전 도착 시 위에 추가):

## [<version>] — 분석일 <YYYY-MM-DD> (직전: <prev-version>)

### Added
- (신규 컴포넌트/셰이더/씬/툴/에셋)

### Modified
- (변경된 타입·메서드·에셋)

### Removed
- (삭제된 것)
-->
