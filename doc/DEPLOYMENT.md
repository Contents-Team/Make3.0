# DEPLOYMENT

> 배포 모드와 환경별 차이.

## Deployment Modes

| 모드 | 용도 | 인프라 |
|---|---|---|
| `local` | 개발 | 단일 프로세스 |
| `staging` | QA | TODO |
| `prod` | 운영 | TODO |

## Environment Variables

| 변수 | 필수 | 용도 |
|---|---|---|
| `DATABASE_URL` | ✅ | DB 연결 문자열 |
| `API_KEY` | ✅ | TODO |
| `LOG_LEVEL` | ❌ | `debug` / `info` / `warn` / `error` |

`.env.example` 를 복사해 시작.

## Deployment Procedure

1. TODO
2. TODO

## Rollback

TODO: 절차와 데이터 호환성 주의.