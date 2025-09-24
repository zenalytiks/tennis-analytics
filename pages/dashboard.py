import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.data_reader import read_data

dash.register_page(__name__, path='/', name='Tennis Analytics')

df = read_data()

STROKE_OPTIONS = df[~df['Stroke'].isin(['Feed','Serve'])]['Stroke'].unique().tolist()
RESULT_OPTIONS = df[~df['Stroke'].isin(['Feed','Serve'])]['Result'].unique().tolist()

def layout(): 
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("Tennis Analytics Dashboard", 
                       className="text-center mb-0",
                       style={'color': '#2C3E50', 'fontWeight': '300', 'letterSpacing': '1px'}),
                html.P("Shot placement and performance analysis", 
                      className="text-center text-muted mb-4",
                      style={'fontSize': '16px'})
            ])
        ]),
        
        # Main Content
        dbc.Row([
            # Left Panel - Court Visualization
            dbc.Col([
                
                dbc.Card([
                    dbc.CardBody([
                        dbc.Stack(
                            [
                                dbc.Button(
                                    "".join([part[0].upper() for part in df['Player'].unique()[0].split()[:2]]),
                                    value=df['Player'].unique()[0],
                                    id='player-1'
                                ),
                                html.P("SHOT PLACEMENT", className='fw-bold fs-4 ms-auto'),
                                dbc.Button(
                                    "".join([part[0].upper() for part in df['Player'].unique()[1].split()[:2]]),
                                    value=df['Player'].unique()[1],
                                    className='ms-auto',
                                    id='player-2'
                                ),
                            ],
                            direction="horizontal",
                            className='p-3'
                            # justify="between",
                        ),
                        dcc.Graph(id='tennis-court-half'),
                        # Stroke Type Selection  
                        html.Div([
                            html.Label("Stroke Types", className="form-label text-muted mb-2", style={'fontSize': '14px', 'fontWeight': '600'}),
                            dbc.Checklist(
                                id='stroke-dropdown',
                                options=STROKE_OPTIONS,
                                value=STROKE_OPTIONS,
                                inline=True,
                                className="mb-3"
                            )
                        ]),
                        
                        html.Hr(className="my-3"),
                        
                        # Shot Result Selection
                        html.Div([
                            html.Label("Shot Results", className="form-label text-muted mb-2", style={'fontSize': '14px', 'fontWeight': '600'}),
                            dbc.Checklist(
                                id='result-filter',
                                options=RESULT_OPTIONS,
                                value=RESULT_OPTIONS,
                                inline=True,
                                className="mb-3"
                            )
                        ]),
                        
                        html.Hr(className="my-3"),
        
                        # Info Panel
                        html.Div([
                            html.Small([
                                html.Strong("Visualization Info:", className="text-muted"),
                                html.Br(),
                                "• Marker size = Ball speed",
                                html.Br(), 
                                "• Colors represent stroke types",
                                html.Br(),
                                "• Markers show shot results"
                            ], className="text-muted", style={'lineHeight': '1.4'})
                        ], className="mt-3 p-2 bg-light rounded")
                    ], className="p-2")
                ], className="tennis-court shadow-sm border-0 mb-4"),
                
            ], md=6),
            
            # Right Panel - Analysis Charts
            dbc.Col([
                # Top Row - Two smaller charts
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.H6("Depth Analysis", className="mb-0 text-muted")
                            ], className="bg-white border-0 py-2"),
                            dbc.CardBody([
                                dcc.Graph(id='depth-analysis')
                            ], className="p-2")
                        ], className="shadow-sm border-0 mb-3")
                    ], md=6),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.H6("Direction Analysis", className="mb-0 text-muted")
                            ], className="bg-white border-0 py-2"),
                            dbc.CardBody([
                                dcc.Graph(id='direction-analysis')
                            ], className="p-2")
                        ], className="shadow-sm border-0 mb-3")
                    ], md=6)
                ]),
                
                # Bottom Row - Speed analysis
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.H6("Speed Analysis", className="mb-0 text-muted")
                            ], className="bg-white border-0 py-2"),
                            dbc.CardBody([
                                dcc.Graph(id='speed-analysis')
                            ], className="p-2")
                        ], className="shadow-sm border-0")
                    ], md=12)
                ])
            ], md=6)
        ]),
        dcc.Store(id='player-store')
        
    ], fluid=True, className="px-4 py-3")