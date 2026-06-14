import pandas as pd
from pathlib import Path
from ingestion.validate import required_columns, check_file_ready, validate_schema

def write_partitioned_output(df: pd.DataFrame, opfile: str | Path) -> None:
    """
    Write the raw data into respective types of transactions into seperate files
    """
    outdir = Path(opfile)
    outdir.mkdir(parents=True,exist_ok=True)
    transact_type = df['type'].unique()
    for t_type in transact_type:
        df_type = df[df['type'] == t_type]
        o_file = outdir / f'transaction_{t_type.upper()}.csv'
        df_type.to_csv(o_file,index = False)
        print(f'{df_type.shape[0]}  Rows written successfully to {o_file}')
    print(f'Total Transaction types: {len(transact_type)}')
    print(f'Total rows written accross all file: {df.shape[0]}')



def load_raw_data(fp: str | Path) -> pd.DataFrame: # Notice that if fp is only string type and filepath inside main is a Path obj. still no error!! This is bcoz  pd.read_csv() internally accepts both str and Path objects — it handles both types itself.
    """
    Load raw PaySim CSV with full validation.
    Checks file readiness, required columns, and data types before returning.
    Raises FileNotFoundError, ValueError, or TypeError on failure.
    """
    fp = Path(fp) # Convert to Path object — ensures .exists(), .suffix(), .stat() work correctly regardless of whether caller passed a str or Path
    check_file_ready(fp)
    df  = pd.read_csv(fp)
    col_req = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig', 'nameDest', 'oldbalanceDest','newbalanceDest', 'isFraud', 'isFlaggedFraud']
    required_columns(df,col_req)
    validate_schema(df)
    return df
    
def main():
    """
    Entry point for the ingestion pipeline.
    Loads raw PaySim data, validates it, and writes partitioned output by transaction type.
    """
    filepath = Path(__file__).parent.parent / "data" / "raw" / "PS_20174392719_1491204439457_log.csv"
    df = load_raw_data(filepath)
    print(f'Rows Loaded: {df.shape[0]}')
    write_partitioned_output(df,Path(__file__).parent.parent / "data" / "processed")

if __name__ == '__main__':
    main()
