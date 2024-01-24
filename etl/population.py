import pandas as pd
import numpy as np
from etl.extract import ProjectZero


class Population:
    '''
    DataFrames containing all features related to Population
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Population
        self.data = ProjectZero().get_data()

    def get_building_population(self):
        
        # df_model instance
        df_model = self.data['hz_model'].copy()
        df_coef = self.data['ksa_coefficients'].copy()

        # rename and merge tables
        df_model.rename(columns=lambda x: x.lower(), inplace=True)
        df_model.typology = df_model.typology.str.lower()
        df_merged = df_model.merge(df_coef, on='typology',how='left')

        # appying coefficients to area
        coef_features = ['efficiency', 'parking req', 'residents', 'employees ', 'visitors']

        for i in coef_features:
            df_merged[i] = (df_merged[i]*df_merged.area).fillna(0 )
            df_merged[i] = df_merged[i].astype(int)

        # rename then return the df
        df_merged.rename(columns={'efficiency':'gfa'}, inplace=True)

        return df_merged
