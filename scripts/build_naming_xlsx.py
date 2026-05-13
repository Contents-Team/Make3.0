"""Build Make Naming Convention v6 spec + example guide as Excel workbook.

Output: doc/assets/MakeNamingConvention_v6.xlsx
"""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "doc" / "assets" / "MakeNamingConvention_v6.xlsx"

# Styles
HDR_FONT = Font(name="Malgun Gothic", size=11, bold=True, color="FFFFFF")
HDR_FILL = PatternFill("solid", fgColor="2F5496")
TITLE_FONT = Font(name="Malgun Gothic", size=14, bold=True, color="2F5496")
SECTION_FONT = Font(name="Malgun Gothic", size=12, bold=True, color="1F3864")
GOOD_FILL = PatternFill("solid", fgColor="E2EFDA")
BAD_FILL = PatternFill("solid", fgColor="FCE4D6")
NOTE_FILL = PatternFill("solid", fgColor="FFF2CC")
THIN = Side(border_style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def style_header_row(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = HDR_FONT
        cell.fill = HDR_FILL
        cell.alignment = CENTER
        cell.border = BORDER


def write_table(ws, start_row, headers, rows, col_widths=None, row_fills=None):
    """Write a table starting at start_row. Returns next free row."""
    for ci, h in enumerate(headers, start=1):
        ws.cell(row=start_row, column=ci, value=h)
    style_header_row(ws, start_row, len(headers))
    for ri, row in enumerate(rows, start=start_row + 1):
        for ci, val in enumerate(row, start=1):
            cell = ws.cell(row=ri, column=ci, value=val)
            cell.alignment = WRAP
            cell.border = BORDER
            cell.font = Font(name="Malgun Gothic", size=10)
            if row_fills and (ri - start_row - 1) < len(row_fills):
                fill = row_fills[ri - start_row - 1]
                if fill:
                    cell.fill = fill
    if col_widths:
        for ci, w in enumerate(col_widths, start=1):
            ws.column_dimensions[get_column_letter(ci)].width = w
    ws.row_dimensions[start_row].height = 22
    return start_row + len(rows) + 2


def title(ws, row, text):
    ws.cell(row=row, column=1, value=text).font = TITLE_FONT
    return row + 2


def section(ws, row, text):
    ws.cell(row=row, column=1, value=text).font = SECTION_FONT
    return row + 1


def note(ws, row, text, span=4):
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = Font(name="Malgun Gothic", size=9, italic=True, color="595959")
    cell.alignment = WRAP
    cell.fill = NOTE_FILL
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)
    ws.row_dimensions[row].height = 30
    return row + 2


wb = Workbook()

# ─────────────────────────────────────────────────────────────
# Sheet 1 — Overview
# ─────────────────────────────────────────────────────────────
ws = wb.active
ws.title = "Overview"
r = title(ws, 1, "Make Asset Naming Convention v6")
ws.cell(row=r, column=1, value="문서 버전: v6 / Repo: Make3.0 v0.1.5 / 작성일: 2026-05-13").font = Font(name="Malgun Gothic", size=10, italic=True)
r += 2

r = section(ws, r, "[ 핵심 원칙 ]")
principles = [
    ("1. 컨텍스트별 형식 분리", "T1 파일 탐색기 / T2 Make Editor / T3 JSON·grep — 각 컨텍스트 최적화"),
    ("2. 인스턴스명에 prefix 없음", "Make Editor 의 타입 아이콘이 종류를 시각적으로 알려주므로 redundant"),
    ("3. 트리 컨텍스트 활용", "부모-자식 위계가 트리에 명시 → 자식 이름은 짧게"),
    ("4. 단일 `_` 통일", "이중 `__` 폐지, 하이픈 명시 금지"),
    ("5. Vocab 축약", "State·Action·Direction 모두 축약형 (3-letter 또는 단문자)"),
    ("6. 자가설명은 시스템 파생만", "사용자 미편집 객체 (T3) 만 prefix 보존 — AI grep·로그 안전"),
]
r = write_table(ws, r, ["원칙", "설명"], principles, col_widths=[28, 80])

r = section(ws, r, "[ 3-Tier 모델 ]")
tiers = [
    ("T1", "Source Asset", "파일시스템 (OS 탐색기)", "PascalCase + 확장자 + 카테고리 토큰", "GlassBottle_v01.fbx, GNB_Active.png, BGM_Tutorial_01.wav"),
    ("T2", "Instance", "Make Editor 트리", "PascalCase, prefix 없음, 단일 _", "GNB_Act, BtnStart, Cupcake, RotationPanel/L"),
    ("T3", "System-Derived", "머티리얼·중간 mesh·texture object", "lower_snake_case + 3-letter kind prefix", "mat_unlit_opaque, tex_cupcake_albedo"),
]
r = write_table(ws, r, ["Tier", "이름", "컨텍스트", "형식", "예시"], tiers,
                col_widths=[6, 16, 28, 38, 50])

r = section(ws, r, "[ 시트 안내 ]")
sheets_info = [
    ("Overview", "본 시트 — 원칙·3-Tier 요약"),
    ("T1 Source", "파일시스템 원본 에셋 명명 규칙 (FBX·PNG·WAV·MP4·Font)"),
    ("T2 Instance", "Make Editor 인스턴스 명명 규칙 + Family/State/Direction Vocab"),
    ("T3 Derived", "시스템 파생 객체 명명 규칙 (머티리얼 등)"),
    ("Animation", "애니메이션 클립 명명 규칙 + Action Vocab"),
    ("Vocab Tables", "UI Family / State / Direction / Action / Audio·Video 카테고리 통합"),
    ("Examples", "실측 파일(Make Templete_20260512.make) 안티패턴 → v6 변환 가이드"),
    ("Checklist", "익스포트 전 검증 체크리스트"),
    ("Anti-Patterns", "금지 패턴 일람"),
]
r = write_table(ws, r, ["시트", "내용"], sheets_info, col_widths=[18, 70])

# ─────────────────────────────────────────────────────────────
# Sheet 2 — T1 Source Asset
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("T1 Source")
r = title(ws, 1, "T1 — Source Asset (Filesystem)")
r = note(ws, r, "모델러·아티스트가 납품 또는 작업 디렉토리에 두는 원본 파일. PascalCase + 확장자. 확장자가 타입을 선언하므로 kind prefix 불필요. 모호한 타입(PNG/WAV/MP4) 만 카테고리·Role 토큰 사용.")

r = section(ws, r, "[ Global Rules ]")
rules = [
    ("공백 없음", "GlassBottle_v01.fbx", "Glass Bottle_v01.fbx"),
    ("구분자 _ 만 (하이픈 금지)", "Contents_3_1_1_2", "Contents_3-1-1-2"),
    ("토큰별 PascalCase", "BatteryPack", "batterypack / battery_pack"),
    ("Variant 2자리 고정", "_01, _02", "_1, _001"),
    ("Version v + 2자리 (옵션)", "_v01, _v02", "_V1, _ver01"),
    ("중복 타입 토큰 금지", "GlassBottle_v01.fbx", "GlassBottle_MOD_v01.fbx"),
    ("영문 전용", "BatteryPack_v01", "배터리팩_v01"),
]
fills = [None] * len(rules)
r = write_table(ws, r, ["Rule", "✅ Correct", "❌ Incorrect"], rules,
                col_widths=[36, 36, 36])

r = section(ws, r, "[ 타입별 규칙 ]")

r = section(ws, r, "■ 3D Model (.fbx)")
note(ws, r, "확장자 .fbx 가 타입 선언. 이름에 타입 토큰 박지 말 것. 자식 부위는 부모 이름 포함.")
r += 2
fbx = [
    ("GlassBottle_v01.fbx", "루트 모델"),
    ("GlassBottle_v02.fbx", "버전 업데이트"),
    ("GlassBottle_Open_v01.fbx", "State 변형"),
    ("GlassBottle_Cap_v01.fbx", "자식 부위 — 부모 이름 포함"),
    ("BatteryPack_TopCover_v01.fbx", "자식 부위"),
]
r = write_table(ws, r, ["파일명", "용도"], fbx, col_widths=[40, 50])

r = section(ws, r, "■ Image — UI Sprite (.png/.jpg)")
sprite = [
    ("Family + Asset + State", "GNB_Act.png, BtnNavi_L_Prs.png"),
    ("Family 단독 사용 OK (단일 자산일 때)", "Logo.png, Tip.png, PnlTablet.png"),
    ("State suffix 는 v6 축약 (Def/Prs/On/Off/Sel)", "GNB_On.png, GNB_Off.png"),
    ("Direction 은 단문자 suffix", "BtnNavi_L.png, Rotation_U.png"),
]
r = write_table(ws, r, ["규칙", "예시"], sprite, col_widths=[50, 50])

r = section(ws, r, "■ Image — 3D Texture (.png)")
note(ws, r, "Role 토큰 필수 — PNG 는 UI 와 텍스처 둘 다이므로 확장자만으론 분간 불가. v<NN> 미사용 (아트 에셋).")
r += 2
roles = [
    ("Sprite", "UI 스프라이트", "PlayBtn_Sprite_01.png"),
    ("ALB", "Albedo / Base Color", "GlassBottle_ALB_01.png"),
    ("NRM", "Normal Map", "GlassBottle_NRM_01.png"),
    ("RGH", "Roughness", "GlassBottle_RGH_01.png"),
    ("MET", "Metallic", "GlassBottle_MET_01.png"),
    ("EMI", "Emission", "GlassBottle_EMI_01.png"),
    ("MSK", "Mask", "GlassBottle_MSK_01.png"),
    ("AO", "Ambient Occlusion", "GlassBottle_AO_01.png"),
]
r = write_table(ws, r, ["Token", "의미", "예시"], roles, col_widths=[12, 30, 50])

r = section(ws, r, "■ Audio (.wav / .mp3)")
note(ws, r, "<Category>_<Description>_<NN>.<ext> — 카테고리·description 사이 _ 삽입 (v6).")
r += 2
audio = [
    ("BGM", "Background Music", "BGM_Tutorial_01.wav, BGM_Boss_01.wav"),
    ("SFX", "Sound Effect (UI 클릭·완료음·경고)", "SFX_UI_Click_01.wav, SFX_StepComplete_01.wav"),
    ("NAR", "Narration / 더빙 (구 VO)", "NAR_Intro_01.wav, NAR_Step01_Guide_01.wav"),
]
r = write_table(ws, r, ["Category", "풀이", "예시"], audio, col_widths=[12, 40, 50])

r = section(ws, r, "■ Video (.mp4)")
video = [
    ("CUT", "Cutscene (시네마틱·서사 영상)", "CUT_AssemblyStep01_01.mp4"),
    ("TUT", "Tutorial (단계별 설명)", "TUT_BatterySwap_Step01_01.mp4"),
    ("LOOP", "Looping background video", "LOOP_WorkshopBackground_01.mp4"),
    ("INTRO", "Intro sequence", "INTRO_Main_01.mp4"),
    ("OUTRO", "Outro sequence", "OUTRO_Credit_01.mp4"),
]
r = write_table(ws, r, ["Category", "풀이", "예시"], video, col_widths=[12, 40, 50])

r = section(ws, r, "■ Font (.ttf / .otf)")
fonts = [
    ("NotoSansKR_Bold_01.ttf", "본체 + Weight"),
    ("NotoSansKR_Regular_01.ttf", ""),
    ("Roboto_Medium_01.ttf", ""),
]
r = write_table(ws, r, ["파일명", "비고"], fonts, col_widths=[40, 40])

# ─────────────────────────────────────────────────────────────
# Sheet 3 — T2 Instance
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("T2 Instance")
r = title(ws, 1, "T2 — Instance (Make Editor visible)")
r = note(ws, r, "Make Editor 트리에 노출되는 사용자 직접 명명 노드. 트리 옆 타입 아이콘이 종류를 시각화하므로 kind prefix 폐지. 부모-자식 트리가 위계를 표현하므로 자식 이름은 짧게.")

r = section(ws, r, "[ Core Rules ]")
core = [
    ("PascalCase 토큰", "BtnStart, GNB_Act", "btn_start, gnb_act"),
    ("Prefix 없음 (T2 한정)", "Cupcake", "mdl_cupcake"),
    ("단일 _ 만", "Contents_3_1_1_2", "Contents__3, Contents-3"),
    ("확장자 없음", "Logo_x4", "Logo_x4.png"),
    ("닫힌 sibling vocab 단문자 OK", "RotationPanel/L /R /U /D", "(자유 명명 sibling 에선 금지)"),
    ("자유 명명 sibling 의미 슬러그", "BtnReset, BtnZoomIn", "R, Z (모호)"),
]
r = write_table(ws, r, ["Rule", "✅ Correct", "❌ Incorrect"], core, col_widths=[32, 36, 40])

r = section(ws, r, "[ Syntax ]")
ws.cell(row=r, column=1, value="<Family><Asset>[_<Direction>][_<State>]").font = Font(name="Consolas", size=11, bold=True)
r += 2
syntax = [
    ("Family", "UI Family Vocab (권장, 선택)", "GNB, LNB, Btn, Pnl, ..."),
    ("Asset", "자산 슬러그 (PascalCase)", "Start, Navi, Rotation"),
    ("Direction", "방향 단문자 (해당 시)", "L, R, U, D, CW, CCW"),
    ("State", "3-letter 축약", "Def, Prs, On, Off, Sel"),
]
r = write_table(ws, r, ["토큰", "설명", "예시"], syntax, col_widths=[14, 40, 30])

# ─────────────────────────────────────────────────────────────
# Sheet 4 — T3 System-Derived
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("T3 Derived")
r = title(ws, 1, "T3 — System-Derived Identifier")
r = note(ws, r, "사용자가 직접 명명하지 않는 객체 (머티리얼·중간 mesh 노드·texture object). AI grep·로그 단독 노출 빈도 높음 → prefix 유지가 가치 큼. 시스템 자동 파생 (Tier C) 이라 사용자 명명 부담 0.")

r = section(ws, r, "[ Format ]")
ws.cell(row=r, column=1, value="<kind>_<asset>[_<component>][_<channel|state>]").font = Font(name="Consolas", size=11, bold=True)
r += 2

r = section(ws, r, "[ Kind Prefix Table (3-letter) ]")
prefixes = [
    ("mdl_", "3D Model (mesh/node)", ".glb", "GLB BIN"),
    ("mat_", "Material", "(논리)", "materials[]"),
    ("tex_", "Texture (3D input)", ".png .jpg", "GLB BIN"),
    ("img_", "UI Image (2D)", ".png .webp", "GLB BIN"),
    ("aud_", "Audio", ".mp3 .wav", "extras.media[]"),
    ("vid_", "Video", ".mp4", "external"),
    ("evt_", "Event trigger", "(논리)", "VNT_Event"),
    ("scn_", "Scene container", "(논리)", "scene root"),
    ("nod_", "Generic group", "(논리)", "empty transform"),
]
r = write_table(ws, r, ["Prefix", "의미", "확장자", "저장 위치"], prefixes,
                col_widths=[10, 30, 18, 30])

r = section(ws, r, "[ Auto-Derivation Rule ]")
deriv = [
    ("일반 mirror", "source 이름의 prefix 만 교체", "img_gnb__active → mat_gnb__active"),
    ("1:N 채널 분기", "채널 suffix 부착", "tex_laptop__screen_albedo / _normal"),
    ("애니메이션 (v6 별도)", "primary channel target 분석", "Cupcake_Rot_R (T2 식별자, prefix 없음)"),
]
r = write_table(ws, r, ["케이스", "규칙", "예시"], deriv, col_widths=[18, 40, 50])

r = section(ws, r, "[ Texture Channel Suffix Vocab ]")
ch = [
    ("_albedo", "Base color / diffuse"),
    ("_normal", "Normal map"),
    ("_roughness", "Roughness"),
    ("_metallic", "Metallic"),
    ("_ao", "Ambient occlusion"),
    ("_emissive", "Emissive"),
    ("_height", "Height / displacement"),
    ("_opacity", "Alpha mask"),
    ("_orm", "Occlusion-Roughness-Metallic 합성"),
]
r = write_table(ws, r, ["Suffix", "의미"], ch, col_widths=[16, 50])

# ─────────────────────────────────────────────────────────────
# Sheet 5 — Animation
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("Animation")
r = title(ws, 1, "Animation Naming (v6)")
r = note(ws, r, "애니메이션은 animations[] 배열에 위치 — 타입이 위치로 선언되므로 prefix 없음. 한 클립이 여러 속성 (rotation/scale/translation/color/opacity) 을 동시에 변경 가능.")

r = section(ws, r, "[ Syntax ]")
ws.cell(row=r, column=1, value="<Target>_<Act1>[_<Dir1>][_<Act2>[_<Dir2>]]...").font = Font(name="Consolas", size=11, bold=True)
r += 1
ws.cell(row=r, column=1, value="다중 속성 순서: Rot → Scl → Mov → Clr → Op (결정론적)").font = Font(name="Malgun Gothic", size=10, italic=True)
r += 2

r = section(ws, r, "[ Action Vocab ]")
actions = [
    ("Rot", "Rotate", "rotation"),
    ("Scl", "Scale", "scale"),
    ("Mov", "Move", "translation"),
    ("Clr", "Color", "material color / texture switch"),
    ("Op", "Opacity", "alpha"),
]
r = write_table(ws, r, ["Abbr", "풀이", "채널 path"], actions, col_widths=[10, 16, 40])

r = section(ws, r, "[ Compound Short-forms (UX 패턴) ]")
compounds = [
    ("ZI", "Zoom In", "Scl + Mov (towards)"),
    ("ZO", "Zoom Out", "Scl + Mov (away)"),
    ("FI", "Fade In", "Op (0→1)"),
    ("FO", "Fade Out", "Op (1→0)"),
    ("Tx", "Transform (full)", "Rot + Scl + Mov"),
    ("Pop", "Pop (scale easing)", "Scl with bounce"),
]
r = write_table(ws, r, ["Abbr", "풀이", "채널 조합"], compounds, col_widths=[10, 20, 40])

r = section(ws, r, "[ Direction Vocab (Rot/Mov 에 부속) ]")
dirs_ = [
    ("L", "Left"),
    ("R", "Right"),
    ("U", "Up"),
    ("D", "Down"),
    ("CW", "Clockwise"),
    ("CCW", "Counter-clockwise"),
]
r = write_table(ws, r, ["Abbr", "의미"], dirs_, col_widths=[10, 30])

r = section(ws, r, "[ 실측 7개 default 애니메이션 변환 ]")
anim_ex = [
    ("new Clip (btn_start, scale)", "scale", "BtnStart_Scl"),
    ("new Clip (3D Model, rotation)", "rotation", "Cupcake_Rot_L"),
    ("new Clip1 (3D Model, rotation)", "rotation", "Cupcake_Rot_R"),
    ("new Clip2 (3D Model, rotation)", "rotation", "Cupcake_Rot_U"),
    ("new Clip3 (3D Model, rotation)", "rotation", "Cupcake_Rot_D"),
    ("new Clip4 (3D Model, scale+translation)", "scale+translation", "Cupcake_ZI"),
    ("new Clip5 (3D Model, scale)", "scale", "Cupcake_ZO"),
]
r = write_table(ws, r, ["현재 (default)", "채널·path", "v6"], anim_ex,
                col_widths=[42, 24, 22])

r = section(ws, r, "[ 다중 속성 예시 ]")
multi = [
    ("Cupcake_Rot_R_Clr", "오른쪽 회전 + 색상 변화"),
    ("BtnStart_Scl_FI", "스케일 + 페이드 인"),
    ("Cupcake_Tx_Clr", "전체 변환 + 색상"),
    ("Logo_Scl_FO", "로고 스케일 + 페이드 아웃"),
]
r = write_table(ws, r, ["이름", "의미"], multi, col_widths=[28, 50])

# ─────────────────────────────────────────────────────────────
# Sheet 6 — Vocab Tables (전체 통합)
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("Vocab Tables")
r = title(ws, 1, "Vocabulary Tables — 통합 참조")

r = section(ws, r, "[ UI Family Vocab (T2 인스턴스용, 권장) ]")
family = [
    ("GNB", "Global Navigation Bar", "Asset 불필요 (단독 사용 OK)"),
    ("LNB", "Local Navigation Bar", "Asset 불필요"),
    ("Btn", "Button (generic)", "Asset 필수"),
    ("Nav", "Navigation control (prev/next)", "Asset 불필요"),
    ("Pnl", "Panel / Background container", "Asset 불필요"),
    ("Ico", "Icon", "Asset 필수"),
    ("Bg", "Background image", "Asset 불필요"),
    ("Logo", "Logo / Brand mark", "Asset 불필요"),
    ("Tip", "Tooltip", "Asset 불필요"),
    ("Txt", "Text / Label (family, prefix 아님)", "Asset 필수"),
]
r = write_table(ws, r, ["Family", "의미", "Asset slug"], family, col_widths=[10, 38, 28])

r = section(ws, r, "[ State Vocab (3-letter PascalCase) ]")
state = [
    ("_Def", "Default", "기본"),
    ("_Prs", "Pressed", "눌림"),
    ("_On", "On (구 Active)", "활성/켜짐"),
    ("_Off", "Off (구 Disabled)", "비활성/꺼짐"),
    ("_Sel", "Selected", "선택됨"),
]
r = write_table(ws, r, ["Suffix", "풀이", "의미"], state, col_widths=[10, 24, 24])
r = note(ws, r, "v6 변경: _Hover / _Focused / _Highlight 제거 (VR/터치 환경 부재). _Active/_Disabled → _On/_Off 통합. 의미 분기는 VNT 컴포넌트 필드에서 처리.")

r = section(ws, r, "[ Direction Vocab (단문자) ]")
dirs_full = [
    ("_L", "Left", "Rot, Mov"),
    ("_R", "Right", "Rot, Mov"),
    ("_U", "Up", "Rot, Mov"),
    ("_D", "Down", "Rot, Mov"),
    ("_CW", "Clockwise", "Rot"),
    ("_CCW", "Counter-clockwise", "Rot"),
]
r = write_table(ws, r, ["Suffix", "의미", "적용 Act"], dirs_full, col_widths=[10, 24, 24])

r = section(ws, r, "[ Audio Category ]")
audio_c = [
    ("BGM", "Background Music", "배경음악"),
    ("SFX", "Sound Effect", "효과음 (UI 클릭·완료음·경고 등)"),
    ("NAR", "Narration", "내레이션·더빙 (구 VO)"),
]
r = write_table(ws, r, ["Category", "풀이", "의미"], audio_c, col_widths=[12, 24, 40])

r = section(ws, r, "[ Video Category ]")
video_c = [
    ("CUT", "Cutscene", "시네마틱·서사 영상 클립"),
    ("TUT", "Tutorial", "단계별 설명·튜토리얼 영상"),
    ("LOOP", "Looping", "반복 재생 배경 영상"),
    ("INTRO", "Intro", "콘텐츠 진입 인트로"),
    ("OUTRO", "Outro", "콘텐츠 종료 아웃트로"),
]
r = write_table(ws, r, ["Category", "풀이", "의미"], video_c, col_widths=[12, 18, 40])

r = section(ws, r, "[ PNG Role Token (T1 한정) ]")
role_v = [
    ("Sprite", "UI 스프라이트", "UI 이미지"),
    ("ALB", "Albedo / Base Color", "3D Texture"),
    ("NRM", "Normal Map", "3D Texture"),
    ("RGH", "Roughness Map", "3D Texture"),
    ("MET", "Metallic Map", "3D Texture"),
    ("EMI", "Emission Map", "3D Texture"),
    ("MSK", "Mask Map", "3D Texture"),
    ("AO", "Ambient Occlusion", "3D Texture"),
]
r = write_table(ws, r, ["Token", "의미", "용도"], role_v, col_widths=[12, 30, 24])

# ─────────────────────────────────────────────────────────────
# Sheet 7 — Examples (실측 변환 가이드)
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("Examples")
r = title(ws, 1, "변환 예시 가이드 — 실측 파일 기준")
r = note(ws, r, "Make Templete_20260512.make (513 노드) 의 실제 명명을 v6 로 변환. 각 행은 안티패턴 → 개선안 매핑.", span=5)

r = section(ws, r, "[ Scene Container & 위계 ]")
scene_ex = [
    ("SceneRoot", "SceneRoot", "T2 인스턴스", "예약어 유지"),
    ("Start", "Start", "T2 인스턴스", "변경 없음 (간결·의미 명확)"),
    ("Contents 1-1", "Contents_1_1", "T2 인스턴스", "공백 → _, 하이픈 → _"),
    ("Contents 3-1-1-2", "Contents_3_1_1_2", "T2 인스턴스", "4단계 위계 평탄화"),
    ("3D Model", "Stage_3D", "T2 인스턴스", "공백 제거 + 의미 부여"),
    ("0016", "Cupcake", "T2 인스턴스 (GLOSSARY)", "숫자 시작 식별자 → 의미 슬러그"),
]
r = write_table(ws, r, ["현재", "v6", "Tier", "변환 사유"], scene_ex,
                col_widths=[26, 28, 22, 36])

r = section(ws, r, "[ UI 이미지 인스턴스 ]")
ui_ex = [
    ("GNB_Active.png", "GNB_On", "T2", "확장자 제거, _Active → _On"),
    ("GNB_default.png", "GNB_Def", "T2", "PascalCase + 축약"),
    ("GNB_Disabled.png", "GNB_Off", "T2", "_Disabled → _Off"),
    ("GNB_Pressed.png", "GNB_Prs", "T2", "축약"),
    ("LNB_Active.png", "LNB_On", "T2", ""),
    ("btn_start.png", "BtnStart", "T2", "Family vocab Btn 적용"),
    ("btn_rotation_off.png", "BtnRotation_Off", "T2", ""),
    ("btn_rotation_on.png", "BtnRotation_On", "T2", ""),
    ("Tablet.png", "PnlTablet", "T2", "Family vocab Pnl 적용"),
    ("Navi.png", "PnlNav", "T2", "Navi → Nav 표기 일관성"),
    ("Logox4.png", "Logo_x4", "T2", "Family vocab Logo, 변형 표시 _x4"),
    ("tooltip.png", "Tip", "T2", "Family vocab Tip 단독"),
    ("Tablet.png 3", "PnlTablet_03", "T2", "Unity 자동 시퀀스 정규화"),
]
r = write_table(ws, r, ["현재", "v6", "Tier", "변환 사유"], ui_ex,
                col_widths=[28, 22, 8, 50])

r = section(ws, r, "[ 방향 컨트롤 (sibling 단문자 vocab) ]")
dir_ex = [
    ("L_btn_navi", "BtnNavi_L", "T2", "방향 prefix → suffix 단문자"),
    ("R_btn_navi", "BtnNavi_R", "T2", ""),
    ("L_btn_navi_Default.png", "BtnNavi_L_Def", "T2", "방향 + State 결합"),
    ("R_btn_navi_Presssed.png", "BtnNavi_R_Prs", "T2", "오타 교정 + 축약"),
    ("L_btn_navi_Highlight.png", "BtnNavi_L_Prs", "T2", "Highlight 제거 → Prs 대체"),
    ("L_rotation", "L", "T2 (sibling)", "부모 RotationPanel 컨텍스트, 단문자 OK"),
    ("R_rotation", "R", "T2 (sibling)", ""),
    ("U_rotation", "U", "T2 (sibling)", ""),
    ("D_rotation", "D", "T2 (sibling)", ""),
    ("R_rotation_Active.png", "R_On", "T2 (sibling)", "방향 단문자 + State"),
]
r = write_table(ws, r, ["현재", "v6", "Tier", "변환 사유"], dir_ex,
                col_widths=[30, 18, 16, 46])

r = section(ws, r, "[ Text / Tooltip 인스턴스 ]")
text_ex = [
    ("Text 1", "StartHeadline", "T2", "의미 부여 (txt_ prefix 미사용, Family Txt 만)"),
    ("txt_Navi_Title", "NavTitle", "T2", "T2 인스턴스 prefix 폐지"),
    ("txt_Navi_page", "NavPage", "T2", ""),
]
r = write_table(ws, r, ["현재", "v6", "Tier", "변환 사유"], text_ex,
                col_widths=[26, 22, 8, 50])

r = section(ws, r, "[ 머티리얼 (T3 시스템 파생) ]")
mat_ex = [
    ("UnlitOpaque (Instance) ×N", "mat_unlit_opaque", "T3 자동 파생", "(Instance) 사슬 제거"),
    ("(없음 — 263 머티리얼 distinct 19)", "mat_<primary_node_slug>", "T3 자동 파생", "사용 노드 분석"),
]
r = write_table(ws, r, ["현재", "v6", "Tier", "변환 사유"], mat_ex,
                col_widths=[36, 30, 16, 36])

r = section(ws, r, "[ 애니메이션 (배열 위치가 타입 선언, prefix 없음) ]")
anim_full = [
    ("new Clip (btn_start, scale)", "BtnStart_Scl", "(animations)", "Target + Act"),
    ("new Clip (3D Model, rotation)", "Cupcake_Rot_L", "(animations)", "Target + Act + Dir"),
    ("new Clip1 (3D Model, rotation)", "Cupcake_Rot_R", "(animations)", ""),
    ("new Clip2 (3D Model, rotation)", "Cupcake_Rot_U", "(animations)", ""),
    ("new Clip3 (3D Model, rotation)", "Cupcake_Rot_D", "(animations)", ""),
    ("new Clip4 (3D Model, scl+mov)", "Cupcake_ZI", "(animations)", "Compound Zoom In"),
    ("new Clip5 (3D Model, scale)", "Cupcake_ZO", "(animations)", "Compound Zoom Out"),
]
r = write_table(ws, r, ["현재", "v6", "Tier", "변환 사유"], anim_full,
                col_widths=[36, 22, 18, 30])

# ─────────────────────────────────────────────────────────────
# Sheet 8 — Checklist
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("Checklist")
r = title(ws, 1, "Validation Checklist (.make 익스포트 전, v6)")

r = section(ws, r, "[ T1 — Source Asset Filesystem ]")
t1_check = [
    ("파일명에 공백 없음", ""),
    ("구분자는 _ 만 (하이픈 0건)", ""),
    ("토큰별 PascalCase", ""),
    ("Variant _NN 2자리 고정", ""),
    ("Version marker _v<NN> 는 옵션·소스 파일에만", ""),
    ("확장자가 타입 선언 시 이름에 타입 토큰 중복 없음", ""),
    ("PNG Role 토큰 (Sprite/ALB/NRM/...) 필수", ""),
    ("Audio 카테고리 (BGM/SFX/NAR) 첫 토큰, _ 로 desc 구분", ""),
    ("Video 카테고리 (CUT/TUT/LOOP/INTRO/OUTRO) 첫 토큰, _ 로 desc 구분", ""),
    ("자식 부위 FBX 는 부모 이름 포함", ""),
    ("영문 전용 (한글 파일명 0건)", ""),
]
r = write_table(ws, r, ["검증 항목", "체크 [✓]"], t1_check, col_widths=[60, 14])

r = section(ws, r, "[ T2 — Instance ]")
t2_check = [
    ("T2 인스턴스에 kind prefix (mdl_/img_/txt_/aud_ 등) 0건", ""),
    ("모든 인스턴스명 PascalCase", ""),
    ("확장자 박제 0건 (*.png/*.fbx 노드명 없음)", ""),
    ("구분자 단일 _ 만 (이중 __ 0건, 하이픈 0건)", ""),
    ("State suffix 는 v6 vocab (_Def/_Prs/_On/_Off/_Sel) 내", ""),
    ("Direction suffix 는 v6 vocab (_L/_R/_U/_D/_CW/_CCW) 내", ""),
    ("단문자 sibling 은 닫힌 vocab 부모 컨텍스트에서만 사용", ""),
    ("UI Family vocab (GNB/LNB/Btn/Nav/Pnl/...) 적용 권장", ""),
    ("4단계 위계는 _ 로 평탄화 (Contents_3_1_1_2)", ""),
]
r = write_table(ws, r, ["검증 항목", "체크 [✓]"], t2_check, col_widths=[60, 14])

r = section(ws, r, "[ Animation ]")
anim_check = [
    ("애니메이션명에 prefix 없음 (<Target>_<Act>[_<Dir>] 패턴)", ""),
    ("Action 토큰이 v6 vocab (Rot/Scl/Mov/Clr/Op 또는 ZI/ZO/FI/FO/Tx/Pop) 내", ""),
    ("다중 속성 클립 토큰 순서 결정론적 (Rot → Scl → Mov → Clr → Op)", ""),
    ("'new Clip' 패턴 (Unity 기본값) 0건", ""),
]
r = write_table(ws, r, ["검증 항목", "체크 [✓]"], anim_check, col_widths=[60, 14])

r = section(ws, r, "[ T3 — System-Derived ]")
t3_check = [
    ("머티리얼명에 (Instance) 사슬 0건", ""),
    ("머티리얼 definition 만 의미 있는 이름", ""),
    ("Texture 채널 suffix (_albedo/_normal/...) 명시", ""),
    ("Mesh·텍스처 객체 prefix (mesh_/tex_) 유지", ""),
]
r = write_table(ws, r, ["검증 항목", "체크 [✓]"], t3_check, col_widths=[60, 14])

r = section(ws, r, "[ ID·Path·Privacy ]")
priv_check = [
    ("모든 ResourceID 가 UUID v4 포맷", ""),
    ("ResourceID 글로벌 유일 (중복 0건)", ""),
    ("공유본 OriginPath 에 사용자 홈 경로 없음 (C:\\Users\\, /home/)", ""),
    ("작성자 식별 정보 누설 없음", ""),
]
r = write_table(ws, r, ["검증 항목", "체크 [✓]"], priv_check, col_widths=[60, 14])

# ─────────────────────────────────────────────────────────────
# Sheet 9 — Anti-Patterns
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("Anti-Patterns")
r = title(ws, 1, "안티패턴 일람 — 실측 파일 기준")
r = note(ws, r, "Make Templete_20260512.make 분석에서 발견된 안티패턴. 모두 v6 검증에서 차단.", span=4)

anti = [
    ("노드명에 .png/.fbx 확장자 박제", "Logox4.png, btn_start.png", "Logo_x4, BtnStart", "Make Editor 아이콘이 타입 표현"),
    ("공백 포함 노드명", "Text 1, 3D Model, Contents 1-1", "StartHeadline, Stage_3D, Contents_1_1", "공백 → _ 또는 의미 부여"),
    ("(Instance) 사슬 머티리얼", "UnlitOpaque (Instance) ×N", "mat_unlit_opaque (T3 정규화)", "임포트 시 instance chain 제거"),
    ("이미지 이름이 UUID 문자열", "6c34f19e-9d40-...", "img_logox4 (Tier C 파생)", "ResourceID 별도, 이름은 의미"),
    ("'new Clip*' 기본 애니메이션", "new Clip, new Clip1, ...", "Cupcake_Rot_L, BtnStart_Scl", "Unity 기본값 차단"),
    ("숫자 시작 노드명", "0016", "Cupcake (GLOSSARY)", "식별자 정규식 위반"),
    ("오타", "L_btn_navi_Presssed.png", "BtnNavi_L_Prs", "정규화·축약"),
    ("하이픈 식별자", "LNB_3-1-1-1, Contents 3-1-1-2", "LNB_3_1_1_1, Contents_3_1_1_2", "하이픈 명시 금지"),
    ("로컬 절대경로 OriginPath", "C:\\Users\\VIRNECT\\Desktop\\...", "<HOME>/... 또는 OriginPath 제거", "정보 누설 방지"),
    ("한글 폴더 경로", "\\리소스\\모델\\...", "/resources/models/", "ASCII + GLOSSARY"),
    ("동일 노드명 sibling 대량 반복", "GNB_Active.png ×44", "GNB_On (parent 가 unique 화)", "트리 컨텍스트 활용"),
    ("Sprite 토큰 부재 (UI vs 3D 텍스처 혼동)", "Random.png", "Random_Sprite.png 또는 Random_ALB.png", "PNG 용도 명시"),
]
fills_anti = [BAD_FILL] * len(anti)
r = write_table(ws, r, ["문제", "현재", "v6 정정", "이유"], anti,
                col_widths=[38, 38, 38, 36])

# ─────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────
OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print(f"Wrote: {OUT}")
print(f"Sheets: {wb.sheetnames}")
