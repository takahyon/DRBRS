import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from WebMonitor import get_data
import dash_daq as daq
import dash_html_components as html

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}


x, y = get_data('csm')
dom_x,dom_y = get_data('dom')
#app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='DRBRS Model Monitor'),

    # html.Div(children='''
    #     divの文章
    # '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': x, 'y': y, 'type': 'line', 'name': 'line'},
            ],
            'layout': {
                'title': 'Current Stream Model'
            }
        }
    ),
#     html.Div(children='''
#     divの文章
# '''),

    dcc.Graph(
        id='disaster-graph',
        figure={
            'data': [
                {'x': dom_x, 'y': dom_y, 'type': 'line', 'name': 'line'},
            ],
            'layout': {
                'title': 'Disaster Stream Model'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
