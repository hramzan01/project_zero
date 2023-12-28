
import pandas as pd
import numpy as np
import sqlite3
import os


class ProjectZero:
    def get_data(self):

        root_path = os.path.dirname(__file__)
        csv_path = os.path.abspath(os.path.join(root_path, '..', 'data', 'raw', 'csv'))

        file_names = [file for file in os.listdir(csv_path) if file.endswith('.csv')]

        key_names = []
        for file in file_names:
            file = file.replace('.csv','')
            file = file.replace('data_','')
            key_names.append(file)

        data = {}

        for (key, df) in zip(key_names, [pd.read_csv(os.path.join(csv_path, file)) for file in file_names]):
            data[key] = df

        return data
