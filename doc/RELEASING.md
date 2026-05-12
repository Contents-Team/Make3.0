# RELEASING

> 버전 태깅, 체인지로그, 배포 자동화 절차.

## Versioning Policy

`Semantic Versioning`. `breaking` → `major`, `feat` → `minor`, `fix` → `patch`.

## Procedure

1. `main` 에서 분기 차단
2. `CHANGELOG.md` 의 `Unreleased` 섹션을 새 버전으로 승격
3. `git tag vX.Y.Z` + `git push --tags`
4. CI 자동 빌드·배포
5. GitHub Release 노트 작성

## Hotfix

TODO: 절차.