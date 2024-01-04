import pandas as pd
import numpy as np
from etl.extract import ProjectZero


class Typologies:
    '''
    DataFrames containing all features related to Typologies
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Typologies
        self.data = ProjectZero().get_data()

    def get_building_typology(self):
        # df_model instance
        df_model = self.data['hz_model'].copy()

        # Drop unecessary columns
        df_model = df_model.drop(columns=['ID','Colour'])

        # filtering str based columns 
        columns = list(df_model.columns)
        str_columns = [column for column in columns if columns != 'Area']

        # replace empty with unassigned
        for column in str_columns:
            df_model[column] = df_model[column].replace(' ','')
        
        # dropping empty values for building column
        df_model = df_model[df_model.Building != '']

        # Group by building type 
        df_grouped = df_model.groupby(['Building', 'Typology','Plot']).sum(False).reset_index().sort_values('Building')
        df_grouped.Area = df_grouped.Area.astype(int)
        
        return df_grouped

    def get_building_facade(self):
        # df_model instance
        df_model = self.data['hz_model'].copy()

        # if facade area not in df then generate estimate with utils.estimate_facade_area
        from etl.utils import estimate_facade_area

        if 'Facade' not in list(df_model.columns):
            df_model['Facade'] = estimate_facade_area(df_model, 4)

        # Create new data frame
        df = pd.DataFrame({'building': df_model.Building, 'area': df_model.Area,'facade': df_model.Facade })

        # dropping empty values for building column
        df = df[df.building != ' ']

        # group and sort
        df = df.groupby('building').sum(False).reset_index().sort_values('building')
        df

        # Turn area into int
        df.area = df.area.astype(int)

        return df

