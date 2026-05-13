"""Build Slide 21 sprite asset analysis HTML (sample).

Output: doc/assets/SpriteAssetAnalysis_S21_Sample.html

Analyzes slide 21 (주회로 넘버링 - EOCR) screen composition and lists
required 2D sprite assets with unique IDs, T1 source names, T2 instance names.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "doc" / "assets" / "SpriteAssetAnalysis_S21_Sample.html"

# ─────────────────────────────────────────────────────────────────
# Common UI Sprites (슬라이드 18 의 화면 영역 정의 기반 — 21~28 공통)
# ─────────────────────────────────────────────────────────────────
COMMON = [
    # (ID, 분류, 영역, 한글이름, 원본 에셋, 인스턴스, 상태, 설명)
    ("SP_HDR_001", "공통", "상단 (z=5)", "상단 헤더 패널", "Pnl_Header_Sprite_v01.png", "PnlHeader", "단일", "현재 진행 단계 이름을 표시하는 상단 띠 배경"),
    ("SP_HDR_002", "공통", "상단 (z=5)", "진행 단계 이름 라벨", "Lbl_StepName_Sprite_v01.png", "LblStepName", "단일", "단계 이름 텍스트가 들어갈 라벨 박스 (텍스트는 동적)"),
    ("SP_LNB_001", "공통", "좌측 (z=2)", "LNB 메뉴 패널 배경", "Pnl_LNB_Sprite_v01.png", "PnlLNB", "단일", "좌측 메뉴 전체 배경판"),
    ("SP_LNB_002", "공통", "좌측 (z=2)", "LNB 1-depth 아이템", "ItemLNB1_Sprite_Def_v01.png / ItemLNB1_Sprite_On_v01.png", "ItemLNB1_Def · ItemLNB1_On", "Def · On", "1차 메뉴 아이템. 현재 위치는 포인트 컬러(On) 강조"),
    ("SP_LNB_003", "공통", "좌측 (z=2)", "LNB 2-depth 아이템", "ItemLNB2_Sprite_Def_v01.png / ItemLNB2_Sprite_On_v01.png", "ItemLNB2_Def · ItemLNB2_On", "Def · On", "들여쓰기 된 2차 메뉴 (현재 작업 \"1. 회로도 넘버링\")"),
    ("SP_LNB_004", "공통", "좌측 (z=2)", "LNB 드롭다운 화살표", "Ico_LNBArrow_Sprite_v01.png", "IcoLNBArrow", "Closed · Open (회전)", "드롭다운 펼침/접힘 표시 (CSS rotate 로 처리 가능)"),
    ("SP_INV_001", "공통", "우측 (z=3)", "우측 아이템 패널 배경", "Pnl_Inventory_Sprite_v01.png", "PnlInventory", "단일", "도구 버튼들이 놓이는 우측 영역 배경"),
    ("SP_INV_002", "공통", "우측 (z=2)", "도면 팝업 배경", "Pnl_Diagram_Sprite_v01.png", "PnlDiagram", "단일", "우측 상단 도면 팝업 (제어판 작업 시 표출)"),
    ("SP_INV_003", "공통", "우측", "도면 확대 버튼", "Btn_DiagZoomIn_Sprite_Def_v01.png / Btn_DiagZoomIn_Sprite_Prs_v01.png", "BtnDiagZoomIn_Def · _Prs", "Def · Prs", "도면 패널 내 + 버튼"),
    ("SP_INV_004", "공통", "우측", "도면 축소 버튼", "Btn_DiagZoomOut_Sprite_Def_v01.png / Btn_DiagZoomOut_Sprite_Prs_v01.png", "BtnDiagZoomOut_Def · _Prs", "Def · Prs", "도면 패널 내 - 버튼"),
    ("SP_INV_005", "공통", "우측", "도면 닫기 버튼", "Btn_DiagClose_Sprite_Def_v01.png / Btn_DiagClose_Sprite_Prs_v01.png", "BtnDiagClose_Def · _Prs", "Def · Prs", "도면 패널 닫기 (필요 시)"),
    ("SP_NAV_001", "공통", "하단 (z=4)", "이전 버튼 〈", "Btn_NavPrev_Sprite_Def_v01.png / Btn_NavPrev_Sprite_Prs_v01.png", "BtnNavPrev_Def · _Prs", "Def · Prs", "Step Navigation - 이전 슬라이드로"),
    ("SP_NAV_002", "공통", "하단 (z=4)", "다음 버튼 〉", "Btn_NavNext_Sprite_Off_v01.png / Btn_NavNext_Sprite_On_v01.png / Btn_NavNext_Sprite_Prs_v01.png", "BtnNavNext_Off · _On · _Prs", "Off · On · Prs", "미션 완료 전 Off, 완료 시 On 으로 활성화"),
    ("SP_FTR_001", "공통", "하단 (z=4)", "자막 영역 배경", "Pnl_Caption_Sprite_v01.png", "PnlCaption", "단일", "하단 자막 텍스트 표시 영역 배경"),
    ("SP_FTR_002", "공통", "하단", "페이지 번호 라벨", "Lbl_PageNum_Sprite_v01.png", "LblPageNum", "단일", "001 / 002 ... 페이지 번호 표시"),
    ("SP_ZOOM_001", "공통", "중앙 (z=1)", "작업공간 줌인 버튼", "Btn_WorkZoomIn_Sprite_Def_v01.png / Btn_WorkZoomIn_Sprite_Prs_v01.png", "BtnWorkZoomIn_Def · _Prs", "Def · Prs", "중앙 작업공간 + 버튼 (배율 100~300%)"),
    ("SP_ZOOM_002", "공통", "중앙 (z=1)", "작업공간 줌아웃 버튼", "Btn_WorkZoomOut_Sprite_Def_v01.png / Btn_WorkZoomOut_Sprite_Prs_v01.png", "BtnWorkZoomOut_Def · _Prs", "Def · Prs", "중앙 작업공간 - 버튼"),
    ("SP_ZOOM_003", "공통", "중앙", "줌 배율 라벨", "Lbl_ZoomScale_Sprite_v01.png", "LblZoomScale", "단일", "현재 배율 텍스트 박스 (100% / 200% 등)"),
    ("SP_CUR_001", "공통", "전역", "드래그 커서 가이드", "Ico_DragHint_Sprite_v01.png", "IcoDragHint", "단일", "드래그로 이동 가능함을 알리는 보조 아이콘 (선택)"),
]

# ─────────────────────────────────────────────────────────────────
# Slide 21 전용 Sprites
# ─────────────────────────────────────────────────────────────────
S21 = [
    ("SP_DIAG_S21_001", "S21 전용", "중앙 (z=1)", "주회로 회로도 전체 (Stage1 주회로용)", "Bg_DiagMain_Sprite_v01.png", "BgDiagMain", "단일", "주회로 작업용 회로도 전체 이미지. 기본 배율 200%, 드래그·줌 가능"),
    ("SP_DIAG_S21_002", "S21 전용", "중앙 (z=1)", "주회로 외 영역 마스크 오버레이", "Bg_DiagMainMask_Sprite_v01.png", "BgDiagMainMask", "단일", "회로도 위에 덮이는 반투명 마스크. 주회로 영역만 뚫려 있음 (alpha 채널 활용)"),
    ("SP_NUM_001", "S21 전용", "중앙", "회로도 넘버링 라벨 - 일반", "Lbl_CircuitNum_Sprite_v01.png", "LblCircuitNum_01 ~ _NN", "단일", "회로도 라인 옆에 표시되는 1, 2, 3, 7, 8, 9 등 번호 라벨 (텍스트는 동적)"),
    ("SP_PTR_001", "S21 전용", "중앙 (z=1)", "클릭 유도 포인팅 - 펄스 링", "Ani_ClickPulse_Sprite_v01.png", "AniClickPulse", "프레임 시트 또는 단일 + CSS Ani", "EOCR 위에 표시되는 클릭 유도 펄스 애니메이션 (확대·페이드 반복)"),
    ("SP_PTR_002", "S21 전용", "중앙 (z=1)", "클릭 유도 포인팅 - 손가락 아이콘", "Ico_ClickHand_Sprite_v01.png", "IcoClickHand", "단일", "펄스 링과 함께 표시되는 손가락 아이콘 (선택)"),
    ("SP_PTR_003", "S21 전용", "중앙 (z=1)", "위치 인디케이터", "Ico_LocIndicator_Sprite_v01.png", "IcoLocIndicator", "단일 (4방향 회전)", "포인팅 영역이 화면 밖으로 나갔을 때 가장자리에 표시되는 화살표. CSS rotate 로 4방향 처리"),
    ("SP_HL_001", "S21 전용", "중앙 (z=1)", "EOCR 클릭 영역 하이라이트", "Ico_HotspotHL_Sprite_v01.png", "IcoHotspotHL", "단일", "EOCR 부품 위치의 클릭 가능 영역 표시 (반투명 외곽선·글로우)"),
]


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
  font-size: 32px;
  color: #1f3864;
  border-bottom: 3px solid #2f5496;
  padding-bottom: 10px;
}
h2 {
  margin: 24px 0 10px 0;
  font-size: 22px;
  color: #2f5496;
}
h3 { font-size: 17px; color: #1f3864; margin: 16px 0 6px; }
p, li { font-size: 15px; line-height: 1.55; }
.subtitle { color: #595959; font-size: 16px; margin-top: -4px; }
.meta { color: #777; font-size: 13px; }
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  margin: 10px 0 22px 0;
}
th {
  background: #2f5496; color: #fff;
  padding: 8px 10px; text-align: left; font-weight: 600;
  position: sticky; top: 0;
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
.tag-com { background: #c5e0b4; color: #385723; }
.tag-s21 { background: #f8cbad; color: #843c0c; }
.tag-state { background: #bdd7ee; color: #1f3864; }
.note {
  background: #fff2cc; border-left: 4px solid #ffc000;
  padding: 12px 16px; font-size: 13px; margin: 12px 0;
  color: #5a4500;
}
.cover { text-align: center; padding: 120px 0; }
.cover h1 { font-size: 38px; border: 0; }
.cover .sub { color: #5a5a5a; font-size: 18px; margin: 8px 0; }

/* 화면 mockup */
.mockup {
  position: relative;
  width: 100%;
  height: 480px;
  background: #f0f0f0;
  border: 2px solid #999;
  margin: 16px 0 22px;
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
.area .label { font-size: 11px; }
.area .ids { font-size: 10px; color: #595959; font-weight: 400; margin-top: 4px; font-family: 'Consolas', monospace; }

.area-header { top: 0; left: 0; right: 0; height: 50px; background: rgba(46,84,150,0.18); }
.area-lnb { top: 50px; left: 0; bottom: 60px; width: 200px; background: rgba(46,84,150,0.10); }
.area-inv-top { top: 50px; right: 0; width: 240px; height: 200px; background: rgba(255,192,0,0.18); }
.area-inv-bot { top: 250px; right: 0; bottom: 60px; width: 240px; background: rgba(255,192,0,0.10); }
.area-center { top: 50px; left: 200px; right: 240px; bottom: 60px; background: rgba(112,173,71,0.10); border-color: #548235; }
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
.mockup .ind { top: 55%; right: 250px; transform: translateY(-50%); background: #ff8c00; }
.mockup .zoom { right: 250px; bottom: 70px; }

.legend { display: flex; gap: 18px; font-size: 12px; margin: 8px 0 16px; }
.legend span { display: flex; align-items: center; gap: 4px; }
.legend .sw { width: 16px; height: 16px; border: 1px dashed #2f5496; }

.summary {
  background: #f4f6fa; border-left: 4px solid #2f5496;
  padding: 14px 18px; margin: 12px 0; border-radius: 4px;
}
.summary b { color: #1f3864; }

ul.checklist li { list-style: none; padding-left: 22px; position: relative; margin: 4px 0; }
ul.checklist li::before { content: '☐'; position: absolute; left: 0; color: #2f5496; }
@media print {
  body { background: #fff; }
  .slide { box-shadow: none; margin: 0; }
}
"""


def row_html(asset):
    aid, cat, area, ko, src, inst, state, desc = asset
    cls = "tag-com" if cat == "공통" else "tag-s21"
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


common_rows = "\n".join(row_html(a) for a in COMMON)
s21_rows = "\n".join(row_html(a) for a in S21)

# ─── Cover ──────────────────────────────────────────────────
cover = '''
<section class="slide">
<div class="cover">
  <h1>2D 스프라이트 자산 분석</h1>
  <div class="sub" style="font-size:24px; color:#1f3864; font-weight:600;">슬라이드 21 — 주회로 넘버링 (EOCR)</div>
  <div class="sub">샘플 분석 (Slide 21 only)</div>
  <div class="meta" style="margin-top:60px;">
    원본: [폴리텍신기술교육원]_전기내선공사 가상 실습_SB_v1.0.pptx<br>
    명명 규칙: Make Asset Naming Convention v6<br>
    작성일: 2026-05-13
  </div>
</div>
</section>
'''

# ─── 슬라이드 21 개요 ───────────────────────────────────────
overview = '''
<section class="slide">
<h1>슬라이드 21 — 개요</h1>

<table>
<tr><th style="width:140px;">항목</th><th>내용</th></tr>
<tr><td>제목</td><td>주회로 넘버링 - EOCR</td></tr>
<tr><td>단계</td><td>Stage 1. 제어판 작업 → 1. 회로도 넘버링 → 주회로</td></tr>
<tr><td>페이지 번호</td><td>001</td></tr>
<tr><td>설명 문구 (자막)</td><td>회로도에 순차적으로 넘버링을 해줍니다.</td></tr>
<tr><td>Main Task</td><td>회로도 내 <b>EOCR</b> 클릭 → 부품 내부 결선도 팝업 호출 + 다음 슬라이드로 이동</td></tr>
<tr><td>View 동작</td><td>회로도 배경 드래그 시 상하좌우 이동, 확대/축소 버튼으로 배율 조절 (100% / 150% / 200%기본 / 250% / 300%)</td></tr>
<tr><td>Nav 동작</td><td>하단 〈, 〉 클릭 시 이전/다음 단계로 강제 이동</td></tr>
</table>

<h2>슬라이드 21 만의 특이 요구</h2>
<div class="note">
  <b>1.</b> 회로도 배경 이미지의 기본 배율 200%. 주회로 영역 외 나머지는 투명도 처리 (마스크 오버레이).<br>
  <b>2.</b> 클릭해야 하는 EOCR 부분에 <b>포인팅 애니메이션</b> 표시. 클릭 시 다음 화면으로 이동.<br>
  <b>3.</b> 해당 영역이 화면 밖으로 나가면 <b>인디케이터로 위치 안내</b>.
</div>
</section>
'''

# ─── 화면 mockup ────────────────────────────────────────────
mockup = '''
<section class="slide">
<h1>화면 영역 매핑 (mockup)</h1>
<p class="subtitle">슬라이드 18 의 공통 화면 사양 + 슬라이드 21 특이 요구를 적용한 영역 구성.</p>

<div class="mockup">
  <div class="area area-header">
    <div class="label">① 상단 — 진행 단계 이름 (z=5)</div>
    <div class="ids">SP_HDR_001, SP_HDR_002</div>
  </div>
  <div class="area area-lnb">
    <div class="label">② 좌측 — LNB 메뉴 (z=2)</div>
    <div class="ids">SP_LNB_001<br>SP_LNB_002 (1-depth)<br>SP_LNB_003 (2-depth, "1. 회로도 넘버링" Active)<br>SP_LNB_004 (drop arrow)</div>
  </div>
  <div class="area area-inv-top">
    <div class="label">③ 우측 상단 — 도면 (z=2)</div>
    <div class="ids">SP_INV_002, _003, _004, _005</div>
  </div>
  <div class="area area-inv-bot">
    <div class="label">④ 우측 하단 — 아이템 / 인벤토리 (z=3)</div>
    <div class="ids">SP_INV_001</div>
  </div>
  <div class="area area-center">
    <div class="label">⑤ 중앙 — 작업공간 / 회로도 (z=1)</div>
    <div class="ids" style="white-space:pre-line;">SP_DIAG_S21_001 (회로도 전체)
SP_DIAG_S21_002 (주회로 외 마스크)
SP_HL_001 (EOCR 클릭 영역 HL)
SP_NUM_001 (넘버링 라벨)
SP_ZOOM_001/002/003</div>
  </div>
  <div class="area area-footer">
    <div class="label">⑥ 하단 — Step Navigation + 자막 (z=4)</div>
    <div class="ids">SP_NAV_001 (〈), SP_NAV_002 (〉), SP_FTR_001 (자막), SP_FTR_002 (페이지 #)</div>
  </div>
  <div class="marker ptr" title="SP_PTR_001/002 클릭 유도 포인팅 (EOCR 위치)">P</div>
  <div class="marker ind" title="SP_PTR_003 위치 인디케이터 (영역 밖 안내)">→</div>
</div>

<div class="legend">
  <span><span class="marker" style="position:relative; transform:none; width:18px; height:18px;">P</span> 클릭 유도 포인팅 (EOCR 위 펄스 + 손가락)</span>
  <span><span class="marker" style="position:relative; transform:none; width:18px; height:18px; background:#ff8c00;">→</span> 위치 인디케이터 (영역 밖일 때 표시)</span>
</div>

<h2>z-index 정리 (슬라이드 18 기준)</h2>
<table>
<tr><th style="width:80px;">z-index</th><th style="width:200px;">영역</th><th>설명</th></tr>
<tr><td>1</td><td>중앙 작업공간</td><td>회로도 배경 + 마스크 + 포인팅 (가장 아래 레이어)</td></tr>
<tr><td>2</td><td>좌측 LNB, 우측 도면</td><td>메뉴와 도면 팝업</td></tr>
<tr><td>3</td><td>우측 아이템</td><td>도구 버튼 영역</td></tr>
<tr><td>4</td><td>하단 자막 + Nav</td><td>Step Navigation 및 자막</td></tr>
<tr><td>5</td><td>상단 헤더</td><td>최상위 — 항상 보임</td></tr>
</table>
</section>
'''

# ─── 자산 ID 부여 규칙 ───────────────────────────────────────
id_rules = '''
<section class="slide">
<h1>자산 고유 ID 부여 규칙</h1>

<h2>형식</h2>
<div class="summary">
  <code class="mono" style="font-size:14px;"><b>SP_&lt;CAT&gt;_&lt;NN&gt;</b></code> &nbsp; (Sprite + 카테고리 + 두 자리 일련번호)<br>
  슬라이드별 고유 자산은 <code class="mono"><b>SP_&lt;CAT&gt;_S&lt;NN&gt;_&lt;NN&gt;</b></code> 형식 (S 뒤에 슬라이드 번호).
</div>

<h2>카테고리 약자</h2>
<table>
<tr><th style="width:120px;">카테고리 약자</th><th style="width:160px;">의미</th><th>대상 자산</th></tr>
<tr><td class="mono"><b>HDR</b></td><td>Header</td><td>상단 진행 단계 표시</td></tr>
<tr><td class="mono"><b>LNB</b></td><td>Left Navigation</td><td>좌측 메뉴 (1-2 depth, drop arrow 포함)</td></tr>
<tr><td class="mono"><b>INV</b></td><td>Inventory · Diagram</td><td>우측 아이템 패널, 도면 팝업, 도면 버튼</td></tr>
<tr><td class="mono"><b>NAV</b></td><td>Navigation (Step)</td><td>하단 〈 〉 이전/다음 버튼</td></tr>
<tr><td class="mono"><b>FTR</b></td><td>Footer</td><td>자막 영역, 페이지 번호</td></tr>
<tr><td class="mono"><b>ZOOM</b></td><td>Zoom Control</td><td>중앙 작업공간 +/- 버튼, 배율 라벨</td></tr>
<tr><td class="mono"><b>DIAG</b></td><td>Diagram</td><td>회로도 이미지·마스크</td></tr>
<tr><td class="mono"><b>NUM</b></td><td>Numbering Label</td><td>회로도 라인 옆 1,2,3 번호 라벨</td></tr>
<tr><td class="mono"><b>PTR</b></td><td>Pointing / Indicator</td><td>클릭 유도 펄스·손가락 아이콘, 위치 인디케이터</td></tr>
<tr><td class="mono"><b>HL</b></td><td>Highlight</td><td>클릭 가능 영역 강조 (EOCR 등 핫스팟)</td></tr>
<tr><td class="mono"><b>CUR</b></td><td>Cursor / Hint</td><td>드래그 가이드 등 보조 아이콘</td></tr>
</table>

<h2>v6 명명 규칙과의 매핑</h2>
<table>
<tr><th>레이어</th><th>형식</th><th>예시</th></tr>
<tr><td><b>T1 — 원본 파일</b></td><td>PascalCase + <code>Sprite</code> Role + state + <code>_v01</code> + <code>.png</code></td><td class="mono">Btn_NavNext_Sprite_On_v01.png</td></tr>
<tr><td><b>T2 — 인스턴스</b></td><td>PascalCase, 종류 약자 없음, 단일 _</td><td class="mono">BtnNavNext_On</td></tr>
<tr><td><b>본 문서의 고유 ID</b></td><td>자산 관리·발주용 시퀀스 ID (실제 파일명·인스턴스명과 별개)</td><td class="mono">SP_NAV_002</td></tr>
</table>

<div class="note">
  <b>주의</b>: 고유 ID(SP_xxx_NN) 는 <b>자산 관리·발주·QA 추적용</b>입니다. 실제 파일 시스템·Make Editor 에는 들어가지 않으며, 본 문서·엑셀·이슈 트래커에서만 사용합니다.
</div>
</section>
'''

# ─── 공통 자산 표 ───────────────────────────────────────────
common_section = f'''
<section class="slide">
<h1>공통 UI 자산 (Common — 슬라이드 21~28 이후 모두 재사용)</h1>
<p class="subtitle">슬라이드 18 의 공통 화면 사양에 정의된 UI 요소. 한 번 발주하면 전체 콘텐츠에서 재사용.</p>

<table>
<tr>
  <th style="width:110px;">고유 ID</th>
  <th style="width:60px;">분류</th>
  <th style="width:90px;">영역</th>
  <th style="width:170px;">한글 이름</th>
  <th style="width:240px;">원본 에셋 (T1)</th>
  <th style="width:180px;">인스턴스 (T2)</th>
  <th style="width:80px;">상태 변형</th>
  <th>설명</th>
</tr>
{common_rows}
</table>
</section>
'''

# ─── 슬라이드 21 자산 표 ────────────────────────────────────
s21_section = f'''
<section class="slide">
<h1>슬라이드 21 전용 자산</h1>
<p class="subtitle">슬라이드 21 (주회로 넘버링 - EOCR) 에만 필요한 자산. 일부는 22~28 (보조회로 넘버링) 에서도 변형으로 재사용 가능.</p>

<table>
<tr>
  <th style="width:140px;">고유 ID</th>
  <th style="width:70px;">분류</th>
  <th style="width:90px;">영역</th>
  <th style="width:200px;">한글 이름</th>
  <th style="width:240px;">원본 에셋 (T1)</th>
  <th style="width:180px;">인스턴스 (T2)</th>
  <th style="width:100px;">상태 변형</th>
  <th>설명</th>
</tr>
{s21_rows}
</table>

<h2>슬라이드 21 ~ 28 의 재사용 가능성</h2>
<table>
<tr><th>자산</th><th>S21</th><th>S22~S27</th><th>S28</th><th>변형 필요?</th></tr>
<tr><td class="mono">SP_DIAG_S21_001 (회로도 전체)</td><td>✅</td><td>✅</td><td>✅</td><td>같은 회로도 재사용</td></tr>
<tr><td class="mono">SP_DIAG_S21_002 (마스크)</td><td>✅</td><td>일부 ✅</td><td>—</td><td>S22~ 결선도 팝업은 별도 마스크 필요할 수 있음</td></tr>
<tr><td class="mono">SP_NUM_001 (넘버링 라벨)</td><td>✅</td><td>✅</td><td>✅</td><td>S28 까지 누적 표시 (1~22)</td></tr>
<tr><td class="mono">SP_PTR_001/002 (클릭 유도)</td><td>✅</td><td>✅</td><td>—</td><td>S28 은 완료 화면이라 포인팅 불필요</td></tr>
<tr><td class="mono">SP_PTR_003 (인디케이터)</td><td>✅</td><td>✅</td><td>✅</td><td>전체 슬라이드 공통</td></tr>
<tr><td class="mono">SP_HL_001 (EOCR HL)</td><td>✅</td><td>— (다른 부품용 HL 필요)</td><td>—</td><td>S24 부터는 MC1/MC2 HL 별도 자산</td></tr>
</table>
</section>
'''

# ─── 발주 요약 + 체크리스트 ────────────────────────────────
summary_section = f'''
<section class="slide">
<h1>발주 요약 + 검증 체크리스트</h1>

<h2>슬라이드 21 자산 발주 단위 요약</h2>
<table>
<tr><th>구분</th><th>자산 그룹 수</th><th>실제 PNG 파일 수 (상태 변형 포함)</th></tr>
<tr><td>공통 UI (Common)</td><td>{len(COMMON)} 그룹</td><td>약 28~30 개</td></tr>
<tr><td>슬라이드 21 전용</td><td>{len(S21)} 그룹</td><td>약 7 개</td></tr>
<tr><td><b>합계</b></td><td><b>{len(COMMON) + len(S21)} 그룹</b></td><td>약 35~37 개</td></tr>
</table>

<h2>모델러 발주 시 체크리스트</h2>
<ul class="checklist">
  <li>모든 PNG 파일이 PascalCase + <code class="mono">Sprite</code> Role 토큰 포함 (T1 규칙)</li>
  <li>상태 변형 (Def/Prs/On/Off) 별로 별도 파일</li>
  <li>버전 표시 <code class="mono">_v01</code> 부착 (필요 시)</li>
  <li>해상도: 작업공간 200% 기본 배율 고려해 충분히 큰 원본 (Retina 2x 권장)</li>
  <li>알파 채널 (PNG-32) — 특히 마스크(SP_DIAG_S21_002) 와 포인팅(SP_PTR_001)</li>
  <li>한글 파일명 0건</li>
  <li>공백·하이픈 0건</li>
  <li>고유 ID 와 파일명 매핑 표를 발주서에 첨부</li>
</ul>

<h2>다음 단계 (이 샘플 다음)</h2>
<div class="note">
  본 문서는 <b>슬라이드 21 샘플 분석</b>입니다. 동일 패턴으로 슬라이드 22~28 분석 진행 시:<br>
  <b>S22</b>: 부품 내부 결선도 팝업 8종 (12핀 릴레이, 8핀 릴레이, EOCR, FLS, T, X, FR, MC) — 신규 자산 그룹 8개<br>
  <b>S23</b>: 넘버링 1·2·3 라벨 생성 (SP_NUM 재사용)<br>
  <b>S24~S26</b>: MC1·MC2 결선도 팝업 (S22 재사용)<br>
  <b>S27</b>: 넘버링 완료 안내 — 완료 메시지 모달 신규<br>
  <b>S28</b>: 완료 화면 — 누적 넘버링 + 다음 단계 (작도) 진입 UI<br>
  → S22~S28 추가 시 약 15~20 자산 그룹 신규 예상.
</div>
</section>
'''


total_pages = 6  # cover + overview + mockup + id_rules + common + s21+summary (slightly off but rough)
deck = cover + overview + mockup + id_rules + common_section + s21_section + summary_section

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>슬라이드 21 — 2D 스프라이트 자산 분석 (Sample)</title>
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
print(f"  Common UI: {len(COMMON)} groups")
print(f"  Slide 21:  {len(S21)} groups")
print(f"  Total:     {len(COMMON) + len(S21)} groups")
