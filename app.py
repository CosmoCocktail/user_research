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



QUESTIONS = [
    {
        "question": "당신은 팀플에서 어떤 사람입니까?",
        "a": {
            "text": "협동 위주",
            "type": "포비"
        },
        "b": {
            "text": "리더십형",
            "type": "에디"
        }
    },
    {
        "question": "새로운 일이 생기면?",
        "a": {
            "text": "바로 도전",
            "type": "뽀로로"
        },
        "b": {
            "text": "계획부터",
            "type": "에디"
        }
    }
]


def choose(character):
    st.session_state.score[character] += 1
    st.session_state.question_idx += 1
    st.rerun()


if st.session_state.page == "home":

    st.markdown(
        "<h1 style='text-align:center'>당신은 어떤 뽀로로입니까?</h1>",
        unsafe_allow_html=True
    )

    st.info("이미지 영역")

    if st.button("시작하기"):
        st.session_state.page = "question"
        st.rerun()

elif (
    st.session_state.page == "question"
    and
    st.session_state.question_idx < len(QUESTIONS)
):

    q = QUESTIONS[st.session_state.question_idx]

    st.markdown(
        f"<h2 style='text-align:center'>{q['question']}</h2>",
        unsafe_allow_html=True
    )

    st.info("질문 이미지 영역")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(q["a"]["text"]):
            choose(q["a"]["type"])

    with col2:
        if st.button(q["b"]["text"]):
            choose(q["b"]["type"])

else:

    result = max(
        st.session_state.score,
        key=st.session_state.score.get
    )

    st.markdown(
        f"<h1 style='text-align:center'>당신의 유형은 {result}입니다.</h1>",
        unsafe_allow_html=True
    )

    if st.button("다시하기"):

        st.session_state.page = "home"
        st.session_state.question_idx = 0

        st.session_state.score = {
            "에디": 0,
            "뽀로로": 0,
            "크롱": 0,
            "포비": 0,
            "루피": 0
        }

        st.rerun()