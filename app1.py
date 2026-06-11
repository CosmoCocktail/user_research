import streamlit as st
import pandas as pd
import os

# ==========================

# 기본 설정

# ==========================

st.set_page_config(
page_title="당신은 어떤 뽀로로입니까?",
page_icon="🐧",
layout="centered"
)

QUESTION_FILE = "questions.xlsx"
RESULT_FILE = "result_database.xlsx"

# ==========================

# 파일 확인

# ==========================

if not os.path.exists(QUESTION_FILE):
    st.error("questions.xlsx 파일이 없습니다.")
    st.stop()

if not os.path.exists(RESULT_FILE):
    init_df = pd.DataFrame(
    columns=["Result"]
)

init_df.to_excel(
    RESULT_FILE,
    index=False
)


# ==========================

# 질문 데이터 불러오기

# ==========================

questions_df = pd.read_excel(
QUESTION_FILE
)

# ==========================

# 유형 리스트 생성

# ==========================

type_list = list(


set(

    questions_df["답변A_유형"].tolist()

    +

    questions_df["답변B_유형"].tolist()

)


)

# ==========================

# 세션 초기화

# ==========================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "question_idx" not in st.session_state:
    st.session_state.question_idx = 0

if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

if "scores" not in st.session_state:
    st.session_state.scores = {}

for t in type_list:

    st.session_state.scores[t] = 0


# ==========================

# 결과 저장

# ==========================

def save_result(result):
    df = pd.read_excel(RESULT_FILE)

    new_row = pd.DataFrame({"Result": [result]})

    df = pd.concat([df, new_row], ignore_index=True)

    df.to_excel(RESULT_FILE, index=False)


# ==========================

# 통계 조회

# ==========================

def get_statistics(result):
    df = pd.read_excel(RESULT_FILE)

    same_count = len(df[df["Result"] == result])

    total_count = len(df)
    return same_count, total_count

# ==========================

# 답변 처리

# ==========================

def choose(answer_type, weight):
    st.session_state.scores[answer_type] += weight

    st.session_state.question_idx += 1

    if st.session_state.question_idx >= len(questions_df):
        st.session_state.page = "result"

    st.rerun()

# ==========================

# 시작 페이지

# ==========================

if st.session_state.page == "home":
    st.markdown(
    """
    <h1 style='text-align:center'>
    당신은 어떤 뽀로로입니까?
    </h1>
    """,
    unsafe_allow_html=True
)

st.info("시작 이미지 영역")

st.write("")

if st.button(
    "시작하기",
    use_container_width=True
):

    st.session_state.page = "question"

    st.rerun()

# ==========================

# 질문 페이지

# ==========================

if st.session_state.page == "question":
    current = questions_df.iloc[
    st.session_state.question_idx
]

st.markdown(
    f"""
    <h2 style='text-align:center'>
    {current['질문']}
    </h2>
    """,
    unsafe_allow_html=True
)

st.info("질문 이미지 영역")

st.write("")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        current["답변A"],
        use_container_width=True
    ):

        choose(
            current["답변A_유형"],
            int(current["답변A_가중치"])
        )

with col2:

    if st.button(
        current["답변B"],
        use_container_width=True
    ):

        choose(
            current["답변B_유형"],
            int(current["답변B_가중치"])
        )

st.progress(

    (
        st.session_state.question_idx + 1
    )

    /

    len(questions_df)

)


# ==========================

# 결과 페이지

# ==========================

if st.session_state.page == "result":
    result = max(
        st.session_state.scores,
        key=st.session_state.scores.get
    )

    if not st.session_state.result_saved:

        save_result(result)

        st.session_state.result_saved = True

    same_count, total_count = get_statistics(
        result
    )

    st.markdown(
        f"""
        <h1 style='text-align:center'>
        당신의 유형은
        {result}
        입니다.
        </h1>
        """,
        unsafe_allow_html=True
    )

st.info(
    f"{result} 결과 이미지 영역"
)

st.write("")

st.markdown(
    f"""
    <h3 style='text-align:center'>
    {same_count}명이
    당신과 같은
    {result}
    유형입니다.
    </h3>
    """,
    unsafe_allow_html=True
)

st.write(
    f"전체 참여자 수 : {total_count}명"
)

if st.button(
    "다시하기",
    use_container_width=True
):

    st.session_state.page = "home"

    st.session_state.question_idx = 0

    st.session_state.result_saved = False

    st.session_state.scores = {}

    for t in type_list:

        st.session_state.scores[t] = 0

    st.rerun()

