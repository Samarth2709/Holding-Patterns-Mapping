import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash_leaflet as dl
import pandas as pd
import numpy as np
import os
import json

# app = dash.Dash(__name__, title='Carbon Emissions', external_stylesheets=[dbc.themes.BOOTSTRAP])
#
# app.layout = html.Div(children=[
# html.Div(children=[dbc.FormGroup([
#                 dbc.RadioItems(
#                     id='sector-button',
#                     options=[
#                         {"label": "Jt Fuel", "value": "jet fuel"},
#                         {"label": "Aviation Gas", "value": "aviation gasoline"},
#                         {"label": "All Fuel", "value": "all fuel"}
#                         #
#                     ],
#                     value='all fuel',
#                     # style={'textAlign': 'center'},
#                     inline=True,
#                     labelStyle={'fontSize':'20px'}
#                         )]),])
# ])
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
# df = pd.DataFrame(np.random.randint(0, 5, size=(100, 4)), columns=list('ABCD'))


# style dict for html elements
#     style = {
#         'textAlign': 'center',
#         'color': colors['text'],
#         'backgroundColor': colors['background'],
#     }

# style dict for dcc elements
#     style = {
#         'color': 'black',
#         "width": '80%',
#         "margin": 'auto',
#         'align-items': 'center',
#         'justify-content': 'center',
#         'padding-left': '0%',
#         'padding-right': '0%'
#     }

# fig = go.Figure(go.Scattermapbox(
#                     lat=[62.3833], # [57.671667] ,
#                     lon=[16.3000], # [11.980833],
#                     mode='markers',
#
#                     marker=dict(
#                             size= 3,
#                             color = 'red',
#                             opacity = .8,
#                             )))
# fig.show()
df = pd.read_excel('all_data_df.xlsx')


def get_json_data(filename='states.json', path=None):
    # get json data (points on map for each state) from files
    if not path:
        path = os.path.join(os.getcwd(), 'Geo-json', filename)
    # jsondata = json.load(open(path, 'r'))
    with open(path, 'r') as json_raw:
        jsondata = json.load(json_raw)
    #     with urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
    #         jsondata = json.load(response)
    return jsondata


def get_center_json(filename='SuperSector2006.json'):
    path = os.path.join(os.getcwd(), 'Aviation_Centers', 'Unziped-json', filename)
    with open(path, 'r') as json_raw:
        jsondata = json.load(json_raw)
    return jsondata


pts = []  # list of points defining boundaries of polygons
for feature in get_center_json()['geometries']:
    pts.extend(feature['coordinates'][0])
    pts.append([None, None])  # mark the end of a polygon

    # else: raise ValueError("geometry type irrelevant for map")
x, y = zip(*pts)
print(x, y)
feature_json = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": 1,
            "properties": {
                "population": 200
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[
                    -103.497447,
                    41.001635
                ],
                    [
                        -104.053249,
                        41.001406
                    ],
                    [
                        -106.05234,
                        41.417865
                    ],
                    [
                        -104.053026,
                        44.885464
                    ],
                    [
                        -104.0526,
                        40.124963
                    ],
                    [
                        -102.053107,
                        40.499964
                    ],
                    [
                        -104.053028,
                        43.000587
                    ]
                ]
                ]
            }
        }
    ]
}
df2 = pd.DataFrame({'id': [0, 1], 'val': [0, 0]})

print(df2)


def update_map_slider(date_dropdown, fuel_type):
    if type(date_dropdown) != str:
        empty_fig = go.Figure(go.Choropleth(), layout=go.Layout(paper_bgcolor='#f2f7ff'))
        empty_fig.update_layout(geo_scope='usa', height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return empty_fig
    year_fuel_type_filter = ((df["Year"] == int(date_dropdown)) & (df["Carbon Output Type"] == fuel_type))
    fuel_type_filter = (df["Carbon Output Type"] == fuel_type) & (df["Carbon Output Value"] > 0.1)
    update_fig = go.Figure([
        go.Choropleth(geojson=json_data, locations=df[year_fuel_type_filter]['ID'],
                      z=df[year_fuel_type_filter]["Carbon Output Value"],
                      # hovertext=date_dropdown.title(),
                      # hoverinfo="text",
                      # hovertextsrc='State',
                      zmax=df.loc[fuel_type_filter, "Carbon Output Value"].max(),
                      zmin=df.loc[fuel_type_filter, "Carbon Output Value"].min(), colorscale="ylorrd"),
        go.Scattergeo(
            lat=[38.639238],
            lon=[-116.932475],
            mode='markers',
            hovertext="Nevadsssa",
            hoverinfo="text",
            marker={'size': 10, "color": "red"}
        ),
        # go.Scattergeo(lon=x, lat=y, mode='lines', marker={'size':2, 'color':'blue'} ),
        go.Choropleth(geojson=feature_json, locations=df2['id'], z=df2['val'], showscale=False, colorscale=[[0, 'rgba(0, 0, 60, 50)']], marker={'opacity': 0.25})],
        # """mode='lines', featureidkey='geometries'"""
        layout=go.Layout(paper_bgcolor='#f2f7ff'))
    # layout=go.Layout(paper_bgcolor=colors['bg']))
    # update_fig.update_layout(geo_scope='usa')
    update_fig.update_layout(height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    update_fig.update_coloraxes(colorbar_tickcolor='#a83232')
    update_fig.update_coloraxes(colorbar_tickfont_color='#a83232')
    # update_fig.add_trace(go.Scattermapbox(
    #     lat=[38.639238],
    #     lon=[-116.932475],
    #     mode='markers',
    #
    #     marker={'size':10, "color":"red"}
    # ))
    # update_fig.update_layout(mapbox_style="white-bg")
    # update_fig.update_layout(autosize=True, showlegend=False,
    #                          mapbox={
    #     'style': "stamen-terrain",
    #     'center': { 'lon': -73.6, 'lat': 45.5},
    #     'zoom': 12, 'layers': [{
    #         'source': {
    #             'type': "FeatureCollection",
    #             'features': [{
    #                 'type': "Feature",
    #                 'geometry': {
    #                     'type': "MultiPolygon",
    #                     'coordinates': [[
    #                         [42.694099, -110.604254], [42.847629, -104.291068],
    #                         [40.673515, -104.348392], [39.832988, -109.663323]
    #                     ]]
    #                 }
    #             }]
    #         },
    #         'type': "fill", 'below': "traces", 'color': "royalblue"}]},
    #                          margin={"r": 0, "t": 0, "l": 0, "b": 0}
    #                          )
    print(str(fuel_type), "max", str(df.loc[fuel_type_filter, "Carbon Output Value"].max()))
    print(str(fuel_type), "min", str(df.loc[fuel_type_filter, "Carbon Output Value"].min()))
    return update_fig


json_data = get_json_data()
app = dash.Dash(__name__, title='Test')

app.layout = html.Div([
    dcc.Graph(
        id='example-map',
        style={"width": '75%', "margin": 'auto', 'align-items': 'center',
               'justifyContent': 'center', "padding": "20px",  # "height":"900px",
               "borderRadius": "25px"},
        # config={'scrollZoom': False},
        figure=update_map_slider('2018', 'all fuel')
    )

])

if __name__ == '__main__':
    print("Running server")
    app.run_server(debug=True)
    print("     Running server -- END")
