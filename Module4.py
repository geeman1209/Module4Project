# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 13:49:11 2021

@author: gabre
"""

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px


#-----------------------------------------------------------------------------
#Preliminary functions


species = pd.read_json('https://data.cityofnewyork.us/resource/nwxe-4ae8.json')

def load_list():
    tree_types = species['spc_common'].dropna().unique()
    tree_list = tree_types.tolist()
    optionsList = [{'label': x, 'value': x} for x in tree_list]
    return optionsList


#Tweaked the API to retrieve the boro AND selected spc_common
#source: https://dev.socrata.com/docs/queries/where.html
def get_data(boro, spc_common):
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' + \
             '$select=spc_common,count(spc_common),health' + \
             '&$where=boroname=\'{}\'&spc_common=\'{}\'' + \
             '&$group=spc_common,health').format(boro, spc_common).replace(' ', '%20')
    df = pd.read_json(soql_url)
    df = df.dropna()
    #Return the dataframe in order to assign to a future variable
    return df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



#-----------------------------------------------------------------------------
#layout

app.layout = html.Div([
    
    
        html.H1("Health of Tree Species by Borough", style={'text-align': 'center'}),
        html.P('Select a Borough: '),
        dcc.Dropdown(id="slct-boro",
                     options=[
                         {"label":"Bronx", "value":"Bronx"},
                         {"label":"Brooklyn", "value":"Brooklyn"},
                         {"label":"Manhattan", "value":"Manhattan"},
                         {"label":"Queens", "value":"Queens"},
                         {"label":"Staten Island", "value":"Staten Island"}],
                     value="Bronx",
                     multi=False,
                     style={'width': "40%"}),
        html.Br(),
        html.P('Select a tree species: '),
        dcc.Dropdown(
                    id="slct_spc_common",
                    options= load_list(),
                    value= 'red maple',
                    style={'width':"40%"}
                     ),
        html.Div(id='output_container', children=[]),
        html.Br(),
        
        
        dcc.Graph(id='my_q1', figure={})
    
    ])
#------------------------------------------------------------------------------
#Connect Plotly graph with Dash
@app.callback(
    Output(component_id='my_q1', component_property = 'figure'),
    [Input(component_id = 'slct-boro', component_property = "value"),
     Input(component_id= 'slct_spc_common', component_property = 'value')]
    )
def create_graph(boro_slct, spc_common_slct):
    tree_frame = get_data(boro_slct, spc_common_slct)
    
    # Plotly Express
    fig = px.pie(tree_frame, values='count_spc_common', names='health', title="Health Percentages")
    return fig

# ----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
