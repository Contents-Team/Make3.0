# HANDOFF — Continuation Context for Next Session

- Status: Active
- Last update: 2026-05-12 (v0.1.3)
- 목적: 새 Claude 세션이 이 문서 1개만 읽으면 즉시 작업 이어받기 가능

## Project at a Glance

- **이름**: Make3.0
- **경로 (로컬)**: `C:\Users\VIRNECT\Downloads\work\01_Other\Make3.0`
- **GitHub**: https://github.com/HamIsBadass/Make3.0 (private, `HamIsBadass` 계정)
- **현재 버전**: v0.1.3
- **브랜치**: `main`
- **타겟 도메인**: VIRNECT 의 `.make` 파일 (VR/AR 콘텐츠 패키지) 분석·문서화

## 현재 단계의 핵심 결과물

### 1. `.make` 포맷 사양
- 파일: `doc/MAKE_FORMAT.md`
- 내용: glTF 2.0 GLB + VNT_* 확장 카탈로그 + 네이밍 규칙 v4

### 2. 네이밍 규칙 v4 (현재 채택본)
- **3-Layer Identity**: ID (UUID, 불변) / Name (ASCII slug, 변경 가능) / DisplayTitle (Unicode, 사용자 화면)
- **Kind prefix 강제** (3-letter): `mdl_`/`mat_`/`tex_`/`img_`/`aud_`/`vid_`/`anm_`/`evt_`/`scn_`/`nod_`
- **Asset Namespace**: `<asset>__<component>` (이중 언더스코어)
- **Tier Responsibility Matrix**:
  - Tier A (user-uploaded): 사용자 슬러그 + 툴 prefix
  - Tier B (user-composed): 사용자 의미 + 툴 prefix
  - Tier C (system-derived): **시스템 자동 mirror, 사람 입력 0**
  - System reserved: VNT 예약어

### 3. 용어집
- 파일: `doc/GLOSSARY.md`
- 등록 의무: 로마자 슬러그가 한국어 고유명사를 대체할 때

### 4. 실제 적용 제안서
- 파일: `doc/plans/2026-05-12-make-templete-renaming-proposal.md`
- 대상: `C:\Users\VIRNECT\Downloads\Make Templete_20260512.make`
- **주의**: v3 시점에 작성됨. v4 패러다임에서는 일부 갱신 필요 (Tier C 항목은 자동 파생으로 표시).

## 분석된 .make 샘플 위치

| 파일 | 경로 | 크기 | 특징 |
|---|---|---|---|
| F1 (Template_260403) | `C:\Users\VIRNECT\Downloads\work\01_Other\260403_Template\Template_260403.make` | 2.1 MB | Unity 6000.0.59f2 URP 익스포트, 한국어 prose 노드명 |
| F2 (Make Templete_20260512) | `C:\Users\VIRNECT\Downloads\Make Templete_20260512.make` | 7.1 MB | Virnect Scene Generator v1.0.1, 513 노드 |

JSON 청크 추출본 (재분석 시 빠르게 접근):
- F1: `$env:TEMP\make1.json` (휘발성 — 세션 새로 시작하면 다시 추출)
- F2: `$env:TEMP\make2.json` (휘발성)

재추출 PowerShell:
```powershell
function Extract-GltfJson($path) {
  $bytes = [System.IO.File]::ReadAllBytes($path)
  $chunkLen = [BitConverter]::ToUInt32($bytes, 12)
  [System.Text.Encoding]::UTF8.GetString($bytes, 20, $chunkLen).TrimEnd([char]0,' ')
}
```

## 네이밍 규칙 진화 이력

| 버전 | 핵심 변화 | 트리거 |
|---|---|---|
| v1 | 단일 문자 prefix + `<NN>` 순번 + 영문 강제 | 초기 |
| v2 | 3-Layer Identity 도입, prefix 선택화 | 자기반박 8개 허점 |
| v3 | mandatory 3-letter prefix + asset namespace + suffix vocab | 사용자: "이름만 봐도 알아야 함" |
| **v4** | **Tier 책임 분리 (Tier C 자동 파생)** | 사용자: "Tier C 명명 불필요" + "에이전트도 읽음" |

## Git 상태

- 푸시 완료: `main` 브랜치, 태그 `v0.1.0` ~ `v0.1.3`
- 작업 디렉토리 깨끗 (last commit 후 변경 없음 가정)

## Open Questions (`make Templete_20260512.make` 적용 시)

다음 세션이 적용을 진행한다면 답변 필요:

- [ ] `Contents X-Y-Z-W` 의 실제 의미가 챕터/레슨/스텝/서브가 맞나? (현재 추정)
- [ ] `Text 1` 의 표시 내용은? (이름만으로 추론 불가)
- [ ] `0016` 의 정체는? (부품 번호로 추정)
- [ ] `A220-300_B738_KoreanAir_ final` 의 sub-mesh 실측 구조
- [ ] 7개 애니메이션의 채널 타겟 노드 (v4 의 auto-derivation 알고리즘 적용 대상)
- [ ] `images[].name` 의 UUID 가 `VNT_ExternalResources.ResourceID` 와 동일한 값인가?

## Next Steps (우선순위)

### 1. (선택) v4 규칙으로 제안서 업데이트
- `doc/plans/2026-05-12-make-templete-renaming-proposal.md` 의 Tier C 섹션 (머티리얼·애니메이션) 을 "시스템 자동 파생" 으로 단순화
- 사용자 명명 부담 ~660 → ~192 로 표기 갱신

### 2. v4 검증 자동화 스크립트
- 권장 경로: `scripts/validate-make-names.ps1` 또는 `scripts/validate-make-names.py`
- 입력: `.make` 파일 경로
- 출력: v4 체크리스트 항목별 PASS/FAIL + 위반 위치

### 3. 마이그레이션 스크립트 (실제 .make 파일 변환)
- 권장 경로: `scripts/migrate-make-naming.ps1`
- v4 auto-derivation 규칙 구현
- **백업 필수** — 원본 보존, 새 파일로 출력
- Open Questions 답변 후 실행

### 4. v3 → v4 의 미세 보강 (선택)
- `txt_` prefix 추가 검토 (Text/Label 노드 — 현재 `nod_` 로 처리)
- UI 그룹 컨테이너 컨벤션 명문화 (예: `nod_*_grp__*`)
- Unity 자동 시퀀스 접미사 (`X 3`) → `__variant<N>` 정규화 규칙

### 5. F1 (Template_260403) 도 동일 분석 + 제안서
- F1 은 한국어 prose 노드명이 다수 → v4 의 로마자 정책 + GLOSSARY 등록 시뮬레이션 좋은 케이스

## Re-Entry Quick Commands

새 세션 진입 시 다음 명령으로 컨텍스트 빠르게 복원:

```powershell
# 프로젝트로 이동 및 git 상태 확인
$root = 'C:\Users\VIRNECT\Downloads\work\01_Other\Make3.0'
Set-Location $root
git log --oneline --decorate -5
git status

# 핵심 문서 빠른 확인
Get-Content "$root\doc\plans\HANDOFF.md" -TotalCount 50  # 이 문서
Get-Content "$root\CHANGELOG.md" -TotalCount 30           # 최근 변경

# .make 샘플 JSON 재추출 (필요 시)
# (Extract-GltfJson 함수 정의 후 사용)
```

## Memory References

영구 메모리 (`~/.claude/projects/.../memory/`) 에 다음 항목 저장됨:

- `project_make30_status.md` — 본 프로젝트 현재 상태
- `reference_make30_repo.md` — GitHub 위치 및 진입점

새 세션은 이 메모리들이 자동 로드되므로 별도 조회 불필요.
