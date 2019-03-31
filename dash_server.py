import dash
import dash_table
import pandas as pd

data = {
"Photo": ["None", "None", "None"]
"Name": ["Ricardo", "Jaspers", "Hugo"], 
"First seen":["28/03/2019 10:32", "28/03/2019 10:32", "28/03/2019 10:32"], 
"Last seen":["28/03/2019 11:32", "28/03/2019 11:32", "28/03/2019 11:32"],
}

df = pd.DataFrame(data)

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    data=df.to_dict('rows'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    style_header={
        'backgroundColor': 'rgb(174, 221, 255)',
        'fontWeight': 'bold',
        'fontSize': '24px',
        'font-family': 'verdana',
    },
    style_cell={
        'padding': '5px',
        'fontSize': '24px',
        'font-family': 'verdana',
    },
    style_cell_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(174, 221, 255)',
        } 
    ],
)

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)