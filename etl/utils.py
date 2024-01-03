from math import radians, sin, cos, asin, sqrt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



# functions to help in scripts

# calculate the facade of a building based on area
def facade_area(area):
    pass


# calculate the number of floors based on the height
def facade_area(height):
    pass

# def extract_csv_from_excel(file,tab)
def excel_to_csv(path, tab):
    df = pd.read_excel(path,tab)
    file = path.replace('.xlsx','.csv').replace('xcl','csv')
    result = df.to_csv(file)
    print(f'\n--csv extracted sucessfully as {file}--\n')

    return result 