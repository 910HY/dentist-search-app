import streamlit as st
import pandas as pd
import os

DATA_FILE = "data/hkcss_clinics.csv"

st.set_page_config(page_title="搜尋牙醫診所 - 社福清單", layout="centered")
st.title("下一次洗牙感覺好開心")
st.markdown("<p style='color:gray;'>搜尋及比較香港社福牙醫診所</p>", unsafe_allow_html=True)

st.markdown("""
<div style='border: 2px solid orange; padding: 20px; border-radius: 12px;'>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    name_keyword = st.text_input("診所名稱 / 關鍵字", placeholder="例如：興民、彩雲")
with col2:
    region = st.text_input("地區 / 地址關鍵字", placeholder="例如：九龍、柴灣")

st.markdown("""</div>""", unsafe_allow_html=True)

if not os.path.exists(DATA_FILE):
    st.error("未能找到診所資料，請先執行 crawl_hkcss.py 擷取資料")
else:
    df = pd.read_csv(DATA_FILE)
    if name_keyword:
        df = df[df["診所名稱"].str.contains(name_keyword, case=False, na=False)]
    if region:
        df = df[df["地區"].str.contains(region, case=False, na=False) | df["地址"].str.contains(region, case=False, na=False)]

    st.write(f"共找到 {len(df)} 筆結果：")
    st.dataframe(df, use_container_width=True)

    # 預留進階功能：排序、地圖、價錢、保險標示
