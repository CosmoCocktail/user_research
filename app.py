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

st.set_page_config(
page_title="당신은 어떤 뽀로로 입니까?",
layout="centered"
)

# -------------------

# 질문 데이터

# -------------------

QUESTIONS = [
{
"question": "당신은 팀플에서 어떤 사람입니까?",
"image": "images/q1.png",
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
"image": "images/q2.png",
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

# -------------------

# 초기화

# -------------------

if "current_question" not in st.session_state:
st.session_state.current_question = 0

if "scores" not in st.session_state:
st.session_state.scores = {
"에디": 0,
"뽀로로": 0,
"크롱": 0,
"포비": 0,
"루피": 0
}

# -------------------

# 답변 처리 함수

# -------------------

def select_answer(score_data):

```
for character, score in score_data.items():
    st.session_state.scores[character] += score

st.session_state.current_question += 1

st.rerun()
```

# -------------------

# 결과 페이지

# -------------------

if st.session_state.current_question >= len(QUESTIONS):

```
result = max(
    st.session_state.scores,
    key=st.session_state.scores.get
)

st.title("결과")

st.markdown(
    f"<h1 style='text-align:center'>{result}</h1>",
    unsafe_allow_html=True
)

st.write(st.session_state.scores)

if st.button("다시하기"):
    st.session_state.current_question = 0

    st.session_state.scores = {
        "에디": 0,
        "뽀로로": 0,
        "크롱": 0,
        "포비": 0,
        "루피": 0
    }

    st.rerun()
```

# -------------------

# 질문 페이지

# -------------------

else:

```
q = QUESTIONS[st.session_state.current_question]

# 상단 질문
st.markdown(
    f"""
    <h2 style='text-align:center'>
    {q['question']}
    </h2>
    """,
    unsafe_allow_html=True
)

st.write("")

# 중앙 이미지
col1, col2, col3 = st.columns([1,4,1])

with col2:
    st.image(
        q["image"],
        use_container_width=True
    )

st.write("")
st.write("")

# 하단 선택지 2개
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
    (st.session_state.current_question + 1)
    / len(QUESTIONS)
)
```

