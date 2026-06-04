import pandas as pd
from pathlib import Path

def load_and_inspect(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, nrows = 10000) #dataframe that stores top 1000 rows of the csv file
    print('Shape:',df.shape) # shape gives column, rows of the dataframe
    print('Columns:', df.columns.tolist()) # columns gives all the columns in the df and to list() shows it as a list of column names
    print('Dtypes: ')
    print(df.dtypes)#gives the datatype of all the columns
    print('Nulls:' ) #isnull() gives theentire df in matrix form of true and false values 
    print(df.isnull().sum()); #the sum() adds the total number of true in a particular column and gives the sum column wise
    return df


def get_positive_transactions(df: pd.DataFrame) -> pd.DataFrame:

    if "amount" not in df.columns:

        raise ValueError("amount column missing")
    print(df[df["amount"] > 0])
    return df[df["amount"] > 0] # df["amount"] > 0 creates a list 
#fpath = Path("/d/Financial-analytics-platform/data/raw/PS_20174392719_1491204439457_log.csv")

fpath = ( Path(__file__).resolve().parent.parent /"data"/"raw"/"PS_20174392719_1491204439457_log.csv")
df = load_and_inspect(fpath)

positive_df = get_positive_transactions(df)

print(positive_df.head())