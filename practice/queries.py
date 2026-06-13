import pandas as pd
from pathlib import Path

fpath = ( Path(__file__).resolve().parent.parent /"data"/"raw"/"PS_20174392719_1491204439457_log.csv")
df = pd.read_csv(fpath)
df['step'].min()
df['step'].max()
df['step'].nunique()
print(df['type'].unique())
print(df['isFraud'].sum())
print(df['isFlaggedFraud'].sum())