from math import radians, sin, cos, asin, sqrt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np



'''functions to help in scripts'''

# def extract_csv_from_excel(file,tab)
def excel_to_csv(path, tab):
    df = pd.read_excel(path,tab)
    file = path.replace('.xlsx','.csv').replace('xcl','csv')
    result = df.to_csv(file)
    print(f'\n--csv extracted sucessfully as {file}--\n')

    return result 

# calculate the facade of a building based on area
def estimate_facade_area(df: pd.DataFrame, height: int):
    area = df.Area
    perimeter = np.sqrt(area) * 4
    facade = perimeter * height
    series = df['Facade'] = facade.astype(int)

    return series

# calculate the volume on the height
def estimate_volume(df: pd.DataFrame, height: int):
    area = df.Area
    volume = area * height
    df['volume_m3'] = volume.astype(int)

    return df