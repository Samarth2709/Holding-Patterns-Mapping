import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import os
import json
import eia_data_pull as dp
from urllib.request import urlopen

# Create dash app with "Carbon Emissions" as tab title
# External_stylesheets is the style of bg and text ect.
app = dash.Dash(__name__, title='Carbon Emissions', external_stylesheets=[])
# dbc.themes.SUPERHERO

# Colors in hex code
colors = {
    'text': '#000000',
    'bg': '#2b3e50'
}


def get_eia_data():  # gets eia data for each state for each sector as a CarbonEmissions class
    # links = get_link_to_all_data_sets_for_state()
    # links = get_data_links_for_aviation_sectors(links)
    # class_data = convert_links_to_classes(links)
    links = dp.get_link_to_all_data_sets_for_state()
    links = dp.get_data_links_for_aviation_sectors(links)
    class_data = dp.convert_links_to_classes(links)
    return class_data


# Creates a dictionary that maps State Names to there ID in json file
def create_state_id_map(json_data):
    state_id_map = {}
    for state_data in json_data['features']:
        state_id_map[state_data['properties']['NAME']] = state_data['id']
    return state_id_map


# Adds id values from json data to ID column in data df
def add_id_to_df(df, geo_json, id_col_name="ID"):
    state_id_map = create_state_id_map(geo_json)
    for row_numb in range(len(df.index)):
        df.loc[row_numb, id_col_name] = state_id_map[df.loc[row_numb, 'State']]
    return df


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


@app.callback(
    Output(component_id='example-map', component_property='figure'),
    [Input(component_id='date-dropdown', component_property='value'),
     Input(component_id='sector-button', component_property='value')])
def update_map_slider(date_dropdown, fuel_type):
    if type(date_dropdown) != str:
        empty_fig = go.Figure(go.Choropleth())
        empty_fig.update_layout(geo_scope='usa')
        return empty_fig
    year_fuel_type_filter = ((df["Year"] == int(date_dropdown)) & (df["Carbon Output Type"] == fuel_type))
    fuel_type_filter = df["Carbon Output Type"] == fuel_type
    update_fig = go.Figure(
        go.Choropleth(geojson=json_data, locations=df[year_fuel_type_filter]['ID'],
                      z=df[year_fuel_type_filter]["Carbon Output Value"],
                      name=date_dropdown.title(),
                      zmax=df[fuel_type_filter]["Carbon Output Value"].max(),
                      zmin=df[fuel_type_filter]["Carbon Output Value"].min(), colorscale="ylorrd"),
        layout={'title': 'Carbon Emissions ' + str(df.loc[0, 'Unit Measurement'])})
    # layout=go.Layout(paper_bgcolor=colors['bg']))
    update_fig.update_layout(geo_scope='usa')
    update_fig.update_layout(height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    update_fig.update_coloraxes(colorbar_tickcolor='#a83232')
    update_fig.update_coloraxes(colorbar_tickfont_color='#a83232')
    return update_fig


# layout = go.Layout(paper_bgcolor=colors['bg']
# bgcolor=colors['bg'] in dict
# plot_bgcolor=colors['bg']
# , layout = go.Layout(
# geo=dict(bgcolor= colors['bg'], lakecolor=colors['bg']),
# paper_bgcolor=colors['bg'],
# plot_bgcolor=colors['bg'])
#     update_fig.update_layout(transition_duration=100, plot_bgcolor=colors['bg'])


# @app.callback(
#     Output(component_id='', component_property=''),
#     [Input(component_id='', component_property='')])
# def update(sector_name):
#     pass

# Updates Title-sector with value into its children parameter (Updates title with type of carbon output(all fuel,
#       aviation gasoline, jet fuel))
@app.callback(
    Output(component_id='Title-sector', component_property='children'),
    [Input(component_id='sector-button', component_property='value')])
def update_sector_name(name):
    return ('Carbon Emissions for ' + name + " from transportation").title()


# Gets the range of years to display in the
def get_range_years_for_dropdown(df):
    option = []
    for year in df["Year"].unique():
        option_dict = {"label": str(year), "value": str(year)}
        option.append(option_dict)
    return option


# Get json data
json_data = get_json_data()

load_data = True
save_df = False
if load_data:
    df = pd.read_excel('all_data_df.xlsx')
else:
    # create df with IDs
    df = dp.combine_state_df_all(data=get_eia_data())
    df = add_id_to_df(df, json_data)
    if save_df:
        df.to_excel('all_data_df.xlsx', index=False)

df.head()

# layout of app
app.layout = dbc.Container(children=[
    html.H1(id='Title-sector'),
    html.H3(children='Data was provided by the EIA.'),
    dcc.Tabs(id='all-tabs', value='raw-carbon', children=[
        dcc.Tab(id='raw-carbon', value='raw-carbon', label='Raw Carbon Emissions',
                style={'color': 'black', 'fontSize': '20px'},
                selected_className='custom-tab--selected',
                children=[
                    html.Div([
                        dbc.Row([
                            dbc.Col(
                                dcc.Dropdown(
                                    id='date-dropdown',
                                    placeholder='Year',
                                    options=get_range_years_for_dropdown(df),
                                    style={'color': 'black', 'width': '100px', 'justify-content': 'center',
                                           "margin": 'auto',
                                           'align-items': 'center'},
                                    value=str(df["Year"].max()),
                                    className='dropdown-date'
                                ), width='auto'),

                            dbc.Col(
                                dbc.RadioItems(
                                    id='sector-button',
                                    options=[
                                        {"label": "Jet Fuel", "value": "jet fuel"},
                                        {"label": "Aviation Gas", "value": "aviation gasoline"},
                                        {"label": "All Fuel", "value": "all fuel"}
                                        #
                                    ],
                                    value='all fuel',
                                    style={'textAlign': 'center', 'width': 'auto'},
                                    inline=True,
                                    labelStyle={'fontSize': '20px'},
                                    className='radioitems-fueltype'
                                ), width='auto'),
                        ],
                            justify="center"),

                        dcc.Graph(
                            id='example-map',
                            style={"width": '75%', "margin": 'auto', 'align-items': 'center',
                                   'justifyContent': 'center', 'padding-left': '0%', 'padding-right': '0%'},
                            config={'scrollZoom': False},
                            #          figure=None
                        ),
                    ], className='div-tab')]),

        dcc.Tab(id='carbon-per-capita', value='carbon-per-capita', label='Carbon Emissions per Capita',
                style={'color': 'black', 'fontSize': '20px'},
                selected_className='custom-tab--selected',
                children=[
                    html.Div(children=[])
                ])
    ]),

    html.H6(children='Updated: ' + df["Updated Time"].iloc[0]),

], fluid=False, className='div-main-background')

if __name__ == '__main__':
    print("Running server")
    app.run_server(debug=True)
    print("     Running server -- END")

