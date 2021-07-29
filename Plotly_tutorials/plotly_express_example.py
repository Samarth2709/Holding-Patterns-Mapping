# Created by Samarth
# Nasa VIP Internship

import json
import pandas as pd
import rand
import numpy as np
import plotly.express as px
# import plotly.io as pio
# pio.renderers.default = 'chrome'
import os

states = [
"Alabama",
"Alaska",
"Arizona",
"Arkansas",
"California",
"Colorado",
"Connecticut",
"Delaware",
"Florida",
"Georgia",
"Hawaii",
"Idaho",
"Illinois",
"Indiana",
"Iowa",
"Kansas",
"Kentucky",
"Louisiana",
"Maine",
"Maryland",
"Massachusetts",
"Michigan",
"Minnesota",
"Mississippi",
"Missouri",
"Montana",
"Nebraska",
"Nevada",
"New Hampshire",
"New Mexico",
"New York",
"North Carolina",
"North Dakota",
"Ohio",
"New Jersey",
"Oklahoma",
"Oregon",
"Pennsylvania",
"Rhode Island",
"South Carolina",
"South Dakota",
"Tennessee",
"Texas",
"Utah",
"Vermont",
"Virginia",
"Washington",
"West Virginia",
"Wisconsin",
"Wyoming",
]
# length of list is 50


path = os.path.join(os.getcwd(), 'Geo-json', 'states.json')
json_data = json.load(open(path, 'r'))
# District of Columbia not in states list
# Puerto Rico not in states list

df = pd.DataFrame({'State': pd.Series(states), 'Random_Data': pd.Series(rand.sample(range(1, 51), 50))}, columns=['State', 'Random_Data', 'ID'])

state_id_map = {}
for state_data in json_data['features']:
    state_id_map[state_data['properties']['NAME']] = state_data['id']


for row_numb in range(len(df.index)):
    df.loc[row_numb, 'ID'] = state_id_map[df.loc[row_numb, 'State']]

fig = px.choropleth(df, geojson=json_data, locations='ID', color='Random_Data', scope="usa", color_continuous_scale="Reds", range_color=(0, 50), hover_name = 'State')
if __name__ == "__main__":
    fig.show()
    print('plotly_express_example.py complete ')
