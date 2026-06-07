import pandas as pd
from pathlib import Path

def required_columns(df: pd.DataFrame, required: list) -> None:
    missed =[col for col in required if col not in df.columns]
    if missed :
        raise ValueError(f"Missing Columns:{missed}")


filep = (Path(__file__).resolve().parent.parent / "data" / "raw" / "PS_20174392719_1491204439457_log.csv")
df = pd.read_csv(filep, nrows=100000)
required = df.columns.to_list()
print(required)
req_col = ['amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig','isFraud', 'isFlaggedFraud']
required_columns(df,req_col)

print(f'__name__ is :{__name__}')
if __name__ == '__main__':
    print("Running directy")
