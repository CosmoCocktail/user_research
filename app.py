import streamlit as st

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
# 질문 페이지(임시)
# ======================

elif st.session_state.page == "question":

    st.title("질문 페이지")

    st.write("다음 단계에서 엑셀 데이터를 연결합니다.")
