"""
This dash app displays
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import flask

# load the data
# eventually the app should allow generating a data file via a query
df_drugs = pd.read_csv('named_drugs.csv')
df_authors = pd.read_csv('authors_metrics.csv')
df_publications = pd.read_csv('pubs_per_year.csv')

# the list of drugs in the dataframe to populate the dropdown menu with
available_drugs = [x.capitalize() for x in df_drugs.columns.values[1:]]

# the list of journals in the dataframe to populate the dropdown menu with
journals = sorted(df_publications.columns[1:])

# the network png directory
image_directory = '/static/'

app = dash.Dash()

app.layout = html.Div( # the top most div gives the left and right margins
    className='ten columns offset-by-one',
    children = [
        html.Div( # this div contains the title
            className='row',
            children = [
                html.Div(
                    className='eight columns',
                    children = [
                        html.H1('Title')
                        ]
                ),
                html.Div(
                    className='one columns',
                    children = [
                        html.H3('logo')
                    ],
                    style = {'float': 'right'}
                )
            ]
        ),
        html.Div( # sub header
            className='row',
            children = [
                html.H5('Some general statistics about the datasets used(?)')
            ]
        ),
        html.Div( # network metrics
            className='row',
            children =[
                html.Div(
                    className='seven columns',
                    children = [
                        html.Div([ # the network metrics graph lives in this div
                            dcc.Graph(id='author_metrics'),
                            html.Div([
                                dcc.RadioItems(
                                    id='metric',
                                    options = [{'label':i, 'value':i} for i in ['Degree', 'Betweenness']],
                                    value='Betweenness'
                                )
                            ], style = {'font-family': ['Verdana', 'Times']})
                        ])
                    ]
                ),
                html.Div(
                    className='five columns',
                    children = [
                        html.H5('Authors network 2003-2018'),
                        html.Img(
                            src='{}networkx_graph_3.png'.format(image_directory),
                            style={'width': '500px', 'margin':'auto'}
                        )
                    ]
                )
            ],
            style={'margin-top': '20px', 'margin-bottom':'30px'}
        ),
        html.Div( # a row for the year slider
            className='row',
            children = [
                html.Div(
                    children = [
                        html.P('Filter by publication year:'),
                        html.Div([
                            dcc.RangeSlider(
                                # a range slider outputs two values
                                id='year-slider',
                                min=df_drugs.year.min(),
                                max=df_drugs.year.max(),
                                value=[df_drugs.year.min(), df_drugs.year.max()],
                                step=1,
                                # Only show every 5th year in the slider
                                marks={str(year): {'label': str(year),
                                                'style':{'font-family':['Verdana', 'Times']}
                                                } for year in df_drugs.year.values if year%5==0
                                }
                            )
                        ])
                    ],
                    style={'margin-top': '20px', 'margin-bottom':'30px'}
                )
            ]
        ),
        html.Div( # a row with dropdown menus
            className='row',
            children = [
                html.Div(
                    className='six columns',
                    children = [
                        html.P('Filter by drug name:'),
                        html.Div([
                            dcc.Dropdown(
                                id='drug_names',
                                options = [{'label':i, 'value':i} for i in available_drugs],
                                value=['Levodopa', 'Amantadine'],
                                multi=True
                            )
                        ], style = {'font-family': ['Verdana', 'Times']})
                    ]
                ),
                html.Div(
                    className='six columns',
                    children = [
                        html.P('Filter by Journal:'),
                        html.Div([
                            dcc.Dropdown(
                                id='journals',
                                options = [{'label': j, 'value': j} for j in journals],
                                value=['Annals of neurology', 'Brain : a journal of neurology',
                                    'Acta neurologica Scandinavica'],
                                multi=True
                            )
                        ], style = {'font-family': ['Verdana', 'Times']})
                    ]
                )
            ]
        ),
        html.Div( # a row with graphs
            className='row',
            children=[
                html.Div(
                    className='six columns',
                    children = [
                        dcc.Graph(id='drug-graph')
                    ]
                ),
                html.Div(
                    className='six columns',
                    children = [
                        dcc.Graph(id='journals-bar')
                    ]
                )
            ],
            style={}
        ),
        html.Div( # another row with graphs
            className='row',
            children=[
                html.Div(
                    className='six columns',
                    children = [
                        dcc.Graph(
                            id='journals-bubble',
                            figure={
                                'data': [
                                    go.Scatter(
                                        x=df_publications.year,
                                        y=df_publications[j],
                                        showlegend=False,
                                        text=j,
                                        mode='markers',
                                        opacity=0.7,
                                        marker={
                                            'size': df_publications[j] * 1.15,
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
                    ]
                ),
                html.Div(
                    className='six columns',
                    children = [
                        dcc.Graph(
                            id='top-journals-bar'
                        )
                    ]
                )
            ],
            style={}
        )
    ]
)

# callbacks for the graphs

# the drug-graph callback
@app.callback(
    Output('drug-graph', 'figure'),
    [Input('year-slider', 'value'),
    Input('drug_names', 'value')]
    )
def callback_a(year_values, drug_name_values):
    # select the range of years to display based on the range slider
    filtered_df = df_drugs.loc[(df_drugs.year >= year_values[0]) & (df_drugs.year <= year_values[1])]
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

# the journals bar graph callback
@app.callback(
    Output('journals-bar', 'figure'),
    [Input('year-slider', 'value'),
    Input('journals', 'value')]
    )
def callback_b(years, journal_names):
    filtered = df_publications.loc[(df_publications.year >= years[0])\
     & (df_publications.year <= years[1])]
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

# the network bar graph callback
@app.callback(
    Output('author_metrics', 'figure'),
    [Input('metric', 'value')]
)
def callback_c(metric_value):
    return {
        'data': [
            go.Scatter(
                x=df_authors['number of publications']\
                    .apply(lambda n: n+(np.random.random_sample()/5-0.1)), # adds jitter
                y=df_authors[metric_value],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 12,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name='scatter',
                text=df_authors.authors,
                hoverinfo='text'
            )
        ],
        'layout': go.Layout(
            xaxis={'title':'number of publications'},
            yaxis={'title':metric_value},
            hovermode='closest',

            title='Authors network metrics'
        )
    }



# serving the network image
@app.server.route('{}<path>.png'.format(image_directory))
def serv_image(path):
    image_name = '{}.png'.format(path)
    return flask.send_from_directory(image_directory, image_name)

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
    app.run_server()
