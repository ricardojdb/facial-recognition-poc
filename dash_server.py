from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash

from datetime import datetime
import mysql.connector
import pandas as pd
import base64
import os

from utils import sql_utils
from utils import utils

app = dash.Dash()
app.css.append_css({'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'})
app.css.append_css({'external_url': 'https://www.w3schools.com/w3css/4/w3.css'})

sql_utils.create_mysql_table()

photos = utils.get_photos("dockers/knn/images")

def generate_html_table(df):
    table = [html.Tr([html.Th(col) for col in df.columns], className="w3-blue")]
    for i in range(len(df)):
        rows = []
        for col in df.columns:
            if col == "Photo":
                row = html.Td(
                        html.Img(
                        src="data:image/png;base64,{0}".format(df.iloc[i][col]), 
                        width="120", 
                        height="120"),
                        className="table-row center")
                rows.append(row)
            else:
                row = html.Td(df.iloc[i][col])
                rows.append(row)
        table.append(html.Tr(rows))

    return html.Table(table, className="table table-bordered w3-table-all w3-hoverable")

app.layout = html.Div([
    html.Div(id='table', className="table-responsive"),
    dcc.Interval(
            id='update-table',
            interval=1*1000, n_intervals=0)
], className="container")

@app.callback(Output('table', 'children'),
              [Input('update-table', 'n_intervals')])
def update_metrics(n):
    conn =  mysql.connector.connect(
        host="localhost",
        user="admin",
        passwd="admin",
        database="facedb")
        
    df = pd.read_sql(
        "SELECT Name, FirstSeen, max(LastSeen) as LastSeen "
        "FROM facedb.recognition "
        "GROUP BY Name "
        "ORDER BY LastSeen desc", conn)

    df["Photo"] = df["Name"].map(lambda x: photos[x])
    
    conn.close()
    return generate_html_table(df)

app.run_server()