"""
This dash app displays a bar chart of the total number of publications vs
publications in top-ranking journals
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash()

df = pd.read_csv('top_jr_counts.csv', index_col='date')

radio_values = ['Total Number of Publications',
                'Number of Publications in Top-Ranking Journals',
                'Percentage of Publications in Top-Ranking Journals']

app.layout = html.Div([
    dcc.RadioItems(
        id='dist',
        options=[{'label': i, 'value': i} for i in radio_values],
        value='Total Number of Publications',
        labelStyle={'display': 'inline'}
    ),
    html.Div([
        html.Div(
            className='six columns',
            children=dcc.Graph(id='pubs-over-time')
        )
    ], style = {'font-family': ['Verdana', 'Times']})
], style = {'font-family': ['Verdana', 'Times']})

@app.callback(
    dash.dependencies.Output('pubs-over-time', 'figure'),
    [dash.dependencies.Input('dist', 'value')])
def display_pubs_over_time(value):
    return {
        'data': [
            {
                'x': df.index,
                'y': df.iloc[:, radio_values.index(value)],
                'type': 'bar'
            }
        ],
        'layout': {
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': '{} of publications'.format(['Number',
                     'Percentage'][radio_values.index(value) == 2])},
            'title': value + ' per Year Since 1999',
            'margin': {'l': 70, 'b': 100, 't': 70, 'r': 25}
        }
    }


if __name__ == '__main__':
    app.run_server()
