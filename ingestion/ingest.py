import time as t
import pandas as pd
from pathlib import Path
from ingestion.validate import required_columns, check_file_ready, validate_schema, validate_business_rules

def write_partitioned_output(df: pd.DataFrame, opfile: str | Path) -> dict:
    """
    Write the raw data into respective types of transactions into seperate files
    """
    outdir = Path(opfile)
    outdir.mkdir(parents=True,exist_ok=True)
    transact_type = df['type'].unique()
    result = {}
    for t_type in transact_type:
        df_type = df[df['type'] == t_type]
        o_file = outdir / f'transaction_{t_type.upper()}.csv'
        df_type.to_csv(o_file,index = False) 
        result[t_type] = df_type['type'].shape[0]
        #print(f'{df_type.shape[0]}  Rows written successfully to {o_file}')
    #print(f'Total Transaction types: {len(transact_type)}')
    #print(f'Total rows written accross all file: {df.shape[0]}')
    return result



def load_raw_data(fp: str | Path) -> dict: # Notice that if fp is only string type and filepath inside main is a Path obj. still no error!! This is bcoz  pd.read_csv() internally accepts both str and Path objects — it handles both types itself.
    """
    Load raw PaySim CSV with full validation.
    Checks file readiness, required columns, and data types before returning.
    Raises FileNotFoundError, ValueError, or TypeError on failure.
    """
    fp = Path(fp) # Convert to Path object — ensures .exists(), .suffix(), .stat() work correctly regardless of whether caller passed a str or Path
    check_file_ready(fp)
    f_valid = 'Passed'
    df  = pd.read_csv(fp)
    col_req = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig', 'nameDest', 'oldbalanceDest','newbalanceDest', 'isFraud', 'isFlaggedFraud']
    required_columns(df,col_req)
    validate_schema(df)
    schema_valid = 'Passed'
    valid_criteria = validate_business_rules(df)
    dict_sum = {
        'df': df,
        'file_check': f_valid,
        'schema_check': schema_valid,
        'business_rule': valid_criteria
    }
    return dict_sum
    
def main():
    """
    Entry point for the ingestion pipeline.
    Loads raw PaySim data, validates it, and writes partitioned output by transaction type.
    """
    timer_s = t.time()
    print(f'Pipeline Started ....')
    print(f'Loading Raw Data ....')
    filepath = Path(__file__).parent.parent / "data" / "raw" / "PS_20174392719_1491204439457_log.csv"
    dict_fin = load_raw_data(filepath)
    print(f"Rows Loaded: {dict_fin['df'].shape[0]}")
    print(f"File Validation: {dict_fin['file_check']}")
    print(f"Schema Validation: {dict_fin['schema_check']}")
    print(f"Business rule validation Summary: {dict_fin['business_rule']}")
    print(f'Writing Partioned output........')
    dict_fin2 = write_partitioned_output(dict_fin["df"],Path(__file__).parent.parent / "data" / "processed")
    print(dict_fin2)
    timer_e = t.time()
    print(f'Pipeline Completed. Total Time {timer_e - timer_s:.1f} seconds')

if __name__ == '__main__':
    main()
