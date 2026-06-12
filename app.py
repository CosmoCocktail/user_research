import streamlit as st
import pandas as pd

# ======================
# 페이지 설정
# ======================

st.set_page_config(
    page_title="팀플 빌런즈 : 눈 속 마을 빌런 테스트",
    page_icon="🐧",
    layout="centered"
)

# ======================
# 데이터 불러오기
# ======================

QUESTION_FILE = "questions.xlsx"

questions_df = pd.read_excel(
    QUESTION_FILE,
    sheet_name="questions"
)

tie_df = pd.read_excel(
    QUESTION_FILE,
    sheet_name="tie_breaker"
)

TYPES = ["루피", "포비", "크롱", "에디", "뽀로로"]


# ======================
# 함수
# ======================

def parse_types(type_text):
    if pd.isna(type_text):
        return []

    type_text = str(type_text)
    type_text = type_text.replace("[", "").replace("]", "")
    type_text = type_text.replace(" ", "")

    return [type_name for type_name in type_text.split(",") if type_name]


def add_score(type_text, score):
    type_list = parse_types(type_text)

    for type_name in type_list:
        if type_name in st.session_state.scores:
            st.session_state.scores[type_name] += int(score)


def check_result():
    max_score = max(st.session_state.scores.values())

    top_types = [
        type_name
        for type_name, score in st.session_state.scores.items()
        if score == max_score
    ]

    if len(top_types) == 1:
        st.session_state.selected_result = top_types[0]
        st.session_state.page = "result"
    else:
        st.session_state.tie_types = top_types
        st.session_state.page = "tie_question"


def reset_test():
    st.session_state.page = "home"
    st.session_state.question_idx = 0
    st.session_state.scores = {type_name: 0 for type_name in TYPES}
    st.session_state.selected_result = None
    st.session_state.tie_types = []


# ======================
# 세션 초기화
# ======================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "question_idx" not in st.session_state:
    st.session_state.question_idx = 0

if "scores" not in st.session_state:
    st.session_state.scores = {type_name: 0 for type_name in TYPES}

if "selected_result" not in st.session_state:
    st.session_state.selected_result = None

if "tie_types" not in st.session_state:
    st.session_state.tie_types = []


# ======================
# 홈 화면
# ======================

if st.session_state.page == "home":

    st.markdown(
        """
        <h1 style='text-align:center;'>
        당신은 어떤 뽀로로입니까?
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.image("단체컷.png", use_column_width=True)

    if st.button("시작하기", use_container_width=True):
        reset_test()
        st.session_state.page = "question"
        st.rerun()


# ======================
# 1~10번 질문 화면
# ======================

elif st.session_state.page == "question":

    current_idx = st.session_state.question_idx

    if current_idx >= len(questions_df):
        check_result()
        st.rerun()

    current = questions_df.iloc[current_idx]

    st.markdown(
        f"""
        <h3 style='text-align:center;'>
        Q{current_idx + 1}. {current['질문']}
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.info("질문 이미지 영역")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(current["답변A"], use_container_width=True):
            add_score(
                current["답변A_유형"],
                current["답변A_점수"]
            )

            st.session_state.question_idx += 1
            st.rerun()

    with col2:
        if st.button(current["답변B"], use_container_width=True):
            add_score(
                current["답변B_유형"],
                current["답변B_점수"]
            )

            st.session_state.question_idx += 1
            st.rerun()


# ======================
# 11번 동점 문항 화면
# ======================

elif st.session_state.page == "tie_question":

    st.markdown(
        """
        <h3 style='text-align:center;'>
        마지막으로 하나만 더!<br>
        의견이 갈렸을 때 너와 가장 가까운 선택은?
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    tie_options = tie_df[
        tie_df["유형"].isin(st.session_state.tie_types)
    ]

    for _, row in tie_options.iterrows():
        type_name = row["유형"]
        answer_text = row["답변"]

        if st.button(answer_text, use_container_width=True):
            st.session_state.selected_result = type_name
            st.session_state.page = "result"
            st.rerun()


# ======================
# 결과 화면
# ======================

elif st.session_state.page == "result":

    result = st.session_state.selected_result

    st.markdown(
        f"""
        <h1 style='text-align:center;'>
        당신의 팀플 빌런 유형은<br>
        {result}!
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("점수 확인")
    st.write(st.session_state.scores)

    if st.button("다시 테스트하기", use_container_width=True):
        reset_test()
        st.rerun()
