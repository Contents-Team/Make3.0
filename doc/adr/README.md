# Architecture Decision Records

이 디렉토리는 프로젝트의 `Architecture Decision Record` (ADR) 를 기록한다.

## Format

`Michael Nygard` 형식. 파일명은 `NNNN-kebab-case.md` (예: `0007-use-postgres-for-storage.md`).

## Lifecycle

`Status` 는 다음 중 하나:
- `Proposed` — 검토 중
- `Accepted` — 채택됨
- `Deprecated` — 더 이상 권장 안 함
- `Superseded by NNNN` — 새 ADR 이 대체

기존 ADR 본문은 수정하지 않는다. 변경이 필요하면 새 ADR 을 만들어 `Superseded by` 로 연결.

## Index

- [0001 — Record architecture decisions](./0001-record-architecture-decisions.md)