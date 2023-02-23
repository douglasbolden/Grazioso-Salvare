from jupyter_plotly_dash import JupyterDash

import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from dash.dependencies import Input, Output

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pymongo import MongoClient


from animal_shelter import AnimalShelter

###########################
# Data Manipulation / Model
###########################
username = "aacuser"
password = "password"
shelter = AnimalShelter(username, password)


# class read method must support return of cursor object and accept projection json input
df = pd.DataFrame.from_records(shelter.read({}))

pil_image = Image.open("assets/Grazioso Salvare Logo.png")


#########################
# Dashboard Layout / View
#########################
app = JupyterDash('Dashboard - Douglas Bolden')

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(
        html.Table(
            html.Tr(children=[
                html.Td(children=[
                    html.A( href="https://www.snhu.edu", target="_blank", children=[
                        html.Img(src=pil_image,
                        alt="Grazioso Salvare Logo", width="100px", height="100px")
                        ]
                        )
                    ]
                ),
                html.Td(
                    html.B(
                        html.H1('Grazioso Salvare Dashboard')
                    )
                )
                ]
            )
        )
    ),
    html.Center(html.A("Application Developed by Douglas Bolden.", href="https://www.linkedin.com/in/douglasbolden/", target="_blank"))
    ,
    html.Hr(),
    html.Div(
        dcc.RadioItems(
            id='filter',
            options=[
               {'label': 'Water Rescue', 'value': 'water'},
               {'label': 'Mountain Rescue', 'value': 'mountain'},
               {'label': 'Disaster Rescue', 'value': 'disaster'},
               {'label': 'All','value': 'all_animals'}
            ],
            value='all_animals',
            labelStyle={'display': 'inline-block'}
        ) 
    ),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
        ],
            
        data=df.to_dict('records'),
        filter_action="native",
        page_size= 10,
        sort_action="native",
        sort_mode="multi",
        style_table={
            'minWidth': '100%',
            'overflowX': 'auto'
        },
        style_cell= {
            'minWidth': '150px'
        }
        

    ),
    html.Br(),
    html.Hr(),
    html.Div(
            id='map-id',
            className='col s12 m6',
            ),
    
    html.Div(
        id = 'piechart-id',
        className='col s13 m7'
    )
    
    
])


#############################################
# Interaction Between Components / Controller
#############################################

@app.callback([Output('datatable-id','data'),
               Output('datatable-id','columns')],
              [Input('filter', 'value')])
def update_dashboard(value):
    
    if (value == 'water'):
        df = pd.DataFrame(shelter.read({'$and': [{'sex_upon_outcome': 'Intact Female'},
                                                          {'$or': [
                                                              {'breed': 'Labrador Retriever Mix'},
                                                              {'breed': 'Chesa Bay Retr Mix'},
                                                              {'breed': 'Newfoundland Mix'},
                                                              {'breed': 'Newfoundland/Labrador Retriever'},
                                                              {'breed': 'Newfoundland/Australian Cattle Dog'},
                                                              {'breed': 'Newfoundland/Great Pyrenees'}]
                                                          },
                                                          {'$and': [{'age_upon_outcome_in_weeks': {'$gte': 26}},
                                                                    {'age_upon_outcome_in_weeks': {'$lte': 156}}]
                                                          }]
                                                }))
    elif (value == 'mountain'):
        df = pd.DataFrame(shelter.read({'$and': [{'sex_upon_outcome': 'Intact Male'},
                                                          {'$or': [
                                                              {'breed': 'German Shepherd'},
                                                              {'breed': 'Alaskan Malamute'},
                                                              {'breed': 'Old English Sheepdog'},
                                                              {'breed': 'Rottweiler'},
                                                              {'breed': 'Siberian Husky'}]
                                                          },
                                                          {'$and': [{'age_upon_outcome_in_weeks': {'$gte': 26}},
                                                                    {'age_upon_outcome_in_weeks': {'$lte': 156}}]
                                                          }]}))
    elif (value == 'disaster'):
        df = pd.DataFrame(shelter.read({'$and': [{'sex_upon_outcome': 'Intact Male'},
                                                          {'$or': [
                                                              {'breed': 'Doberman Pinscher'},
                                                              {'breed': 'German Shepherd'},
                                                              {'breed': 'Golden Retriever'},
                                                              {'breed': 'Bloodhound'},
                                                              {'breed': 'Rottweiler'}]
                                                          },
                                                          {'$and': [{'age_upon_outcome_in_weeks': {'$gte': 20}},
                                                                    {'age_upon_outcome_in_weeks': {'$lte': 300}}]
                                                          }]
                                                }))
    elif (value == 'all_animals'):
        df = pd.DataFrame.from_records(shelter.read({}))
        
    columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')

    return (data,columns)

#This callback will highlight a row on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3AA'
    } for i in selected_columns]


@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])

def update_map(viewData):
    dff = pd.DataFrame.from_dict(viewData)
    # Austin TX is at [30.75,-97.48]
    
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[dff.location_lat[0], dff.location_long[0]], zoom=10, children=[
        dl.TileLayer(id="base-layer-id"),
        # Marker with tool tip and popup
        dl.Marker(position=[dff.location_lat[0],dff.location_long[0]], children=[
            dl.Tooltip(dff.breed[0]),
            dl.Popup([html.H1("Animal Name"), html.P(dff.name[0]), html.P(dff.animal_type[0]), html.P(dff.color[0]), html.P(dff.age_upon_outcome[0]), html.P(sex_upon_outcome[0])])
            ])
        ])
]

    

app