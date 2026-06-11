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

    for character, score in score_data.items():
        st.session_state.scores[character] += score

    st.session_state.current_question += 1

    st.rerun()

# -------------------

# 결과 페이지

# -------------------

if st.session_state.current_question >= len(QUESTIONS):
    
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
import pandas as pd
import os
import streamlit as st

# -------------------

# 통계 저장 파일

# -------------------

EXCEL_FILE = "result_database.xlsx"

# 최초 생성

if not os.path.exists(EXCEL_FILE):

```
init_df = pd.DataFrame(
    columns=["Result"]
)

init_df.to_excel(
    EXCEL_FILE,
    index=False
)
```

# -------------------

# 결과 저장 함수

# -------------------

def save_result(result):

```
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
```

# -------------------

# 통계 조회 함수

# -------------------

def get_statistics(result):

```
df = pd.read_excel(EXCEL_FILE)

total_count = len(df)

same_type_count = len(
    df[df["Result"] == result]
)

ratio = 0

if total_count > 0:

    ratio = round(
        same_type_count
        / total_count
        * 100,
        1
    )

return (
    same_type_count,
    total_count,
    ratio
)
```

# -------------------

# 결과 설명 데이터

# -------------------

RESULT_INFO = {

```
"에디": {
    "image": "images/eddy.png",
    "description": """
    분석적이고 계획적인 발명가형.
    문제 해결을 즐기며 체계적으로 움직입니다.
    """
},

"뽀로로": {
    "image": "images/pororo.png",
    "description": """
    호기심이 많고 도전을 즐기는 모험가형.
    새로운 경험을 좋아합니다.
    """
},

"크롱": {
    "image": "images/crong.png",
    "description": """
    에너지가 넘치고 솔직한 행동파.
    감정 표현이 풍부합니다.
    """
},

"포비": {
    "image": "images/poby.png",
    "description": """
    배려심이 깊고 든든한 지원자형.
    협력을 중요하게 생각합니다.
    """
},

"루피": {
    "image": "images/loopy.png",
    "description": """
    감수성이 풍부하고 공감 능력이 높은 유형.
    관계를 중요하게 생각합니다.
    """
}
```

}

# -------------------

# 결과 페이지

# -------------------

result = max(
st.session_state.scores,
key=st.session_state.scores.get
)

# 중복 저장 방지

if "result_saved" not in st.session_state:

```
save_result(result)

st.session_state.result_saved = True
```

same_count, total_count, ratio = get_statistics(result)

# 상단

st.markdown(
f""" <h1 style='text-align:center'>
당신의 유형은 {result}입니다. </h1>
""",
unsafe_allow_html=True
)

st.write("")

# 중간 이미지

col1, col2, col3 = st.columns([1, 3, 1])

with col2:

```
st.image(
    RESULT_INFO[result]["image"],
    use_container_width=True
)
```

# 결과 설명

st.markdown(
f""" <div style='text-align:center;
             font-size:20px;
             padding:20px;'>
{RESULT_INFO[result]["description"]} </div>
""",
unsafe_allow_html=True
)

st.write("")
st.divider()

# 하단 통계

st.markdown(
f""" <h3 style='text-align:center'>
현재까지 총 {same_count}명이
당신과 같은 {result} 유형으로
판별되었습니다. </h3>
""",
unsafe_allow_html=True
)

st.markdown(
f""" <p style='text-align:center'>
전체 참여자 {total_count}명 중
{ratio}%에 해당합니다. </p>
""",
unsafe_allow_html=True
)

# 다시하기

if st.button(
"다시 검사하기",
use_container_width=True
):

```
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
```

