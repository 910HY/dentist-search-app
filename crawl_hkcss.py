import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def crawl_hkcss():
    url = "https://www.hkcss.org.hk/ngo-se-dental-clinic-list/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, "html.parser")

    # 嘗試找 HTML 表格
    table = soup.find("table")
    rows = table.find_all("tr")

    data = []
    headers = [th.text.strip() for th in rows[0].find_all("th")]

    for row in rows[1:]:
        cols = [td.text.strip() for td in row.find_all("td")]
        if len(cols) == len(headers):
            data.append(dict(zip(headers, cols)))

    return pd.DataFrame(data)

# Streamlit UI
st.set_page_config(page_title="香港牙醫搜尋平台", layout="centered")
st.title("社福牙醫診所清單")

try:
    df = crawl_hkcss()
    st.success(f"成功擷取 {len(df)} 筆資料。")
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error("未能成功擷取資料。")
    st.exception(e)
