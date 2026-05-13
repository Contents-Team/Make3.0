"""Build HTML slide guide: v6 naming applied to 전기내선공사 가상실습 (Polytec storyboard).

Output: doc/assets/MakeNamingGuide_ElectricalWiring_v6.html

Each <section class="slide"> is one slide. Keyboard ← → navigates.
Print-friendly: each slide on its own page.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "doc" / "assets" / "MakeNamingGuide_ElectricalWiring_v6.html"

# ─────────────────────────────────────────────────────────────────
# Domain data — extracted from PPTX slides 7-14
# ─────────────────────────────────────────────────────────────────

# Wire color codes (5종)
WIRE_COLORS = [
    ("갈", "Brown", "Br", "갈색", "#8B4513"),
    ("검", "Black", "Bk", "흑색", "#1a1a1a"),
    ("회", "Gray", "Gr", "회색", "#808080"),
    ("녹-황", "GreenYellow", "GY", "녹색-황색 (접지선)", "linear-gradient(45deg,#2e7d32 50%,#fbc02d 50%)"),
    ("황", "Yellow", "Yl", "황색", "#fbc02d"),
]

# 카테고리별 기구·공구 리스트 (PPTX 슬라이드 7-10)
CATEGORIES = [
    {
        "title": "단자대 (소켓베이스 / Terminal Block)",
        "key": "tb",
        "items": [
            # (한국어 이름, 원본 에셋명, 인스턴스명 예시, 비고)
            ("10핀 TB", "TB10Pin_v01.glb", "TB10_01, TB10_02", "Terminal Block 10핀"),
            ("8핀 소켓베이스", "TB8Pin_v01.glb", "TB8_01, TB8_02", "회로도상 TB5 등으로 사용"),
            ("12핀 소켓베이스", "TB12Pin_v01.glb", "TB12_01, TB12_02", "회로도상 TB6 등으로 사용"),
        ],
    },
    {
        "title": "동작검사용 기구 (Operation Test)",
        "key": "op",
        "items": [
            ("릴레이 8Pin", "Relay8Pin_v01.glb", "Relay_01, Relay_02", "보조계전기"),
            ("MC (전자 접촉기)", "MC_v01.glb", "MC_01, MC_02", "Magnetic Contactor"),
            ("EOCR (전자식 과전류계전기)", "EOCR_v01.glb", "EOCR_01", "Electronic Over Current Relay"),
            ("퓨즈 홀더", "FuseHolder_v01.glb", "FuseHolder_01", ""),
            ("타이머", "Timer_v01.glb", "Timer_01", "회로도상 T"),
            ("플리커", "Flicker_v01.glb", "Flicker_01", "회로도상 FR"),
            ("FLS (Floatless Level Switch)", "FLS_v01.glb", "FLS_01", "수위 검출 스위치"),
        ],
    },
    {
        "title": "제어판 기구 (Control Panel Devices)",
        "key": "ctrl",
        "items": [
            ("MCCB (배선용 차단기)", "MCCB_v01.glb", "MCCB_01", "Molded Case Circuit Breaker"),
            ("퓨즈", "Fuse_v01.glb", "Fuse_01, Fuse_02", ""),
        ],
    },
    {
        "title": "스위치 / 버튼 (Switch / Button)",
        "key": "btn",
        "items": [
            ("푸쉬버튼 — 적색", "PushBtn_Red_v01.glb", "PushBtn_Red_01", "Push Button"),
            ("푸쉬버튼 — 녹색", "PushBtn_Green_v01.glb", "PushBtn_Green_01", ""),
            ("푸쉬버튼 — 청색", "PushBtn_Blue_v01.glb", "PushBtn_Blue_01", ""),
            ("셀렉터 스위치 (A타입)", "SelectorSw_A_v01.glb", "SelectorSw_A_01", "Selector Switch A"),
            ("셀렉터 스위치 (B타입)", "SelectorSw_B_v01.glb", "SelectorSw_B_01", "Selector Switch B"),
        ],
    },
    {
        "title": "램프 · 부저 (Lamp / Buzzer)",
        "key": "lamp",
        "items": [
            ("파일럿램프 — 적색", "PilotLamp_Red_v01.glb", "PilotLamp_Red_01", ""),
            ("파일럿램프 — 황색", "PilotLamp_Yellow_v01.glb", "PilotLamp_Yellow_01", ""),
            ("파일럿램프 — 녹색", "PilotLamp_Green_v01.glb", "PilotLamp_Green_01", ""),
            ("파일럿램프 — 백색", "PilotLamp_White_v01.glb", "PilotLamp_White_01", ""),
            ("부저", "Buzzer_v01.glb", "Buzzer_01", ""),
        ],
    },
    {
        "title": "기타 컨트롤 (Other Controls)",
        "key": "etc",
        "items": [
            ("전원 공급 스위치 (단상 2선식)", "PowerSw_1P2W_v01.glb", "PowerSw_01", "Single Phase 2 Wire"),
            ("2구 컨트롤박스", "ControlBox_2Way_v01.glb", "ControlBox_01", ""),
            ("8각 박스", "Box_Octagon_v01.glb", "Box_Octagon_01", "Junction Box"),
        ],
    },
    {
        "title": "배관 · 커넥터 · 케이블 (Conduit / Connector / Cable)",
        "key": "conduit",
        "items": [
            ("PE 전선관", "PipePE_v01.glb", "PipePE_01, PipePE_02", "Polyethylene Conduit"),
            ("플렉시블 전선관 (CD관)", "PipeCD_v01.glb", "PipeCD_01", "Combine Duct (flexible)"),
            ("CV 케이블", "CableCV_v01.glb", "CableCV_01", "Cross-linked Vinyl"),
            ("새들 (소)", "Saddle_S_v01.glb", "Saddle_S_01", "2가지 사이즈"),
            ("새들 (대)", "Saddle_L_v01.glb", "Saddle_L_01", ""),
            ("커넥터 — CD관", "Connector_CD_v01.glb", "Connector_CD_01", ""),
            ("커넥터 — PE관", "Connector_PE_v01.glb", "Connector_PE_01", ""),
            ("케이블 그랜드", "CableGland_v01.glb", "CableGland_01", ""),
        ],
    },
    {
        "title": "진단기기 · 공구 · 재료 (Tools / Materials)",
        "key": "tool",
        "items": [
            ("벨 테스터기", "BellTester_v01.glb", "BellTester_01", "Continuity tester"),
            ("드릴", "Drill_v01.glb", "Drill_01", ""),
            ("스트리퍼", "Stripper_v01.glb", "Stripper_01", "Wire stripper"),
            ("파이프 커터", "PipeCutter_v01.glb", "PipeCutter_01", ""),
            ("나사못", "Screw_v01.glb", "Screw_01, Screw_02", ""),
            ("자", "Ruler_v01.glb", "Ruler_01", "60×10cm"),
            ("분필", "Chalk_v01.glb", "Chalk_01", ""),
            ("마스킹테이프", "MaskingTape_v01.glb", "MaskingTape_01", ""),
        ],
    },
]

# 전선 객체 (모델링이며 .glb)
WIRE_ASSETS = [
    # (원본명, 인스턴스 패턴, 설명)
    ("Wire_Br_v01.glb", "Wire_Br_*", "갈색 전선 (단심)"),
    ("Wire_Bk_v01.glb", "Wire_Bk_*", "흑색 전선 (단심)"),
    ("Wire_Gr_v01.glb", "Wire_Gr_*", "회색 전선 (단심)"),
    ("Wire_GY_v01.glb", "Wire_GY_*", "녹-황 전선 (접지)"),
    ("Wire_Yl_v01.glb", "Wire_Yl_*", "황색 전선 (단심)"),
]

# 주회로 22선 — PPTX 슬라이드 11-12
MAIN_CIRCUIT = [
    (1, "GY", "TB5 단자대 10", "TB6 단자대 10"),
    (2, "GY", "TB6 단자대 10", "TB6 단자대 18"),
    (3, "Br", "TB5 단자대 7", "MCCB 갈 input"),
    (4, "Bk", "TB5 단자대 8", "MCCB 검 input"),
    (5, "Gr", "TB5 단자대 9", "MCCB 회 input"),
    (6, "Br", "MCCB 갈 output", "EOCR 1"),
    (7, "Bk", "MCCB 검 output", "EOCR 2"),
    (8, "Gr", "MCCB 회 output", "EOCR 3"),
    (9, "Br", "EOCR 1", "퓨즈홀더 갈 input"),
    (10, "Gr", "EOCR 3", "퓨즈홀더 회 input"),
    (11, "Br", "EOCR 7", "MC1 1"),
    (12, "Bk", "EOCR 8", "MC1 2"),
    (13, "Gr", "EOCR 9", "MC1 3"),
    (14, "Br", "MC1 1", "MC2 1"),
    (15, "Bk", "MC1 2", "MC2 2"),
    (16, "Gr", "MC1 3", "MC2 3"),
    (17, "Br", "MC1 7", "TB6 단자대 15"),
    (18, "Bk", "MC1 8", "TB6 단자대 16"),
    (19, "Gr", "MC1 9", "TB6 단자대 17"),
    (20, "Br", "MC2 7", "TB6 단자대 7"),
    (21, "Bk", "MC2 8", "TB6 단자대 8"),
    (22, "Gr", "MC2 9", "TB6 단자대 9"),
]

# 보조회로 39선 — PPTX 슬라이드 13-14 (No. | 출발 | 도착, 색상 미명시 — 보통 황색·검정 등)
# 색상이 표에 없음 → 인스턴스명에 색상 생략 또는 별도 명시
AUX_CIRCUIT = [
    (1, "퓨즈홀더 갈", "EOCR 12"),
    (2, "EOCR 12", "EOCR 10"),
    (3, "EOCR 4", "TB5 단자대 16"),
    (4, "TB5 단자대 16", "TB5 단자대 18"),
    (5, "TB5 단자대 18", "X 8"),
    (6, "X 8", "MC1 10"),
    (7, "MC1 10", "MC2 10"),
    (8, "EOCR 5", "TB5 단자대 2"),
    (9, "TB5 단자대 2", "TB5 단자대 4"),
    (10, "TB5 단자대 15", "FLS 4"),
    (11, "FLS 4", "FLS 6"),
    (12, "TB5 단자대 17", "TB6 단자대 2"),
    (13, "TB6 단자대 1", "TB6 단자대 4"),
    (14, "TB6 단자대 4", "X 3"),
    (15, "TB6 단자대 3", "T 7"),
    (16, "T 7", "FLS 3"),
    (17, "FLS 3", "X 1"),
    (18, "X 1", "X 7"),
    (19, "X 6", "T 8"),
    (20, "T 6", "FR 7"),
    (21, "FR 7", "FR 8"),
    (22, "FR 5", "MC1 12"),
    (23, "FR 6", "MC2 12"),
    (24, "MC1 4", "TB5 단자대 14"),
    (25, "MC2 4", "TB5 단자대 12"),
    (26, "TB5 단자대 11", "TB5 단자대 13"),
    (27, "TB5 단자대 13", "MC2 6"),
    (28, "MC2 6", "MC1 6"),
    (29, "MC1 6", "FR 2"),
    (30, "FR 2", "T 2"),
    (31, "T 2", "X 2"),
    (32, "X 2", "FLS 5"),
    (33, "FLS 5", "TB5 단자대 3"),
    (34, "TB5 단자대 3", "TB5 단자대 1"),
    (35, "TB5 단자대 1", "EOCR 6"),
    (36, "EOCR 6", "퓨즈홀더 회"),
    (37, "FLS 7", "TB6 단자대 11"),
    (38, "FLS 8", "TB6 단자대 12"),
    (39, "FLS 1", "TB6 단자대 13"),
]

# ─────────────────────────────────────────────────────────────────
# HTML rendering
# ─────────────────────────────────────────────────────────────────

CSS = """
* { box-sizing: border-box; }
html, body {
  margin: 0; padding: 0;
  font-family: 'Malgun Gothic', '맑은 고딕', system-ui, sans-serif;
  background: #2b2b2b;
  color: #222;
}
.deck { position: relative; }
.slide {
  width: 1280px;
  min-height: 720px;
  margin: 24px auto;
  padding: 40px 56px;
  background: #fff;
  box-shadow: 0 6px 20px rgba(0,0,0,0.35);
  page-break-after: always;
  break-after: page;
  position: relative;
  overflow: hidden;
}
.slide h1 {
  margin: 0 0 8px 0;
  font-size: 32px;
  color: #1f3864;
  border-bottom: 3px solid #2f5496;
  padding-bottom: 10px;
}
.slide h2 {
  margin: 24px 0 10px 0;
  font-size: 22px;
  color: #2f5496;
}
.slide h3 {
  margin: 16px 0 6px 0;
  font-size: 18px;
  color: #1f3864;
}
.slide p, .slide li { font-size: 15px; line-height: 1.55; }
.slide .subtitle { color: #595959; font-size: 16px; margin-top: -4px; }
.page-num {
  position: absolute; right: 24px; bottom: 16px;
  color: #888; font-size: 13px;
}
.cover { display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding-top: 200px; }
.cover h1 { font-size: 44px; border: 0; color: #1f3864; }
.cover .tag { font-size: 18px; color: #5a5a5a; margin: 10px 0; }
.cover .meta { margin-top: 60px; color: #777; font-size: 14px; }

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  margin: 10px 0 18px 0;
}
th {
  background: #2f5496; color: #fff;
  padding: 8px 10px; text-align: left;
  font-weight: 600;
}
td {
  padding: 7px 10px; border-bottom: 1px solid #d9d9d9;
  vertical-align: top;
}
tr:nth-child(even) td { background: #f4f6fa; }
.mono { font-family: 'Consolas', 'D2Coding', monospace; font-size: 13px; }
.tag-T1 { background: #c5e0b4; color: #385723; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
.tag-T2 { background: #bdd7ee; color: #1f3864; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
.tag-T3 { background: #ffd966; color: #7f5f00; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
.tag-ANIM { background: #f4b183; color: #843c0c; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
.note {
  background: #fff2cc; border-left: 4px solid #ffc000;
  padding: 10px 14px; font-size: 13px; margin: 12px 0;
  color: #5a4500;
}
.tree {
  font-family: 'Consolas', monospace; font-size: 13px;
  background: #f4f6fa; padding: 18px 22px; border-left: 4px solid #2f5496;
  white-space: pre; line-height: 1.65;
  border-radius: 4px;
}
.colorbox { display: inline-block; width: 16px; height: 16px; vertical-align: middle; border: 1px solid #999; border-radius: 3px; margin-right: 6px; }
.cols2 { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }
.toc li { margin: 6px 0; }
.principle {
  background: #f4f6fa; border-left: 4px solid #2f5496;
  padding: 12px 16px; margin: 8px 0; border-radius: 4px;
}
.principle b { color: #1f3864; }
.checklist li { list-style: none; margin: 5px 0; padding-left: 24px; position: relative; }
.checklist li::before {
  content: '☐'; position: absolute; left: 0; color: #2f5496; font-size: 18px; line-height: 1;
}
@media print {
  body { background: #fff; }
  .slide { box-shadow: none; margin: 0; }
  .nav { display: none !important; }
}
.nav {
  position: fixed; bottom: 20px; right: 20px;
  background: rgba(0,0,0,0.65); color: #fff; padding: 8px 14px; border-radius: 24px;
  font-size: 13px; user-select: none;
  z-index: 100;
}
.nav span { font-weight: bold; padding: 0 6px; }
"""

JS = """
const slides = document.querySelectorAll('.slide');
let cur = 0;
function go(i) {
  cur = Math.max(0, Math.min(slides.length - 1, i));
  slides[cur].scrollIntoView({behavior: 'smooth', block: 'start'});
  document.getElementById('pgnum').textContent = (cur + 1) + ' / ' + slides.length;
}
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); go(cur + 1); }
  if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); go(cur - 1); }
  if (e.key === 'Home') { e.preventDefault(); go(0); }
  if (e.key === 'End') { e.preventDefault(); go(slides.length - 1); }
});
window.addEventListener('scroll', () => {
  for (let i = 0; i < slides.length; i++) {
    const r = slides[i].getBoundingClientRect();
    if (r.top >= -100 && r.top < window.innerHeight / 2) { cur = i; break; }
  }
  document.getElementById('pgnum').textContent = (cur + 1) + ' / ' + slides.length;
});
"""

slides_html = []
total_slides_placeholder = "__TOTAL__"


def make_slide(num, body):
    return f'<section class="slide"><div class="page-num">슬라이드 {num} / {total_slides_placeholder}</div>{body}</section>'


# ─── Slide 1 — Cover ───────────────────────────────────────────
s = f'''
<div class="cover">
  <h1>전기내선공사 가상 실습</h1>
  <h1 style="margin-top: -10px;">3D 모델·전선 네이밍 가이드</h1>
  <div class="tag">Make Asset Naming Convention v6 적용</div>
  <div class="tag">한국폴리텍신기술교육원 협력 / VR·XR 실습 콘텐츠</div>
  <div class="meta">
    원본 기획서: [폴리텍신기술교육원]_전기내선공사 가상 실습_SB_v1.0.pptx (127 슬라이드)<br>
    명명 규칙: doc/MAKE_FORMAT.md 의 Naming Rules v6<br>
    작성일: 2026-05-13
  </div>
</div>
'''
slides_html.append(make_slide(1, s))


# ─── Slide 2 — 목차 ────────────────────────────────────────────
toc_items = [
    "1. 표지",
    "2. 이 문서의 목적·범위",
    "3. v6 명명 규칙 핵심 5가지",
    "4. 3-Tier 모델 — T1·T2·T3 한눈에",
    "5. 전선 색상 약자 정의 (5종)",
]
n = 6
for c in CATEGORIES:
    toc_items.append(f"{n}. 카테고리 — {c['title']}")
    n += 1
toc_items.append(f"{n}. 전선 원본 에셋 (.glb) 명명")
n += 1
toc_items.append(f"{n}. 주회로 22선 인스턴스 (Wire_<Color>_<NN>)")
n += 1
toc_items.append(f"{n}. 주회로 배선표 — 전체 22선 매핑")
n += 1
toc_items.append(f"{n}. 보조회로 39선 인스턴스")
n += 1
toc_items.append(f"{n}. 보조회로 배선표 — 전체 39선 매핑")
n += 1
toc_items.append(f"{n}. 전체 씬 트리 구조 (인스턴스 위계)")
n += 1
toc_items.append(f"{n}. 머티리얼 명명 (T3 자동 파생)")
n += 1
toc_items.append(f"{n}. 검증 체크리스트")
n += 1
toc_items.append(f"{n}. 변환 사유 요약 + 다음 단계")

toc_html = "\n".join(f"<li>{escape(t)}</li>" for t in toc_items)
s = f'''
<h1>목차</h1>
<ol class="toc" style="font-size:16px; line-height:1.85; columns: 2; column-gap: 40px;">
{toc_html}
</ol>
'''
slides_html.append(make_slide(2, s))


# ─── Slide 3 — v6 핵심 5가지 ──────────────────────────────────
principles = [
    ("어디서 보는지에 따라 형식이 다름",
     "OS 파일 탐색기(T1) / Make Editor(T2) / 자동 생성(T3) — 각 컨텍스트별 최적화."),
    ("Make Editor 인스턴스는 종류 약자 생략",
     "트리 옆 아이콘이 종류를 시각화 → mdl_, img_ 같은 앞 약자 불필요. PascalCase 로 간결하게."),
    ("구분 기호는 언더바 _ 하나만",
     "이중 __ 와 하이픈 - 은 사용 금지. 모든 토큰 경계는 단일 _."),
    ("약자는 정해진 단어 모음 안에서만",
     "State (_Def/_Prs/_On/_Off/_Sel), Direction (_L/_R/_U/_D), Action (Rot/Scl/Mov/...). 5종 색상 (Br/Bk/Gr/GY/Yl)."),
    ("원본 파일에는 _v01 버전 표시 가능",
     "T1 원본만 _v01 가능. T2 인스턴스에는 버전 표시 금지 — Make 가 인스턴스 단위 버전 관리 안 함."),
]
ps = "\n".join(f'<div class="principle"><b>{i+1}. {p[0]}</b><br>{p[1]}</div>' for i, p in enumerate(principles))
s = f'''
<h1>v6 명명 규칙 핵심 5가지</h1>
<p class="subtitle">상세 규칙은 doc/MAKE_FORMAT.md 또는 doc/assets/MakeNamingConvention_v6.xlsx 참고.</p>
{ps}
'''
slides_html.append(make_slide(3, s))


# ─── Slide 4 — 3-Tier 모델 ───────────────────────────────────
s = f'''
<h1>3-Tier 모델 한눈에</h1>
<table>
<tr><th style="width:60px;">단계</th><th style="width:200px;">무엇</th><th style="width:280px;">어디서 보임</th><th>형식·예시</th></tr>
<tr><td><span class="tag-T1">T1</span></td><td><b>원본 파일</b><br>모델러 납품</td><td>OS 파일 탐색기</td><td class="mono">MCCB_v01.glb, Wire_Br_v01.glb, PushBtn_Red_v01.glb</td></tr>
<tr><td><span class="tag-T2">T2</span></td><td><b>Make Editor 인스턴스</b><br>씬에 배치된 객체</td><td>Make Editor 의 씬 트리 (타입 아이콘 옆)</td><td class="mono">MCCB_01, Wire_Br_001, PushBtn_Red_01</td></tr>
<tr><td><span class="tag-T3">T3</span></td><td><b>자동 생성 객체</b><br>머티리얼·중간 mesh</td><td>머티리얼 패널 (간접)</td><td class="mono">mat_wire_brown, mat_mccb_body, tex_pushbtn_red_albedo</td></tr>
<tr><td><span class="tag-ANIM">ANIM</span></td><td><b>애니메이션</b><br>animations[] 배열</td><td>애니메이션 패널</td><td class="mono">MC_Pop, Lamp_FI, Buzzer_Op (prefix 없음)</td></tr>
</table>

<h2>왜 단계마다 다른가?</h2>
<div class="note">
  <b>T1</b> 은 OS 파일 탐색기에 보이므로 확장자가 종류를 알려줍니다.<br>
  <b>T2</b> 는 Make Editor 의 아이콘이 종류를 시각화하므로 이름에 종류 약자가 필요 없습니다.<br>
  <b>T3</b> 는 사람이 직접 안 보고 AI·로그가 단독 노출하므로 종류 약자(mat_, tex_) 를 유지합니다.
</div>
'''
slides_html.append(make_slide(4, s))


# ─── Slide 5 — 전선 색상 약자 ─────────────────────────────────
rows = []
for ko, en, ab, desc, color in WIRE_COLORS:
    rows.append(f'<tr><td><span class="colorbox" style="background:{color};"></span><b>{ko}</b></td>'
                f'<td>{desc}</td><td class="mono">{en}</td><td class="mono"><b>{ab}</b></td>'
                f'<td class="mono">Wire_{ab}_v01.glb</td><td class="mono">Wire_{ab}_001 ~ Wire_{ab}_NNN</td></tr>')
s = f'''
<h1>전선 색상 약자 정의 (5종)</h1>
<p class="subtitle">기획서에 명시된 5색 — 모든 전선은 색상별로 별도 모델(.glb) 로 분리. 인스턴스명에 색상 약자를 포함해 회로도와 직접 대조 가능.</p>
<table>
<tr><th>한글 표기 (회로도)</th><th>설명</th><th>영문</th><th>약자</th><th>원본 에셋 (T1)</th><th>인스턴스 (T2)</th></tr>
{"".join(rows)}
</table>

<div class="note">
  <b>녹-황(GY)</b> 은 접지선으로 일반적으로 1선 형태. 시각 구분을 위해 머티리얼(T3) 도 분리: <span class="mono">mat_wire_greenyellow</span>.<br>
  보조회로(39선)는 기획서에 색상 표기가 없으므로 인스턴스명에 색상 약자를 생략하거나 시공 시 결정. 본 가이드는 <b>WireAux_NNN</b> 형식으로 표기.
</div>
'''
slides_html.append(make_slide(5, s))


# ─── Slides 6~13 — 카테고리별 ────────────────────────────────
for cat in CATEGORIES:
    rows = []
    for it in cat["items"]:
        ko, src, inst, note = it
        rows.append(f'<tr><td>{escape(ko)}</td>'
                    f'<td class="mono">{escape(src)}</td>'
                    f'<td class="mono">{escape(inst)}</td>'
                    f'<td>{escape(note)}</td></tr>')
    s = f'''
<h1>카테고리 — {escape(cat["title"])}</h1>
<table>
<tr><th style="width:30%;">한글 명칭 (기획서)</th><th style="width:25%;">원본 에셋 <span class="tag-T1">T1</span></th><th style="width:25%;">인스턴스 <span class="tag-T2">T2</span></th><th>비고</th></tr>
{"".join(rows)}
</table>
<div class="note">
  • 원본은 모두 <b>.glb</b> 확장자, PascalCase + <span class="mono">_v01</span>.<br>
  • 인스턴스는 PascalCase, 종류 약자 없음, 동일 모델이 여러 곳에 쓰이면 <span class="mono">_01, _02, ...</span> 로 번호 부여.<br>
  • 부모 노드(예: <span class="mono">ControlPanel</span>) 컨텍스트가 있으면 더 짧게 가능.
</div>
'''
    slides_html.append(make_slide(len(slides_html) + 1, s))


# ─── Slide — 전선 원본 에셋 ─────────────────────────────────
rows = []
for src, inst, desc in WIRE_ASSETS:
    rows.append(f'<tr><td class="mono">{src}</td><td class="mono">{inst}</td><td>{desc}</td></tr>')
s = f'''
<h1>전선 원본 에셋 (.glb) — 5종</h1>
<p class="subtitle">색상별로 별도 모델 — 머티리얼 색상이 GLB 안에 포함되어 임포트 시 즉시 가시화.</p>
<table>
<tr><th>원본 에셋 <span class="tag-T1">T1</span></th><th>인스턴스 패턴 <span class="tag-T2">T2</span></th><th>설명</th></tr>
{"".join(rows)}
</table>

<h2>대안 설계: 단일 전선 모델 + 머티리얼 교체</h2>
<table>
<tr><th>안</th><th>장점</th><th>단점</th></tr>
<tr><td><b>색상별 분리</b> (권장)</td><td>임포트 즉시 가시화, GLB 가 자체 완결</td><td>5개 파일 관리</td></tr>
<tr><td>단일 + 머티리얼 교체</td><td>파일 1개, 길이·구부림 공통</td><td>씬에서 머티리얼 명시 필요, AI 가 색상 식별 어려움</td></tr>
</table>
<div class="note">본 가이드는 <b>색상별 분리</b> 채택. AI 가 인스턴스명(<span class="mono">Wire_Br_005</span>) 만 봐도 색상 파악 가능.</div>
'''
slides_html.append(make_slide(len(slides_html) + 1, s))


# ─── Slide — 주회로 인스턴스 명명 규칙 ────────────────────────
s = f'''
<h1>주회로 22선 인스턴스 명명 규칙</h1>
<h2>형식</h2>
<div class="tree">WireM_&lt;NN&gt;_&lt;Color&gt;

WireM   주회로(Main) 식별
NN      회로도 라인 번호 (01~22, 두 자리 고정)
Color   색상 약자 (Br/Bk/Gr/GY/Yl)</div>

<h2>예시</h2>
<table>
<tr><th style="width:60px;">No</th><th>이름</th><th>의미</th></tr>
<tr><td>1</td><td class="mono">WireM_01_GY</td><td>주회로 1번선 — 녹-황 (TB5 단자대 10 → TB6 단자대 10)</td></tr>
<tr><td>3</td><td class="mono">WireM_03_Br</td><td>주회로 3번선 — 갈색 (TB5 단자대 7 → MCCB 갈 input)</td></tr>
<tr><td>9</td><td class="mono">WireM_09_Br</td><td>주회로 9번선 — 갈색 (EOCR 1 → 퓨즈홀더 갈 input)</td></tr>
<tr><td>17</td><td class="mono">WireM_17_Br</td><td>주회로 17번선 — 갈색 (MC1 7 → TB6 단자대 15)</td></tr>
</table>

<div class="note">
  <b>설계 결정</b>: 출발·도착 정보를 인스턴스명에 담지 않음 — 너무 길어짐 (<span class="mono">Wire_TB5_10_TB6_10_GY</span> 같은 형식 회피).<br>
  대신 <b>씬 트리 구조</b>로 표현: <span class="mono">MainCircuit/WireM_01_GY</span>. 출발·도착은 VNT 컴포넌트의 <span class="mono">FromNodeId</span>/<span class="mono">ToNodeId</span> 필드로.
</div>
'''
slides_html.append(make_slide(len(slides_html) + 1, s))


# ─── Slide — 주회로 전체 22선 표 ──────────────────────────────
rows = []
for no, col, fr, to in MAIN_CIRCUIT:
    rows.append(f'<tr><td>{no}</td><td class="mono">WireM_{no:02d}_{col}</td><td>{escape(fr)}</td><td>{escape(to)}</td></tr>')
s = f'''
<h1>주회로 배선표 — 전체 22선 (Line 22)</h1>
<table style="font-size:12px;">
<tr><th style="width:50px;">No</th><th style="width:180px;">인스턴스 이름 <span class="tag-T2">T2</span></th><th>출발</th><th>도착</th></tr>
{"".join(rows)}
</table>
'''
slides_html.append(make_slide(len(slides_html) + 1, s))


# ─── Slide — 보조회로 인스턴스 명명 규칙 ──────────────────────
s = f'''
<h1>보조회로 39선 인스턴스 명명 규칙</h1>
<h2>형식</h2>
<div class="tree">WireA_&lt;NN&gt;

WireA   보조회로(Auxiliary) 식별
NN      회로도 라인 번호 (01~39, 두 자리 고정)</div>

<h2>색상 약자가 없는 이유</h2>
<div class="note">
  기획서 슬라이드 13-14 의 보조회로 배선표에는 <b>색상 칼럼이 없음</b>.<br>
  실제 시공에서 보조회로는 보통 <b>황색 단심선</b>으로 통일하지만, 설계상 색상이 정해지지 않은 경우는 인스턴스명에 색상 약자 생략.<br>
  설계 단계에서 색상이 확정되면 <span class="mono">WireA_01_Yl</span> 형식으로 확장 가능.
</div>

<h2>예시</h2>
<table>
<tr><th style="width:60px;">No</th><th>이름</th><th>의미</th></tr>
<tr><td>1</td><td class="mono">WireA_01</td><td>보조회로 1번선 (퓨즈홀더 갈 → EOCR 12)</td></tr>
<tr><td>14</td><td class="mono">WireA_14</td><td>보조회로 14번선 (TB6 단자대 4 → X 3)</td></tr>
<tr><td>21</td><td class="mono">WireA_21</td><td>보조회로 21번선 (FR 7 → FR 8)</td></tr>
<tr><td>36</td><td class="mono">WireA_36</td><td>보조회로 36번선 (EOCR 6 → 퓨즈홀더 회)</td></tr>
</table>
'''
slides_html.append(make_slide(len(slides_html) + 1, s))


# ─── Slide — 보조회로 전체 39선 표 ────────────────────────────
# 39 lines, split into 2 columns for fit
def split_two(items):
    half = (len(items) + 1) // 2
    return items[:half], items[half:]

left, right = split_two(AUX_CIRCUIT)
def render_aux(rows_):
    out = []
    for no, fr, to in rows_:
        out.append(f'<tr><td>{no}</td><td class="mono">WireA_{no:02d}</td><td>{escape(fr)}</td><td>{escape(to)}</td></tr>')
    return "".join(out)

s = f'''
<h1>보조회로 배선표 — 전체 39선 (Line 39)</h1>
<div class="cols2">
<table style="font-size:11px;">
<tr><th>No</th><th>이름</th><th>출발</th><th>도착</th></tr>
{render_aux(left)}
</table>
<table style="font-size:11px;">
<tr><th>No</th><th>이름</th><th>출발</th><th>도착</th></tr>
{render_aux(right)}
</table>
</div>
'''
slides_html.append(make_slide(len(slides_html) + 1, s))


# ─── Slide — 전체 씬 트리 ────────────────────────────────────
tree = '''SceneRoot
├── ControlPanel                          ← 제어판 컨테이너 (Stage 1·2)
│   ├── MCCB_01
│   ├── EOCR_01
│   ├── MC_01                             ← MC1 = 첫 번째 전자 접촉기
│   ├── MC_02                             ← MC2 = 두 번째
│   ├── FuseHolder_01
│   ├── Fuse_01, Fuse_02
│   ├── TB10_01                           ← 10핀 TB
│   ├── TB8_01                            ← 회로도상 TB5
│   ├── TB12_01                           ← 회로도상 TB6
│   ├── Timer_01                          ← 회로도 T
│   ├── Flicker_01                        ← 회로도 FR
│   ├── FLS_01
│   └── Relay_01 ~ Relay_NN
│
├── ControlBox                            ← 2구 컨트롤박스 + 푸쉬버튼·셀렉터·램프
│   ├── ControlBox_01
│   ├── PushBtn_Red_01, PushBtn_Green_01, PushBtn_Blue_01
│   ├── SelectorSw_A_01, SelectorSw_B_01
│   ├── PilotLamp_Red_01, PilotLamp_Green_01, PilotLamp_Yellow_01, PilotLamp_White_01
│   └── Buzzer_01
│
├── Conduit                               ← 배관 시스템 (Stage 2)
│   ├── PipePE_01 ~ PipePE_NN
│   ├── PipeCD_01 ~ PipeCD_NN
│   ├── Saddle_S_01 ~ , Saddle_L_01 ~
│   ├── Connector_PE_01 ~ , Connector_CD_01 ~
│   └── CableGland_01 ~
│
├── MainCircuit                           ← 주회로 22선 (Stage 3)
│   ├── WireM_01_GY                       ← TB5_10 → TB6_10  (녹-황 접지)
│   ├── WireM_02_GY                       ← TB6_10 → TB6_18  (녹-황 접지)
│   ├── WireM_03_Br                       ← TB5_7 → MCCB_In_Br
│   └── ... WireM_22_Gr
│
├── AuxCircuit                            ← 보조회로 39선
│   ├── WireA_01                          ← 퓨즈홀더_갈 → EOCR_12
│   └── ... WireA_39
│
├── Tools                                 ← 인벤토리 도구
│   ├── BellTester_01
│   ├── Drill_01, Stripper_01, PipeCutter_01
│   └── Ruler_01, Chalk_01, MaskingTape_01, Screw_01...
│
└── Materials                             ← (선택) 8각 박스 등 부재
    ├── Box_Octagon_01
    └── CableCV_01'''
s = f'''
<h1>전체 씬 트리 구조 (인스턴스 위계)</h1>
<p class="subtitle">부모 노드가 카테고리를 표현 — 자식 인스턴스명은 짧게 유지. AI 가 트리 컨텍스트로 의미 합성 가능.</p>
<div class="tree">{escape(tree)}</div>
'''
slides_html.append(make_slide(len(slides_html) + 1, s))


# ─── Slide — 머티리얼 명명 ───────────────────────────────────
mat_rows = [
    ("Wire_Br_v01.glb", "mat_wire_brown", "갈색 전선 머티리얼 (단색 또는 albedo 텍스처)"),
    ("Wire_Bk_v01.glb", "mat_wire_black", "흑색 전선"),
    ("Wire_Gr_v01.glb", "mat_wire_gray", "회색 전선"),
    ("Wire_GY_v01.glb", "mat_wire_greenyellow", "녹-황 접지선 (이중색)"),
    ("Wire_Yl_v01.glb", "mat_wire_yellow", "황색 전선"),
    ("MCCB_v01.glb", "mat_mccb_body", "MCCB 본체 (검정 플라스틱)"),
    ("MCCB_v01.glb", "mat_mccb_lever", "MCCB 레버 (적색)"),
    ("PushBtn_Red_v01.glb", "mat_pushbtn_red", "푸쉬버튼 적색 머티리얼"),
    ("PilotLamp_Yellow_v01.glb", "mat_pilotlamp_yellow", "황색 램프 (반투명 + 발광)"),
]
rows = "".join(f'<tr><td class="mono">{s}</td><td class="mono">{m}</td><td>{d}</td></tr>' for s, m, d in mat_rows)
s = f'''
<h1>머티리얼 명명 (T3 — 자동 파생)</h1>
<p class="subtitle">사용자가 직접 명명하지 않음 — 시스템이 사용 노드 분석으로 자동 생성. lower_snake_case + <span class="mono">mat_</span> 약자 유지.</p>
<table>
<tr><th>원본 에셋 (T1)</th><th>머티리얼 이름 <span class="tag-T3">T3</span></th><th>설명</th></tr>
{rows}
</table>

<h3>채널별 텍스처 (필요 시)</h3>
<div class="tree">mat_mccb_body
├── tex_mccb_body_albedo       ← 기본 색상
├── tex_mccb_body_normal       ← 표면 굴곡
├── tex_mccb_body_roughness    ← 거칠기
└── tex_mccb_body_metallic     ← 금속성</div>

<div class="note">
  사용자는 머티리얼 패널에서만 가끔 확인 — Make Editor 씬 트리에는 직접 노출되지 않음.<br>
  AI·로그가 단독 노출하므로 <span class="mono">mat_</span> 약자 유지가 가독성·검색 효율에 유리.
</div>
'''
slides_html.append(make_slide(len(slides_html) + 1, s))


# ─── Slide — 검증 체크리스트 ──────────────────────────────────
checks_t1 = [
    "모든 원본 .glb 가 PascalCase + _v<NN> 형식",
    "전선은 색상별 5개 파일 (Wire_Br/Bk/Gr/GY/Yl_v01.glb)",
    "기구는 카테고리별 슬라이드의 원본 에셋명 표 기준",
    "한글 파일명 0건",
    "공백·하이픈 0건",
]
checks_t2 = [
    "Make Editor 인스턴스에 종류 약자 (mdl_/img_) 0건",
    "주회로 22선이 WireM_NN_<Color> 패턴",
    "보조회로 39선이 WireA_NN 패턴",
    "기구 인스턴스는 <원본명>_01, _02 ... 순차 번호",
    "부모 노드(ControlPanel/MainCircuit/AuxCircuit/...) 가 카테고리 표현",
    "이름 끝에 확장자 (.glb 등) 박제 0건",
]
checks_t3 = [
    "머티리얼 이름이 mat_<asset>_<part> 패턴",
    "(Instance) 사슬 0건",
    "텍스처 채널 약자 (_albedo/_normal/...) 명시",
]
checks_anim = [
    "버튼 누를 때 효과 애니메이션이 <Target>_<Act>[_<Dir>] 패턴",
    "예: PushBtn_Red_Pop (눌릴 때 바운스), PilotLamp_Yellow_FI (켜질 때 페이드인)",
    "Unity 'new Clip' 패턴 0건",
]

def render_checks(items):
    return "<ul class='checklist'>" + "".join(f"<li>{escape(x)}</li>" for x in items) + "</ul>"

s = f'''
<h1>검증 체크리스트</h1>
<div class="cols2">
  <div>
    <h2>T1 — 원본 파일</h2>
    {render_checks(checks_t1)}
    <h2>T2 — Make Editor 인스턴스</h2>
    {render_checks(checks_t2)}
  </div>
  <div>
    <h2>T3 — 자동 생성 (머티리얼)</h2>
    {render_checks(checks_t3)}
    <h2>애니메이션</h2>
    {render_checks(checks_anim)}
    <div class="note">
      체크리스트 상세는 <span class="mono">doc/assets/MakeNamingConvention_v6.xlsx</span> 의 Checklist 시트 참고.
    </div>
  </div>
</div>
'''
slides_html.append(make_slide(len(slides_html) + 1, s))


# ─── Slide — 변환 사유 + 다음 단계 ────────────────────────────
s = f'''
<h1>변환 사유 요약 + 다음 단계</h1>

<h2>왜 이 명명 규칙이 합리적인가</h2>
<table>
<tr><th>고려 사항</th><th>적용된 결정</th></tr>
<tr><td>회로도와 직접 대조 필요</td><td>주회로 인스턴스에 색상 약자 포함 → <span class="mono">WireM_03_Br</span> 만 봐도 회로도 라인 3번 갈색임을 식별</td></tr>
<tr><td>513 노드 규모 대비 가독성</td><td>부모 노드로 카테고리 그룹핑 (<span class="mono">MainCircuit/...</span>) → 자식은 짧게 (<span class="mono">WireM_01_GY</span>)</td></tr>
<tr><td>모델러·기획자 협업</td><td>T1 원본명 = PascalCase + 영문 (모델러 도구 친화). T2 인스턴스 = 동일 PascalCase (학습 비용 0)</td></tr>
<tr><td>AI 보조 편집</td><td>씬 트리 + 인스턴스명 조합으로 출발·도착 의미 완결. 추가 VNT 컴포넌트 필드로 정밀 결선 정보</td></tr>
<tr><td>11개 Contents 페이지 (Stage1~3)</td><td>각 페이지에서 동일 모델 재사용 — <span class="mono">_01, _02, _03</span> 순차 번호로 인스턴스 구별</td></tr>
</table>

<h2>다음 단계 권장</h2>
<ol>
<li><b>모델러 발주</b>: 카테고리별 슬라이드의 T1 원본명 표 기준으로 .glb 작업 의뢰</li>
<li><b>전선 5종 우선</b>: <span class="mono">Wire_Br/Bk/Gr/GY/Yl_v01.glb</span> 부터 제작 — 주회로·보조회로 양쪽 공통</li>
<li><b>GLOSSARY 등록</b>: 한국어 기획서 용어 → 영문 슬러그 매핑을 <span class="mono">doc/GLOSSARY.md</span> 에 추가 (예: 단자대 → TB, 차단기 → MCCB)</li>
<li><b>VNT 컴포넌트 설계</b>: 전선 인스턴스에 <span class="mono">FromNodeId/ToNodeId</span> 필드 정의 — 결선 정보를 이름 외부에 보존</li>
<li><b>임포트 검증 스크립트</b>: <span class="mono">scripts/validate-make-names.py</span> 작성 — 본 문서의 체크리스트 자동 검사</li>
</ol>

<div class="note">
  본 가이드는 기획서 v1.1 기준. PPTX 갱신 시 <span class="mono">scripts/build_wiring_naming_html.py</span> 의 데이터 표 갱신 후 재생성.
</div>
'''
slides_html.append(make_slide(len(slides_html) + 1, s))


# ─────────────────────────────────────────────────────────────────
# Assemble
# ─────────────────────────────────────────────────────────────────
total = len(slides_html)
deck = "\n".join(slides_html).replace(total_slides_placeholder, str(total))

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>전기내선공사 가상 실습 — 네이밍 가이드 (v6)</title>
<style>{CSS}</style>
</head>
<body>
<div class="deck">
{deck}
</div>
<div class="nav">← → 또는 PgUp/PgDn · <span id="pgnum">1 / {total}</span></div>
<script>{JS}</script>
</body>
</html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT} ({len(html):,} bytes, {total} slides)")
