import pandas as pd
from pathlib import Path

def required_columns(df: pd.DataFrame, required: list) -> None:
    missed =[col for col in required if col not in df.columns]
    if missed :
        raise ValueError(f"Missing Columns:{missed}")
