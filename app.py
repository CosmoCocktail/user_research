import streamlit as st

st.set_page_config(
    page_title="당신은 어떤 뽀로로 입니까?",
    page_icon="🐧",
    layout="centered"
)

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"

# 시작 버튼 함수
def start_test():
    st.session_state.page = "question"
    st.rerun()

# 홈 화면
if st.session_state.page == "home":

    st.title("당신은 어떤 뽀로로 입니까?")

    st.image(
        "pororo_main.png",
        use_container_width=True
    )

    if st.button("🚀 시작하기"):
        start_test()

# 질문 페이지
elif st.session_state.page == "question":

    st.title("질문 페이지")

    st.write("첫 번째 질문이 표시될 영역")

    if st.button("처음으로"):
        st.session_state.page = "home"
        st.rerun()
