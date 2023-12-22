import pandas as pd
import numpy as np

def generate_facade(df: pd.DataFrame, height: int):
    area = df.area
    perimeter = np.sqrt(area) * 4
    facade = perimeter * height
    df['facade_m2'] = facade.astype(int)
    
    return df

def generate_volume(df: pd.DataFrame, height: int):
    area = df.area
    volume = area * height
    df['volume_m3'] = volume.astype(int)
    
    return df