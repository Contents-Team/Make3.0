# 협업자 온보딩 — Claude로 이 레포 작업하기

> 비개발자 5인 + Claude(AI) 협업 기준. **main 은 보호돼 있어 직접 푸시가 막힌다** — 모든 변경은
> 브랜치 → PR → 승인 → Squash 머지로만 들어간다. 이 문서는 접속·연결·규칙 요약이다.

## 0. 한 번만 준비 (최초 셋업)

1. **접근 권한 받기**: 관리자(Contents-Team owner)에게 이 레포 collaborator(권한 `Write`) 추가 요청.
2. **도구 설치**: [Git](https://git-scm.com), [GitHub CLI `gh`](https://cli.github.com), [Claude Code](https://claude.com/claude-code).
3. **GitHub 로그인**: 터미널에서
   ```bash
   gh auth login          # GitHub.com → HTTPS → 브라우저 인증 (repo 권한 포함)
   ```
   > private 레포여도 동일 — 접근 권한만 있으면 `gh`/Claude 모두 정상 동작한다.
4. **클론**:
   ```bash
   gh repo clone Contents-Team/Make3.0
   ```
5. **Claude 연결**: 클론한 `Make3.0` 폴더를 Claude Code로 열기(또는 그 폴더에서 실행). Claude가
   `AGENTS.md`·`doc/UPDATE_WORKFLOW.md` 를 읽고 규약대로 일한다.

## 1. 작업 규칙 (main 보호 — 반드시 지켜짐)

| 규칙 | 의미 (실무) |
|---|---|
| **main 직접 푸시 금지** | main 으로 push 하면 GitHub 가 거부. 항상 새 브랜치에서 작업 → PR. (웹 UI 편집도 자동으로 브랜치+PR 생성) |
| **PR 승인 1명 필요** | 다른 사람 1명이 Approve 해야 머지 가능. **자기 PR 은 자기가 승인 못 함** → 자연스러운 상호 리뷰 |
| **대화(코멘트) 해결 후 머지** | 리뷰 코멘트를 다 Resolve 해야 머지 버튼 활성 |
| **Squash 머지만** | 병합 시 커밋 1개로 합쳐짐(이력 깔끔). merge/rebase 옵션은 꺼둠 |
| **머지 후 브랜치 자동 삭제** | 정리 자동. 로컬은 `git checkout main && git pull` 로 갱신 |
| **force-push·브랜치 삭제 금지(main)** | 이력 파괴 사고 차단 |

> 관리자(admin)는 긴급 시 예외로 처리할 수 있게 열려 있음(enforce_admins off). 평상시엔 모두 PR 흐름 준수.

## 2. Claude 에게 시키는 법 (요약)

무엇이 바뀌었는지 + 관련 파일/버전만 말하면 Claude 가 **브랜치 생성 → 변경 → 올바른 로그 기록 → PR 생성**까지 한다.
사람은 **리뷰·승인·머지**만. 상황별 명령 예시는 → [`doc/UPDATE_WORKFLOW.md`](./UPDATE_WORKFLOW.md).

- 문서/네이밍 규칙 변경 → `CHANGELOG.md` 에 기록
- 제품(설치파일/빌드) 변경 → `PRODUCT_CHANGELOG.md` 에 기록
- 자세한 기여 규약·금지사항 → [`AGENTS.md`](../AGENTS.md), [`CONTRIBUTING.md`](../CONTRIBUTING.md)

## 3. 전형적 흐름 (예: 오탈자 수정)

```bash
# Claude 에게: "GLOSSARY 에 오타 있어, 'Strat'을 'Start'로 고쳐줘"
# → Claude 가 브랜치 만들고 수정 + CHANGELOG Unreleased 기록 + PR 생성
# 그다음 사람이:
#   1) PR 열어 변경 확인
#   2) 동료가 Approve
#   3) "Squash and merge" 클릭
```

## 4. 자주 막히는 지점

- **"내 PR 을 내가 승인 못 해요"** → 정상. 다른 협업자에게 승인 요청. (활성 인원 최소 2명 유지 권장)
- **"머지 버튼이 비활성"** → 리뷰 코멘트 미해결이거나 승인 부족. Resolve + Approve 확인.
- **"main 에 push 가 거부돼요"** → 의도된 보호. 브랜치 만들어 PR 로.
- **선택**: 특정 폴더의 기본 리뷰어를 지정하려면 `CODEOWNERS` 추가(요청 시 Claude 가 설정).
