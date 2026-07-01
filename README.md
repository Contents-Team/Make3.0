# Make3.0

> VIRNECT **Make 3.0** 콘텐츠 저작을 위한 `.make` 파일 포맷 명세와 에셋 네이밍 규칙의 단일 진실 원천(SSOT). 사람과 AI 에이전트(MCP 저작 포함)가 함께 참조한다.

## What is Make3.0

`Make` 는 VIRNECT 의 3D/AR 학습·실습 콘텐츠 저작 도구이고, 그 산출물이 `.make` 파일이다. 이 저장소는 Make 제품 소스가 아니라, **`.make` 포맷이 실제로 어떻게 생겼는지**(glTF 2.0 GLB + `VNT_*` 커스텀 확장)와 **에셋·노드를 어떻게 이름 붙여야 하는지**(네이밍 규칙)를 분석·정리한 **지식 문서 저장소**다.

목적은 하나 — 사람이든 AI 에이전트든 이 문서만 보면 `.make` 콘텐츠를 **추측 없이 일관되게** 저작·검수할 수 있게 하는 것. 네이밍 규칙은 실측 `.make` 파일(수백 노드)에서 안티패턴과 실사용 어휘를 뽑아 v1 → v7 로 반복 개정해 왔고, 그 변천은 [CHANGELOG.md](./CHANGELOG.md) 에 기록돼 있다.

## Features

- **`.make` 포맷 명세** — GLB 컨테이너 구조 + 8종 `VNT_*` 확장 카탈로그(`VNT_NodeProperty`·`VNT_Event`·`VNT_Animation`·`VNT_Settings_*`·`VNT_ExternalResources` 등), `ResourceType` enum, 컴포넌트 스키마. → [doc/MAKE_FORMAT.md](./doc/MAKE_FORMAT.md)
- **에셋 네이밍 규칙 (현재 v7)** — 2-Tier 모델(T1 원본 파일 / T2 Make Editor 인스턴스), 상태·방향·애니메이션 효과 어휘, 씬 하이어아키 표준, 검증 체크리스트.
- **비개발자용 워크북** — [doc/assets/MakeNamingConvention_v7.xlsx](./doc/assets/MakeNamingConvention_v7.xlsx) (Overview/T1/T2/Hierarchy/Animation/Vocab/Examples/Checklist/Anti-Patterns 9시트).
- **용어 매핑** — 로마자 슬러그 ↔ 한국어 정식 명칭. → [doc/GLOSSARY.md](./doc/GLOSSARY.md)
- **버전 추적** — 규칙 개정 이력을 Keep a Changelog + SemVer 로 관리.

## Problems Make3.0 solves

- **저작 일관성 부재** → `.make` 노드·에셋 이름이 제각각이던 문제를 Tier 기반 네이밍 규칙으로 표준화.
- **AI 에이전트의 포맷 오독** → glTF 표준 뷰어는 무시하는 VNT 인터랙션 정보(이벤트·오디오·AR 타겟)를 명세로 노출해, MCP 저작 시 에이전트가 정확히 참조.
- **규칙의 임의 변경** → 개정마다 근거(실측 갭·자기반박)와 변경 내역을 CHANGELOG 로 남겨 추적 가능.

## Quickstart

```bash
# 1) 포맷·네이밍 규칙 SSOT 읽기
open doc/MAKE_FORMAT.md          # .make 구조 + 네이밍 v7

# 2) 비개발자용 네이밍 워크북
open doc/assets/MakeNamingConvention_v7.xlsx

# 3) (선택) 워크북·자산 재생성 스크립트
python scripts/build_naming_xlsx.py
```

이 저장소는 `.make` 포맷·에셋 네이밍 규칙 문서를 다룬다. 핵심은 [doc/MAKE_FORMAT.md](./doc/MAKE_FORMAT.md) 참조.

## FAQ

**Q. `.make` 파일은 무엇인가요?**
A. glTF 2.0 Binary(GLB) 컨테이너에 VIRNECT 커스텀 확장(`VNT_*`)을 얹은 Make 콘텐츠 패키지입니다. 3D 씬은 표준 glTF, 이벤트·오디오·AR 타겟 등 인터랙션은 VNT 확장에 담깁니다. 상세는 `doc/MAKE_FORMAT.md`.

**Q. 에셋 네이밍 규칙은?**
A. `doc/MAKE_FORMAT.md` 의 `Naming Rules` (현재 v7) 참조. 용어 매핑은 `doc/GLOSSARY.md`.

**Q. 규칙 버전이 바뀌면 어디를 보나요?**
A. [CHANGELOG.md](./CHANGELOG.md). 각 개정(v1→v7)의 변경 근거와 항목이 버전·날짜와 함께 기록됩니다.

**Q. Make 제품(설치파일) 버전이 올라가면 뭐가 바뀌었는지는?**
A. [PRODUCT_CHANGELOG.md](./PRODUCT_CHANGELOG.md). 문서/네이밍 변경(CHANGELOG.md)과 **분리**해서, 설치파일 빌드 버전별 기능 추가/수정/삭제를 분석일과 함께 기록합니다.

## Development

핵심 문서는 [doc/MAKE_FORMAT.md](./doc/MAKE_FORMAT.md) (포맷·네이밍 규칙) 참조. 변경 로그는 두 갈래로 분리 관리한다 — 문서/네이밍 변경은 [CHANGELOG.md](./CHANGELOG.md), 제품(설치파일) 빌드 변경은 [PRODUCT_CHANGELOG.md](./PRODUCT_CHANGELOG.md). 문서 자산 생성 스크립트는 `scripts/` (Python).

## Roadmap

분기별 마일스톤은 [ROADMAP.md](./ROADMAP.md) 참조.

## Contributing

기여 절차는 [CONTRIBUTING.md](./CONTRIBUTING.md). AI 에이전트는 [AGENTS.md](./AGENTS.md) 의 작업 규약을 먼저 읽을 것. 문서 변경 시 [CHANGELOG.md](./CHANGELOG.md) `Unreleased` 섹션 갱신 필수. 팀원↔Claude 업데이트 명령·PR 흐름은 [doc/UPDATE_WORKFLOW.md](./doc/UPDATE_WORKFLOW.md) 참조.

## Telemetry

없음. 이 저장소는 문서만 다루며 어떤 데이터도 수집하지 않는다.

## License

MIT — [LICENSE](./LICENSE)
