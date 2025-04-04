import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# 目標網站（模擬示例，可替換成實際牙醫網站）
BASE_URL = "https://www.finddoc.com/doctors/%E7%89%99%E9%86%AB/hong-kong?page="

def crawl_finddoc(max_pages=2):
    data = []
    for page in range(1, max_pages + 1):
        url = BASE_URL + str(page)
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")

        listings = soup.select(".doctors-list .item")
        for item in listings:
            name = item.select_one(".doc-name").text.strip() if item.select_one(".doc-name") else ""
            clinic = item.select_one(".clinic-name").text.strip() if item.select_one(".clinic-name") else ""
            address = item.select_one(".address").text.strip() if item.select_one(".address") else ""
            phone = item.select_one(".phone").text.strip() if item.select_one(".phone") else ""
            data.append({
                "牙醫姓名": name,
                "診所名稱": clinic,
                "地址": address,
                "電話": phone
            })
    return pd.DataFrame(data)

# Streamlit 介面設定
st.set_page_config(page_title="香港牙醫資訊平台", layout="wide")
st.title("香港牙醫搜尋平台")

# 抓取資料
with st.spinner("正在載入牙醫資料..."):
    df = crawl_finddoc(max_pages=3)

# 搜尋欄位
search_name = st.text_input("輸入牙醫或診所名稱：")
search_district = st.text_input("輸入地址關鍵字（例如：中環、旺角）：")

# 資料過濾
filtered_df = df[df["牙醫姓名"].str.contains(search_name, case=False, na=False)]
filtered_df = filtered_df[filtered_df["地址"].str.contains(search_district, case=False, na=False)]

st.write(f"共找到 {len(filtered_df)} 筆資料：")
st.dataframe(filtered_df, use_container_width=True)
