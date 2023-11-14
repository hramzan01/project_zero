from flask import Flask, render_template, request
import sqlite3
import pandas as pd

app = Flask(__name__)

# Replace this with your SQLite database connection details
DATABASE = 'db_project_zero.sqlite'

def fetch_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def fetch_table_data(table_name):
    conn = sqlite3.connect(DATABASE)
    query = f"SELECT * FROM {table_name};"
    table_data = pd.read_sql_query(query, conn)
    conn.close()
    return table_data


@app.route("/", methods=["GET", "POST"])
def index():
    tables = fetch_tables()
    table_data = None

    if request.method == "POST":
        selected_table = request.form["table"]
        table_data = fetch_table_data(selected_table)

    return render_template("index.html", tables=tables, table_data=table_data)

if __name__ == "__main__":
    app.run()