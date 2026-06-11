import streamlit as st
# 페이지 설정

st.set_page_config(
page_title="당신은 어떤 뽀로로 입니까?",
page_icon="🐧",
layout="centered"
)

# 세션 상태 초기화

if "page" not in st.session_state:
    st.session_state.page = "home"

# 시작하기 버튼 클릭 시

def start_test():
    st.session_state.page = "question"
    st.rerun()

# 초기 화면

if st.session_state.page == "home":

```
st.markdown(
    "<h1 style='text-align:center;'>당신은 어떤 뽀로로 입니까?</h1>",
    unsafe_allow_html=True
)

st.write("")
st.write("")

# 이미지 영역
st.image(
    "pororo_main.png",
    caption="나와 가장 닮은 뽀로로 친구를 찾아보세요!",
    use_container_width=True
)

st.write("")
st.write("")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.button(
        "🚀 시작하기",
        use_container_width=True,
        on_click=start_test
    )
```

# 다음 페이지(임시)

elif st.session_state.page == "question":

```
st.title("질문 페이지")

st.write("여기에 첫 번째 질문이 표시됩니다.")

if st.button("처음으로"):
    st.session_state.page = "home"
    st.rerun()
```


