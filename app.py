import streamlit as st
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
        .reindex(["A", "B", "C", "D", "E"], fill_value=0)
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
