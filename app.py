import streamlit as st

st.set_page_config(page_title="뽀로로 테스트")

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":

    st.title("당신은 어떤 뽀로로입니까?")

    if st.button("시작하기"):
        st.session_state.page = "question"
        st.rerun()

elif st.session_state.page == "question":

    st.title("질문 페이지")

    if st.button("결과 보기"):
        st.session_state.page = "result"
        st.rerun()

else:

    st.title("결과 페이지")
