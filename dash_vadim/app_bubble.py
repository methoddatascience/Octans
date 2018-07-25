"""
This dash app displays a bubble chart of the number of publications in various
neurological journals since 1969
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

app = dash.Dash()

# based on the Parkinson's data
df = pd.read_csv('pubs_per_year.csv')

journals = sorted(df.columns[1:])

app.layout = html.Div([
    dcc.Graph(
        id='pubs-per-year',
        figure={
            'data': [
                go.Scatter(
                    x=df.year,
                    y=df[j],
                    showlegend=False,
                    text=j,
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': df[j] * 1.15,
                        'sizemin': 3},
                ) for j in journals
            ],
            'layout': go.Layout(
                xaxis={'title': 'Year'},
                yaxis={'type': 'log', 'title': 'Number of publications'},
                title='Journal Publications per Year Since 1969<br>' +
                      '(on a logarithmic scale)',
                margin={'l': 70, 'b': 100, 't': 100, 'r': 25},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server()
