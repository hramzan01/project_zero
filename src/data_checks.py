# data_checks.py
import pandas as pd

def check_data_integrity(df):
    issues = []

    if df.isnull().values.any():
        issues.append("Missing values found.")

    if df.duplicated().any():
        issues.append("Duplicate rows found.")

    return issues
