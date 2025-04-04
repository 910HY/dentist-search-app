import requests
from bs4 import BeautifulSoup
import streamlit as st

st.set_page_config(page_title="社福牙醫診所測試", layout="centered")
st.title("社福牙醫診所資料擷取")

# Step 1: 請求網站資料
url = "https://www.hkcss.org.hk/ngo-se-dental-clinic-list/"
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(url, headers=headers)
res.encoding = "utf-8"

# Step 2: 顯示 HTML 原始碼
st.subheader("網站 HTML 原始碼預覽")
st.code(res.text[:3000], language="html")  # 避免整頁太長

# Step 3: 嘗試顯示 table 數量
soup = BeautifulSoup(res.text, "html.parser")
tables = soup.find_all("table")

if tables:
    st.success(f"發現 {len(tables)} 個 <table> 元素")
else:
    st.warning("此網站似乎無 <table> 結構，可能是 JavaScript 動態載入")
