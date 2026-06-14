import pandas as pd
from pathlib import Path

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
      
