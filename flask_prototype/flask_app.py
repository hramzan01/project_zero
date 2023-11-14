from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import plotly.express as px

app = Flask(__name__, static_folder='static')

# Replace this with your SQLite database connection details
DATABASE = 'C:/Users/hramzan/documents/github/dapzero/db_project_zero.sqlite'

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

def generate_bar_chart(data):
    fig = px.bar(data, x='Rating System')
    return fig.to_html(full_html=False)

@app.route("/", methods=["GET", "POST"])
def index():
    tables = fetch_tables()
    table_data = None
    bar_chart = None

    if request.method == "POST":
        selected_table = request.form["table"]
        table_data = fetch_table_data(selected_table)
        bar_chart = generate_bar_chart(table_data)

    return render_template("index.html", tables=tables, table_data=table_data, bar_chart=bar_chart)

if __name__ == "__main__":
    app.run()
