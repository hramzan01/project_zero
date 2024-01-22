import pandas as pd
import numpy as np
import pickle
from etl.extract import ProjectZero



class Utilities:
    '''
    DataFrames containing all features related to Utilities
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Utilities
        self.data = ProjectZero().get_data()

    ''''''

    def preprocess_design_data(self):
        # df_model instance
        design_data = self.data['hz_model'].copy()

        # drop irrelevant columns
        design_data.drop(columns=['ID','Volume','Elevation','Colour', 'Envelope'], inplace=True)
        
        # Rank areas within each building type
        design_data['Area_Rank'] = design_data.groupby('Building')['Area'].rank(ascending=False)

        # Sort by building and area rank
        design_data = design_data.sort_values(by=['Building', 'Area_Rank'])

        # Rank areas within each building and typology
        design_data['Area_Rank'] = design_data.groupby(['Building', 'Typology'])['Area'].rank(ascending=False)

        # Sort by building, typology, and area rank
        design_data = design_data.sort_values(by=['Building', 'Typology', 'Area_Rank'])

        # Set index before groupby to preserve all rows
        design_data.set_index(['Plot', 'Building', 'Typology', 'Area_Rank'], inplace=True)

        # Group by index and calculate the sum
        result_df = design_data.groupby(level=[0, 1, 2, 3]).sum()

        # Reset index to bring back the original DataFrame structure
        result_df.reset_index(inplace=True)

        # Find the index of the maximum 'Area_Rank' within each group
        max_rank_index = result_df.groupby(['Plot', 'Building'])['Area_Rank'].idxmax()

        # Create a new DataFrame with the highest ranked Typology and Area for each building
        primary_asset_df = result_df.loc[max_rank_index, ['Plot', 'Building', 'Typology', 'Area_Rank', 'Area']].reset_index(drop=True)

        # Rename the columns for clarity
        primary_asset_df.rename(columns={'Typology': 'Primary_Asset', 'Area': 'Primary_Asset_Area'}, inplace=True)

        # Merge the primary_asset_df back to the original DataFrame without automatic renaming of 'Area_Rank'
        result_df = pd.merge(result_df, primary_asset_df, left_on=['Plot', 'Building', 'Area_Rank'], right_on=['Plot', 'Building', 'Area_Rank'], how='left')

        # Exclude the rows corresponding to the maximum rank
        result_df_excluded_max = result_df[~result_df.index.isin(max_rank_index)]

        # Find the index of the second maximum 'Area_Rank' within each group in the remaining rows
        second_max_rank_index = result_df_excluded_max.groupby(['Plot', 'Building'])['Area_Rank'].idxmax()

        # Create a new DataFrame with the second highest ranked Typology and Area for each building
        second_primary_asset_df = result_df_excluded_max.loc[second_max_rank_index, ['Plot', 'Building', 'Typology', 'Area_Rank', 'Area']].reset_index(drop=True)

        # Rename the columns for clarity
        second_primary_asset_df.rename(columns={'Typology': 'Second_Asset', 'Area': 'Second_Asset_Area'}, inplace=True)

        # Merge the second_primary_asset_df back to the original DataFrame without automatic renaming of 'Area_Rank'
        result_df = pd.merge(result_df, second_primary_asset_df, left_on=['Plot', 'Building', 'Area_Rank'], right_on=['Plot', 'Building', 'Area_Rank'], how='left')

        agg_result = result_df.groupby(['Building','Plot']).agg({
            'Area': 'sum',
            'Primary_Asset': 'first',  # Assuming 'Primary_Asset' is the same for all rows within a building
            'Primary_Asset_Area': 'sum',
            'Second_Asset': 'first',   # Assuming 'Second_Asset' is the same for all rows within a building
            'Second_Asset_Area': 'sum'  # Assuming 'Second_Asset_Area' is the same for all rows within a building
        }).reset_index()

        from datetime import datetime
        # Get the current date
        current_year = datetime.now().year

        # adding missing columns
        agg_result['year_built'] = current_year
        agg_result['occupancy'] = 100
        agg_result['num_buildings'] = 1

        # rename and reorder to match training set
        preproc_design_data = pd.DataFrame({
            'building_id': agg_result['Building'],
            'plot_id': agg_result['Plot'],
            'building_typology': agg_result['Primary_Asset'].str.lower(),
            'building_gfa': agg_result['Area'],
            'primary_gfa': agg_result['Primary_Asset_Area'],
            'secondary_typology': agg_result['Second_Asset'].str.lower(),
            'secondary_gfa': agg_result['Second_Asset_Area'],
            'year_built': agg_result['year_built'],
            'occupancy': agg_result['occupancy'],
            'num_buildings': agg_result['num_buildings']
            })

        return preproc_design_data
    
    ''''''
                    
    def get_training_data(self):
        # df_model instance
        df = self.data['ext_nyc'].copy()

        # Consider important features that can get from design model
        features = [
            'Property Id',
            'Postal Code',
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
            'Property Id': 'building_id',
            'Postal Code': 'plot_id',
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
        'K-12 School': 'education',
        'Hotel': 'hotel',
        'Multifamily Housing': 'residential',
        'Hospital (General Medical & Surgical)': 'hospital',
        'Museum': 'museum',
        'Retail Store': 'retail',
        'College/University': 'education',
        'Laboratory': 'laboratory',
        'Other - Mall': 'mall',
        'Performing Arts': 'community',
        'Prison/Incarceration': 'prison',
        'Courthouse': 'courthouse'
        }

        df_renamed['building_typology'] = df_renamed['building_typology'].replace(typology_remap)
        df_renamed['secondary_typology'] = df_renamed['secondary_typology'].replace(typology_remap)
        
        # change secondary typology names to lower case and replace space with underscore
        df_renamed['secondary_typology'] = df_renamed['secondary_typology'].str.lower().str.replace(' ','_')

        return df_renamed
    
    ''''''

    def return_energy_demmand(self):
        import dill
        
        self.data = Utilities().preprocess_design_data()
        preproc_design_data = self.data.copy()

        # Load the pipeline using dill
        with open('pipeline/pipeline.pkl', 'rb') as file:
            pipe = dill.load(file)

        preproc_design_data.reset_index(drop=True, inplace=True)
        preproc_design_data['electricity_demmand'] = pipe.predict(preproc_design_data).astype(int)

        return preproc_design_data