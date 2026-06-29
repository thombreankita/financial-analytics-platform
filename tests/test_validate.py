import pytest
import pandas as pd
from pathlib import Path
from ingestion.validate import(
    required_columns,
    check_file_ready,
    validate_schema,
    validate_business_rules
)

@pytest.fixture
def valid_df() -> pd.Dataframe:
    df = pd.read_csv('Path(__file__).parent.parent / "data" / "raw" / "PS_20174392719_1491204439457_log.csv"', nrows = 10000)
    return df
pass

def required_columns_passed_with_validdf(valid_df: pd.DataFrame):
    col_req = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig', 'nameDest', 'oldbalanceDest','newbalanceDest', 'isFraud', 'isFlaggedFraud']
    required_columns(valid_df,col_req)
    pass


