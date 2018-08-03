"""
This dash app displays
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

# eventually the app should allow generating a data file via a query
df = pd.read_csv('../../static/dash_data/named_drugs.csv')

# the list of drugs in the dataframe to populate the dropdown menu with
available_drugs = [x.capitalize() for x in df.columns.values[1:]]

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='drug_names',
            options = [{'label':i, 'value':i} for i in available_drugs],
            value=['Levodopa', 'Amantadine'],
            multi=True
        )
    ], style = {'font-family': ['Verdana', 'Times']}),
    dcc.Graph(id='graph-with-slider'), # updated with the update_figure function below
    dcc.RangeSlider(
        # a range slider outputs two values
        id='year-slider',
        min=df.year.min(),
        max=df.year.max(),
        value=[df.year.min(), df.year.max()],
        step=1,
        # Only show every 5th year in the slider
        marks={str(year): {'label': str(year),
                           'style':{'font-family':['Verdana', 'Times']}
                           } for year in df.year.values if year%5==0
        }
    )
], style = {'width': '80%'})

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value'),
    Input('drug_names', 'value')]
    )
def update_figure(year_values, drug_name_values):
    # select the range of years to display based on the range slider
    filtered_df = df.loc[(df.year >= year_values[0]) & (df.year <= year_values[1])]
    traces = []
    for i in drug_name_values:
        # create a bar graph for each drug in the dropdown menu
        traces.append(go.Bar(
            x=filtered_df.year,
            y=filtered_df[i.upper()], # in the csv file the drugs are uppercase
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            barmode='group',
            xaxis={'title': 'Year'},
            yaxis={'title': 'Number of mentions'},
            title='Drug Mentions in Scientific Abstracts per Year Since 1969',
            margin={'l': 70, 'b': 100, 't': 100, 'r': 25},
            legend={'x': 0.8, 'y': 1},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
