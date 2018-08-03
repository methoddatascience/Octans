"""
This dash app displays a bar graph of the number of publications in various
neurological journals since 1969
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

# based on the Parkinson's data
df = pd.read_csv('../../static/dash_data/pubs_per_year.csv')

journals = sorted(df.columns[1:])

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='journals',
            options = [{'label': j, 'value': j} for j in journals],
            value=['Annals of neurology', 'Brain : a journal of neurology',
                   'Acta neurologica Scandinavica'],
            multi=True
        )
    ], style = {'font-family': ['Verdana', 'Times']}),
    dcc.Graph(id='graph-with-slider'),
    dcc.RangeSlider(
        id='year-slider',
        min=df.year.min(),
        max=df.year.max(),
        value=[df.year.min(), df.year.max()],
        step=1,
        marks={str(year): {'label': str(year),
                           'style':{'font-family':['Verdana', 'Times']}
                           } for year in df.year if year % 5 == 0
        }
    )
], style = {'width': '80%'})

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value'),
    Input('journals', 'value')]
    )
def update_figure(years, journal_names):
    filtered = df.loc[(df.year >= years[0]) & (df.year <= years[1])]
    traces = []
    for j in journal_names:
        traces.append(go.Bar(
            x=filtered.year,
            y=filtered[j],
            name=j
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            barmode='group',
            xaxis={'title': 'Year'},
            yaxis={'title': 'Number of publications'},
            title='Journal Publications per Year Since 1969',
            margin={'l': 70, 'b': 100, 't': 100, 'r': 25},
            legend={'x': 0.8, 'y': 1},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
