import pandas as pd
import numpy as np
import os


class ProjectZero:
    def get_data(self):

        root_path = os.path.dirname(__file__)
        csv_path = os.path.abspath(os.path.join(root_path, '..', 'data', 'csv'))
        
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

    def server_grab(self):

        root_path = os.path.dirname(__file__)
        csv_path = os.path.abspath(os.path.join(root_path, '..', 'data', 'csv'))
        #server_path = os.path.abspath(r'X:\13470_Project_Zero\00_Production\00_BIM\01_Schedules\DataSources\00_Hangzhou_RhinoSourceSchedule.csv')
        server_path = input('Specify file path from server➡️:')

        df = pd.read_csv(server_path)
        output = df.to_csv(os.path.abspath(os.path.join(csv_path, 'data_city_hz.csv')), index=False)

        print('--data transfer complete!--')

        return output



    
