import pandas as pd
import numpy as np
from etl.extract import ProjectZero


class Utilities:
    '''
    DataFrames containing all features related to Utilities
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Utilities
        self.data = ProjectZero().get_data()

    def get_training_data(self):
        # df_model instance
        df = self.data['ext_nyc'].copy()

        # Consider important features that can get from design model
        features = [
            'Primary Property Type - Self Selected',
            'Self-Reported Gross Floor Area (ft²)',
            'Year Built',
            'Occupancy',
            'Number of Buildings',
            'Electricity Use - Grid Purchase (kWh)'
        ]

        df = df[features]

        # rename nyc columns to match seattle
        df_renamed = df.rename(columns={
            'Primary Property Type - Self Selected': 'building_typology' ,
            'Self-Reported Gross Floor Area (ft²)': 'building_gfa',
            'Year Built': 'year_built',
            'Occupancy': 'occupancy',
            'Number of Buildings': 'num_buildings',
            'Electricity Use - Grid Purchase (kWh)': 'electricity_demmand'
        })

        # drop duplicates
        df_renamed.drop_duplicates(inplace=True)
        
        # missing data
        df_renamed.dropna(subset=['electricity_demmand'], inplace=True)

        # dropping outliers with booelan filtering

        #dropping huge outliers
        df_renamed = df_renamed[~((df_renamed['electricity_demmand'] > 50000000) | (df_renamed['building_gfa'] > 3000000))]

        # dropping outliers by typology
        # K-12 School
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'K-12 School') & (df_renamed['building_gfa'] > 800000))]

        # Hotel
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Hotel') & (df_renamed['building_gfa'] > 100000))]
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Hotel') & (df_renamed['building_gfa'] < 20000))]
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Hotel') & (df_renamed['electricity_demmand'] > 3000000))]

        # Multifamily Housing
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Multifamily Housing') & (df_renamed['building_gfa'] > 2000000))]
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Multifamily Housing') & (df_renamed['electricity_demmand'] > 14000000))]
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Multifamily Housing') & (df_renamed['electricity_demmand'] < 2000000) & (df_renamed['building_gfa'] > 700000) )]

        # Hospital (General Medical & Surgical)
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Hospital (General Medical & Surgical)') & (df_renamed['electricity_demmand'] < 20000000) & (df_renamed['building_gfa'] > 1300000) )]
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Hospital (General Medical & Surgical)') & (df_renamed['electricity_demmand'] < 30000000) & (df_renamed['building_gfa'] > 1700000) )]

        # Museum
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Museum') & (df_renamed['building_gfa'] > 500000))]

        # Retail Store
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Retail Store') & (df_renamed['building_gfa'] > 1000000))]

        # College/University
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'College/University') & (df_renamed['electricity_demmand'] > 20000000))]
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'College/University') & (df_renamed['electricity_demmand'] < 5000000) & (df_renamed['building_gfa'] > 249000) )]
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'College/University') & (df_renamed['electricity_demmand'] > 10000000) & (df_renamed['building_gfa'] < 500000) )]

        # Performing Arts
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Performing Arts') & (df_renamed['electricity_demmand'] > 15000000))]

        # Prison/Incarceration
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Prison/Incarceration') & (df_renamed['electricity_demmand'] > 20000000))]

        # Courthouse
        df_renamed = df_renamed[~((df_renamed['building_typology'] == 'Courthouse') & (df_renamed['building_gfa'] > 1000000))]

        # Year Build
        df_renamed = df_renamed[df_renamed.year_built > 1850]

        # number of buildings
        df_renamed = df_renamed[df_renamed.num_buildings < 20]

        return df_renamed
                
