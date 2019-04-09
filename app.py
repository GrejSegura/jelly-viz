# In[]:
# Import required libraries
import os
import pickle
import copy
import datetime as dt

import pandas as pd
import numpy as np
from flask import Flask
from flask_cors import CORS
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.plotly as py

# Multi-dropdown options
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS

# change the working directory path to where this file is located #
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
daily_attend_data = pd.DataFrame(fact.groupby('first_visit')['count_2019'].sum()).reset_index()
reg_type_data = pd.DataFrame(fact.groupby('Reg_Type')['count_2019'].sum()).reset_index()
topcountries_data = pd.DataFrame(fact.groupby('Country')['count_2019'].sum()).reset_index().sort_values('count_2019', ascending=False)[1:11].sort_values('count_2019', ascending=True)

group_data = pd.DataFrame(fact.groupby('Group')['count_2019'].sum()).reset_index()
revisit_data = pd.DataFrame(attendance.groupby('attendance')['count_2019'].sum()).reset_index().sort_values('count_2019', ascending=False).sort_values('count_2019', ascending=True)
countries_data = pd.DataFrame(fact.groupby('Country')['count_2019'].sum()).reset_index()
#################################################################

# Create global chart template
mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'  # noqa: E501


layout = dict(
    autosize=True,
    height=500,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="dark",
        center=dict(
            lon=-78.05,
            lat=42.54
        ),
        zoom=7,
    )
)


# In[]:
# Create app layout
app.layout = html.Div(
    [
        ## add banner - this includes the logo and title
        html.Img(
            src="https://raw.githubusercontent.com/GrejSegura/jelly-viz/master/www/banner.PNG",
            className='one columns',
            style={
                'height': '233',
                'width': '1585',
                'float': 'center',
                'position': 'relative',
            },
        ),

        ## add the filters here -- TODO TODO TODO TODO
        html.Div([


        ##  this is where the filters will be placed!!!


        ]),

        ## first row of the charts
        html.Div(
            [
                ## Daily Attendance
                html.Div(
                    [
                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Bar(
                                        x=daily_attend_data['first_visit'],
                                        y=daily_attend_data['count_2019'],
                                        name='Day Attended',
                                        marker=go.bar.Marker(
                                            color='#620A20'
                                        )
                                    )
                                ],
                                layout=go.Layout(
                                    title='Daily Attendance',
                                    margin=go.layout.Margin(l=0, r=100, t=40, b=40)
                                )
                            )
                            ,id='daily_attendance'
                        )
                    ],
                    className='four columns',
                    style={'margin-top': '50'}
                ),

                ## Registration Type
                html.Div(
                    [
                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Pie(
                                        hole=0.55,
                                        sort=False,
                                        direction='clockwise',
                                        values=reg_type_data['count_2019'],
                                        labels=reg_type_data['Reg_Type'],
                                        textinfo='label',
                                        textposition='outside',
                                        marker={'colors': ['#B41D2D', '#620A20'],
                                                'line': {'color': 'white', 'width': 1}}
                                    )
                                ],
                                layout=go.Layout(
                                    title='Registration Type',
                                    margin=go.layout.Margin(l=0, r=100, t=40, b=40)
                                )
                            )
                            ,id='registration_type'
                        )
                    ],
                    className='four columns',
                    style={'margin-top': '50'}
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
                                        marker=go.bar.Marker(
                                            color='#620A20'),
                                        orientation='h'
                                    )
                                ],
                                layout=go.Layout(
                                    title='Top 10 International Countries',
                                    margin=go.layout.Margin(l=150, r=0, t=40, b=40)
                                )
                            )
                            ,id='top_international_countries'
                        )
                    ],
                    className='four columns',
                    style={'margin-top': '50'}
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
                                        marker=go.bar.Marker(
                                            color='#620A20'),
                                        orientation='h'
                                    )
                                ],
                                layout=go.Layout(
                                    title='Attendees with Revisit (Daily Influx)',
                                    margin=go.layout.Margin(l=40, r=100, t=40, b=40)
                                )
                            )
                        ,id='attendees_revisit')
                    ],
                    className='four columns',
                    style={'margin-top': '50'}
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
                                    margin=go.layout.Margin(l=0, r=100, t=40, b=40)
                                )
                            )
                        ,id='uae_vs_intl')
                    ],
                    className='four columns',
                    style={'margin-top': '50'}
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
                                    marker = go.choropleth.Marker(
                                        line = go.choropleth.marker.Line(
                                            color = 'rgb(180,180,180)',
                                            width = 0.5
                                        )),
                                )],
                                layout = go.Layout(
                                    title = go.layout.Title(
                                        text = 'Participating Countries'
                                    ),
                                    geo = go.layout.Geo(
                                        showframe = False,
                                        showcoastlines = False,
                                        projection = go.layout.geo.Projection(
                                            type = 'equirectangular'
                                        )
                                    ),
                                    annotations = [go.layout.Annotation(
                                        x = 0.55,
                                        y = 0.1,
                                        xref = 'paper',
                                        yref = 'paper',
                                        showarrow = False
                                    ),],
                                    margin=go.layout.Margin(l=0, r=100, t=40, b=40)
                                )
                            )
                        ,id='participating_countries')
                    ],
                    className='four columns',
                    style={'margin-top': '50'}
                ),
            ],
            className='row'
        ),
    ],
    className='ten columns offset-by-one'
)


# In[]:
# Helper functions

def filter_dataframe(df, well_statuses, well_types, year_slider):
    dff = df[df['Well_Status'].isin(well_statuses)
             & df['Well_Type'].isin(well_types)
             & (df['Date_Well_Completed'] > dt.datetime(year_slider[0], 1, 1))
             & (df['Date_Well_Completed'] < dt.datetime(year_slider[1], 1, 1))]
    return dff


## Helper functions to create new data
def fetch_individual(api):
    try:
        points[api]
    except:
        return None, None, None, None

    index = list(range(min(points[api].keys()), max(points[api].keys()) + 1))
    gas = []
    oil = []
    water = []

    for year in index:
        try:
            gas.append(points[api][year]['Gas Produced, MCF'])
        except:
            gas.append(0)
        try:
            oil.append(points[api][year]['Oil Produced, bbl'])
        except:
            oil.append(0)
        try:
            water.append(points[api][year]['Water Produced, bbl'])
        except:
            water.append(0)

    return index, gas, oil, water


def fetch_aggregate(selected, year_slider):

    index = list(range(max(year_slider[0], 1985), 2016))
    gas = []
    oil = []
    water = []

    for year in index:
        count_gas = 0
        count_oil = 0
        count_water = 0
        for api in selected:
            try:
                count_gas += points[api][year]['Gas Produced, MCF']
            except:
                pass
            try:
                count_oil += points[api][year]['Oil Produced, bbl']
            except:
                pass
            try:
                count_water += points[api][year]['Water Produced, bbl']
            except:
                pass
        gas.append(count_gas)
        oil.append(count_oil)
        water.append(count_water)

    return index, gas, oil, water



# In[]:
# Main
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
