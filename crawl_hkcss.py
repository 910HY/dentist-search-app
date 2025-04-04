import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

DATA_PATH = "data"
DATA_FILE = os.path.join(DATA_PATH, "hkcss_clinics.csv")

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
            if df.iloc[0].str.contains("診所名稱", na=False).any():
                df.columns = df.iloc[0]
                df = df[1:]
            all_df.append(df)
        except:
            continue

    full_df = pd.concat(all_df, ignore_index=True)
    full_df = full_df.rename(columns=lambda x: str(x).strip())
    full_df = full_df.dropna(subset=["診所名稱"])
    return full_df

def save_to_csv(df):
    os.makedirs(DATA_PATH, exist_ok=True)
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    df = get_all_clinic_tables()
    save_to_csv(df)
    print(f"已成功擷取 {len(df)} 筆資料並儲存到 {DATA_FILE}")
