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
QUESTION_FILE = "questions.xlsx"

questions_df = pd.read_excel(
    QUESTION_FILE
)


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


   