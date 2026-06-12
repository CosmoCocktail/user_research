import streamlit as st
import pandas as pd

# ======================
# 페이지 설정
# ======================

st.set_page_config(
    page_title="당신은 어떤 뽀로로입니까?",
    page_icon="🐧",
    layout="centered"
)

# ======================
# 세션 초기화
# ======================

RESULT_FILE = "result_database.xlsx"

if not os.path.exists(RESULT_FILE):

    pd.DataFrame(
        columns=["Result"]
    ).to_excel(
        RESULT_FILE,
        index=False
    )

QUESTION_FILE = "questions.xlsx"

questions_df = pd.read_excel(
    QUESTION_FILE
)

CHARACTERS = {

    "에디": {
        "description": "분석적이고 계획적인 발명가형",
        "image": "images/eddy.png"
    },

    "크롱": {
        "description": "에너지 넘치는 행동파",
        "image": "images/crong.png"
    },

    "뽀로로": {
        "description": "호기심 많은 모험가형",
        "image": "images/pororo.png"
    },

    "포비": {
        "description": "배려심 깊은 협력형",
        "image": "images/poby.png"
    },

    "루피": {
        "description": "공감능력이 뛰어난 감성형",
        "image": "images/loopy.png"
    }
}

if "page" not in st.session_state:
    st.session_state.page = "home"

# ======================
# 시작 페이지
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

    st.info("이미지 삽입 영역")

    st.write("")

    if st.button(
        "시작하기",
        use_container_width=True
    ):

        st.session_state.page = "question"

        st.rerun()

# ======================
elif st.session_state.page == "question":

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

    st.write("")

    st.info("질문 이미지 영역")

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            current["답변A"],
            use_container_width=True
        ):

            st.session_state.question_idx += 1

            st.rerun()

    with col2:

        if st.button(
            current["답변B"],
            use_container_width=True
        ):

            st.session_state.question_idx += 1

            st.rerun()

elif st.session_state.page == "question":

    st.success("모든 질문이 종료되었습니다.")

    st.write("다음 단계에서 결과 페이지를 연결합니다.")


def save_result(result):

    df = pd.read_excel(
        RESULT_FILE
    )

    new_row = pd.DataFrame(
        {"Result": [result]}
    )

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    df.to_excel(
        RESULT_FILE,
        index=False
    )

def get_result_count(result):

    df = pd.read_excel(
        RESULT_FILE
    )

    same_type_count = len(
        df[df["Result"] == result]
    )

    total_count = len(df)

    return same_type_count, total_count




if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

elif st.session_state.page == "result":

    result = max(
        st.session_state.scores,
        key=st.session_state.scores.get
    )

    if not st.session_state.result_saved:

        save_result(result)

        st.session_state.result_saved = True

    same_count, total_count = get_result_count(
        result
    )

    st.markdown(
        f"""
        <h1 style='text-align:center'>
        당신의 유형은
        {result}
        입니다
        </h1>
        """,
        unsafe_allow_html=True
    )

    image_path = CHARACTERS[
        result
    ]["image"]

    if os.path.exists(image_path):

        st.image(
            image_path,
            use_container_width=True
        )

    st.markdown(
        f"""
        <div style='text-align:center;
                    font-size:20px'>
        {CHARACTERS[result]["description"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        f"""
        <h3 style='text-align:center'>
        현재까지
        {same_count}명이
        {result} 유형으로
        판별되었습니다.
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <p style='text-align:center'>
        전체 참여자 수 :
        {total_count}명
        </p>
        """,
        unsafe_allow_html=True
    )

if st.button(
    "다시하기",
    use_container_width=True
):

    st.session_state.page = "home"

    st.session_state.question_idx = 0

    st.session_state.result_saved = False

    st.session_state.scores = {

        "에디": 0,
        "크롱": 0,
        "뽀로로": 0,
        "포비": 0,
        "루피": 0
    }

    st.rerun()