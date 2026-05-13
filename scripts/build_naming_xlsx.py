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

r = section(ws, r, "[ 이 문서를 읽기 전에 — 용어 안내 ]")
glossary = [
    ("원본 에셋 (Source Asset)", "모델러·디자이너가 만들어 전달하는 원본 파일. 예: .fbx, .png, .wav"),
    ("인스턴스 (Instance)", "Make Editor 안에 배치된 객체. 원본 파일을 씬에 가져다 놓은 것"),
    ("씬 트리 (Scene Tree)", "Make Editor 의 왼쪽 계층 구조. 부모-자식 관계로 객체가 묶여 있음"),
    ("앞 약자 / 뒤 약자", "이름 맨 앞 또는 맨 뒤에 붙는 짧은 표시 글자 (예: GNB_, _On)"),
    ("Vocab (정해진 단어 모음)", "허용된 단어 목록. 이 안에서만 골라 써야 함"),
    ("T1 / T2 / T3", "이 문서가 정한 세 단계: 원본 파일 / 배치된 인스턴스 / 자동 생성 객체"),
]
r = write_table(ws, r, ["용어", "쉽게 풀어 쓰기"], glossary, col_widths=[28, 80])

r = section(ws, r, "[ 이 규칙이 따르는 6가지 큰 원칙 ]")
principles = [
    ("1. 어디서 보는지에 따라 다르게", "OS 파일 탐색기 / Make Editor / 코드 검색 — 각자 보기 좋은 모양이 다름"),
    ("2. Make Editor 안의 이름은 짧게", "Make Editor 가 이미 아이콘으로 종류를 알려주므로 이름에 종류 표시 약자는 생략"),
    ("3. 부모-자식 관계는 트리로 표현", "부모 이름을 자식 이름에 반복해 적지 않음 — 트리가 이미 알려주니까"),
    ("4. 구분 기호는 언더바 _ 하나만", "이중 언더바 __ 와 하이픈 - 은 모두 사용 금지"),
    ("5. 약자로 짧게 쓰기", "상태·동작·방향 모두 정해진 짧은 약자로 (3글자 또는 1글자)"),
    ("6. 자동 생성 객체만 종류 표시", "사람이 직접 안 만지는 머티리얼·중간 노드만 mat_ 같은 약자 유지"),
]
r = write_table(ws, r, ["원칙", "쉬운 설명"], principles, col_widths=[34, 80])

r = section(ws, r, "[ 3단계 (T1 / T2 / T3) ]")
tiers = [
    ("T1", "원본 파일", "OS 파일 탐색기에서 보임", "PascalCase + 확장자 + (필요 시) 카테고리 약자", "GlassBottle_v01.fbx, GNB_Active.png, BGM_Tutorial_01.wav"),
    ("T2", "Make Editor 인스턴스", "Make Editor 의 씬 트리에서 보임", "PascalCase, 종류 약자 없음, 언더바 하나만", "GNB_Act, BtnStart, Cupcake, RotationPanel/L"),
    ("T3", "자동 생성 객체", "사람이 직접 안 만지는 머티리얼·중간 노드", "소문자_snake_case + 3글자 종류 약자", "mat_unlit_opaque, tex_cupcake_albedo"),
]
r = write_table(ws, r, ["단계", "무엇인지", "어디서 보이는지", "쓰는 모양", "예시"], tiers,
                col_widths=[6, 18, 34, 44, 50])

r = section(ws, r, "[ 시트 안내 ]")
sheets_info = [
    ("Overview", "이 시트 — 큰 원칙과 3단계 요약"),
    ("T1 Source", "원본 파일 이름 규칙 (3D 모델·이미지·소리·영상·폰트)"),
    ("T2 Instance", "Make Editor 인스턴스 이름 규칙 + 자주 쓰는 단어 모음"),
    ("T3 Derived", "자동으로 만들어지는 객체 이름 규칙"),
    ("Animation", "애니메이션 이름 규칙 + 동작·방향 약자 모음"),
    ("Vocab Tables", "약자·단어 모음 한눈에 보기"),
    ("Examples", "실제 파일을 v6 규칙으로 바꾼 비교표"),
    ("Checklist", "내보내기 전에 확인할 항목 (체크리스트)"),
    ("Anti-Patterns", "이렇게 쓰면 안 되는 예시"),
]
r = write_table(ws, r, ["시트", "내용"], sheets_info, col_widths=[18, 70])

# ─────────────────────────────────────────────────────────────
# Sheet 2 — T1 Source Asset
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("T1 Source")
r = title(ws, 1, "T1 — 원본 파일 이름 규칙")
r = note(ws, r, "모델러·디자이너가 만들어서 전달하는 원본 파일(작업 폴더에 있는 파일)에 적용. PascalCase 로 쓰고 확장자(.fbx, .png 등)를 붙임. 확장자가 종류를 알려주므로 이름 앞에 종류 약자(mdl_ 등)는 생략. 단, PNG·WAV·MP4 처럼 같은 확장자가 여러 용도로 쓰이는 경우에만 카테고리 약자를 이름 안에 넣음.")

r = section(ws, r, "[ 공통 규칙 ]")
rules = [
    ("이름에 공백을 넣지 않는다", "GlassBottle_v01.fbx", "Glass Bottle_v01.fbx"),
    ("구분 기호는 언더바 _ 만 (하이픈 - 금지)", "Contents_3_1_1_2", "Contents_3-1-1-2"),
    ("단어마다 첫 글자는 대문자 (PascalCase)", "BatteryPack", "batterypack / battery_pack"),
    ("변형 번호는 두 자리로 통일", "_01, _02", "_1, _001"),
    ("버전은 v + 두 자리 (선택 사항)", "_v01, _v02", "_V1, _ver01"),
    ("확장자가 알려주는 종류를 이름에 또 적지 않는다", "GlassBottle_v01.fbx", "GlassBottle_MOD_v01.fbx"),
    ("영문으로만 적기 (한글 파일명 금지)", "BatteryPack_v01", "배터리팩_v01"),
]
fills = [None] * len(rules)
r = write_table(ws, r, ["규칙", "✅ 이렇게 쓰세요", "❌ 이렇게 쓰지 마세요"], rules,
                col_widths=[44, 36, 36])

r = section(ws, r, "[ 파일 종류별 규칙 ]")

r = section(ws, r, "■ 3D 모델 (.fbx)")
note(ws, r, "확장자 .fbx 가 \"3D 모델\"이라는 종류를 알려줍니다. 이름에 또 적지 마세요. 자식 부품을 별도 파일로 보낼 때는 부모 이름을 함께 적어 어떤 모델의 부품인지 알 수 있게 하세요.")
r += 2
fbx = [
    ("GlassBottle_v01.fbx", "기본 모델"),
    ("GlassBottle_v02.fbx", "수정된 버전 (v02)"),
    ("GlassBottle_Open_v01.fbx", "다른 형태 (뚜껑 열린 버전)"),
    ("GlassBottle_Cap_v01.fbx", "자식 부품 — 부모 이름 포함"),
    ("BatteryPack_TopCover_v01.fbx", "자식 부품"),
]
r = write_table(ws, r, ["파일 이름", "쓰임새"], fbx, col_widths=[40, 50])

r = section(ws, r, "■ 이미지 — UI 스프라이트 (.png/.jpg)")
sprite = [
    ("종류 약자(Family) + 이름 + 상태", "GNB_Act.png, BtnNavi_L_Prs.png"),
    ("Family 만으로 충분할 때는 단독 사용 OK", "Logo.png, Tip.png, PnlTablet.png"),
    ("상태 약자는 정해진 5개 안에서만 사용", "GNB_On.png, GNB_Off.png"),
    ("방향은 한 글자로 (L/R/U/D)", "BtnNavi_L.png, Rotation_U.png"),
]
r = write_table(ws, r, ["규칙", "예시"], sprite, col_widths=[50, 50])

r = section(ws, r, "■ 이미지 — 3D 텍스처 (.png)")
note(ws, r, "용도 약자(Role)를 반드시 넣으세요. PNG 는 UI 와 3D 텍스처 둘 다에 쓰여서 확장자만으론 어디 쓰이는지 알 수 없기 때문입니다. 텍스처는 \"버전 표시 _v01\" 을 쓰지 않습니다 (디자이너가 자유롭게 갱신하는 아트 자산이므로).")
r += 2
roles = [
    ("Sprite", "UI 스프라이트 (버튼·아이콘 등)", "PlayBtn_Sprite_01.png"),
    ("ALB", "Albedo / 기본 색상 텍스처", "GlassBottle_ALB_01.png"),
    ("NRM", "Normal Map (표면 굴곡)", "GlassBottle_NRM_01.png"),
    ("RGH", "Roughness (거칠기)", "GlassBottle_RGH_01.png"),
    ("MET", "Metallic (금속성)", "GlassBottle_MET_01.png"),
    ("EMI", "Emission (자체 발광)", "GlassBottle_EMI_01.png"),
    ("MSK", "Mask (마스킹)", "GlassBottle_MSK_01.png"),
    ("AO", "Ambient Occlusion (음영)", "GlassBottle_AO_01.png"),
]
r = write_table(ws, r, ["약자", "의미", "예시"], roles, col_widths=[12, 36, 44])

r = section(ws, r, "■ 소리 (.wav / .mp3)")
note(ws, r, "형식: <카테고리>_<설명>_<번호>.확장자. 카테고리 약자와 설명 사이에 언더바 _ 를 한 번 넣습니다.")
r += 2
audio = [
    ("BGM", "배경 음악", "BGM_Tutorial_01.wav, BGM_Boss_01.wav"),
    ("SFX", "효과음 (버튼 클릭·완료음·경고음 등)", "SFX_UI_Click_01.wav, SFX_StepComplete_01.wav"),
    ("NAR", "내레이션·더빙 (이전 이름: VO)", "NAR_Intro_01.wav, NAR_Step01_Guide_01.wav"),
]
r = write_table(ws, r, ["카테고리", "의미", "예시"], audio, col_widths=[14, 44, 50])

r = section(ws, r, "■ 영상 (.mp4)")
video = [
    ("CUT", "컷씬 (서사·시네마틱 영상)", "CUT_AssemblyStep01_01.mp4"),
    ("TUT", "튜토리얼 (단계별 설명 영상)", "TUT_BatterySwap_Step01_01.mp4"),
    ("LOOP", "반복 재생되는 배경 영상", "LOOP_WorkshopBackground_01.mp4"),
    ("INTRO", "콘텐츠 시작 인트로", "INTRO_Main_01.mp4"),
    ("OUTRO", "콘텐츠 끝 아웃트로", "OUTRO_Credit_01.mp4"),
]
r = write_table(ws, r, ["카테고리", "의미", "예시"], video, col_widths=[14, 44, 50])

r = section(ws, r, "■ 폰트 (.ttf / .otf)")
fonts = [
    ("NotoSansKR_Bold_01.ttf", "폰트 이름 + 굵기"),
    ("NotoSansKR_Regular_01.ttf", ""),
    ("Roboto_Medium_01.ttf", ""),
]
r = write_table(ws, r, ["파일 이름", "구성"], fonts, col_widths=[40, 40])

# ─────────────────────────────────────────────────────────────
# Sheet 3 — T2 Instance
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("T2 Instance")
r = title(ws, 1, "T2 — Make Editor 인스턴스 이름 규칙")
r = note(ws, r, "Make Editor 의 씬 트리에 보이는, 사용자가 직접 이름을 짓는 객체입니다. 트리 옆 아이콘이 종류를 알려주므로 이름에 종류 약자(mdl_, img_ 같은 것) 는 생략합니다. 부모-자식 관계는 트리가 이미 보여주므로 자식 이름은 짧게 적습니다.")

r = section(ws, r, "[ 가장 중요한 규칙 ]")
core = [
    ("단어마다 첫 글자 대문자 (PascalCase)", "BtnStart, GNB_Act", "btn_start, gnb_act"),
    ("종류 약자 생략 (T2 에서만 해당)", "Cupcake", "mdl_cupcake"),
    ("언더바 _ 하나만 사용", "Contents_3_1_1_2", "Contents__3, Contents-3"),
    ("이름 끝에 확장자 안 붙이기", "Logo_x4", "Logo_x4.png"),
    ("정해진 4방향 자식은 한 글자로 OK", "RotationPanel 아래에 L /R /U /D", "(자유롭게 이름 짓는 형제 노드 사이에선 금지)"),
    ("자유 명명일 때는 의미 있는 이름", "BtnReset, BtnZoomIn", "R, Z (무슨 뜻인지 모름)"),
]
r = write_table(ws, r, ["규칙", "✅ 이렇게 쓰세요", "❌ 이렇게 쓰지 마세요"], core, col_widths=[40, 36, 40])

r = section(ws, r, "[ 이름 짜는 순서 ]")
ws.cell(row=r, column=1, value="<종류 약자><고유 이름>[_<방향>][_<상태>]").font = Font(name="Consolas", size=11, bold=True)
r += 2
syntax = [
    ("종류 약자 (Family)", "어떤 UI 인지 알려주는 짧은 약자 (선택 사항, 권장)", "GNB, LNB, Btn, Pnl, ..."),
    ("고유 이름", "이 객체만의 이름 (PascalCase)", "Start, Navi, Rotation"),
    ("방향", "방향 정보가 있을 때 한 글자로", "L, R, U, D, CW, CCW"),
    ("상태", "3글자 약자", "Def, Prs, On, Off, Sel"),
]
r = write_table(ws, r, ["부분", "설명", "예시"], syntax, col_widths=[18, 42, 30])

# ─────────────────────────────────────────────────────────────
# Sheet 4 — T3 System-Derived
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("T3 Derived")
r = title(ws, 1, "T3 — 자동 생성 객체 이름 규칙")
r = note(ws, r, "사용자가 직접 이름을 짓지 않는 객체입니다 (머티리얼·중간 mesh 노드·텍스처 등). 시스템이 자동으로 만들고, 사용자는 머티리얼 패널 등에서 가끔 본다는 정도. 이런 객체는 이름이 단독으로 로그·검색 결과에 나타나므로 종류 약자(mat_, tex_ 등)를 유지해 \"이게 뭔지\" 알 수 있게 합니다.")

r = section(ws, r, "[ 이름 형식 ]")
ws.cell(row=r, column=1, value="<종류약자>_<이름>[_<부위>][_<채널 또는 상태>]").font = Font(name="Consolas", size=11, bold=True)
r += 2

r = section(ws, r, "[ 종류 약자 (3글자) ]")
prefixes = [
    ("mdl_", "3D 모델 (mesh/node)", ".glb", "GLB BIN"),
    ("mat_", "머티리얼 (재질)", "(개념상)", "materials[]"),
    ("tex_", "텍스처 (3D 모델 표면용)", ".png .jpg", "GLB BIN"),
    ("img_", "UI 이미지 (2D)", ".png .webp", "GLB BIN"),
    ("aud_", "오디오", ".mp3 .wav", "extras.media[]"),
    ("vid_", "비디오", ".mp4", "외부 파일"),
    ("evt_", "이벤트 트리거", "(개념상)", "VNT_Event"),
    ("scn_", "씬 컨테이너", "(개념상)", "scene root"),
    ("nod_", "일반 그룹", "(개념상)", "빈 transform"),
]
r = write_table(ws, r, ["약자", "의미", "확장자", "저장 위치"], prefixes,
                col_widths=[10, 32, 18, 30])

r = section(ws, r, "[ 자동으로 이름 만드는 방법 ]")
deriv = [
    ("기본 (1:1)", "원본 이름의 약자만 바꿔치기", "img_gnb__active → mat_gnb__active"),
    ("하나의 원본이 여러 곳에 쓰일 때", "채널 약자를 뒤에 붙임", "tex_laptop__screen_albedo / _normal"),
    ("애니메이션 (v6 별도 규칙)", "주로 어떤 노드를 움직이는지 분석", "Cupcake_Rot_R (T2 이름, 종류 약자 없음)"),
]
r = write_table(ws, r, ["상황", "규칙", "예시"], deriv, col_widths=[24, 40, 50])

r = section(ws, r, "[ 텍스처 채널 뒤 약자 ]")
ch = [
    ("_albedo", "기본 색상 (Base color / diffuse)"),
    ("_normal", "표면 굴곡 (Normal map)"),
    ("_roughness", "거칠기"),
    ("_metallic", "금속성"),
    ("_ao", "음영 (Ambient occlusion)"),
    ("_emissive", "자체 발광"),
    ("_height", "높낮이 (Height / displacement)"),
    ("_opacity", "투명도 (Alpha mask)"),
    ("_orm", "음영·거칠기·금속성 합쳐 놓은 텍스처"),
]
r = write_table(ws, r, ["뒤 약자", "의미"], ch, col_widths=[16, 60])

# ─────────────────────────────────────────────────────────────
# Sheet 5 — Animation
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("Animation")
r = title(ws, 1, "애니메이션 이름 규칙 (v6)")
r = note(ws, r, "애니메이션은 \"애니메이션 목록\"이라는 별도 공간에 들어 있어서 종류 약자가 필요 없습니다. 하나의 애니메이션이 회전·크기·위치·색상·투명도 등 여러 속성을 동시에 바꿀 수 있습니다.")

r = section(ws, r, "[ 이름 짜는 순서 ]")
ws.cell(row=r, column=1, value="<움직일 대상>_<동작1>[_<방향1>][_<동작2>[_<방향2>]]...").font = Font(name="Consolas", size=11, bold=True)
r += 1
ws.cell(row=r, column=1, value="여러 동작이 섞일 때 적는 순서: 회전 → 크기 → 이동 → 색상 → 투명도").font = Font(name="Malgun Gothic", size=10, italic=True)
r += 2

r = section(ws, r, "[ 동작 약자 ]")
actions = [
    ("Rot", "Rotate (회전)", "회전축이 바뀜"),
    ("Scl", "Scale (크기)", "크기가 바뀜"),
    ("Mov", "Move (이동)", "위치가 바뀜"),
    ("Clr", "Color (색상)", "재질 색상 / 텍스처 교체"),
    ("Op", "Opacity (투명도)", "투명/불투명 변화"),
]
r = write_table(ws, r, ["약자", "풀이", "어떤 동작인지"], actions, col_widths=[10, 22, 40])

r = section(ws, r, "[ 자주 쓰는 동작 묶음 (한 줄로 줄인 형태) ]")
compounds = [
    ("ZI", "Zoom In (확대)", "크기 + 이동 (가까이 오기)"),
    ("ZO", "Zoom Out (축소)", "크기 + 이동 (멀어지기)"),
    ("FI", "Fade In (서서히 나타남)", "투명도 0→1"),
    ("FO", "Fade Out (서서히 사라짐)", "투명도 1→0"),
    ("Tx", "Transform (전체 변형)", "회전 + 크기 + 이동"),
    ("Pop", "Pop (튕기듯 등장)", "크기에 바운스 효과"),
]
r = write_table(ws, r, ["약자", "풀이", "어떤 조합인지"], compounds, col_widths=[10, 28, 40])

r = section(ws, r, "[ 방향 약자 (회전·이동에 함께 사용) ]")
dirs_ = [
    ("L", "Left (왼쪽)"),
    ("R", "Right (오른쪽)"),
    ("U", "Up (위)"),
    ("D", "Down (아래)"),
    ("CW", "Clockwise (시계 방향)"),
    ("CCW", "Counter-clockwise (반시계 방향)"),
]
r = write_table(ws, r, ["약자", "의미"], dirs_, col_widths=[10, 40])

r = section(ws, r, "[ 실제 파일의 \"new Clip\" 7개를 v6 로 바꾼 예 ]")
anim_ex = [
    ("new Clip (btn_start, 크기)", "크기 변화", "BtnStart_Scl"),
    ("new Clip (3D Model, 회전)", "회전", "Cupcake_Rot_L"),
    ("new Clip1 (3D Model, 회전)", "회전", "Cupcake_Rot_R"),
    ("new Clip2 (3D Model, 회전)", "회전", "Cupcake_Rot_U"),
    ("new Clip3 (3D Model, 회전)", "회전", "Cupcake_Rot_D"),
    ("new Clip4 (3D Model, 크기+이동)", "크기 + 이동", "Cupcake_ZI"),
    ("new Clip5 (3D Model, 크기)", "크기 변화", "Cupcake_ZO"),
]
r = write_table(ws, r, ["현재 이름 (기본값)", "어떤 속성이 바뀌나", "v6"], anim_ex,
                col_widths=[42, 28, 22])

r = section(ws, r, "[ 여러 속성이 섞인 경우 ]")
multi = [
    ("Cupcake_Rot_R_Clr", "오른쪽 회전 + 색상 변화"),
    ("BtnStart_Scl_FI", "크기 변화 + 서서히 나타남"),
    ("Cupcake_Tx_Clr", "전체 변형 + 색상 변화"),
    ("Logo_Scl_FO", "로고 크기 변화 + 서서히 사라짐"),
]
r = write_table(ws, r, ["이름", "의미"], multi, col_widths=[28, 56])

# ─────────────────────────────────────────────────────────────
# Sheet 6 — Vocab Tables (전체 통합)
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("Vocab Tables")
r = title(ws, 1, "약자·단어 모음 한눈에 보기")

r = section(ws, r, "[ UI 종류 약자 (T2 인스턴스용, 권장) ]")
family = [
    ("GNB", "Global Navigation Bar (전체 메뉴바)", "이름 추가 안 해도 됨"),
    ("LNB", "Local Navigation Bar (하위 메뉴바)", "이름 추가 안 해도 됨"),
    ("Btn", "Button (버튼)", "이름 반드시 함께"),
    ("Nav", "Navigation control (앞/뒤 이동 버튼)", "이름 추가 안 해도 됨"),
    ("Pnl", "Panel / Background container (패널·배경판)", "이름 추가 안 해도 됨"),
    ("Ico", "Icon (아이콘)", "이름 반드시 함께"),
    ("Bg", "Background image (배경 이미지)", "이름 추가 안 해도 됨"),
    ("Logo", "Logo / Brand mark (로고)", "이름 추가 안 해도 됨"),
    ("Tip", "Tooltip (말풍선·도움말)", "이름 추가 안 해도 됨"),
    ("Txt", "Text / Label (텍스트·라벨)", "이름 반드시 함께"),
]
r = write_table(ws, r, ["약자", "의미", "이름이 함께 필요한지"], family, col_widths=[10, 44, 32])

r = section(ws, r, "[ 상태 약자 (3글자) ]")
state = [
    ("_Def", "Default", "기본 상태"),
    ("_Prs", "Pressed", "눌려 있는 상태"),
    ("_On", "On (이전: Active)", "켜짐 / 활성 상태"),
    ("_Off", "Off (이전: Disabled)", "꺼짐 / 비활성 상태"),
    ("_Sel", "Selected", "선택된 상태"),
]
r = write_table(ws, r, ["약자", "풀이", "의미"], state, col_widths=[10, 26, 30])
r = note(ws, r, "v6 에서 바뀐 점: _Hover / _Focused / _Highlight 제거 (VR·터치 환경에서는 마우스 호버·포커스가 없음). _Active 와 _Disabled 는 _On / _Off 로 통합. \"왜 꺼졌나\" 같은 세부 구분은 이름 대신 VNT 설정 항목에서 처리.")

r = section(ws, r, "[ 방향 약자 (한 글자) ]")
dirs_full = [
    ("_L", "Left (왼쪽)", "회전 · 이동"),
    ("_R", "Right (오른쪽)", "회전 · 이동"),
    ("_U", "Up (위)", "회전 · 이동"),
    ("_D", "Down (아래)", "회전 · 이동"),
    ("_CW", "Clockwise (시계 방향)", "회전"),
    ("_CCW", "Counter-clockwise (반시계 방향)", "회전"),
]
r = write_table(ws, r, ["약자", "의미", "쓰는 곳"], dirs_full, col_widths=[10, 30, 24])

r = section(ws, r, "[ 오디오 카테고리 ]")
audio_c = [
    ("BGM", "Background Music", "배경음악"),
    ("SFX", "Sound Effect", "효과음 (UI 클릭·완료음·경고음 등)"),
    ("NAR", "Narration", "내레이션·더빙 (이전 이름: VO)"),
]
r = write_table(ws, r, ["카테고리", "풀이", "의미"], audio_c, col_widths=[12, 24, 44])

r = section(ws, r, "[ 비디오 카테고리 ]")
video_c = [
    ("CUT", "Cutscene", "서사·시네마틱 영상 클립"),
    ("TUT", "Tutorial", "단계별 설명·튜토리얼 영상"),
    ("LOOP", "Looping", "반복 재생 배경 영상"),
    ("INTRO", "Intro", "콘텐츠 시작 인트로"),
    ("OUTRO", "Outro", "콘텐츠 끝 아웃트로"),
]
r = write_table(ws, r, ["카테고리", "풀이", "의미"], video_c, col_widths=[12, 18, 44])

r = section(ws, r, "[ PNG 용도 약자 (T1 — 원본 파일에서만 사용) ]")
role_v = [
    ("Sprite", "UI 스프라이트 (버튼·아이콘 등)", "UI 이미지"),
    ("ALB", "Albedo / 기본 색상", "3D 텍스처"),
    ("NRM", "Normal Map (표면 굴곡)", "3D 텍스처"),
    ("RGH", "Roughness (거칠기)", "3D 텍스처"),
    ("MET", "Metallic (금속성)", "3D 텍스처"),
    ("EMI", "Emission (자체 발광)", "3D 텍스처"),
    ("MSK", "Mask (마스킹)", "3D 텍스처"),
    ("AO", "Ambient Occlusion (음영)", "3D 텍스처"),
]
r = write_table(ws, r, ["약자", "의미", "어디 쓰이는지"], role_v, col_widths=[12, 36, 24])

# ─────────────────────────────────────────────────────────────
# Sheet 7 — Examples (실측 변환 가이드)
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("Examples")
r = title(ws, 1, "실제 파일을 v6 규칙으로 바꾼 비교표")
r = note(ws, r, "실제 파일(Make Templete_20260512.make, 노드 513개)의 이름을 v6 규칙으로 바꾼 예시입니다. 각 행은 \"현재 이름 → v6 이름 + 왜 바꾸는지\" 입니다.", span=5)

r = section(ws, r, "[ 씬·페이지·계층 ]")
scene_ex = [
    ("SceneRoot", "SceneRoot", "T2 인스턴스", "시스템 예약 이름 — 그대로 유지"),
    ("Start", "Start", "T2 인스턴스", "이미 짧고 의미가 명확함 — 그대로 유지"),
    ("Contents 1-1", "Contents_1_1", "T2 인스턴스", "공백·하이픈 → 언더바로 통일"),
    ("Contents 3-1-1-2", "Contents_3_1_1_2", "T2 인스턴스", "4단계 위계도 언더바로 평탄화"),
    ("3D Model", "Stage_3D", "T2 인스턴스", "공백 제거 + 의미 있는 이름 부여"),
    ("0016", "Cupcake", "T2 인스턴스 (용어집 등록)", "숫자로 시작하는 이름 → 의미 있는 이름으로"),
]
r = write_table(ws, r, ["현재 이름", "v6 이름", "단계", "왜 바꾸나"], scene_ex,
                col_widths=[26, 28, 22, 36])

r = section(ws, r, "[ UI 이미지 인스턴스 ]")
ui_ex = [
    ("GNB_Active.png", "GNB_On", "T2", "확장자 제거, _Active → _On"),
    ("GNB_default.png", "GNB_Def", "T2", "PascalCase + 축약형으로"),
    ("GNB_Disabled.png", "GNB_Off", "T2", "_Disabled → _Off"),
    ("GNB_Pressed.png", "GNB_Prs", "T2", "축약형으로"),
    ("LNB_Active.png", "LNB_On", "T2", ""),
    ("btn_start.png", "BtnStart", "T2", "Family 약자 Btn 사용"),
    ("btn_rotation_off.png", "BtnRotation_Off", "T2", ""),
    ("btn_rotation_on.png", "BtnRotation_On", "T2", ""),
    ("Tablet.png", "PnlTablet", "T2", "Family 약자 Pnl(패널) 사용"),
    ("Navi.png", "PnlNav", "T2", "Navi → Nav 로 표기 통일"),
    ("Logox4.png", "Logo_x4", "T2", "Family 약자 Logo, 변형 표시는 _x4"),
    ("tooltip.png", "Tip", "T2", "Family 약자 Tip 단독 사용"),
    ("Tablet.png 3", "PnlTablet_03", "T2", "Unity 가 자동으로 붙인 번호를 정리"),
]
r = write_table(ws, r, ["현재 이름", "v6 이름", "단계", "왜 바꾸나"], ui_ex,
                col_widths=[28, 22, 8, 50])

r = section(ws, r, "[ 방향이 있는 컨트롤 (형제 노드 한 글자 사용) ]")
dir_ex = [
    ("L_btn_navi", "BtnNavi_L", "T2", "방향을 앞이 아닌 뒤에 한 글자로"),
    ("R_btn_navi", "BtnNavi_R", "T2", ""),
    ("L_btn_navi_Default.png", "BtnNavi_L_Def", "T2", "방향 + 상태 결합"),
    ("R_btn_navi_Presssed.png", "BtnNavi_R_Prs", "T2", "오타 교정 + 축약"),
    ("L_btn_navi_Highlight.png", "BtnNavi_L_Prs", "T2", "Highlight 약자 제거 → Prs 로 대체"),
    ("L_rotation", "L", "T2 (형제 노드)", "부모(RotationPanel) 컨텍스트가 있어 한 글자만으로 OK"),
    ("R_rotation", "R", "T2 (형제 노드)", ""),
    ("U_rotation", "U", "T2 (형제 노드)", ""),
    ("D_rotation", "D", "T2 (형제 노드)", ""),
    ("R_rotation_Active.png", "R_On", "T2 (형제 노드)", "방향 + 상태"),
]
r = write_table(ws, r, ["현재 이름", "v6 이름", "단계", "왜 바꾸나"], dir_ex,
                col_widths=[30, 18, 18, 46])

r = section(ws, r, "[ 텍스트·말풍선 인스턴스 ]")
text_ex = [
    ("Text 1", "StartHeadline", "T2", "의미 있는 이름 부여 (T2 에선 txt_ 같은 종류 약자 안 씀)"),
    ("txt_Navi_Title", "NavTitle", "T2", "T2 에서는 txt_ 같은 종류 약자 생략"),
    ("txt_Navi_page", "NavPage", "T2", ""),
]
r = write_table(ws, r, ["현재 이름", "v6 이름", "단계", "왜 바꾸나"], text_ex,
                col_widths=[26, 22, 8, 50])

r = section(ws, r, "[ 머티리얼 (T3 — 자동 생성) ]")
mat_ex = [
    ("UnlitOpaque (Instance) ×N", "mat_unlit_opaque", "T3 자동 생성", "(Instance) 사슬 제거"),
    ("(현재 263개 중 의미 중복 19개)", "mat_<쓰이는 노드 이름>", "T3 자동 생성", "어떤 노드에 쓰이는지 분석해서 이름 부여"),
]
r = write_table(ws, r, ["현재 이름", "v6 이름", "단계", "왜 바꾸나"], mat_ex,
                col_widths=[36, 30, 18, 36])

r = section(ws, r, "[ 애니메이션 (애니메이션 목록에 들어가므로 종류 약자 없음) ]")
anim_full = [
    ("new Clip (btn_start, 크기)", "BtnStart_Scl", "(애니메이션)", "대상 + 동작"),
    ("new Clip (3D Model, 회전)", "Cupcake_Rot_L", "(애니메이션)", "대상 + 동작 + 방향"),
    ("new Clip1 (3D Model, 회전)", "Cupcake_Rot_R", "(애니메이션)", ""),
    ("new Clip2 (3D Model, 회전)", "Cupcake_Rot_U", "(애니메이션)", ""),
    ("new Clip3 (3D Model, 회전)", "Cupcake_Rot_D", "(애니메이션)", ""),
    ("new Clip4 (3D Model, 크기+이동)", "Cupcake_ZI", "(애니메이션)", "Zoom In 합친 형태"),
    ("new Clip5 (3D Model, 크기)", "Cupcake_ZO", "(애니메이션)", "Zoom Out 합친 형태"),
]
r = write_table(ws, r, ["현재 이름", "v6 이름", "단계", "왜 바꾸나"], anim_full,
                col_widths=[36, 22, 18, 30])

# ─────────────────────────────────────────────────────────────
# Sheet 8 — Checklist
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("Checklist")
r = title(ws, 1, "내보내기 전에 확인할 항목 (v6 체크리스트)")
r = note(ws, r, ".make 파일을 만들기 전에 한 번씩 확인하세요. 모든 항목에 ✓ 가 들어가면 v6 규칙을 잘 따른 파일입니다.", span=2)

r = section(ws, r, "[ T1 — 원본 파일 ]")
t1_check = [
    ("파일 이름에 공백이 없는가", ""),
    ("구분자가 언더바 _ 만 쓰이는가 (하이픈 - 없음)", ""),
    ("단어마다 첫 글자가 대문자인가 (PascalCase)", ""),
    ("변형 번호가 두 자리인가 (_01, _02)", ""),
    ("버전 표시 _v01 은 원본 파일에만 쓰이는가", ""),
    ("확장자가 알려주는 종류를 이름에 또 적지 않았는가", ""),
    ("PNG 에 용도 약자 (Sprite/ALB/NRM/...) 가 있는가", ""),
    ("오디오 카테고리 (BGM/SFX/NAR) 가 맨 앞에 _ 와 함께 있는가", ""),
    ("비디오 카테고리 (CUT/TUT/LOOP/INTRO/OUTRO) 가 맨 앞에 _ 와 함께 있는가", ""),
    ("자식 부품 FBX 에 부모 이름이 포함되어 있는가", ""),
    ("한글 파일명이 없는가 (영문만)", ""),
]
r = write_table(ws, r, ["확인 항목", "체크 [✓]"], t1_check, col_widths=[64, 14])

r = section(ws, r, "[ T2 — Make Editor 인스턴스 ]")
t2_check = [
    ("종류 약자 (mdl_/img_/txt_/aud_ 등) 가 없는가", ""),
    ("모든 인스턴스명이 PascalCase 로 적혀 있는가", ""),
    ("이름 끝에 확장자 (.png/.fbx 등) 가 안 붙어 있는가", ""),
    ("구분자가 언더바 _ 하나만 쓰이는가 (이중 __ 없음, 하이픈 없음)", ""),
    ("상태 약자가 정해진 5개 (_Def/_Prs/_On/_Off/_Sel) 안에 있는가", ""),
    ("방향 약자가 정해진 6개 (_L/_R/_U/_D/_CW/_CCW) 안에 있는가", ""),
    ("한 글자 형제 노드는 정해진 4방향 같은 묶음에서만 쓰이는가", ""),
    ("UI 종류 약자 (GNB/LNB/Btn/Nav/Pnl/...) 를 사용했는가 (권장)", ""),
    ("4단계 위계가 하이픈 대신 언더바로 적혀 있는가 (Contents_3_1_1_2)", ""),
]
r = write_table(ws, r, ["확인 항목", "체크 [✓]"], t2_check, col_widths=[64, 14])

r = section(ws, r, "[ 애니메이션 ]")
anim_check = [
    ("애니메이션 이름이 <대상>_<동작>[_<방향>] 형태인가", ""),
    ("동작 약자가 정해진 단어 (Rot/Scl/Mov/Clr/Op 또는 ZI/ZO/FI/FO/Tx/Pop) 안에 있는가", ""),
    ("여러 속성이 섞일 때 순서가 회전→크기→이동→색상→투명도 인가", ""),
    ("'new Clip' 같은 Unity 기본값 이름이 남아 있지 않은가", ""),
]
r = write_table(ws, r, ["확인 항목", "체크 [✓]"], anim_check, col_widths=[64, 14])

r = section(ws, r, "[ T3 — 자동 생성 객체 ]")
t3_check = [
    ("머티리얼 이름에 (Instance) 가 반복되어 있지 않은가", ""),
    ("머티리얼은 원본 정의만 의미 있는 이름인가", ""),
    ("텍스처 끝 약자 (_albedo/_normal 등) 가 명시되어 있는가", ""),
    ("Mesh·텍스처 객체에 종류 약자 (mesh_/tex_) 가 유지되는가", ""),
]
r = write_table(ws, r, ["확인 항목", "체크 [✓]"], t3_check, col_widths=[64, 14])

r = section(ws, r, "[ ID·경로·개인정보 ]")
priv_check = [
    ("모든 ResourceID 가 UUID v4 형식인가", ""),
    ("ResourceID 가 파일 전체에서 중복되지 않는가", ""),
    ("외부 공유본의 OriginPath 에 사용자 홈 경로 (C:\\Users\\, /home/) 가 없는가", ""),
    ("작성자 식별 정보 (이메일·계정명 등) 가 누설되지 않는가", ""),
]
r = write_table(ws, r, ["확인 항목", "체크 [✓]"], priv_check, col_widths=[64, 14])

# ─────────────────────────────────────────────────────────────
# Sheet 9 — Anti-Patterns
# ─────────────────────────────────────────────────────────────
ws = wb.create_sheet("Anti-Patterns")
r = title(ws, 1, "이렇게 쓰면 안 되는 예시")
r = note(ws, r, "실제 파일(Make Templete_20260512.make) 분석에서 찾은 잘못된 이름들입니다. v6 규칙에서는 모두 막거나 자동으로 고쳐집니다.", span=4)

anti = [
    ("노드 이름에 .png/.fbx 같은 확장자가 붙어 있음", "Logox4.png, btn_start.png", "Logo_x4, BtnStart", "Make Editor 아이콘이 종류를 알려주므로 확장자 불필요"),
    ("공백이 들어간 노드 이름", "Text 1, 3D Model, Contents 1-1", "StartHeadline, Stage_3D, Contents_1_1", "공백을 언더바 _ 로 바꾸거나 의미 있는 이름으로"),
    ("(Instance) 가 계속 반복된 머티리얼 이름", "UnlitOpaque (Instance) ×N", "mat_unlit_opaque (T3 자동 정리)", "내보낼 때 자동으로 instance 사슬 제거"),
    ("이미지 이름이 알 수 없는 UUID 문자열", "6c34f19e-9d40-...", "img_logox4 (자동 생성)", "UUID 는 ID 로만 쓰고, 이름은 의미 있게"),
    ("'new Clip' 같은 Unity 기본값 애니메이션 이름", "new Clip, new Clip1, ...", "Cupcake_Rot_L, BtnStart_Scl", "Unity 기본값 그대로 두지 말 것"),
    ("숫자로 시작하는 노드 이름", "0016", "Cupcake (용어집에 등록)", "이름은 영문 글자로 시작"),
    ("오타", "L_btn_navi_Presssed.png", "BtnNavi_L_Prs", "정정 + 축약형으로"),
    ("하이픈 - 이 들어간 이름", "LNB_3-1-1-1, Contents 3-1-1-2", "LNB_3_1_1_1, Contents_3_1_1_2", "하이픈은 사용 금지"),
    ("OriginPath 에 작성자 PC 경로가 그대로 남음", "C:\\Users\\VIRNECT\\Desktop\\...", "<HOME>/... 또는 OriginPath 자체 제거", "개인정보·환경 정보 누설 방지"),
    ("폴더 경로에 한글이 들어감", "\\리소스\\모델\\...", "/resources/models/", "영문으로 통일, 한글 용어는 용어집에"),
    ("같은 이름이 형제 노드에 대량 중복", "GNB_Active.png 가 44번 반복", "GNB_On (부모 이름으로 구별)", "부모-자식 트리 컨텍스트로 구별"),
    ("PNG 용도 약자가 빠짐 (UI 인지 3D 텍스처인지 모름)", "Random.png", "Random_Sprite.png 또는 Random_ALB.png", "PNG 는 어디 쓰이는지 약자로 명시"),
]
fills_anti = [BAD_FILL] * len(anti)
r = write_table(ws, r, ["문제", "현재", "v6 에서는", "이유"], anti,
                col_widths=[44, 38, 38, 44])

# ─────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────
OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print(f"Wrote: {OUT}")
print(f"Sheets: {wb.sheetnames}")
