# In[]:
# Import required libraries
import os
import pickle
import copy
import datetime as dt
from typing import Any, Union

import pandas as pd
import numpy as np
from flask import Flask
from flask_cors import CORS
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.plotly as py
from textwrap import dedent as d


# Multi-dropdown options
from controls import Countries

# change the working directory path to where this file is located #
from pandas import DataFrame, Series
from pandas.core.generic import NDFrame

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


app = dash.Dash(__name__)
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501
server = app.server
CORS(server)

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'  # noqa: E501
    })


# Create controls
# TODO TODO TODO


# Load data
fact = pd.read_csv(r'./data/fact.csv', encoding='latin-1')
attendance = pd.read_csv(r'./data/attendance.csv', encoding='latin-1')

## TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
#daily_attend_data = pd.DataFrame(fact.groupby('first_visit')['count_2019'].sum()).reset_index()
#reg_type_data = pd.DataFrame(fact.groupby('Reg_Type')['count_2019'].sum()).reset_index()
topcountries_data = pd.DataFrame(fact.groupby('Country')['count_2019'].sum()).reset_index().sort_values('count_2019', ascending=False)[1:11].sort_values('count_2019', ascending=True)

group_data = pd.DataFrame(fact.groupby('Group')['count_2019'].sum()).reset_index()
revisit_data = pd.DataFrame(attendance.groupby('attendance')['count_2019'].sum()).reset_index().sort_values('count_2019', ascending=False).sort_values('count_2019', ascending=True)
countries_data = pd.DataFrame(fact.groupby('Country')['count_2019'].sum()).reset_index()
#################################################################


# Create app layout
app.layout = html.Div(
    [
        ## add banner - this includes the logo and title
        html.Div(
            [
                html.Img(
                    src="https://raw.githubusercontent.com/GrejSegura/jelly-viz/master/www/banner.PNG",
                    #className='one columns',
                    style={
                        'height': '228',
                        'width': '1558',
                        'float': 'center',
                        'position': 'center',
                    }
                )
            ],
            className='ten columns',
            style={'margin-bottom':50}
        ),
        ## add the filters here -- TODO TODO TODO TODO
        html.Div(
            [
                html.Div(
                    [
                    html.P('Select Country'),
                    dcc.Dropdown(
                        id='countries_dropdown',
                        options=[{'label': i, 'value': i} for i in sorted(fact['Country'].unique())],
                        multi=True
                        ),
                    ],
                    style={'margin-bottom':20,'margin-right':50,'width': '20%', 'display': 'inline-block'},
                ),
                html.Div(
                    [
                    html.P('Select Region'),
                        dcc.Dropdown(
                            id='region_dropdown',
                            options=[{'label': i, 'value': i} for i in sorted(fact['Region'].unique())],
                            multi=True
                        ),
                    ],
                    style={'margin-right':50,'width': '20%', 'display': 'inline-block'},
                ),
                html.Div(
                    [
                    html.P('Select Attendance'),
                        dcc.Dropdown(
                            id='attendance_dropdown',
                            options=[{'label': i, 'value': i} for i in sorted(fact['first_visit'].unique())],
                            multi=True
                            # value='United_Arab_Emirates'
                        ),
                    ],
                    style={'margin-right':120,'width': '20%', 'display': 'inline-block'},
                ),
                # html.Div(
                #     [
                #     html.P('Select Group'),
                #     dcc.RadioItems(
                #         id='group_dropdown',
                #         options=[{'label': i, 'value': i} for i in sorted(fact['Group'].unique())],
                #         )
                #     ],
                #     style={'margin-right':50,'width': '10%', 'display': 'inline-block'},
                # ),
                # html.Div(
                #     [
                #     html.P('Select Registration'),
                #     dcc.RadioItems(
                #         id='reg_type_dropdown',
                #         options=[{'label': i, 'value': i} for i in sorted(fact['Reg_Type'].unique())],
                #         )
                #     ],
                #     style={'width': '10%', 'display': 'inline-block'},
                # )

        ##  this is where the filters will be placed!!!


            ],
            style={'backgroundColor': '#F5F5F5'},
        ),

        ## first row of the charts
        html.Div(
            [
                ## Daily Attendance
                html.Div(
                    [
                        dcc.Graph(
                        id='daily_attendance'
                        )
                    ],
                    className='four columns',
                    style={'margin-top': '50', 'backgroundColor': '#ECFCF8'}
                ),

                ## Registration Type
                html.Div(
                    [
                        dcc.Graph(
                        id='registration_type'
                        )
                    ],
                    className='four columns',
                    style={'margin-top': '50', 'backgroundColor': '#F4F4F4'},
                    ## Top 10 International Countries
                ),
                html.Div(
                    [
                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Bar(
                                        y=topcountries_data['Country'],
                                        x=topcountries_data['count_2019'],
                                        name='Top 10 International Countries',
                                        marker=dict(
                                            color='#620A20'),
                                        orientation='h'
                                    )
                                ],
                                layout=go.Layout(
                                    title='Top 10 International Countries',
                                    margin=dict(l=150, r=0, t=40, b=40),
                                    paper_bgcolor = '#F4F4F4',
                                    plot_bgcolor = '#F4F4F4',
                                )
                            )
                        ,id='top_international_countries'
                        )
                    ],
                    className='four columns',
                    style={'margin-top': '50', 'backgroundColor': '#F4F4F4'}
                ),
            ],
            className='row'
        ),

        ## 2nd row of the charts
        html.Div(
            [
                ## Attendees with Revisit
                html.Div(
                    [
                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Bar(
                                        y=revisit_data['attendance'][revisit_data['attendance']!='No Show'],
                                        x=revisit_data['count_2019'][revisit_data['attendance']!='No Show'],
                                        name='Attendees with Revisit (Daily Influx)',
                                        marker=dict(
                                            color='#620A20'),
                                        orientation='h'
                                    )
                                ],
                                layout=go.Layout(
                                    title='Attendees with Revisit (Daily Influx)',
                                    margin=dict(l=40, r=100, t=40, b=40),
                                    paper_bgcolor = '#F4F4F4',
                                    plot_bgcolor = '#F4F4F4',
                                )
                            )
                        ,id='attendees_revisit')
                    ],
                    className='four columns',
                    style={'margin-top': '10', 'backgroundColor': '#F4F4F4'}
                ),
                ## UAE vs International
                html.Div(
                    [
                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Pie(
                                        hole=0.55,
                                        sort=False,
                                        direction='clockwise',
                                        values=group_data['count_2019'],
                                        labels=group_data['Group'],
                                        textinfo='label',
                                        textposition='outside',
                                        marker={'colors': ['#B41D2D', '#620A20'],
                                                'line': {'color': 'white', 'width': 1}}
                                    )
                                ],
                                layout=go.Layout(
                                    title='UAE vs International',
                                    margin=dict(l=0, r=100, t=40, b=40),
                                    paper_bgcolor = '#F4F4F4',
                                    plot_bgcolor = '#F4F4F4',
                                )
                            )
                        ,id='uae_vs_intl')
                    ],
                    className='four columns',
                    style={'margin-top': '10', 'backgroundColor': '#F4F4F4'}
                ## Participating Countries
                ),
                html.Div(
                    [
                        dcc.Graph(
                            figure=go.Figure(
                                data = [go.Choropleth(
                                    locations = countries_data['Country'],
                                    locationmode = 'country names',
                                    z = countries_data['count_2019'],
                                    text = countries_data['Country'],
                                    autocolorscale = False,
                                    reversescale = False,
                                    marker = dict(
                                        line = dict(
                                            color = 'rgb(180,180,180)',
                                            width = .5
                                        )),

                                    showscale=False
                                )],
                                layout = go.Layout(
                                    title = dict(
                                        text = 'Participating Countries'
                                    ),
                                    geo = dict(
                                        showframe = False,
                                        showcoastlines = True,
                                        projection = dict(
                                            type = 'equirectangular',
                                        )
                                    ),
                                    annotations = [dict(
                                        x = 1,
                                        y = 0.5,
                                        xref = 'paper',
                                        yref = 'paper',
                                        showarrow = False
                                    ),],
                                    #margin=dict(l=0, r=100, t=40, b=40),
                                    paper_bgcolor = '#F4F4F4',
                                    plot_bgcolor = '#F4F4F4',
                                    showlegend=False,

                                )
                            )
                        ,id='participating_countries')
                    ],
                    className='four columns',
                    style={'margin-top': '10', 'backgroundColor': '#F4F4F4'}
                ),
            ],
            className='row'
        )
    ],
    className='ten columns offset-by-one',
)


# callback functions for the FILTERS
# Countries Dropdown
@app.callback(Output('daily_attendance', 'figure'),
            [Input('countries_dropdown','value')])
def update_fact_data_country(country_selected):
    if not country_selected:
        daily_attend_data = fact
    else:
        daily_attend_data = pd.DataFrame()
        for country in country_selected:
            per_country_data = pd.DataFrame(fact[fact['Country']==country]) #.groupby('first_visit')['count_2019'].sum()).reset_index()
            daily_attend_data = daily_attend_data.append(per_country_data, ignore_index=True)

    daily_attend_data_agg = daily_attend_data.groupby('first_visit')['count_2019'].sum().reset_index()

    figure = go.Figure(
        data=[
            go.Bar(
                x=daily_attend_data_agg['first_visit'],
                y=daily_attend_data_agg['count_2019'],
                text=daily_attend_data_agg['count_2019'],
                textposition='auto',
                hoverinfo='text',
                marker=dict(
                    color='#620A20'
                )
            )
        ],
        layout=go.Layout(
            title='Daily Attendance',
            margin=dict(l=0, r=100, t=40, b=40),
            paper_bgcolor = '#F4F4F4',
            plot_bgcolor = '#F4F4F4',
        )
    )
    return figure

@app.callback(Output('registration_type', 'figure'),
              [Input('countries_dropdown', 'value')])
def update_fact_data_reg_type(country_selected):
    if not country_selected:
        reg_type_data = fact
    else:
        reg_type_data = pd.DataFrame()
        for country in country_selected:
            per_country_data = pd.DataFrame(fact[fact['Country']==country]) #.groupby('first_visit')['count_2019'].sum()).reset_index()
            reg_type_data = reg_type_data.append(per_country_data, ignore_index=True)

    reg_type_data_agg = reg_type_data.groupby('Reg_Type')['count_2019'].sum().reset_index()

    figure = go.Figure(
        data=[
            go.Pie(
                hole=0.55,
                sort=False,
                direction='clockwise',
                values=reg_type_data_agg['count_2019'],
                labels=reg_type_data_agg['Reg_Type'],
                textinfo='label',
                textposition='outside',
                marker={'colors': ['#B41D2D', '#620A20'],
                        'line': {'color': 'white', 'width': 1}}
            )
        ],
        layout=go.Layout(
            title='Daily Attendance',
            margin=dict(l=0, r=100, t=40, b=40),
            paper_bgcolor = '#F4F4F4',
            plot_bgcolor = '#F4F4F4',
        )
    )
    return figure

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)

