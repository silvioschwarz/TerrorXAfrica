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
    name='earthquake-distances-app',
    #    sharing=True,
    #    url_base_pathname='/earthquake-distances',
    external_stylesheets=external_css
)

app.title = "Fatalities trough Terror"

# app.config.update({
# as the proxy server will remove the prefix
#  'routes_pathname_prefix': '/earhtquake-distances/',

# the front-end will prefix this string to the requests
# that are made to the proxy server
#   'requests_pathname_prefix': '/earthquake-distances/'
# })


server = app.server

# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
#data = pd.read_csv('./data/acledTerror.csv')

app.layout = html.Div([
    ############################
    # CONTROLS
    html.Div([html.H1(children='Fatalities Trough Terror'),
                  html.Div([
                      dcc.Graph(
                          # figure=figure,
                          id='distance-simulation'
                      ),
                       html.Br(),
            html.Label('From 2007 to 2017'),
            dcc.RangeSlider(
                id='year_slider',
                min=1991,
                max=2020,
                value=[1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020],
                marks={
                    '1991': '1991',
                    '1992': '1992',
                    '1993': '1993',
                    '1994': '1994',
                    '1995': '1995',
                    '1996': '1996',
                    '1997': '1997',
                    '1998': '1998',
                    '1999': '1999',
                    '2000': '2000',
                    '2001': '2001',
                    '2002': '2002',
                    '2003': '2003',
                    '2004': '2004',
                    '2005': '2005',
                    '2006': '2006',
                    '2007': '2007',
                    '2008': '2008',
                    '2009': '2009',
                    '2010': '2010',
                    '2011': '2011',
                    '2012': '2012',
                    '2013': '2013',
                    '2014': '2014',
                    '2015': '2015',
                    '2016': '2016',
                    '2017': '2017',
                    '2018': '2018',
                    '2019': '2019',
                    '2020': '2020'
                }
            )
                  ],
                      style={
                      'display': 'inline-block',
                          'width': '68%'
                  }
                  ),
        html.Div([
        html.Div([
            html.Label('Length'),
            dcc.Slider(
                id='Length',
                min=0,
                max=100,
                value=20.0,
                step=1,
                marks={
                    '0': '0',
                    '50': '50',
                    '100': '100'
                }
            ),
            #html.Br(),
            html.Label('Strike'),
            dcc.Slider(
                id='Strike',
                min=0,
                max=360,
                value=10.0,
                step=1,
                marks={
                    '0': '0',
                    '90': '90',
                    '180': '180',
                    '270': '270',
                    '360': '360'
                }
            ),
            #html.Br(),
            html.Label('Dip'),
            dcc.Slider(
                id='Dip',
                min=0,
                max=90,
                value=45,
                step=1,
                marks={
                    '0': '0',
                    '30': '30',
                    '60': '60',
                    '90': '90'
                }
            )

        ],
        style={'height': '10%',
               'width': '30%',
               'display': 'inline-block'
               }
    ),
html.Br(),
        #####################################
        # Graphics
        html.Div([
            dcc.Graph(
                id='contour-of-distance'
            )
        ],
            style={
                   'display': 'inline-block',
                   'width': '39%'
                   }
        )],
    style={#'float': 'left',
            'height': '10%',
           'width': '19%',
           'display': 'inline-block'
           }
    )]
    )]
    )

@app.callback(
    dash.dependencies.Output('contour-of-distance', 'figure'),
     [dash.dependencies.Input('Length', 'value'),
     dash.dependencies.Input('Strike', 'value'),
     dash.dependencies.Input('Dip', 'value'),
     ])
# def update_graph(EVENTLAT,EVENTLON,EQDEPTH,Width,DeltaW,Length,DeltaL,Strike,Dip):
def update_graph(Length, Strike, Dip):

    Length=float(Length)

    Strike=float(Strike)
    Dip=float(Dip)

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
        x=data.fatalities,
        nbinsx = 4
    )

    trace1=go.Histogram(
        x=data.fatalities,
        nbinsx = 40
    )

    trace2=go.Histogram(
        x=data.fatalities,
        nbinsx = 400
    )


    fig=plotly.tools.make_subplots(
        rows=3,
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
    fig.append_trace(trace1, 2, 1)
    fig.append_trace(trace2, 3, 1)

    fig['layout'].update(
        height=600,
        width=500,
        title='additional plots',
        autosize=False,
        scene=dict(
            aspectmode="data"
        )
    )

    return fig


@app.callback(
    dash.dependencies.Output('distance-simulation', 'figure'),
    [dash.dependencies.Input('Length', 'value'),
     dash.dependencies.Input('Strike', 'value'),
     dash.dependencies.Input('Dip', 'value'),
     dash.dependencies.Input('year_slider', 'value'),
     ]
)
# def update_simulation(EQLAT,EQLON,EQDEPTH,EVENTLAT,EVENTLON,Width,DeltaW,Length,DeltaL,Strike,Dip):
def update_simulation(Length, Strike, Dip, year_slider):

    Length=float(Length)
    Strike=np.deg2rad(float(Strike))
    Dip=np.deg2rad(float(Dip))

    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
    # df.head()

    scl=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"], [0.5, "rgb(70, 100, 245)"],
           [0.6, "rgb(90, 120, 245)"], [0.7, "rgb(106, 137, 247)"], [1, "rgb(220, 220, 220)"]]

    df=pd.read_csv('./data/TerrorAfrica.csv')
    df = df[df.fatalities!=0]

    df = df[0:1000]
    #df = df[df.event_date in year_slider]

    return{
        'data': [go.Scattergeo(
            # locationmode = 'USA-states',
            lon=df["longitude"],
            lat=df["latitude"],
            text=df["text"],
            mode='markers',
            marker=dict(
                size=df["fatalities"]/10,
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
            title='Fatalities through Terror<br>(Hover for airport names)',
                height=800,
                width=1200,
            geo=dict(
                scope='africa',
                projection=dict(type='mercator'),
                showland=True,
                landcolor="rgb(250, 250, 250)",
                subunitcolor="rgb(217, 217, 217)",
                countrycolor="rgb(217, 217, 217)",
                countrywidth=0.5,
                subunitwidth=0.5
            ),
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
#    app.run_server(debug=True, host='127.0.0.1', port=6000)
