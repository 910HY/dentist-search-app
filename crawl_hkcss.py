import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

st.set_page_config(page_title="社福牙醫診所資料擷取", layout="wide")
st.title("社福牙醫診所名單 - 多表格分析")

url = "https://www.hkcss.org.hk/ngo-se-dental-clinic-list/"
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(url, headers=headers)
res.encoding = "utf-8"

soup = BeautifulSoup(res.text, "html.parser")
tables = soup.find_all("table")

st.success(f"共發現 {len(tables)} 個 <table> 元素")

# 顯示每個表格的前幾行
for idx, table in enumerate(tables):
    st.markdown(f"### 表格 #{idx+1}")
    try:
        df = pd.read_html(str(table))[0]
        st.dataframe(df.head(5), use_container_width=True)
    except Exception as e:
        st.warning(f"第 {idx+1} 個表格讀取失敗")
        st.exception(e)
