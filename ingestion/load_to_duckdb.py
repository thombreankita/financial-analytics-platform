from pathlib import Path
import pandas as pd
import duckdb

def load_csv_to_duckdb(csv_path : str, db_path:str, table_name: str):
    conn =  duckdb.connect(db_path)
    df = pd.read_csv(csv_path)
    conn.execute(f" CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
    count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f'Loaded {count} rows into {table_name}')
    print(f'Rows : {df.shape[0]}')
    conn.close()

def main() :
    fp = str(Path(__file__).parent.parent / "data" /"raw"/"PS_20174392719_1491204439457_log.csv")
    dbp = str(Path(__file__).parent.parent / "dbt_project" / "financial_analytics" / "dev.duckdb")
    load_csv_to_duckdb(fp,dbp,"paysim_raw")

if __name__ == "__main__":
    main()

