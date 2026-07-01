# tools/ — 제품 빌드 지문·diff 워크플로우

Make 설치파일(빌드)에서 **실행 없이** 구조/컴포넌트를 뽑아 버전 간 비교하는 도구.
결과는 `PRODUCT_CHANGELOG.md`(요약) + `doc/product/BUILD_<v>.md`(관찰) + `versions/<v>.*.json`(원시)로 남긴다.

> **언어 주의**: `.NET` 어셈블리 메타데이터 판독이 필요해 이 스크립트는 **PowerShell**(무설치 `System.Reflection.Metadata`)
> 로 작성됐다. 레포의 다른 스크립트(`scripts/*.py`)는 Python — 여기 도구만 예외.

## 1. 설치파일 추출 (NSIS, 미실행)

NSIS는 **풀 `7z.exe`**(축소판 `7za.exe`엔 NSIS 핸들러 없음)로만 풀린다.

```powershell
# 7-Zip 풀버전 무설치 확보: 7zr.exe 로 공식 설치 SFX 를 풀어 7z.exe 획득
#   7zr.exe x 7z<ver>-x64.exe -o<dir>     (7z.exe + 7z.dll)
& 7z.exe x "MakeInstaller_3.1.0.8.exe" -o"_builds\3.1.0.8" -y
```
- `.zip` 배포본(`make_windows_*`)은 `Expand-Archive` 로 충분.

## 2. C# API 표면 지문

```powershell
./dump-api.ps1 -BuildDir "_builds\3.1.0.8" -OutJson "versions\3.1.0.8.api.json"
```
- `Assembly-CSharp.dll`, `VIRNECT_Extension.dll`(← `VIRNECT.Components.*` 정의처), `com.virnect.train.dll`,
  `VirnectNetworkLibrary.dll` 의 public 타입·필드를 **실행 없이** 열거.
- 컴포넌트 카탈로그는 `ns == 'VIRNECT.Components'` 필터로 추출(레포엔 VIRNECT.* 만 커밋 — 3rd-party 노이즈 제외).

## 3. 버전 diff

두 버전의 api JSON 을 `asm|ns|name` 키로 비교 → **추가/삭제 타입 + 필드 변경**.
컴파일러 자동생성(`<>c__DisplayClass*`, `<...>d__NN`, `__StaticArrayInitTypeSize*`)은 **노이즈라 제외**하고 읽는다.

## 4. 기록 (사람 언어)

- `PRODUCT_CHANGELOG.md` — 버전·분석일 + `[Added]/[Modified]/[Removed]`.
- `doc/product/BUILD_<v>.md` — 관찰 상세(컴포넌트 카탈로그 등). **규칙 SSOT `doc/MAKE_FORMAT.md` 반영은 사람 승인 후.**

## 한계
- 빌드 **표면**만 본다 — 내부 로직만 바뀐 변경은 안 드러남.
- 타입 존재 ≠ `.make` 저작 표면 노출. 승격 전 사람 검토.
- Mono 빌드 전제(현재 `6000.3.11f1`). IL2CPP 로 바뀌면 판독 방식 재검토 필요.
