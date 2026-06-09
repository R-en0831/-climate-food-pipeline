import requests
import pandas as pd
import duckdb
from datetime import date, timedelta

# --- 設定 ---
# 東京の緯度経度
LATITUDE = 35.6895
LONGITUDE = 139.6917

# 取得期間：今日から過去1年分
end_date = date.today() - timedelta(days=1)  # 昨日まで（当日はデータ未確定のことが多い）
start_date = end_date - timedelta(days=365)

# Open-Meteo 過去気象API（APIキー不要）
URL = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": start_date.isoformat(),
    "end_date": end_date.isoformat(),
    # 日次データとして「平均気温」と「降水量合計」を取得
    "daily": "temperature_2m_mean,precipitation_sum",
    "timezone": "Asia/Tokyo",
}

def main():
    print(f"取得期間: {start_date} 〜 {end_date}")

    # --- APIを叩く ---
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()  # エラーなら例外を投げる（重要な作法）
    data = response.json()

    # --- レスポンスをDataFrameに整形 ---
    daily = data["daily"]
    df = pd.DataFrame({
        "date": daily["time"],
        "temp_mean_c": daily["temperature_2m_mean"],
        "precipitation_mm": daily["precipitation_sum"],
    })

    # --- 簡単な確認 ---
    print(f"取得件数: {len(df)} 行")
    print(df.head())

    # --- CSVに保存（コメントアウト） ---
    # output_path = "weather_tokyo.csv"
    # df.to_csv(output_path, index=False)
    # print(f"保存しました: {output_path}")

    # --- DuckDBに格納 ---
    db_path = "pipeline.duckdb"
    con = duckdb.connect(db_path)

    # 再実行に強くする：既存テーブルを作り直してから入れる（冪等性）
    con.execute("CREATE OR REPLACE TABLE raw_weather AS SELECT * FROM df")

    # 確認：格納された件数を数える
    count = con.execute("SELECT COUNT(*) FROM raw_weather").fetchone()[0]
    print(f"raw_weather に {count} 件を格納しました")

    con.close()


if __name__ == "__main__":
    main()
