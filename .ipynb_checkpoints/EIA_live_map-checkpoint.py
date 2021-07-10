import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import os
import json
import eia_data_pull as dp


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


json_data = get_json_data()

sector = "jet fuel"
df = dp.combine_state_df(sector, data=get_eia_data())
df = add_id_to_df(df, json_data)
df = df[df["Year"] == 2000]
print(df)
# print(df["Carbon Output Value"])


fig = go.Figure(go.Choropleth(geojson=json_data, locations=df.ID, z=df["Carbon Output Value"], name=sector.title()))

# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })
# fig = go.Figure(px.choropleth(df, geojson=json_data, locations='ID', color='Random_Data', scope="usa",
#                     color_continuous_scale="Reds", range_color=(0, 50), hover_name = 'State'))

# df = pd.read_csv('Geothermals.csv')
# df['text'] = df['Name'] + ', ' + df['State']

# fig = go.Figure(data=go.Scattergeo(
#     lon=df['Lon_84'],
#     lat=df['Lat_84'],
#     text=df['text'],
#     mode='markers',
#     marker_color=df['Temp_C_ML']
# ))

fig.update_layout(
    geo_scope='usa')
fig.update_layout(height=800, margin={"r":0,"t":0,"l":0,"b":0})

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children=('Carbon Emissions for ' + sector + " in the transportation sector").title()),
    html.Div(children='''
        This data was provided by the EIA.
    '''),
    html.H5(children='Updated: ' + df["Updated Time"].iloc[0]),

    dcc.Graph(
        id='example-map',
        figure=fig
    )
])

if __name__ == '__main__':
    print("Running server")
    app.run_server(debug=True, use_reloader=False)
    print("     Running server -- END")
