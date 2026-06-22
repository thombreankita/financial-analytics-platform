import pandas as pd
from pathlib import Path

VIOLATION_THRESHOLD = 0.05  

def required_columns(df: pd.DataFrame, required: list) -> None:
    """
    Check if all the required columns needed for the analysis are present in the dataframe
    """
    missed =[col for col in required if col not in df.columns]
    if missed :
        raise ValueError(f"Missing Columns:{missed}")

def check_file_ready(fp: Path) -> bool:
   """
   Verifies if the file is in correct format, exists and has data in it
   """
   if not fp.exists():
      raise FileNotFoundError("File Not Found!!")
   if fp.suffix != ".csv":
      raise ValueError("This is not a .csv file!!")
   if fp.stat().st_size == 0:
      raise ValueError("Empty File")
   return True

def validate_schema(df: pd.DataFrame) -> None:
   """
   Verifies the schema of the columns is correct or not
   """
   numeric_columns = ['amount', 'step', 'isFraud', 'isFlaggedFraud', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']
   required_columns(df,numeric_columns)
   for col in numeric_columns:
      if not pd.api.types.is_numeric_dtype(df[col]):
         raise TypeError(f'The {col} column type should be numeric but type found is: {df[col].dtype}')

def validate_demo(df: pd.DataFrame) -> None:
   critical_col = ['step','type','amount','nameOrig','nameDest','isFraud']
   res_validnulls = df[critical_col].isnull().any(axis=1).sum()  # this line gives the list of row numbers that have atleast one null in the specified column and then sums/counts the list len or items.
   print(f'{res_validnulls}') 


def validate_business_rules(df: pd.DataFrame) -> dict:
    """
    Validates business logic rules on PaySim transaction data.
    Returns a summary dict of violation counts per rule.
    Raises ValueError if any single rule violation exceeds 5% of total rows.
    """
    total_rows = df.shape[0]
    res_amt = df[df['amount']<=0].shape[0]
    res_err = df[df['nameDest'] == df['nameOrig']].shape[0]
    critical_col = ['step','type','amount','nameOrig','nameDest','isFraud']
    res_notnulls = df[critical_col].isnull().any(axis=1).sum()
    res_transfer = df[(df['type'] == "TRANSFER") & (df['newbalanceDest']<=df['oldbalanceDest'])].shape[0]
    res_debit = df[(df['type'] == 'DEBIT') & (df['oldbalanceOrg'] <= df['amount'])].shape[0]
    valid_types = ['DEBIT','TRANSFER','CASH_OUT','PAYMENT','CASH_IN']
    res_type = df[~df['type'].isin(valid_types)].shape[0]

    result = {'Amount': res_amt,
              'Error': res_err,
              'Not Null_Columns': res_notnulls,
              'Transfer_valid': res_transfer,
              'Debit_valid': res_debit,
              'Type_valid': res_type}
    
    for r,count in result.items():
       if count > VIOLATION_THRESHOLD  * total_rows:
          raise ValueError(f'{r} violation exceeds 5% of total data!!')

    return result
