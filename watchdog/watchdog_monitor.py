import sys
import time
import logging
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CustomEventHandler(FileSystemEventHandler):
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def on_any_event(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'modified' and event.src_path == self.csv_path:
            # Run the script only when the specified CSV file is modified
            self.convert_design_data()


# Functions to process the design data once a modified csv has been detected
    
    def convert_design_data(self):
        import os
        import pandas as pd

        # ////////////////////////////////////////////////////////////////////// READING DATA 

        # # define csv path
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..', '..')) # uncomment for packaging 
        parent_directory = os.path.abspath(os.path.join(script_directory)) # uncomment for testing
        csv_file_name = 'data_design.csv'

        # Construct the full path to the CSV file
        csv_path = os.path.join(parent_directory, csv_file_name)
        df = pd.read_csv(csv_path)
        print('----------------------')
        print('reading raw model data...')

        # ////////////////////////////////////////////////////////////////////// PROCESSING DATA
        
        # 00 Retreiving energy demmand
        def preprocess_design_data(df): # define preprocessed data for utilities
            
                # df_model instance
                design_data = df.copy()

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
        result = preprocess_design_data(df)      
        def return_energy_demmand(result): # run processed de through pipe
            import dill
            
            preproc_design_data = result

            # Construct the full path to the CSV file
            pickle_file = 'pipeline.pkl'
            pickle_path = os.path.join(parent_directory, pickle_file)

            # Load the pipeline using dill
            with open(pickle_path, 'rb') as file:
                pipe = dill.load(file)

            preproc_design_data.reset_index(drop=True, inplace=True)
            preproc_design_data['electricity_demmand'] = pipe.predict(preproc_design_data).astype(int)

            return preproc_design_data
        energy_demmands = return_energy_demmand(result) # define outputs
        print('processing demmand data...')

        # 01 Retreiving population data
        def get_building_population(df):
                
            # df_model instance
            df_model = df.copy()
            df_coef = pd.read_csv(os.path.join(parent_directory, 'data_coefficients.csv')) 

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
        population_data = get_building_population(df)
        print('processing population data...')


        # ////////////////////////////////////////////////////////////////////// EXPORTING DATA    

        # Exporting Energy Demmand
        export_file_demmand = 'data_demmand.csv'
        export_path_demmand = os.path.join(parent_directory, export_file_demmand)
        energy_demmands.to_csv(export_path_demmand, index=False)
        print('exported data demmand successfuly ✓')

        # Exporting Population Demmand
        export_file_population = 'data_population.csv'
        export_path_population = os.path.join(parent_directory, export_file_population)
        population_data.to_csv(export_path_population, index=False)
        print('exported data population successfuly ✓')
    


if __name__ == "__main__":

    # # define csv path
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..', '..')) # uncomment for packaging 
    parent_directory = os.path.abspath(os.path.join(script_directory)) # uncomment for testing
    csv_file_name = 'data_design.csv'


    # Construct the full path to the CSV file
    csv_path = os.path.join(parent_directory, csv_file_name)

    # print welcome message
    print('--------------------------')
    print('* Watchdog is monitoring *')
    print('--------------------------')
    print("  / \\__")
    print(" (    @\\____")
    print(" /           O")
    print("/   (_____/")
    print("/_____/   U")
    print("                          ")
    print(csv_path)

    # print logging information
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


    event_handler = CustomEventHandler(csv_path)
    observer = Observer()
    observer.schedule(event_handler, parent_directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
