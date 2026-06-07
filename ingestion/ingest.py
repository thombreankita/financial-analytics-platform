import pandas as pd
from pathlib import Path
from ingestion.validate import required_columns

def load_raw_data(fp: str | Path) -> pd.DataFrame: # Notice that if fp is only string type and filepath inside main is a Path obj. still no error!! This is bcoz  pd.read_csv() internally accepts both str and Path objects — it handles both types itself.
    df  = pd.read_csv(fp)
    col_req = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig', 'nameDest', 'oldbalanceDest','newbalanceDest', 'isFraud', 'isFlaggedFraud']
    rq(df,col_req)
    return df
def main():
    filepath = Path(__file__).parent.parent / "data" / "raw" / "PS_20174392719_1491204439457_log.csv"
    df = load_raw_data(filepath)
    print(f'Rows Loaded: {df.shape[0]}')

if __name__ == '__main__':
    main()
