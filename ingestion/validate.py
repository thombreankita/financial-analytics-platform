import pandas as pd
from pathlib import Path

def required_columns(df: pd.DataFrame, required: list) -> None:
    missed =[col for col in required if col not in df.columns]
    if missed :
        raise ValueError(f"Missing Columns:{missed}")

def check_file_ready(fp: Path) -> bool:
   if not fp.exists():
      raise FileNotFoundError("File Not Found!!")
   if fp.suffix != ".csv":
      raise ValueError("This is not a .csv file!!")
   if fp.stat().st_size == 0:
      raise ValueError("Empty File")
   return True
