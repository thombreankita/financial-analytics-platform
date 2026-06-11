import pandas as pd
from pathlib import Path

def check_file_ready(fp: Path) -> bool:
   if not fp.exists():
      raise FileNotFoundError("File Not Found!!")
   if fp.suffix != ".csv":
      raise ValueError("This is not a .csv file!!")
   if fp.stat().st_size == 0:
      raise ValueError("Empty File")
   return True

filep = Path(__file__).parent.parent / "data" / "processed" / "transaction_CASH_OUT.csv"
try:
   print(check_file_ready(filep))
except (ValueError,FileNotFoundError) as e:
   print(f'Error: {e}')