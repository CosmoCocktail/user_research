import streamlit as st
import pandas as pd
import ast
import os
from openpyxl import load_workbook, Workbook

# ======================
# 페이지 설정
# ======================
st.set_page_config(
    page_title="팀플 빌런즈 : 눈 속 마을 빌런 테스트",
    page_icon="🐧",
    layout="centered"
)

# ======================
# 상수
# ======================
QUESTION_FILE = "questions.xlsx"
RESULT_FILE = "result.xlsx"
CHARACTERS = ["에디", "크롱", "뽀로로", "루피", "포비"]

# ======================
# 데이터 로드
# ======================
@st.cache_data
def load_questions():
    df = pd.read_excel(QUESTION_FILE)
    return df

questions_df = load_questions()

# ======================
# result.xlsx 저장 함수
# ======================
def save_result(character: str):
    """
    result.xlsx 구조 (단일 행 누적):
    행1 헤더: 에디 | 크롱 | 뽀로로 | 루피 | 포비
    행2 값  :  3  |  5  |   2   |  7  |  4

    참여 완료 시 결과 캐릭터 열의 값 +1 갱신
    """
    if os.path.exists(RESULT_FILE):
        wb = load_workbook(RESULT_FILE)
        ws = wb.active

        # 헤더 행에서 캐릭터 열 위치 파악
        header = [cell.value for cell in ws[1]]

        if character in header:
            col_idx = header.index(character) + 1  # openpyxl은 1-based
            current_val = ws.cell(row=2, column=col_idx).value or 0
            ws.cell(row=2, column=col_idx).value = current_val + 1
        
    else:
        # 파일 없으면 헤더 + 초기값 행 생성
        wb = Workbook()
        ws = wb.active
        ws.append(CHARACTERS)                          # 행1: 헤더 (캐릭터명)
        init_row = [1 if c == character else 0 for c in CHARACTERS]
        ws.append(init_row)                            # 행2: 누적 카운트

    wb.save(RESULT_FILE)

# ======================
# result.xlsx 집계 함수
# ======================
def load_result_counts():
    """
    행2의 각 캐릭터 카운트 값을 읽어
    - counts: {캐릭터: 카운트}
    - total: 전체 합계 (= 총 참여자 수)
    반환
    """
    if not os.path.exists(RESULT_FILE):
        return {c: 0 for c in CHARACTERS}, 0

    df = pd.read_excel(RESULT_FILE, header=0)

    # 열 이름이 CHARACTERS와 일치하는지 확인
    if not all(c in df.columns for c in CHARACTERS):
        return {c: 0 for c in CHARACTERS}, 0

    # 첫 번째 데이터 행(행2)에서 카운트 읽기
    counts = {c: int(df[c].iloc[0]) for c in CHARACTERS}
    total = sum(counts.values())
    return counts, total

# ======================
# 점수 파싱 함수
# ======================
def parse_types(type_str: str) -> list:
    try:
        cleaned = type_str.strip()
        result = ast.literal_eval(cleaned)
        return [r.strip() for r in result]
    except Exception:
        return []

# ======================
# 세션 초기화
# ======================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "question_idx" not in st.session_state:
    st.session_state.question_idx = 0

if "scores" not in st.session_state:
    st.session_state.scores = {c: 0 for c in CHARACTERS}

if "result_character" not in st.session_state:
    st.session_state.result_character = None

if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

# ======================
# 공통 스타일
# ======================
st.markdown("""
    <style>
        .big-title {
            text-align: center;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .sub-title {
            text-align: center;
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 1.5rem;
        }
        .question-text {
            text-align: center;
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }
        .progress-text {
            text-align: center;
            font-size: 0.9rem;
            color: #888;
            margin-bottom: 0.5rem;
        }
        .result-character {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 900;
            margin: 1rem 0;
        }
        .stat-box {
            background-color: #f0f4ff;
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1rem;
            text-align: center;
        }
        .stat-title {
            font-size: 1rem;
            color: #444;
            margin-bottom: 0.5rem;
        }
        .stat-total {
            font-size: 1.6rem;
            font-weight: 800;
            color: #3355ff;
        }
    </style>
""", unsafe_allow_html=True)

# ======================
# 홈 페이지
# ======================
if st.session_state.page == "home":

    st.markdown("<div class='big-title'>당신은 어떤 뽀로로입니까?</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>팀플 빌런즈 : 눈 속 마을 빌런 테스트</div>", unsafe_allow_html=True)

    st.image("단체컷.png", use_container_width=True)

    st.write("")

    if st.button("🐧 시작하기", use_container_width=True):
        st.session_state.page = "question"
        st.session_state.question_idx = 0
        st.session_state.scores = {c: 0 for c in CHARACTERS}
        st.session_state.result_character = None
        st.session_state.result_saved = False
        st.rerun()

# ======================
# 질문 페이지
# ======================
elif st.session_state.page == "question":

    total_questions = len(questions_df)
    idx = st.session_state.question_idx

    # 모든 질문 완료 → 결과 계산
    if idx >= total_questions:
        scores = st.session_state.scores
        max_score = max(scores.values())
        top_characters = [c for c, s in scores.items() if s == max_score]

        # 동점이면 scores 중 높은 순서대로 우선 캐릭터 선택 (단순 처리)
        result = top_characters[0]

        st.session_state.result_character = result

        if not st.session_state.result_saved:
            save_result(result)
            st.session_state.result_saved = True

        st.session_state.page = "result"
        st.rerun()

    current = questions_df.iloc[idx]

    # 진행 상황
    st.markdown(
        f"<div class='progress-text'>질문 {idx + 1} / {total_questions}</div>",
        unsafe_allow_html=True
    )
    st.progress((idx) / total_questions)

    st.write("")

    # 질문 텍스트
    st.markdown(
        f"<div class='question-text'>{current['질문']}</div>",
        unsafe_allow_html=True
    )

    st.write("")

    # 답변 버튼
    col1, col2 = st.columns(2)

    def select_answer(types_str, score):
        types = parse_types(str(types_str))
        for char in types:
            if char in st.session_state.scores:
                st.session_state.scores[char] += score
        st.session_state.question_idx += 1
        st.rerun()

    with col1:
        if st.button(
            current["답변A"],
            use_container_width=True,
            key=f"A_{idx}"
        ):
            select_answer(current["답변A_유형"], current["답변A_점수"])

    with col2:
        if st.button(
            current["답변B"],
            use_container_width=True,
            key=f"B_{idx}"
        ):
            select_answer(current["답변B_유형"], current["답변B_점수"])

# ======================
# 결과 페이지
# ======================
elif st.session_state.page == "result":

    character = st.session_state.result_character
    counts, total = load_result_counts()

    st.markdown("<div class='big-title'>🎉 결과 발표!</div>", unsafe_allow_html=True)
    st.write("")

    # 캐릭터 이미지 (파일명: 캐릭터이름.png 규칙)
    img_path = f"{character}.png"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

    st.markdown(
        f"<div class='result-character'>당신은 <span style='color:#3355ff'>{character}</span>입니다!</div>",
        unsafe_allow_html=True
    )

    st.write("")

    # 참여 인원 통계
    st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
    st.markdown("<div class='stat-title'>지금까지 이 테스트에 참여한 인원</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-total'>총 {total}명</div>", unsafe_allow_html=True)
    st.write("")

    # 캐릭터별 결과 분포 — "XX%의 인원이 {캐릭터}를 선택했습니다"
    st.markdown("**캐릭터별 결과 분포**")
    for char in CHARACTERS:
        count = counts.get(char, 0)
        pct = round(count / total * 100, 1) if total > 0 else 0.0
        st.write(f"**{pct}%** 의 인원이 **{char}** 를 선택했습니다. ({count}명)")

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # 다시하기 버튼
    if st.button("🔄 다시하기", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.question_idx = 0
        st.session_state.scores = {c: 0 for c in CHARACTERS}
        st.session_state.result_character = None
        st.session_state.result_saved = False
        st.rerun()
