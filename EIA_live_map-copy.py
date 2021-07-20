# Created by Samarth Kumbla
# Nasa VIP Internship

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import os
import json
import eia_data_pull as dp

# Create dash app with "Carbon Emissions" as tab title
# External_stylesheets is the style of bg and text ect.
app = dash.Dash(__name__, title='Carbon Emissions')  # external_stylesheets=[dbc.themes.BOOTSTRAP]
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
def update_raw_map(date_dropdown, fuel_type):
    if type(date_dropdown) != str:
        empty_fig = go.Figure(go.Choropleth(), layout=go.Layout(paper_bgcolor='#f2f7ff'))
        empty_fig.update_layout(geo_scope='usa', height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return empty_fig
    year_fuel_type_filter = ((df["Year"] == int(date_dropdown)) & (df["Carbon Output Type"] == fuel_type))
    fuel_type_filter = (df["Carbon Output Type"] == fuel_type) & (df["Carbon Output Value"] > 0.1)
    update_fig = go.Figure(
        go.Choropleth(geojson=json_data, locations=df[year_fuel_type_filter]['ID'],
                      z=df[year_fuel_type_filter]["Carbon Output Value"],
                      name=date_dropdown.title(),
                      zmax=df.loc[fuel_type_filter, "Carbon Output Value"].max(),
                      zmin=df.loc[fuel_type_filter, "Carbon Output Value"].min(), colorscale="ylorrd"),
        layout=go.Layout(paper_bgcolor='#f2f7ff'))
    # layout=go.Layout(paper_bgcolor=colors['bg']))
    update_fig.update_layout(geo_scope='usa')
    update_fig.update_layout(height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    update_fig.update_coloraxes(colorbar_tickcolor='#a83232')
    update_fig.update_coloraxes(colorbar_tickfont_color='#a83232')
    print(str(fuel_type), "max", str(df.loc[fuel_type_filter, "Carbon Output Value"].max()))
    print(str(fuel_type), "min", str(df.loc[fuel_type_filter, "Carbon Output Value"].min()))
    return update_fig


# Update carbon emissions map per major airport
@app.callback(
    Output(component_id='emissions-per-air', component_property='figure'),
    [Input(component_id='date-dropdown-per-air', component_property='value'),
     Input(component_id='sector-button-per-air', component_property='value')])
def update_per_map(date_dropdown, fuel_type):
    if type(date_dropdown) != str:
        empty_fig = go.Figure(go.Choropleth(), layout=go.Layout(paper_bgcolor='#f2f7ff'))
        empty_fig.update_layout(geo_scope='usa', height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return empty_fig
    year_fuel_type_filter = ((df["Year"] == int(date_dropdown)) & (df["Carbon Output Type"] == fuel_type))
    fuel_type_filter = (df["Carbon Output Type"] == fuel_type) & (df['Carbon per Airport Count'] > 0.1)
    update_fig = go.Figure([
        go.Choropleth(geojson=json_data, locations=df[year_fuel_type_filter]['ID'],
                      z=df[year_fuel_type_filter]["Carbon per Airport Count"],
                      name=date_dropdown.title(),
                      zmax=df.loc[fuel_type_filter, 'Carbon per Airport Count'].max(),
                      zmin=df.loc[fuel_type_filter, 'Carbon per Airport Count'].min(), colorscale="ylorrd"),
        # go.Scattergeo(lon=, lat=, fillcolor=)

    ],
        layout=go.Layout(paper_bgcolor='#f2f7ff'))
    update_fig.update_layout(geo_scope='usa')
    update_fig.update_layout(height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})
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
    [Input(component_id='sector-button', component_property='value'),
     Input(component_id='sector-button-per-air', component_property='value'),
     Input(component_id='all-tabs', component_property='value')])
def update_sector_name(raw_name, per_air_name, tab):
    if tab == 'raw-carbon':
        return ('Carbon Emissions for ' + raw_name + " from transportation").title()
    elif tab == 'carbon-per-air':
        return ('Carbon Emissions for ' + per_air_name + " from transportation").title()


# Gets the range of years to display in the
def get_range_years_for_dropdown(df):
    option = []
    for year in df["Year"].unique():
        option_dict = {"label": str(year), "value": str(year)}
        option.append(option_dict)
    return option


# Get json data
json_data = get_json_data()

load_data = False
save_df = True
if load_data:
    df = pd.read_excel('all_data_df.xlsx')
else:
    # create df with IDs
    df = dp.combine_state_df_all(data=get_eia_data())
    df = dp.add_major_airport_count(data=df)
    df = add_id_to_df(df, json_data)
    if save_df:
        df.to_excel('all_data_df.xlsx', index=False)

df.head()
print(df)
print(df.columns)

# layout of app
app.layout = html.Div(children=[
    html.H1(id='Title-sector', style={"margin": 0}),
    html.H3(children='Data was provided by the EIA.'),
    dcc.Tabs(id='all-tabs', value='raw-carbon', children=[
        dcc.Tab(id='raw-carbon', value='raw-carbon', label='Raw Carbon Emissions',
                style={'color': 'black', 'fontSize': '20px'},
                selected_className='custom-tab--selected',
                children=[
                    html.Div([
                        dcc.Dropdown(
                            id='date-dropdown',
                            placeholder='Year',
                            options=get_range_years_for_dropdown(df),
                            style={'color': 'black', 'justifyContent': 'center', 'alignItems': 'center'},
                            # "margin": 'auto', 'align-items': 'center'
                            value=str(df["Year"].max()),
                            className='child-dropdown'
                        ),

                        dcc.RadioItems(
                            id='sector-button',
                            options=[
                                {"label": "Jet Fuel", "value": "jet fuel"},
                                {"label": "Aviation Gas", "value": "aviation gasoline"},
                                {"label": "All Fuel", "value": "all fuel"}
                                #
                            ],
                            value='all fuel',
                            style={},  # 'textAlign': 'center', 'width': 'auto'
                            labelStyle={'fontSize': '20px'},
                            className='child-radioitems'
                        )
                    ], className='container'),

                    dcc.Graph(
                        id='example-map',
                        style={"width": '75%', "margin": 'auto', 'align-items': 'center',
                               'justifyContent': 'center', "padding": "20px", "height": "800px",
                               "borderRadius": "25px", "padding-bottom": "10px"},
                        config={'scrollZoom': False},
                        #          figure=None
                    ),
                ]),

        dcc.Tab(id='carbon-per-air', value='carbon-per-air', label='Carbon Emissions per Major Airport',
                style={'color': 'black', 'fontSize': '20px'},
                selected_className='custom-tab--selected',
                children=[
                    html.Div([
                        dcc.Dropdown(
                            id='date-dropdown-per-air',
                            placeholder='Year',
                            options=get_range_years_for_dropdown(df),
                            style={'color': 'black', 'justifyContent': 'center', 'alignItems': 'center'},
                            # "margin": 'auto', 'align-items': 'center'
                            value=str(df["Year"].max()),
                            className='child-dropdown'
                        ),

                        dcc.RadioItems(
                            id='sector-button-per-air',
                            options=[
                                {"label": "Jet Fuel", "value": "jet fuel"},
                                {"label": "Aviation Gas", "value": "aviation gasoline"},
                                {"label": "All Fuel", "value": "all fuel"}
                                #
                            ],
                            value='all fuel',
                            style={},  # 'textAlign': 'center', 'width': 'auto'
                            labelStyle={'fontSize': '20px'},
                            className='child-radioitems'
                        )
                    ], className='container'),

                    dcc.Graph(
                        id='emissions-per-air',
                        style={"width": '75%', "margin": 'auto', 'align-items': 'center',
                               'justifyContent': 'center', "padding": "20px", "height": "800px",
                               "borderRadius": "25px", "padding-bottom": "10px"},
                        config={'scrollZoom': False},
                        #          figure=None
                    )
                ]),
    ]),
    html.H4(children='Updated: ' + dp.format_eia_update_date(df["Updated Time"].iloc[0]), style={'padding-left': '12.5%'}, className='bottom-text'),
    html.H4(children='Carbon Emissions in ' + df['Unit Measurement'].iloc[0], style={'padding-left': '12.5%'}, className='bottom-text'),

], className='div-main-background')

if __name__ == '__main__':
    print("Running server")
    app.run_server(debug=True)
    print("     Running server -- END")

# TODO Rows and columns of app.layout
# TODO Plot sectors
# TODO Create per capita map
# TODO get embedded figure
# TODO fix CO2 for all fuel (millions -> normal)
