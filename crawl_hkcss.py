import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def get_all_clinic_tables():
    url = "https://www.hkcss.org.hk/ngo-se-dental-clinic-list/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, "html.parser")
    tables = soup.find_all("table")

    all_df = []
    for table in tables:
        try:
            df = pd.read_html(str(table))[0]
            # 假如第一列是欄位名稱，將它設為標題
            if df.iloc[0].str.contains("診所名稱", na=False).any():
                df.columns = df.iloc[0]
                df = df[1:]
            all_df.append(df)
        except:
            continue

    full_df = pd.concat(all_df, ignore_index=True)
    full_df = full_df.rename(columns=lambda x: str(x).strip())  # 清洗欄位名稱
    full_df = full_df.dropna(subset=["診所名稱"])
    return full_df

# Streamlit UI 預覽
st.set_page_config(page_title="社福牙醫診所總表", layout="wide")
st.title("香港社福牙醫診所總表")

try:
    df = get_all_clinic_tables()
    st.success(f"成功合併 {len(df)} 筆資料")
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error("擷取資料失敗")
    st.exception(e)
