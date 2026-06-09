import pandas as pd
import duckdb

# --- 設定 ---
INPUT_PATH = "data/fao_food_price_indices_data.csv"
OUTPUT_PATH = "food_prices.csv"

def main():
    # --- CSVを読み込む ---
    # 先頭2行（タイトル・基準値の説明）を skiprows でスキップし、
    # 3行目を列名(header)として読む。
    # ※ skiprows=2 で先頭2行を飛ばすと、その次の行が自動的にヘッダーになる
    df = pd.read_csv(INPUT_PATH, skiprows=2)

    # --- 不要な列を取り除く ---
    # 行末の余分なカンマで生まれる "Unnamed" 列を削除
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # --- 空行を取り除く ---
    # Date が空の行（区切りの空行など）を削除
    df = df.dropna(subset=["Date"])

    # --- 列名を扱いやすい形に統一 ---
    df = df.rename(columns={
        "Date": "month",
        "Food Price Index": "food_price_index",
        "Meat": "meat",
        "Dairy": "dairy",
        "Cereals": "cereals",
        "Oils": "oils",
        "Sugar": "sugar",
    })

    # --- 確認 ---
    print(f"取得件数: {len(df)} 行")
    print("列名:", list(df.columns))
    print(df.head())
    print("...")
    print(df.tail())

    # --- DuckDBに格納 ---
    db_path = "pipeline.duckdb"
    con = duckdb.connect(db_path)

    con.execute("CREATE OR REPLACE TABLE raw_food_prices AS SELECT * FROM df")

    count = con.execute("SELECT COUNT(*) FROM raw_food_prices").fetchone()[0]
    print(f"raw_food_prices に {count} 件を格納しました")

    con.close()


if __name__ == "__main__":
    main()
