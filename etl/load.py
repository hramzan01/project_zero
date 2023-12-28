import pandas as pd
import numpy as np
import sqlite3
import os

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
