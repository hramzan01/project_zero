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

    def preprocess_design_data(self):
        # df_model instance
        df_model = self.data['hz_model'].copy()
        
        return df_model
    
        # drop unneeded columns
        df_model.drop(columns=[''])
                    
    def get_training_data(self):
        # df_model instance
        df = self.data['ext_nyc'].copy()

        # Consider important features that can get from design model
        features = [
            'Primary Property Type - Self Selected',
            'Self-Reported Gross Floor Area (ft²)',
            'Largest Property Use Type - Gross Floor Area (ft²)',
            '2nd Largest Property Use Type',
            '2nd Largest Property Use - Gross Floor Area (ft²)',
            'Year Built',
            'Occupancy',
            'Number of Buildings',
            'Electricity Use - Grid Purchase (kWh)'
        ]

        df = df[features]
        
        # fill NaN for 2nd property type/gfa with primary
        df['2nd Largest Property Use Type'] = df['2nd Largest Property Use Type'].fillna(df['Primary Property Type - Self Selected'])
        df['2nd Largest Property Use - Gross Floor Area (ft²)'] = df['2nd Largest Property Use - Gross Floor Area (ft²)'].fillna(df['Largest Property Use Type - Gross Floor Area (ft²)']) 

        # rename nyc columns to match seattle
        df_renamed = df.rename(columns={
            'Primary Property Type - Self Selected': 'building_typology' ,
            'Self-Reported Gross Floor Area (ft²)': 'building_gfa',
            'Year Built': 'year_built',
            'Occupancy': 'occupancy',
            'Number of Buildings': 'num_buildings',
            'Electricity Use - Grid Purchase (kWh)': 'electricity_demmand',
            'Largest Property Use Type - Gross Floor Area (ft²)': 'primary_gfa',
            '2nd Largest Property Use Type': 'secondary_typology',
            '2nd Largest Property Use - Gross Floor Area (ft²)': 'secondary_gfa'
            })

        # Regressing GFA to Electricty consumption by filtered property type
        keep_types = [
            'Office',
            'K-12 School',
            'Hotel',
            'Multifamily Housing',
            'Hospital (General Medical & Surgical)',
            'Museum',
            'Retail Store',
            'College/University',
            'Laboratory',
            'Other - Mall',
            'Performing Arts',
            'Prison/Incarceration',
            'Courthouse'
       ]

        df_renamed = df_renamed[df_renamed.building_typology.isin(keep_types)]

        # drop duplicates
        df_renamed.drop_duplicates(inplace=True)
        
        # missing data
        df_renamed.dropna(subset=['electricity_demmand'], inplace=True)




        '''dropping outliers with booelan filtering'''

        # filtering out electricity demmand greater than 0
        df_renamed = df_renamed[df_renamed.electricity_demmand >= 0]

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

        '''renaming columns'''

        typology_remap = {
        # primary unique typologies
        'Office': 'office',
        'K-12 School': 'school',
        'Hotel': 'hotel',
        'Multifamily Housing': 'residential',
        'Hospital (General Medical & Surgical)': 'hospital',
        'Museum': 'museum',
        'Retail Store': 'retail',
        'College/University': 'university',
        'Laboratory': 'laboratory',
        'Other - Mall': 'mall',
        'Performing Arts': 'performing_arts',
        'Prison/Incarceration': 'prison',
        'Courthouse': 'courthouse'
        }

        df_renamed['building_typology'] = df_renamed['building_typology'].replace(typology_remap)
        df_renamed['secondary_typology'] = df_renamed['secondary_typology'].replace(typology_remap)
        
        # change secondary typology names to lower case and replace space with underscore
        df_renamed['secondary_typology'] = df_renamed['secondary_typology'].str.lower().str.replace(' ','_')

        return df_renamed
    
