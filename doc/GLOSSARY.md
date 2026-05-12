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
