"""Build Slide 21 sprite asset analysis HTML (v2 — Revised).

Output: doc/assets/SpriteAssetAnalysis_S21_Sample.html

v2 정정:
- 도면 (Diagram popup) 및 인벤토리 (Inventory) 자산을 슬라이드 21 에서 제거
- 슬라이드 21 의 Description 표에 명시된 항목 + [공통] 라벨이 붙은 동작만 자산으로 인정
- 착각 원인 분석 + 해결 방안 섹션 추가
- 사용 / 미사용 자산 매트릭스 추가
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "doc" / "assets" / "SpriteAssetAnalysis_S21_Sample.html"

# ─────────────────────────────────────────────────────────────────
# 슬라이드 21 에 실제 표시되는 자산 (Description 표 + [공통] 라벨 동작 + 슬라이드 메타데이터)
# ─────────────────────────────────────────────────────────────────
SLIDE21_USED = [
    # ── 슬라이드 메타데이터 (모든 슬라이드 공통, 슬라이드 마스터 차원)
    ("SP_HDR_001", "메타", "상단 (z=5)", "상단 헤더 패널",
     "Pnl_Header_Sprite_v01.png", "PnlHeader", "단일",
     "슬라이드 마스터 차원의 진행 단계 띠 배경. 슬라이드 21 화면 상단에 \"주회로 넘버링 - EOCR\" 텍스트와 함께 표시"),
    ("SP_HDR_002", "메타", "상단 (z=5)", "진행 단계 이름 라벨",
     "Lbl_StepName_Sprite_v01.png", "LblStepName", "단일",
     "단계 이름 텍스트 박스 (텍스트는 슬라이드별 동적)"),
    ("SP_LNB_001", "메타", "좌측 (z=2)", "LNB 메뉴 패널 배경",
     "Pnl_LNB_Sprite_v01.png", "PnlLNB", "단일",
     "슬라이드 21 좌측에 \"1. 제어판 작업 – 1. 회로도 넘버링 - 주회로\" 위치 표시"),
    ("SP_LNB_002", "메타", "좌측 (z=2)", "LNB 1-depth 아이템",
     "ItemLNB1_Sprite_Def_v01.png / ItemLNB1_Sprite_On_v01.png",
     "ItemLNB1_Def · ItemLNB1_On", "Def · On",
     "Stage 1·2·3 메뉴 (현재 Stage 1 Active)"),
    ("SP_LNB_003", "메타", "좌측 (z=2)", "LNB 2-depth 아이템",
     "ItemLNB2_Sprite_Def_v01.png / ItemLNB2_Sprite_On_v01.png",
     "ItemLNB2_Def · ItemLNB2_On", "Def · On",
     "들여쓰기 된 2차 메뉴 (\"1. 회로도 넘버링\" Active)"),
    ("SP_LNB_004", "메타", "좌측 (z=2)", "LNB 드롭다운 화살표",
     "Ico_LNBArrow_Sprite_v01.png", "IcoLNBArrow", "Closed · Open (회전)",
     "드롭다운 펼침/접힘 표시"),
    ("SP_FTR_001", "메타", "하단 (z=4)", "자막 영역 배경",
     "Pnl_Caption_Sprite_v01.png", "PnlCaption", "단일",
     "슬라이드 21 자막 \"회로도에 순차적으로 넘버링을 해줍니다.\" 표시 영역"),
    ("SP_FTR_002", "메타", "하단", "페이지 번호 라벨",
     "Lbl_PageNum_Sprite_v01.png", "LblPageNum", "단일",
     "슬라이드 21 페이지 번호 \"001\" 표시"),

    # ── User Scenario 의 [공통] Nav 동작 — 〈 〉 버튼
    ("SP_NAV_001", "[공통]Nav", "하단 (z=4)", "이전 버튼 〈",
     "Btn_NavPrev_Sprite_Def_v01.png / Btn_NavPrev_Sprite_Prs_v01.png",
     "BtnNavPrev_Def · _Prs", "Def · Prs",
     "이전 단계로 강제 이동 ([공통]Nav)"),
    ("SP_NAV_002", "[공통]Nav", "하단 (z=4)", "다음 버튼 〉",
     "Btn_NavNext_Sprite_Off_v01.png / Btn_NavNext_Sprite_On_v01.png / Btn_NavNext_Sprite_Prs_v01.png",
     "BtnNavNext_Off · _On · _Prs", "Off · On · Prs",
     "슬라이드 21 진입 시 Off (EOCR 클릭 전), 클릭 후 On 전환"),

    # ── User Scenario 의 [공통] View 동작 — 확대/축소 버튼
    ("SP_ZOOM_001", "[공통]View", "중앙 (z=1)", "작업공간 줌인 버튼",
     "Btn_WorkZoomIn_Sprite_Def_v01.png / Btn_WorkZoomIn_Sprite_Prs_v01.png",
     "BtnWorkZoomIn_Def · _Prs", "Def · Prs",
     "회로도 배율 증가 (100~300% 단계, 기본 200%)"),
    ("SP_ZOOM_002", "[공통]View", "중앙 (z=1)", "작업공간 줌아웃 버튼",
     "Btn_WorkZoomOut_Sprite_Def_v01.png / Btn_WorkZoomOut_Sprite_Prs_v01.png",
     "BtnWorkZoomOut_Def · _Prs", "Def · Prs",
     "회로도 배율 감소"),
    ("SP_ZOOM_003", "[공통]View", "중앙", "줌 배율 라벨",
     "Lbl_ZoomScale_Sprite_v01.png", "LblZoomScale", "단일",
     "현재 배율 텍스트 박스 (\"200%\" 등)"),

    # ── 슬라이드 21 Description 표의 #1 — 회로도 배경
    ("SP_DIAG_S21_001", "S21 전용", "중앙 (z=1)", "주회로 회로도 전체",
     "Bg_DiagMain_Sprite_v01.png", "BgDiagMain", "단일",
     "Description #1. 기본 배율 200%, 드래그 가능. 주회로 작업용 회로도"),
    ("SP_DIAG_S21_002", "S21 전용", "중앙 (z=1)", "주회로 외 영역 마스크 오버레이",
     "Bg_DiagMainMask_Sprite_v01.png", "BgDiagMainMask", "단일",
     "Description #1. 주회로 영역 외 나머지 투명도 처리 (alpha 채널 마스크)"),

    # ── 슬라이드 21 Description 표의 #2 — 클릭 유도 포인팅
    ("SP_PTR_001", "S21 전용", "중앙 (z=1)", "클릭 유도 포인팅 - 펄스 링",
     "Ani_ClickPulse_Sprite_v01.png", "AniClickPulse",
     "프레임 시트 또는 CSS Ani",
     "Description #2. EOCR 위치에 표시되는 클릭 유도 펄스 애니메이션"),
    ("SP_PTR_002", "S21 전용", "중앙 (z=1)", "클릭 유도 포인팅 - 손가락 아이콘",
     "Ico_ClickHand_Sprite_v01.png", "IcoClickHand", "단일",
     "Description #2. 펄스 링과 함께 표시되는 손가락 아이콘 (선택)"),
    ("SP_PTR_003", "S21 전용", "중앙 (z=1)", "위치 인디케이터",
     "Ico_LocIndicator_Sprite_v01.png", "IcoLocIndicator", "단일 (4방향 회전)",
     "Description #2. 포인팅 영역이 화면 밖으로 나갔을 때 가장자리에 표시"),
    ("SP_HL_001", "S21 전용", "중앙 (z=1)", "EOCR 클릭 영역 하이라이트",
     "Ico_HotspotHL_Sprite_v01.png", "IcoHotspotHL", "단일",
     "Main Task. EOCR 부품 위치의 클릭 가능 영역 강조 (반투명 외곽선·글로우)"),
]

# ─────────────────────────────────────────────────────────────────
# 슬라이드 21 에 미표시 (v1 에서 잘못 포함했던 자산)
# ─────────────────────────────────────────────────────────────────
SLIDE21_UNUSED = [
    ("SP_INV_001", "도면·인벤토리", "우측 (z=3)", "우측 아이템 패널 배경",
     "도구 사용 단계가 아님. 슬라이드 18 정의: \"제어판 작업에 사용되는 도구 버튼 제공\" — 21번은 단순 클릭 입력만"),
    ("SP_INV_002", "도면·인벤토리", "우측 (z=2)", "도면 팝업 배경",
     "슬라이드 18 정의: \"제어판 작업 시 우측 상단에 팝업 형태\" — 21번 Description 에 명시 없음"),
    ("SP_INV_003", "도면·인벤토리", "우측", "도면 확대 버튼",
     "도면 미표시이므로 부수 자산도 미사용"),
    ("SP_INV_004", "도면·인벤토리", "우측", "도면 축소 버튼",
     "동일"),
    ("SP_INV_005", "도면·인벤토리", "우측", "도면 닫기 버튼",
     "동일"),
    ("SP_NUM_001", "S23~ 자산", "중앙", "회로도 넘버링 라벨",
     "21번은 EOCR 클릭만 — 넘버링 생성은 슬라이드 23 부터 시작"),
    ("SP_CUR_001", "보조", "전역", "드래그 커서 가이드",
     "슬라이드 21 Description 에 명시 없음 — 보수적으로 미사용 분류"),
]

# 슬라이드별 사용 매트릭스 (S21~S28, 자산별)
# True = 사용, False = 미사용, "?" = 추정 (재분석 필요)
USE_MATRIX = {
    # asset_id: {S21, S22, S23, S24, S25, S26, S27, S28}
    "SP_HDR_001":  ["✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"],
    "SP_HDR_002":  ["✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"],
    "SP_LNB_001":  ["✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"],
    "SP_LNB_002":  ["✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"],
    "SP_LNB_003":  ["✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"],
    "SP_FTR_001":  ["✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"],
    "SP_FTR_002":  ["✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"],
    "SP_NAV_001":  ["✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"],
    "SP_NAV_002":  ["✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"],
    "SP_ZOOM_001": ["✓", "?", "?", "?", "?", "?", "?", "?"],
    "SP_ZOOM_002": ["✓", "?", "?", "?", "?", "?", "?", "?"],
    "SP_DIAG_S21_001": ["✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"],
    "SP_DIAG_S21_002": ["✓", "?", "?", "?", "?", "?", "?", "—"],
    "SP_PTR_001":  ["✓", "✓", "?", "✓", "✓", "?", "—", "—"],
    "SP_PTR_002":  ["✓", "?", "?", "?", "?", "?", "—", "—"],
    "SP_PTR_003":  ["✓", "?", "?", "?", "?", "?", "?", "?"],
    "SP_HL_001":   ["✓", "—", "—", "—", "—", "—", "—", "—"],  # EOCR HL — S21 만
    "SP_INV_001":  ["—", "?", "?", "?", "?", "?", "?", "?"],
    "SP_INV_002":  ["—", "✓", "—", "✓", "—", "—", "—", "—"],  # 부품 결선도 팝업 = S22, S25
    "SP_NUM_001":  ["—", "—", "✓", "—", "—", "✓", "✓", "✓"],  # 넘버링 생성 = S23, S26, S27, S28
}


# ─────────────────────────────────────────────────────────────────
# HTML
# ─────────────────────────────────────────────────────────────────

CSS = """
* { box-sizing: border-box; }
html, body {
  margin: 0; padding: 0;
  font-family: 'Malgun Gothic', '맑은 고딕', system-ui, sans-serif;
  background: #2b2b2b; color: #222;
}
.deck { padding: 24px; }
.slide {
  max-width: 1280px;
  margin: 24px auto;
  background: #fff;
  padding: 40px 56px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.35);
  page-break-after: always;
  break-after: page;
}
h1 {
  margin: 0 0 12px 0;
  font-size: 30px;
  color: #1f3864;
  border-bottom: 3px solid #2f5496;
  padding-bottom: 10px;
}
h2 {
  margin: 22px 0 8px 0;
  font-size: 20px;
  color: #2f5496;
}
h3 { font-size: 16px; color: #1f3864; margin: 14px 0 6px; }
p, li { font-size: 14px; line-height: 1.55; }
.subtitle { color: #595959; font-size: 15px; margin-top: -4px; }
.meta { color: #777; font-size: 13px; }
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  margin: 8px 0 18px 0;
}
th {
  background: #2f5496; color: #fff;
  padding: 7px 10px; text-align: left; font-weight: 600;
}
td {
  padding: 7px 10px; border-bottom: 1px solid #d9d9d9;
  vertical-align: top;
}
tr:nth-child(even) td { background: #f4f6fa; }
.mono { font-family: 'Consolas', 'D2Coding', monospace; font-size: 12px; }
.tag {
  padding: 2px 8px; border-radius: 10px;
  font-size: 11px; font-weight: 600; white-space: nowrap;
}
.tag-meta   { background: #d9e1f2; color: #1f3864; }
.tag-com    { background: #c5e0b4; color: #385723; }
.tag-s21    { background: #f8cbad; color: #843c0c; }
.tag-state  { background: #bdd7ee; color: #1f3864; }
.tag-unused { background: #d9d9d9; color: #595959; }
.note {
  background: #fff2cc; border-left: 4px solid #ffc000;
  padding: 12px 16px; font-size: 13px; margin: 12px 0;
  color: #5a4500;
}
.alert {
  background: #fbe5d6; border-left: 4px solid #c00000;
  padding: 14px 18px; font-size: 14px; margin: 12px 0;
  color: #843c0c;
}
.alert b { color: #c00000; }
.cover { text-align: center; padding: 100px 0; }
.cover h1 { font-size: 36px; border: 0; }
.cover .sub { color: #5a5a5a; font-size: 18px; margin: 8px 0; }
.banner {
  background: #ffe699; border: 2px solid #ffc000;
  padding: 10px 16px; margin: 16px 0; font-size: 14px;
  border-radius: 6px;
}

/* 화면 mockup */
.mockup {
  position: relative;
  width: 100%;
  height: 460px;
  background: #f0f0f0;
  border: 2px solid #999;
  margin: 14px 0 18px;
  font-size: 11px;
  border-radius: 4px;
}
.area {
  position: absolute;
  border: 1.5px dashed #2f5496;
  background: rgba(189, 215, 238, 0.35);
  padding: 6px 8px;
  color: #1f3864;
  font-weight: 600;
  display: flex; flex-direction: column;
}
.area.unused {
  border: 1.5px dashed #999;
  background: rgba(217, 217, 217, 0.4);
  color: #888;
  text-decoration: line-through;
}
.area .label { font-size: 11px; }
.area .ids { font-size: 10px; color: #595959; font-weight: 400; margin-top: 4px; font-family: 'Consolas', monospace; text-decoration: none; }

.area-header { top: 0; left: 0; right: 0; height: 50px; background: rgba(46,84,150,0.18); }
.area-lnb { top: 50px; left: 0; bottom: 60px; width: 200px; background: rgba(46,84,150,0.10); }
.area-inv-top { top: 50px; right: 0; width: 240px; height: 200px; }
.area-inv-bot { top: 250px; right: 0; bottom: 60px; width: 240px; }
.area-center { top: 50px; left: 200px; right: 0; bottom: 60px; background: rgba(112,173,71,0.10); border-color: #548235; }
.area-footer { bottom: 0; left: 0; right: 0; height: 60px; background: rgba(46,84,150,0.15); }

.mockup .marker {
  position: absolute;
  background: #c00; color: #fff;
  width: 22px; height: 22px; border-radius: 50%;
  font-size: 11px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 0 2px #fff, 0 2px 6px rgba(0,0,0,0.3);
}
.mockup .ptr { top: 50%; left: 45%; }
.mockup .ind { top: 55%; right: 20px; transform: translateY(-50%); background: #ff8c00; }

.matrix table { font-size: 11px; }
.matrix th, .matrix td { text-align: center; padding: 5px 6px; }
.matrix td:first-child, .matrix th:first-child { text-align: left; min-width: 140px; }
.matrix td:nth-child(2), .matrix th:nth-child(2) { text-align: left; min-width: 160px; }
.cell-y { background: #c5e0b4; color: #385723; font-weight: 700; }
.cell-n { background: #fbe5d6; color: #843c0c; }
.cell-q { background: #fff2cc; color: #5a4500; }

.diff-table th { background: #c00; }
.diff-add { background: #c5e0b4; color: #385723; }
.diff-del { background: #fbe5d6; color: #843c0c; text-decoration: line-through; }
.diff-keep { background: #f4f6fa; color: #595959; }

ul.cause li, ul.fix li { margin: 8px 0; padding-left: 4px; font-size: 14px; line-height: 1.6; }
ul.fix { counter-reset: f; list-style: none; padding-left: 0; }
ul.fix li { padding-left: 36px; position: relative; }
ul.fix li::before {
  counter-increment: f; content: counter(f);
  position: absolute; left: 0; top: 0;
  background: #2f5496; color: #fff;
  width: 26px; height: 26px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 13px;
}
@media print {
  body { background: #fff; }
  .slide { box-shadow: none; margin: 0; }
}
"""


def tag_class(cat):
    if cat == "메타": return "tag-meta"
    if cat.startswith("[공통]"): return "tag-com"
    if cat == "S21 전용": return "tag-s21"
    return "tag-state"


def row_html(asset):
    aid, cat, area, ko, src, inst, state, desc = asset
    cls = tag_class(cat)
    return (f"<tr>"
            f"<td class='mono'><b>{aid}</b></td>"
            f"<td><span class='tag {cls}'>{escape(cat)}</span></td>"
            f"<td>{escape(area)}</td>"
            f"<td>{escape(ko)}</td>"
            f"<td class='mono'>{escape(src)}</td>"
            f"<td class='mono'>{escape(inst)}</td>"
            f"<td><span class='tag tag-state'>{escape(state)}</span></td>"
            f"<td>{escape(desc)}</td>"
            f"</tr>")


used_rows = "\n".join(row_html(a) for a in SLIDE21_USED)
unused_rows = "\n".join(
    f"<tr>"
    f"<td class='mono'><b>{aid}</b></td>"
    f"<td><span class='tag tag-unused'>{escape(cat)}</span></td>"
    f"<td>{escape(area)}</td>"
    f"<td>{escape(ko)}</td>"
    f"<td>{escape(reason)}</td>"
    f"</tr>"
    for aid, cat, area, ko, reason in SLIDE21_UNUSED
)

# ─── Cover ──────────────────────────────────────────────────
cover = '''
<section class="slide">
<div class="cover">
  <h1>2D 스프라이트 자산 분석</h1>
  <div class="sub" style="font-size:22px; color:#1f3864; font-weight:600;">슬라이드 21 — 주회로 넘버링 (EOCR)</div>
  <div class="sub" style="color:#c00; font-weight:700; margin-top:18px;">v2 — Revised (도면·인벤토리 미사용으로 정정)</div>
  <div class="meta" style="margin-top:50px;">
    원본: [폴리텍신기술교육원]_전기내선공사 가상 실습_SB_v1.0.pptx<br>
    명명 규칙: Make Asset Naming Convention v6<br>
    작성일: 2026-05-13
  </div>
</div>
</section>
'''

# ─── v1 → v2 변경 사항 알림 ─────────────────────────────────
diff_section = '''
<section class="slide">
<h1>v1 → v2 변경 사항</h1>

<div class="alert">
  <b>v1 의 오류</b>: 슬라이드 21 에 도면 (Diagram popup) 과 인벤토리 (Inventory) 자산을 공통 UI 로 잘못 포함시켰습니다. 사용자 지적에 따라 슬라이드 21 Description 표 + User Scenario 의 [공통] 라벨을 다시 정확히 확인한 결과, 해당 자산들은 슬라이드 21 에서 표시되지 않음을 확인했습니다.
</div>

<table class="diff-table">
<tr><th>구분</th><th>v1 (오류)</th><th>v2 (정정)</th></tr>
<tr><td>SP_INV_001 (인벤토리 패널)</td><td class="diff-del">슬라이드 21 사용</td><td class="diff-add">미사용 — 21번은 도구 사용 없음</td></tr>
<tr><td>SP_INV_002 (도면 팝업 배경)</td><td class="diff-del">슬라이드 21 사용</td><td class="diff-add">미사용 — Description 에 명시 없음</td></tr>
<tr><td>SP_INV_003/004/005 (도면 줌·닫기)</td><td class="diff-del">슬라이드 21 사용</td><td class="diff-add">미사용 — 도면 자체가 없음</td></tr>
<tr><td>SP_NUM_001 (넘버링 라벨)</td><td class="diff-del">슬라이드 21 사용</td><td class="diff-add">미사용 — 넘버링은 S23~ 부터</td></tr>
<tr><td>SP_CUR_001 (드래그 가이드)</td><td class="diff-del">슬라이드 21 사용</td><td class="diff-add">미사용 — 명시 없음</td></tr>
<tr><td>공통 UI 자산 그룹 수</td><td class="diff-del">19 그룹</td><td class="diff-add">13 그룹 (메타 8 + [공통] 5)</td></tr>
<tr><td>S21 전용 자산 그룹 수</td><td class="diff-keep">7 그룹 (변경 없음)</td><td class="diff-keep">6 그룹 (HL_001 만, 나머지 동일)</td></tr>
<tr><td>슬라이드 21 자산 합계</td><td class="diff-del">26 그룹</td><td class="diff-add">19 그룹</td></tr>
</table>
</section>
'''

# ─── 착각 원인 분석 ────────────────────────────────────────
cause_section = '''
<section class="slide">
<h1>착각 원인 분석</h1>
<p class="subtitle">왜 v1 에서 도면·인벤토리를 슬라이드 21 자산에 포함시켰는가? — 4가지 원인.</p>

<ul class="cause">
  <li>
    <b>1. 공통 사양 = "항상 표시" 로 오인 (구조 인식 오류)</b><br>
    슬라이드 18 (화면 영역 정의) 의 5개 영역 — 중앙·좌·우·하단·상단 — 을 "팔레트" (각 슬라이드가 골라 쓰는 모음) 가 아니라 "프레임" (모든 슬라이드에 고정 표시) 으로 잘못 해석. <span class="mono">우측 영역: "1. 도면 - 제어판 작업 시... 2. 아이템 - 제어판 작업에 사용되는 도구 버튼"</span> 의 <b>"제어판 작업 시"</b> 조건절을 간과.
  </li>
  <li>
    <b>2. 슬라이드 21 의 Description 표 미정독 (입력 검증 누락)</b><br>
    슬라이드 21 Description 표는 <b>딱 2개 항목만</b> 명시: ① 회로도 배경 ② 클릭 유도 포인팅. 그 외 도면·인벤토리·자막·헤더는 어디에도 언급 없음. v1 작성 시 이 표를 truth-source 로 삼지 않고, 슬라이드 17·18 의 전체 layout 스케치에 의존.
  </li>
  <li>
    <b>3. [공통] 라벨 의미 오해</b><br>
    User Scenario 의 <span class="mono">"2. [공통]화면 제어(View) ... 3. [공통]내비게이션(Nav)"</span> 표기는 <b>"동작"</b> (드래그·줌·〈〉) 에 한해 공통임을 의미. v1 은 이를 "공통 UI 자산은 항상 표시" 로 확대 해석. 도면·인벤토리에는 [공통] 라벨이 붙어 있지 않음.
  </li>
  <li>
    <b>4. UX 상식 부재 — 단순 클릭 입력 단계에 도구 패널 불필요</b><br>
    슬라이드 21 의 Main Task 는 "EOCR 클릭 → 다음 슬라이드 이동" — 단일 클릭 입력. 도구 박스나 도면 참고가 필요한 단계가 아님. UX 흐름을 고려했으면 자연스럽게 "이 단계엔 도구가 필요 없다" 추론 가능했음.
  </li>
</ul>

<div class="note">
  <b>요약</b>: 원인은 (1) 구조 인식 오류 + (2) 입력 검증 누락 + (3) 라벨 해석 실수 + (4) UX 추론 미흡 의 복합. 가장 큰 원인은 (1)·(2) 의 "공통 사양 = 항상 표시" 오인.
</div>
</section>
'''

# ─── 해결 방안 ─────────────────────────────────────────────
fix_section = '''
<section class="slide">
<h1>해결 방안 — 슬라이드 분석 프로세스 개선</h1>

<ul class="fix">
  <li>
    <b>각 슬라이드의 Description 표를 1차 truth-source 로 삼는다</b><br>
    슬라이드별 Description 표에 <b>명시된 항목만</b> "이 슬라이드에 표시되는 자산". 슬라이드 17·18 의 전체 layout 정의는 "사용 가능한 자산 풀" 일 뿐, 자동 포함 아님.
  </li>
  <li>
    <b>User Scenario 의 [공통] 라벨을 정확히 추출</b><br>
    각 슬라이드의 User Scenario 에서 <b>[공통] 라벨이 붙은 동작</b> 만 공통 UI 자산을 자동 호출. (예: [공통]View → ZOOM 자산, [공통]Nav → NAV 자산). [공통] 라벨 없는 영역은 슬라이드별 명시 필요.
  </li>
  <li>
    <b>슬라이드 메타데이터 vs Description 항목 분리</b><br>
    "헤더 (단계 이름), LNB, 자막, 페이지 번호" 는 PPTX 슬라이드 마스터 차원의 메타데이터로, Description 에 명시 안 되어도 표시되는 슬라이드 마스터 자산. 이는 별도 카테고리 (<span class="tag tag-meta">메타</span>) 로 분류.
  </li>
  <li>
    <b>사용 / 미사용 양쪽 자산을 표에 명시</b><br>
    "이 슬라이드에 사용되는 자산" 만 적지 말고, "전체 자산 풀 중 이 슬라이드에서 미사용인 자산" 도 함께 명시. 미사용 사유까지 적어 인계 시 오해 방지.
  </li>
  <li>
    <b>슬라이드 × 자산 매트릭스 도입</b><br>
    S21~S28 한 번에 분석할 때, 행=자산 / 열=슬라이드 매트릭스로 한눈에 어느 슬라이드에 어느 자산이 보이는지 추적. 추정 셀은 <span class="tag" style="background:#fff2cc;color:#5a4500;">?</span> 마크로 재분석 필요 명시.
  </li>
  <li>
    <b>UX 흐름 추론을 검증 단계로 추가</b><br>
    Description + [공통] 라벨로 1차 자산 목록을 만든 후, "이 단계의 Main Task 가 이 자산을 필요로 하는가?" UX 관점에서 한 번 더 검증. 단순 클릭 단계엔 도구·인벤토리 불필요.
  </li>
</ul>
</section>
'''

# ─── 슬라이드 21 정확 개요 ───────────────────────────────────
overview_section = '''
<section class="slide">
<h1>슬라이드 21 — 정확 개요 (Description 기반)</h1>

<table>
<tr><th style="width:140px;">항목</th><th>내용</th></tr>
<tr><td>제목</td><td>주회로 넘버링 - EOCR</td></tr>
<tr><td>단계</td><td>Stage 1. 제어판 작업 → 1. 회로도 넘버링 → 주회로</td></tr>
<tr><td>페이지 번호</td><td>001</td></tr>
<tr><td>자막</td><td>회로도에 순차적으로 넘버링을 해줍니다.</td></tr>
</table>

<h2>Description 표 (자산 truth-source) — 2개 항목</h2>
<table>
<tr><th style="width:50px;">No</th><th style="width:180px;">제목</th><th>요구사항</th></tr>
<tr><td>1</td><td>회로도 배경</td><td>이미지 기본 배율 200% / 주회로 영역 외 나머지는 투명도 처리 / 마우스 드래그로 화면 이동 가능</td></tr>
<tr><td>2</td><td>클릭 유도 포인팅</td><td>클릭 해야 하는 부분 포인팅 Ani / 클릭 시 다음 화면으로 이동 / 해당 영역이 화면 밖으로 나가면 인디케이터로 위치 안내</td></tr>
</table>

<h2>User Scenario</h2>
<table>
<tr><th style="width:80px;">라벨</th><th>동작</th></tr>
<tr><td><b>Main Task</b></td><td>회로도 내 <b>EOCR</b> 클릭 → "부품 내부 결선도 팝업" 호출하며 다음 슬라이드로 이동</td></tr>
<tr><td><span class="tag tag-com">[공통]View</span></td><td>회로도 배경 드래그 시 상하좌우 이동, 확대/축소 버튼으로 배율 조절</td></tr>
<tr><td><span class="tag tag-com">[공통]Nav</span></td><td>하단 화살표(〈, 〉) 클릭 시 이전/다음 단계로 강제 이동</td></tr>
</table>

<div class="banner">
  <b>핵심</b>: 슬라이드 21 에서 "표시되는 자산" 은 (i) Description 표 2개 항목 + (ii) [공통] 라벨 동작 (View·Nav) + (iii) 슬라이드 메타데이터 (헤더·LNB·자막·페이지#). <b>도면·인벤토리는 명시 없음 → 미사용</b>.
</div>
</section>
'''

# ─── 화면 mockup (수정) ───────────────────────────────────
mockup_section = '''
<section class="slide">
<h1>화면 영역 매핑 — v2 정정</h1>
<p class="subtitle">우측 영역(도면·인벤토리) 회색 처리 = 슬라이드 21 에서 미사용.</p>

<div class="mockup">
  <div class="area area-header">
    <div class="label">① 상단 — 진행 단계 (z=5)</div>
    <div class="ids">SP_HDR_001, _002</div>
  </div>
  <div class="area area-lnb">
    <div class="label">② 좌측 — LNB (z=2)</div>
    <div class="ids">SP_LNB_001~004</div>
  </div>
  <div class="area area-inv-top unused">
    <div class="label">③ 우측 상단 — 도면</div>
    <div class="ids">미사용 (Description 명시 없음)</div>
  </div>
  <div class="area area-inv-bot unused">
    <div class="label">④ 우측 하단 — 인벤토리</div>
    <div class="ids">미사용 (도구 사용 단계 아님)</div>
  </div>
  <div class="area area-center">
    <div class="label">⑤ 중앙 — 작업공간 (z=1)</div>
    <div class="ids" style="white-space:pre-line;">SP_DIAG_S21_001 (회로도)
SP_DIAG_S21_002 (마스크)
SP_HL_001 (EOCR HL)
SP_PTR_001/002 (포인팅 P)
SP_PTR_003 (인디케이터 →)
SP_ZOOM_001/002/003 ([공통]View)</div>
  </div>
  <div class="area area-footer">
    <div class="label">⑥ 하단 — Nav + 자막 (z=4)</div>
    <div class="ids">SP_NAV_001/002 ([공통]Nav), SP_FTR_001/002</div>
  </div>
  <div class="marker ptr" title="SP_PTR_001/002">P</div>
  <div class="marker ind" title="SP_PTR_003">→</div>
</div>

<div class="note">
  <b>변경점</b>: 우측 영역 (③·④) 을 <span style="text-decoration:line-through;">사용</span> → <b>미사용</b> 으로 정정. 작업공간 영역은 우측 끝까지 확장 (도면 패널 자리 차지 안 함).
</div>
</section>
'''

# ─── 슬라이드 21 사용 자산 표 ──────────────────────────────
used_section = f'''
<section class="slide">
<h1>슬라이드 21 — 사용 자산 (19 그룹)</h1>
<p class="subtitle">메타 8 + [공통]Nav·View 5 + S21 전용 6 = 19 자산 그룹.</p>

<table>
<tr>
  <th style="width:110px;">고유 ID</th>
  <th style="width:80px;">분류</th>
  <th style="width:90px;">영역</th>
  <th style="width:170px;">한글 이름</th>
  <th style="width:240px;">원본 에셋 (T1)</th>
  <th style="width:180px;">인스턴스 (T2)</th>
  <th style="width:90px;">상태 변형</th>
  <th>설명</th>
</tr>
{used_rows}
</table>

<div class="note">
  <b>분류 기준</b><br>
  • <span class="tag tag-meta">메타</span>: 슬라이드 마스터 차원의 메타데이터 — 헤더·LNB·자막·페이지번호. PPTX 슬라이드별 명시 없어도 항상 표시.<br>
  • <span class="tag tag-com">[공통]Nav·View</span>: User Scenario 에 [공통] 라벨이 붙은 동작에 필요한 자산.<br>
  • <span class="tag tag-s21">S21 전용</span>: 슬라이드 21 Description 표 + Main Task 에 명시된 자산.
</div>
</section>
'''

# ─── 슬라이드 21 미사용 자산 표 ────────────────────────────
unused_section = f'''
<section class="slide">
<h1>슬라이드 21 — 미사용 자산 (참고용)</h1>
<p class="subtitle">전체 자산 풀에 있으나 슬라이드 21 에서는 표시되지 않는 자산. v1 에서 잘못 포함시켰던 항목 + 향후 다른 슬라이드에서 사용 예정.</p>

<table>
<tr>
  <th style="width:110px;">고유 ID</th>
  <th style="width:120px;">분류</th>
  <th style="width:120px;">영역</th>
  <th style="width:200px;">한글 이름</th>
  <th>이 슬라이드에서 미사용인 이유</th>
</tr>
{unused_rows}
</table>

<div class="note">
  <b>인계 시 주의</b>: 이 자산들이 슬라이드 22 이후에서 사용될 가능성은 높음 (예: SP_INV_002 도면 팝업 → S22 부품 내부 결선도 팝업으로 사용 가능, SP_NUM_001 넘버링 라벨 → S23 부터). S22~S28 분석 시 각 슬라이드별로 다시 검증 필요.
</div>
</section>
'''

# ─── 슬라이드 × 자산 사용 매트릭스 ─────────────────────────
matrix_rows = []
asset_lookup = {a[0]: a for a in (SLIDE21_USED + [(aid, cat, area, ko, None, None, None, None) for aid, cat, area, ko, _ in SLIDE21_UNUSED])}
for aid in USE_MATRIX:
    info = asset_lookup.get(aid)
    if info:
        _, _, _, ko, *_ = info
    else:
        ko = ""
    cells = []
    for use in USE_MATRIX[aid]:
        if use == "✓":
            cells.append(f"<td class='cell-y'>✓</td>")
        elif use == "—":
            cells.append(f"<td class='cell-n'>—</td>")
        else:
            cells.append(f"<td class='cell-q'>?</td>")
    matrix_rows.append(f"<tr><td class='mono'><b>{aid}</b></td><td>{escape(ko)}</td>{''.join(cells)}</tr>")

matrix_section = f'''
<section class="slide matrix">
<h1>슬라이드 × 자산 사용 매트릭스 (S21~S28)</h1>
<p class="subtitle">S21 은 본 문서에서 확정. S22~S28 의 ? 셀은 추후 분석 시 확정 필요.</p>

<table>
<tr>
  <th>자산 ID</th>
  <th>한글 이름</th>
  <th>S21</th><th>S22</th><th>S23</th><th>S24</th><th>S25</th><th>S26</th><th>S27</th><th>S28</th>
</tr>
{"".join(matrix_rows)}
</table>

<div class="legend" style="font-size:13px; display:flex; gap:20px; margin-top:10px;">
  <span><span class="tag cell-y" style="padding:2px 10px;">✓</span> 사용 (확정)</span>
  <span><span class="tag cell-n" style="padding:2px 10px;">—</span> 미사용 (확정)</span>
  <span><span class="tag cell-q" style="padding:2px 10px;">?</span> 미확정 (재분석 필요)</span>
</div>

<div class="note">
  본 매트릭스는 슬라이드 21 만 확정. S22~S28 의 ? 셀들은 다음 분석 작업에서 확정. 매트릭스 형식은 인계·QA·발주 우선순위 판단에 활용.
</div>
</section>
'''

# ─── 발주 요약 ───────────────────────────────────────────
summary_section = f'''
<section class="slide">
<h1>발주 요약 (v2)</h1>

<table>
<tr><th>구분</th><th>자산 그룹 수 (v1)</th><th>자산 그룹 수 (v2)</th><th>변경</th></tr>
<tr><td>슬라이드 마스터 메타 (HDR/LNB/FTR)</td><td>—</td><td>8</td><td class="diff-add">분류 신설</td></tr>
<tr><td>[공통]Nav·View (NAV/ZOOM)</td><td>—</td><td>5</td><td class="diff-add">분류 신설</td></tr>
<tr><td>도면·인벤토리 (INV)</td><td>5</td><td>0</td><td class="diff-del">슬라이드 21 미사용</td></tr>
<tr><td>S21 전용 (DIAG/PTR/HL)</td><td>7</td><td>6</td><td class="diff-del">NUM_001 → S23~ 로 이관</td></tr>
<tr><td>보조 (CUR)</td><td>1</td><td>0</td><td class="diff-del">명시 없음</td></tr>
<tr><th>슬라이드 21 합계</th><th>26</th><th>19</th><th class="diff-add">7 그룹 감소</th></tr>
</table>

<h2>이 자산들로 실제 발주할 PNG 파일 수 (state 변형 포함)</h2>
<table>
<tr><th>분류</th><th>그룹</th><th>실제 PNG 파일</th></tr>
<tr><td>메타</td><td>8</td><td>10 (LNB 1·2 depth 가 Def/On 각 1장씩)</td></tr>
<tr><td>[공통]Nav·View</td><td>5</td><td>9 (Nav 5 + Zoom 4)</td></tr>
<tr><td>S21 전용</td><td>6</td><td>6 (모두 단일 또는 알파 마스크 1장)</td></tr>
<tr><th>합계</th><th>19 그룹</th><th>약 25 PNG 파일</th></tr>
</table>

<h2>다음 단계</h2>
<div class="note">
  <b>본 샘플 (S21) 의 교훈을 반영해</b> S22~S28 분석 시 다음 프로세스 적용:<br>
  1. 슬라이드별 Description 표 정독 → 자산 명시 항목 추출<br>
  2. User Scenario 의 [공통] 라벨 추출 → 자동 호출 자산 결정<br>
  3. 메타데이터 (헤더·LNB·자막) 는 항상 포함<br>
  4. 도면·인벤토리는 명시된 경우에만 포함<br>
  5. UX 흐름 검증 — Main Task 와 자산이 일치하는지<br>
  6. 사용/미사용 양쪽 명시 + 매트릭스 업데이트
</div>
</section>
'''

deck = (cover + diff_section + cause_section + fix_section + overview_section
        + mockup_section + used_section + unused_section + matrix_section + summary_section)

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>슬라이드 21 — 2D 스프라이트 자산 분석 (v2 Revised)</title>
<style>{CSS}</style>
</head>
<body>
<div class="deck">
{deck}
</div>
</body>
</html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT}")
print(f"  Used (S21):     {len(SLIDE21_USED)} groups")
print(f"  Unused (참고):  {len(SLIDE21_UNUSED)} groups")
