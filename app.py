import streamlit as st
import pandas as pd
import os

# =====================

# 페이지 설정

# =====================

st.set_page_config(
page_title="당신은 어떤 뽀로로입니까?",
page_icon="🐧",
layout="centered"
)

# =====================

# 결과 저장 파일

# =====================

EXCEL_FILE = "result_database.xlsx"

if not os.path.exists(EXCEL_FILE):
    init_df = pd.DataFrame(
    columns=["Result"]
)

init_df.to_excel(
    EXCEL_FILE,
    index=False
)
# 질문 데이터
QUESTIONS = [

{
    "question": "당신은 팀플에서 어떤 사람입니까?",
    "image": None,
    "answers": [
        {
            "text": "협동 위주로 참여한다",
            "score": {"포비": 2, "루피": 1}
        },
        {
            "text": "주도적으로 이끈다",
            "score": {"에디": 2, "뽀로로": 1}
        }
    ]
},

{
    "question": "새로운 일이 생기면?",
    "image": None,
    "answers": [
        {
            "text": "바로 도전한다",
            "score": {"뽀로로": 2, "크롱": 1}
        },
        {
            "text": "충분히 계획한다",
            "score": {"에디": 2, "포비": 1}
        }
    ]
}

]

# =====================

# 결과 설명

# =====================

RESULT_INFO = {

"에디":
    "분석적이고 계획적인 발명가형",

"뽀로로":
    "호기심 많고 도전을 즐기는 모험가형",

"크롱":
    "에너지 넘치는 행동파",

"포비":
    "배려심 깊은 협력형",

"루피":
    "감수성이 풍부한 공감형"


}



# 세션 초기화


if "page" not in st.session_state:
    st.session_state.page = "home"

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

if "scores" not in st.session_state:
    st.session_state.scores = {

    "에디": 0,
    "뽀로로": 0,
    "크롱": 0,
    "포비": 0,
    "루피": 0
}



# 함수

def save_result(result):
    df = pd.read_excel(EXCEL_FILE)
    new_row = pd.DataFrame(
    {"Result": [result]}
)

df = pd.concat(
    [df, new_row],
    ignore_index=True
)

df.to_excel(
    EXCEL_FILE,
    index=False
)


def get_statistics(result):
    df = pd.read_excel(EXCEL_FILE)
    
    total_count = len(df)
    
    same_type_count = len(
        df[df["Result"] == result]
    )
    
    return same_type_count, total_count

def start_test():
    st.session_state.page = "question"
st.rerun()


def select_answer(score_data):
    for character, score in score_data.items():
        st.session_state.scores[character] += score
        st.session_state.current_question += 1
        st.rerun()


# =====================

# 시작화면

# =====================

if st.session_state.page == "home":
    st.markdown(
    "<h1 style='text-align:center;'>당신은 어떤 뽀로로입니까?</h1>",
    unsafe_allow_html=True
)

st.write("")

st.info("이미지 삽입 영역")

st.write("")

if st.button(
    "시작하기",
    use_container_width=True
):
    start_test()


# 질문 페이지


elif st.session_state.page == "question" and st.session_state.current_question < len(QUESTIONS):
    q = QUESTIONS[
    st.session_state.current_question
]

st.markdown(
    f"""
    <h2 style='text-align:center'>
    {q["question"]}
    </h2>
    """,
    unsafe_allow_html=True
)

st.write("")

st.info("질문 이미지 영역")

st.write("")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        q["answers"][0]["text"],
        use_container_width=True
    ):
        select_answer(
            q["answers"][0]["score"]
        )

with col2:

    if st.button(
        q["answers"][1]["text"],
        use_container_width=True
    ):
        select_answer(
            q["answers"][1]["score"]
        )

st.progress(
    (
        st.session_state.current_question + 1
    )
    / len(QUESTIONS)
    )


# 결과 페이지

if st.session_state.current_question < len(QUESTIONS):
    with col2:
        if st.button(
            q["answers"][1]["text"],
            use_container_width=True
        ):
            select_answer(q["answers"][1]["score"])

    st.progress((st.session_state.current_question + 1) / len(QUESTIONS))
else:result = max(
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
    당신의 유형은 {result}입니다.
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("")

st.info("결과 이미지 영역")

st.write("")

st.markdown(
    f"""
    <div style='text-align:center;
                font-size:20px;'>
    {RESULT_INFO[result]}
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.markdown(
    f"""
    <h3 style='text-align:center'>
    총 {same_count}명이
    당신과 같은 유형입니다.
    </h3>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <p style='text-align:center'>
    전체 참여자 수 : {total_count}명
    </p>
    """,
    unsafe_allow_html=True
)

if st.button(
    "다시 검사하기",
    use_container_width=True
):

    st.session_state.page = "home"

    st.session_state.current_question = 0

    st.session_state.result_saved = False

    st.session_state.scores = {

        "에디": 0,
        "뽀로로": 0,
        "크롱": 0,
        "포비": 0,
        "루피": 0
    }

    st.rerun()