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


import pandas as pd
import os

# 엑셀 파일명
EXCEL_FILE = "result_database.xlsx"

# 최초 실행 시 엑셀 생성
if not os.path.exists(EXCEL_FILE):
    init_df = pd.DataFrame(columns=["Result"])
    init_df.to_excel(EXCEL_FILE, index=False)

st.title("유형 결과 통계")

# 결과 선택
result = st.selectbox(
    "도출된 결과를 선택하세요.",
    ["에디", "크롱", "뽀로로", "포비", "루피"]
)

# 결과 저장
if st.button("결과 저장"):
    df = pd.read_excel(EXCEL_FILE)

    new_row = pd.DataFrame({"Result": [result]})
    df = pd.concat([df, new_row], ignore_index=True)

    df.to_excel(EXCEL_FILE, index=False)

    st.success(f"{result} 유형이 저장되었습니다.")

# 통계 조회
df = pd.read_excel(EXCEL_FILE)

if len(df) > 0:

    total_count = len(df)

    counts = (
        df["Result"]
        .value_counts()
        .reindex(["에디", "크롱", "뽀로로", "포비", "루피"], fill_value=0)
    )

    st.subheader("누적 통계")

    for category, count in counts.items():
        ratio = (count / total_count) * 100

        st.write(
            f"**{category} 유형** : {ratio:.1f}% "
            f"(총 {count}명 / 전체 {total_count}명)"
        )

    stats_df = pd.DataFrame({
        "유형": counts.index,
        "인원수": counts.values,
        "비율(%)": [
            round((c / total_count) * 100, 1)
            for c in counts.values
        ]
    })

    st.dataframe(stats_df, use_container_width=True)

else:
    st.info("아직 저장된 데이터가 없습니다.")
