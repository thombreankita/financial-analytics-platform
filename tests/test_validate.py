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
def valid_df() -> pd.DataFrame:
    fpat = Path(__file__).parent.parent / "data" / "raw" / "PS_20174392719_1491204439457_log.csv"
    df = pd.read_csv(fpat, nrows = 10000)
    return df
pass

def test_required_columns_passed_with_validdf(valid_df: pd.DataFrame):
    col_req = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig', 'nameDest', 'oldbalanceDest','newbalanceDest', 'isFraud', 'isFlaggedFraud']
    required_columns(valid_df,col_req)
    pass

def test_required_columns_raises_with_one_missing_column(valid_df : pd.DataFrame):
    col_req = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig', 'nameDest', 'oldbalanceDest','newbalanceDest', 'isFraud', 'isFlaggedFraud']
    df = valid_df.drop(columns=['type'])
    with pytest.raises(ValueError):
        required_columns(df,col_req)

def test_check_file_ready_raises_onmissing_file():
    fpath = Path(__file__).parent.parent / "data" / "test" / "PS_20174392719_1491204439457_log.csv"
    with pytest.raises(FileNotFoundError):
        check_file_ready(fpath)

def test_check_file_ready_raises_with_non_csv():
    fp = Path(__file__).parent.parent / "data" / "raw" / "datafile.txt"
    with pytest.raises(ValueError):
        check_file_ready(fp)

def test_validate_schema_with_validdf(valid_df: pd.DataFrame):
    validate_schema(valid_df)

def test_validate_schema_on_wrong_type(valid_df):
    df2 = valid_df.copy()
    df2 ["amount"] = df2["amount"].astype(str)
    with pytest.raises(TypeError):
        validate_schema(df2)

def test_validate_business_rules_with_validdf(valid_df: pd.DataFrame):
    validate_business_rules(valid_df)

def test_validate_business_rules_flags_negative_amount(valid_df: pd.DataFrame):
    df = valid_df.copy()
    df.loc[len(df)] = {
    "step": 1,
    "type": "PAYMENT",
    "amount": -500,
    "nameOrig": "C123",
    "oldbalanceOrg": 1000,
    "newbalanceOrig": 1500,
    "nameDest": "C456",
    "oldbalanceDest": 0,
    "newbalanceDest": 500,
    "isFraud": 0,
    "isFlaggedFraud": 0}
    result = validate_business_rules(df)
    assert result ['Amount'] == 1
    
