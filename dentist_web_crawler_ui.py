# 主網站：dentist_web_crawler_ui.py
import streamlit as st
import pandas as pd
import os

DATA_FILE = "data/hkcss_clinics.csv"

st.set_page_config(page_title="香港牙醫搜尋平台", layout="centered")
st.title("香港牙醫搜尋平台")
st.markdown("<p style='color:gray;'>搜尋及比較香港社福牙醫診所</p>", unsafe_allow_html=True)

# 地區選項劃分（港島、九龍、新界 + 細分）
region_options = {
    "港島": ["中西區", "灣仔", "東區", "南區"],
    "九龍": ["油尖旺", "深水埗", "九龍城", "黃大仙", "觀塘"],
    "新界": ["荃灣", "屯門", "元朗", "北區", "大埔", "西貢", "沙田", "葵青", "離島"]
}

flat_regions = [(area, main) for main, sublist in region_options.items() for area in sublist]

# 搜尋欄
st.markdown("""
<div style='border: 2px solid orange; padding: 20px; border-radius: 12px;'>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    search_name = st.text_input("診所名稱 / 關鍵字", placeholder="例如：彩雲、仁愛")
with col2:
    region_group = st.selectbox("選擇主要區域", list(region_options.keys()))
    subregion = st.selectbox("選擇地區", region_options[region_group])

st.markdown("""</div>""", unsafe_allow_html=True)

# 載入資料
if not os.path.exists(DATA_FILE):
    st.error("未能找到診所資料，請先執行 crawl_hkcss.py 擷取資料")
else:
    df = pd.read_csv(DATA_FILE)

    # 搜尋條件
    filtered_df = df[
        df["診所名稱"].str.contains(search_name, case=False, na=False) |
        df["地址"].str.contains(search_name, case=False, na=False)
    ]
    filtered_df = filtered_df[
        filtered_df["地區"].str.contains(subregion, case=False, na=False)
    ]

    st.write(f"共找到 {len(filtered_df)} 筆結果：")
    st.dataframe(filtered_df, use_container_width=True)
