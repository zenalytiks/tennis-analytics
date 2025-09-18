import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.data_reader import read_data

dash.register_page(__name__, path='/', name='Swing Vision')


df = read_data()

def layout(): 
    return dbc.Container([
    html.H1("Tennis Court Shot Placement Analytics", 
           style={'textAlign': 'center', 'color': '#2E8B57', 'marginBottom': 30}),
    
    dbc.Row([
        dbc.Col([
            html.Label("Select Player:", style={'fontWeight': 'bold', 'marginBottom': 10}),
            dcc.Dropdown(
                id='player-dropdown',
                options=[{'label': 'All Players', 'value': 'all'}] + 
                        [{'label': player, 'value': player} for player in df['Player'].unique()],
                value='all',
                style={'marginBottom': 20}
            ),
            
            html.Label("Select Stroke Type:", style={'fontWeight': 'bold', 'marginBottom': 10}),
            dcc.Dropdown(
                id='stroke-dropdown',
                options=[{'label': 'All Strokes', 'value': 'all'}] + 
                        [{'label': stroke, 'value': stroke} for stroke in df['Stroke'].unique()],
                value='all',
                style={'marginBottom': 20}
            ),
            
            html.Label("Color By:", style={'fontWeight': 'bold', 'marginBottom': 10}),
            dcc.RadioItems(
                id='color-by',
                options=[
                    {'label': 'Player', 'value': 'Player'},
                    {'label': 'Direction', 'value': 'Direction'},
                    {'label': 'Result', 'value': 'Result'}
                ],
                value='Player',
                style={'marginBottom': 20}
            ),
            
            html.Label("Shot Result:", style={'fontWeight': 'bold', 'marginBottom': 10}),
            dcc.Checklist(
                id='result-filter',
                options=[{'label': result, 'value': result} for result in df['Result'].unique()],
                value=df['Result'].unique().tolist(),
                style={'marginBottom': 20}
            )
        ],md=2),
        
        dbc.Col([
            dcc.Graph(id='tennis-court')
        ],md=10, className="shadow p-0 mb-5 bg-white rounded border-light")
    ]),
    
    html.Hr(),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id='depth-analysis')
            ],className="shadow bg-white rounded border-light")
            
        ],md=6),
        
        dbc.Col([
            html.Div([
                dcc.Graph(id='direction-analysis') 
            ],className="shadow bg-white rounded border-light")
             
        ],md=6,className='mb-3'),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id='speed-analysis')
            ],className="shadow bg-white rounded border-light")
            
        ],md=12, className='')
    ])
],className='mt-5 mb-5')
