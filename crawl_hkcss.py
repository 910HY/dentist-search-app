import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import os

DATA_PATH = "data"
DATA_FILE = os.path.join(DATA_PATH, "hkcss_clinics.csv")


def get_all_clinic_tables():
    url = "https://www.hkcss.org.hk/ngo-se-dental-clinic-list/"
    scraper = cloudscraper.create_scraper()  # 模擬瀏覽器防止被擋
    res = scraper.get(url)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, "html.parser")
    tables = soup.find_all("table")

    all_df = []
    for table in tables:
        try:
            df = pd.read_html(StringIO(str(table)))[0]
            df.columns = df.iloc[0]
            df = df[1:]
            df = df.dropna(subset=["診所名稱"], errors="ignore")
            df = df.rename(columns=lambda x: str(x).strip())
            df = df.fillna("")
            df["診所類型"] = "社福牙醫診所"
            all_df.append(df)
        except Exception as e:
            continue

    if not all_df:
        raise ValueError("未能擷取任何診所資料，可能網站結構已改變或被擋")

    full_df = pd.concat(all_df, ignore_index=True)
    return full_df


def save_to_csv(df):
    os.makedirs(DATA_PATH, exist_ok=True)
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    df = get_all_clinic_tables()
    save_to_csv(df)
    print(f"已成功擷取 {len(df)} 筆資料並儲存到 {DATA_FILE}")
