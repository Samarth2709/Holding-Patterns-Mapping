import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import os

# Starting an application
app = dash.Dash()

# Html of page
# Creating a div tag
app.layout = html.Div(children=[
    html.H1('Dash'),
    dcc.Input(id='input', value='', type='tel'),
    html.Div(id='output')
])

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')])
def update_value(input_data):
    return "Input: {}".format(input_data)

if __name__ == '__main__':
    print(os.path.basename(__file__), "Completed")
    app.run_server(debug = True)
