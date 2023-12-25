
import pandas as pd
import numpy as np
import sqlite3
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


# Function to read CSV files and push to SQLite
def csv_to_sqlite(csv_file, conn):
    # Read CSV into DataFrame
    df = pd.read_csv(csv_file)

    # Extract table name from file name (without extension)
    table_name = os.path.splitext(os.path.basename(csv_file))[0]

    # Save DataFrame to SQLite database
    df.to_sql(table_name, conn, index=False, if_exists='replace')

# Define the parent folder and the data/sqlite folder
parent_folder = '..'  # Assuming your parent folder is one level above the current script
sqlite_folder = os.path.join(parent_folder, 'data', 'sqlite')

# Connect to SQLite database in the sqlite_folder
db_file = os.path.join(sqlite_folder, 'db_project_zero.sqlite')
conn = sqlite3.connect(db_file)

# Get a list of all CSV files in the current folder
csv_files = [file for file in os.listdir() if file.endswith('.csv')]

# Iterate through CSV files and push to SQLite
for csv_file in csv_files:
    csv_to_sqlite(csv_file, conn)

# Close the database connection
conn.close()

print("---Data import completed---")
