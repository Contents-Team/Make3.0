# ADR-0001: Record architecture decisions

- Status: Accepted
- Date: 2026-05-12

## Context

프로젝트 결정이 휘발되면 미래의 개발자(자기 자신 포함)가 이유를 잃는다. 코드만 봐서는 *왜 이렇게 했는지* 알 수 없는 경우가 많다.

## Decision

`Michael Nygard` 형식 ADR 을 `doc/adr/` 에 `NNNN-kebab-case.md` 파일로 기록한다.

각 ADR 은:
- 번호 (zero-padded 4자리) 와 짧은 영문 제목
- `Status`, `Date`
- `Context`, `Decision`, `Consequences`

## Consequences

- 결정 이력이 git 에 남는다
- 새 ADR 로 기존 결정을 `supersede` 할 수 있다
- 신규 컨트리뷰터의 온보딩이 빨라진다