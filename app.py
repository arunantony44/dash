import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "yellow"
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Dash it!!!", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Section 1", href="/page-1", active="exact"),
                dbc.NavLink("Section 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True
        ),
    ],
    style=SIDEBAR_STYLE
)

index_page = html.Div(
    id='index_page',
    children=[
        html.Div([
            html.H1("Welcome", style={'color': 'cyan'})
        ])
    ]
)

page_1_layout = html.Div(
    id='page_1_layout',
    className='text-center',
    children=[
        html.Div(
            [
                html.H3("Enter a value between 0 and 1000 (inclusive)"),
                html.Div([
                    "Input: ",
                    dcc.Input(
                        id='my-input',
                        value=0,
                        type='number',
                        min=0,
                        max=1000,
                        debounce=True
                    ),
                    dcc.Store(id='user-input', storage_type='session')
                ])
            ],
        ),
        html.Br(),
        html.Div(id='page-1-content')
    ]
)

page_2_layout = html.Div(
    id='page_2_layout',
    className='display-6 text-center',
    children=[
        html.Div(id='page-2-content', style={'font-family': 'Comic Sans', 'color': 'orange', 'padding': '12rem 6rem'})
    ]
)

content = html.Div(id="page-content", children=[index_page, page_1_layout, page_2_layout], style=CONTENT_STYLE)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        sidebar,
        content
    ],
    style={'background-color': '#9467bd'}
)


@app.callback(
    [Output(page, 'style') for page in ['index_page', 'page_1_layout', 'page_2_layout']],
    [Input('url', 'pathname')])
def display_page(pathname):
    return_value = [{'display': 'block', 'line-height': '0', 'height': '0', 'overflow': 'hidden'} for _ in range(3)]

    if pathname == '/page-1':
        return_value[1] = {'height': 'auto', 'display': 'inline-block'}
        return return_value
    elif pathname == '/page-2':
        return_value[2] = {'height': 'auto', 'display': 'inline-block'}
        return return_value
    else:
        return_value[0] = {'height': 'auto', 'display': 'inline-block'}
        return return_value


@app.callback(
    [
        Output('page-1-content', 'children'),
        Output('user-input', 'data')
    ],
    [
        Input('my-input', 'value')
    ]
)
def page_1_output(x):
    text = 'You have entered: {}'.format(x)
    return text, x + 5


@app.callback(Output('page-2-content', 'children'),
              [Input('user-input', 'data')])
def page_2_output(y):
    return 'The all-important value driving our business decisions is {}'.format(y)


if __name__ == '__main__':
    app.run_server(debug=True)
