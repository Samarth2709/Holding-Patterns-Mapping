# Created by Samarth
# Nasa VIP Internship


import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import os
import json
import eia_data_pull as dp

app = dash.Dash(__name__)


def get_eia_data(): # gets eia data for each state for each sector as a CarbonEmissions class
    # links = get_link_to_all_data_sets_for_state()
    # links = get_data_links_for_aviation_sectors(links)
    # class_data = convert_links_to_classes(links)
    links = dp.get_link_to_all_data_sets_for_state()
    links = dp.get_data_links_for_aviation_sectors(links)
    class_data = dp.convert_links_to_classes(links)
    return class_data


def create_state_id_map(json_data):
    state_id_map = {}
    for state_data in json_data['features']:
        state_id_map[state_data['properties']['NAME']] = state_data['id']
    return state_id_map


def add_id_to_df(df, geo_json, id_col_name = "ID"):
    state_id_map = create_state_id_map(geo_json)
    for row_numb in range(len(df.index)):
        df.loc[row_numb, id_col_name] = state_id_map[df.loc[row_numb, 'State']]
    return df


def get_json_data(filename='states.json', path = None):
    # get json data (points on map for each state) from files
    if not path:
        path = os.path.join(os.getcwd(), 'Geo-json', filename)
    jsondata = json.load(open(path, 'r'))
    return jsondata


@app.callback(
    Output(component_id='example-map', component_property='figure'),
    [Input(component_id='date-slider', component_property='value')])
def update_map_slider(slider_val):
    year_filter = df["Year"] == slider_val
    update_fig = go.Figure(go.Choropleth(geojson=json_data, locations=df[year_filter].ID, z=df[year_filter]["Carbon Output Value"], name=sector.title()))
    update_fig.update_layout(geo_scope='usa')
    update_fig.update_layout(height=900, margin={"r":0,"t":0,"l":0,"b":0})
    update_fig.update_layout(transition_duration=100)
    return update_fig


json_data = get_json_data()


sector = "jet fuel"
df = dp.combine_state_df(sector, data=get_eia_data())
df = add_id_to_df(df, json_data)


df.head()


fig = go.Figure(go.Choropleth(geojson=json_data, locations=df.ID, z=df["Carbon Output Value"], name=sector.title()))


fig.update_layout(geo_scope='usa')
fig.update_layout(height=900, margin={"r": 0, "t": 0, "l": 0, "b": 0})


app.layout = html.Div(children=[
    html.H1(id='Title-sector', children=('Carbon Emissions for ' + sector + " in the transportation sector").title()),
    html.H3(children='This data was provided by the EIA.'),
    html.H4(children='Updated: ' + df["Updated Time"].iloc[0]),

    dcc.Graph(
        id='example-map'
        # figure=fig
    ),

    dcc.Slider(
        id='date-slider',
        min=df["Year"].min(),
        max=df["Year"].max(),
        step=None,
        value=df["Year"].max(),
        updatemode='drag',
        marks={str(i): str(i) for i in range(df["Year"].min(), df["Year"].max() + 1)}
    ),

    #     dcc.RadioItems(
    #         id='sector-radiobutton',
    #         options=[
    #             {"label": "Jet Fuel", "value":"jet fuel"},
    #             {"label": "Aviation Gas", "value": "aviation gasoline"},
    #             {"label": "All Fuel", "value": "all fuel"}
    #         ],
    #         value='all fuel'
    #         style={'width':'70%'}
    #     )
])


if __name__ == '__main__':
    print("Running server")
    app.run_server(debug=True, use_reloader=False)
    print("     Running server -- END")






