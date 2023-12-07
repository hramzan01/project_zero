    import pandas as pd
    import os

    def server_grab(self):

        root_path = os.path.dirname(__file__)
        csv_path = os.path.abspath(os.path.join(root_path, '..', 'data', 'csv'))
        server_path = os.path.abspath(r'X:\13470_Project_Zero\00_Production\00_BIM\01_Schedules\DataSources\00_Hangzhou_RhinoSourceSchedule.csv')

        df = pd.read_csv(server_path)
        output = df.to_csv(os.path.abspath(os.path.join(csv_path, 'data_city_hz.csv')), index=False)

        print('--data transfer complete!--')

        return output
