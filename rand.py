import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

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
df = pd.DataFrame(np.random.randint(0,5,size=(100, 4)), columns=list('ABCD'))
df.loc[df['B']==2, "A"] = df.loc[df['B']==2, 'A']* 100
print(df)
print(df[df['B']==2])

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