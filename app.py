import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
from flask import Flask

import os
import base64
import datetime
import io

from scipy.spatial.distance import cdist

external_css = ["css/style.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]

app = dash.Dash(
    name='TerrorXAfrica',
    #    sharing=True,
    #    url_base_pathname='/earthquake-distances',
    external_stylesheets=external_css
)

app.title = "Fatalities trough Terror"
#app.config.requests_pathname_prefix = app.config.routes_pathname_prefix.split('/')[-1]


# app.config.update({
# as the proxy server will remove the prefix
#  'routes_pathname_prefix': '/earhtquake-distances/',

# the front-end will prefix this string to the requests
# that are made to the proxy server
#   'requests_pathname_prefix': '/earthquake-distances/'
# })


server = app.server

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
data = pd.read_csv('./data/TerrorAfricaTime.csv')
opts = [{'label' : i, 'value' : i} for i in data.event_type.unique()]
#opts[0]['all'] = 'all'

app.layout = html.Div([
    ############################
    # CONTROLS
    html.Div([html.H1(children='Fatalities Trough Terror'),
                  html.Div([
                  html.Div([
                      dcc.Graph(
                          # figure=figure,
                          id='distance-simulation'
                      )],
                      style={'width': '99%',
                           'padding': '0px 0px 0px 0px',
                           'display': 'inline-block',
                           'margin':{'t': 0}
                           })
                  ],
                      style={
                      "margin":{'t': 0},
                      'display': 'inline-block',
                          'width': '38%'
                  }
                  ),
        html.Div([
        html.Div([
        # dropdown
                html.P([
                    html.Label("Choose type of violence"),
                    dcc.Dropdown(id = 'opt',
                                 options=opts,
                                 #[
                                    # {'label': 'New York City', 'value': 'NYC'},
                                    # {'label': 'Montreal', 'value': 'MTL'},
                                    # {'label': 'San Francisco', 'value': 'SF'}
                                    # ],
                                 value='Violence against civilians'
                                 )
                        ], style = {'width': '400px',
                                    'fontSize' : '20px',
                                    'padding-left' : '50px',
                                    'display': 'inline-block',
                                    'margin':{'t': 40}
                                    }
                ),
            html.Br(),
            html.Label('Fatalities'),
            dcc.Slider(
                id='Fatalities',
                min=0,
                max=100,
                value=20.0,
                step=1,
                #marks={str(h) : {'label' : str(h), 'style':{'color':'red'} for h in range(0, 24)},
                marks={
                    '0': '0',
                    '50': '50',
                    '100': '100'
                }
            )

        ],
        style={'height': '10%',
               'width': '30%',
               'display': 'inline-block'
               }
    ),
     html.Br(),
      html.Br(),
   html.Div([
      dcc.Graph(
          # figure=figure,
          id='time'
      )],
      style={'width': '99%',
           #'padding': '0px 0px 0px 0px',
           #'display': 'inline-block',
           'margin':{'t': 40}
           }),
      html.Div(dcc.Slider(
           id='yearSlider',
           min=data['year'].min(),
           max=data['year'].max(),
           value=data['year'].max(),
           marks={str(year): str(year) for year in data['year'].unique()}
           ),
       style={'width': '99%',
            'padding': '0px 10px 0px 40px',
            'display': 'inline-block',
            'margin':{'t': 40}
            }),
html.Br(),
# html.Div(DataTable(rows=[{}]), style={'display': 'none'})
# html.Div([
#     dash_table.DataTable(
#         id='highscore',
#         columns=[{"name": i, "id": i, 'deletable': True} for i in data.fatalities],
#         editable=True,
#         n_fixed_columns=2,
#         style_table={'maxWidth': '1500px'},
#         row_selectable="multi",
#         selected_rows=[0],
#         style_cell = {"fontFamily": "Arial", "size": 10, 'textAlign': 'left'}
#         )
#     ]),# className=" twelve columns"),
    html.Br(),
        #####################################
        # Graphics
        html.Div([
            dcc.Graph(
                id='contour-of-distance'
            )
        ],
            style={'float': 'left',
                    "margin":{'t': 40},
                   'display': 'inline-block',
                   'width': '49%'
                   }
        )],
    style={'float': 'right',
            'height': '10%',
           'width': '39%',
           'display': 'inline-block'
           }
    )],style={
            #"margin":{'t': 0},
             'display': 'inline-block'
           }
    )],style={
            #"margin":{'t': 0},
             'display': 'inline-block'
           }
    )

@app.callback(
    dash.dependencies.Output('distance-simulation', 'figure'),
    [dash.dependencies.Input('Fatalities', 'value'),
     dash.dependencies.Input('opt', 'value'),
     dash.dependencies.Input('yearSlider', 'value')
     # dash.dependencies.Input('year_slider', 'value'),
     ]
)


def update_simulation(Fatalities, opt,yearSlider):

    Fatalities=float(Fatalities)

    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
    # df.head()

    scl=[[0, "rgb(172, 10, 5)"], [0.35, "rgb(190, 60, 40)"], [0.5, "rgb(245, 100, 70)"],
           [0.6, "rgb(245, 120, 90)"], [0.7, "rgb(247, 137, 106)"], [1, "rgb(255, 220, 220)"]]


    df = data[data['year'] == int(yearSlider)]
    if opt =="all":
        df = df
    else:
        df = df[df.event_type == opt]
    #df = df[df.fatalities!=0]

    df = df[0:2000]
    #df = df[df.event_date in year_slider]

    return{
        'data': [go.Scattergeo(
            # locationmode = 'USA-states',
            lon=df["longitude"],
            lat=df["latitude"],
            text=df["text"],
            mode='markers',
            marker=dict(
                size=np.log(df["fatalities"]+1)*10,
                opacity=0.8,
                reversescale=True,
                autocolorscale=False,
                symbol='square',
                line=dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale=scl,
                cmin=1,
                color=df["fatalities"],
                cmax=df["fatalities"].max(),
                colorbar=dict(
                    title="Fatalities through Terror"
                )
            ))],
        'layout':  go.Layout(
            #title='Fatalities through Terror<br>(Hover for info)',
                height=900,
                width=1000,
            geo=dict(
                scope='africa',
                projection=dict(type='mercator'),
                showland=True,
                landcolor="rgb(180,180,180)",
                subunitcolor="rgb(217, 217, 217)",
                countrycolor="rgb(217, 217, 217)",
                countrywidth=0.5,
                subunitwidth=0.5
            ),
        )
    }

@app.callback(
    dash.dependencies.Output('time', 'figure'),
    [dash.dependencies.Input('Fatalities', 'value'),
     dash.dependencies.Input('yearSlider', 'value')
     # dash.dependencies.Input('year_slider', 'value'),
     ]
)

def update_time(Fatalities, yearSlider):

    df = data[data['year'] == int(yearSlider)]
    #df = df[df.event_type == opt[1]]
    Fatalities=float(Fatalities)


    #data = pd.read_csv('data/TerrorAfricaTime.csv')
    trace = go.Scatter(x=data.event_date,
                    y=data.fatalities,
                    line=dict(
                        color='rgb(172, 10, 5)')
                        )

    fig=plotly.tools.make_subplots(
        rows=1,
        cols=1,
        #horizontal_spacing=0.1,
        #vertical_spacing=0.1,
    )

    fig.append_trace(trace, 1, 1)


    fig['layout'].update(
        title="",#'From 1991 to 2019',
        yaxis=dict(
            title="fatalities",
            range=[0, 1500],
            autorange=False,
            showgrid=True,
            zeroline=True,
            showline=True,
            ticks='',
            showticklabels=True
            ),
        xaxis=dict(
            title="time",
            rangeslider=dict(
                visible = True
                ),
            type='date'
            ),
        height=200,
        width=800,
        autosize=False,
        scene=dict(
            aspectmode="data"
        ),
        margin={'t':10}
    )

    return fig
    #
    #
    # layout = dict(
    #     title='Time series with range slider and selectors',
    #     yaxis=dict(
    #         range=[0, 2000],
    #         autorange=False,
    #         showgrid=True,
    #         zeroline=True,
    #         showline=True,
    #         ticks='',
    #         showticklabels=True
    #         ),
    #     xaxis=dict(
    #         rangeselector=dict(
    #             buttons=list([
    #                 dict(count=1,
    #                     label='1m',
    #                     step='month',
    #                     stepmode='backward'),
    #                 dict(count=6,
    #                     label='6m',
    #                     step='month',
    #                     stepmode='backward'),
    #                 dict(count=1,
    #                     label='YTD',
    #                     step='year',
    #                     stepmode='todate'),
    #                 dict(count=1,
    #                     label='1y',
    #                     step='year',
    #                     stepmode='backward'),
    #                 dict(step='all')
    #                 ])
    #         ),
    #         rangeslider=dict(
    #             visible = True
    #             ),
    #         type='date'
    #         )
    #     )
    #
    # fig =dict(data=data, layout=layout)
    # return fig
# Step 5. Add callback functions

# @app.callback(Output('highscore', 'data'),
# 	[dash.dependencies.Input('yearSlider', 'value')
#     ])
# def update_table(yearSlider):
#     df = df[df['year'] == int(yearSlider)]
#     return df

@app.callback(
    dash.dependencies.Output('contour-of-distance', 'figure'),
     [dash.dependencies.Input('Fatalities', 'value'),

     dash.dependencies.Input('yearSlider', 'value')
     ])
def update_graph(Fatalities, yearSlider):
    df = data[data['year'] == int(yearSlider)]

    Fatalities=float(Fatalities)



    contoursDict=dict(start=0,
                        end=70,
                        size=5,
                        coloring='heatmap',
                        showlabels=True,
                        labelfont=dict(
                            family='Raleway',
                            size=12,
                            color='white')
                        )

    colorBarDict=dict(
        title='Distance [km]',
        titleside='top',
        x=1.2,
        # xpad=100,
        titlefont=dict(
            size=14,
            family='Arial, sans-serif'
        )
    )

    autoContour=False

    trace0=go.Histogram(
        x=df.fatalities,
        marker=dict(
            color='rgb(172, 10, 5)'),
        nbinsx = 100
    )

    # trace1=go.Histogram(
    #     x=data.fatalities,
    #     nbinsx = 40
    # )
    #
    # trace2=go.Histogram(
    #     x=data.fatalities,
    #     nbinsx = 400
    # )


    fig=plotly.tools.make_subplots(
        rows=1,
        cols=1,
        horizontal_spacing=0.1,
        vertical_spacing=0.1,
        subplot_titles=(
            "Number of Incidents",
            "",
            ""
        )
    )

    fig.append_trace(trace0, 1, 1)
    #fig.append_trace(trace1, 2, 1)
    #fig.append_trace(trace2, 3, 1)

    fig['layout'].update(
    xaxis=dict(
        title="fatalities",
        #type='log',
        autorange=True
    ),
    yaxis=dict(
        title="frequency",
        type='log',
        autorange=True
    ),
        height=400,
        width=800,
        autosize=False,
        scene=dict(
            aspectmode="data"
        )
    )

    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
#    app.run_server(debug=True, host='127.0.0.1', port=6000)
