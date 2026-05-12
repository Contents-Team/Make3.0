# DEVELOPING

> 로컬 개발 환경 셋업과 테스트 절차.

## Prerequisites

- TODO: `Node.js` x.y+ / `pnpm` / `Docker` 등 명시
- TODO: 환경변수 (`DATABASE_URL`, `API_KEY`)

## Start Dev

```bash
git clone <repo>
cd Make3.0
pnpm install
cp .env.example .env
pnpm dev
```

## Test Commands

```bash
pnpm test
pnpm test:integration
pnpm test:e2e
```

## Local Instance Layout

TODO: 로컬 실행 시 어떤 프로세스/포트가 뜨는지
- API server: localhost:3000
- DB: localhost:5432

## Database in Dev

- TODO: 자동 마이그레이션 여부
- TODO: 시드 데이터 명령

## Docker Quickstart

```bash
docker compose up
```

## CLI Client Operations

```bash
TODO
```