import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="당신은 어떤 뽀로로입니까?",
    page_icon="🐧",
    layout="centered"
)

if "page" not in st.session_state:
    st.session_state.page = "home"

if "score" not in st.session_state:
    st.session_state.score = {
        "에디": 0,
        "뽀로로": 0,
        "크롱": 0,
        "포비": 0,
        "루피": 0
    }


# 질문 엑셀 파일

QUESTION_FILE = "questions.xlsx"

# 질문 불러오기

questions_df = pd.read_excel(QUESTION_FILE)

# 세션 초기화

if "question_idx" not in st.session_state:
    st.session_state.question_idx = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

# 질문 종료 여부 확인

if st.session_state.question_idx < len(questions_df):

    current = questions_df.iloc[
        st.session_state.question_idx
    ]
# 질문
st.markdown(
    f"""
    <h2 style='text-align:center'>
    {current['질문']}
    </h2>
    """,
    unsafe_allow_html=True
)

st.write("")

# 이미지 영역
st.info("질문 이미지 영역")

st.write("")

# 답변 버튼
col1, col2 = st.columns(2)

with col1:

    if st.button(
        current["답변A"],
        use_container_width=True
    ):

        st.session_state.answers.append(
            current["답변A"]
        )

        st.session_state.question_idx += 1

        st.rerun()

with col2:

    if st.button(
        current["답변B"],
        use_container_width=True
    ):

        st.session_state.answers.append(
            current["답변B"]
        )

        st.session_state.question_idx += 1

        st.rerun()

# 진행률 표시
st.progress(
    (st.session_state.question_idx + 1)
    / len(questions_df)
)
