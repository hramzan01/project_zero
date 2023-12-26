import pandas as pd
import numpy as np
import pytest
from numpy import nan
import os


csv_path = os.path.abspath('data/csv/data_utilities.csv')
# get data
df = pd.read_csv(csv_path)

# check if column exists
def test_col_exists():
    name="area"
    assert name in df.columns


# check for nulls
def test_null_check():
    assert df['area'].notnull().all()


# check values are unique
def test_unique_check():
    assert pd.Series(df['area']).is_unique


# check data type
def test_features_dtype_int():
    assert (df['area'].dtype == int or df['demmand'].dtype == float)
'''
# check data type
def test_productname_dtype_srt():
    assert (df['EnglishProductName'].dtype == str or  df['EnglishProductName'].dtype == 'O')

# check values in range
def test_range_val():
    assert df['SafetyStockLevel'].between(0,1000).any()

# check values in a list
def test_range_val_str():
    assert set(df.Color.unique()) == {'NA', 'Black', 'Silver', 'Red', 'White', 'Blue', 'Multi', 'Yellow','Grey', 'Silver/Black'}
'''
