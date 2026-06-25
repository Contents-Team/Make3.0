"""Bundle authoritative repo docs into ONE markdown file for Claude.ai Projects.

Claude.ai (web) Projects cannot fetch repo URLs — knowledge must be the actual
document text. This script concatenates the core docs into a single file you
upload to the project's knowledge. Re-run + re-upload whenever docs change to
"refresh" the project's view to the latest version.

Usage:
    py scripts/build_project_knowledge.py

Output:
    doc/assets/CLAUDE_PROJECT_KNOWLEDGE.md   (header stamped with git commit + date)

To change scope: edit DOCS below (paths are repo-relative).
"""
from pathlib import Path
import subprocess
import datetime

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "doc" / "assets" / "CLAUDE_PROJECT_KNOWLEDGE.md"

# Core naming-convention docs. Add/remove paths to change the bundle scope.
DOCS = [
    "README.md",
    "doc/MAKE_FORMAT.md",
    "doc/GLOSSARY.md",
    "CHANGELOG.md",
]


def git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return "(unknown)"


def main() -> None:
    commit = git("rev-parse", "--short", "HEAD")
    committed_at = git("log", "-1", "--format=%cI")
    remote = git("config", "--get", "remote.origin.url")
    built_at = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

    parts: list[str] = []
    parts.append("# Make3.0 — Project Knowledge Bundle")
    parts.append("")
    parts.append(
        "> 이 파일은 레포 문서를 하나로 묶은 **스냅샷**입니다. Claude.ai 프로젝트 "
        "지식에 이 파일을 업로드해 참조하세요. 레포가 갱신되면 "
        "`py scripts/build_project_knowledge.py` 재실행 후 이 파일을 다시 업로드하면 최신화됩니다."
    )
    parts.append("")
    parts.append("| 항목 | 값 |")
    parts.append("|---|---|")
    parts.append(f"| Repo | {remote} |")
    parts.append(f"| Commit | `{commit}` |")
    parts.append(f"| Commit date | {committed_at} |")
    parts.append(f"| Bundle built | {built_at} |")
    parts.append(f"| Included docs | {len(DOCS)} |")
    parts.append("")
    parts.append("## 포함 문서")
    for d in DOCS:
        parts.append(f"- `{d}`")
    parts.append("")

    missing: list[str] = []
    for rel in DOCS:
        p = ROOT / rel
        parts.append("")
        parts.append("---")
        parts.append("")
        parts.append(f"# ===== FILE: {rel} =====")
        parts.append("")
        if not p.exists():
            missing.append(rel)
            parts.append(f"> ⚠️ 파일 없음: `{rel}`")
            continue
        parts.append(p.read_text(encoding="utf-8"))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")

    size_kb = OUT.stat().st_size / 1024
    print(f"Wrote: {OUT}  ({size_kb:.1f} KB, {len(DOCS) - len(missing)}/{len(DOCS)} docs)")
    if missing:
        print(f"Missing (skipped): {', '.join(missing)}")
    print(f"Stamp: commit {commit} @ {committed_at}")


if __name__ == "__main__":
    main()
