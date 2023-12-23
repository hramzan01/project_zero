# test_data_checks.py
import pandas as pd
from src.data_checks import check_data_integrity

def test_check_data_integrity_no_issues():
    # Test case with clean data
    df = pd.DataFrame({"col1": [1, 2, 3, 4], "col2": ["a", "b", "c", "d"]})
    issues = check_data_integrity(df)
    assert not issues, f"Unexpected issues found: {issues}"

def test_check_data_integrity_with_missing_values():
    # Test case with missing values
    df = pd.DataFrame({"col1": [1, 2, None, 4], "col2": ["a", "b", "c", "d"]})
    issues = check_data_integrity(df)
    assert "Missing values found." in issues, f"Missing values issue not found: {issues}"

def test_check_data_integrity_with_duplicates():
    # Test case with duplicate rows
    df = pd.DataFrame({"col1": [1, 2, 3, 3], "col2": ["a", "b", "c", "c"]})
    issues = check_data_integrity(df)
    assert "Duplicate rows found." in issues, f"Duplicate rows issue not found: {issues}"
