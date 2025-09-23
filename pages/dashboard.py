import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.data_reader import read_data

dash.register_page(__name__, path='/', name='Tennis Analytics')

df = read_data()

df = df[~df['Stroke'].isin(['Feed','Serve'])]

# Define stroke colors for consistency
STROKE_COLORS = {
    'Forehand': '#FF6B6B',
    'Backhand': '#4ECDC4', 
    'Serve': '#45B7D1',
    'Return': '#96CEB4',
    'Volley': '#FFEAA7',
    'Smash': '#DDA0DD'
}

def create_stroke_checklist():
    """Create colored stroke checklist items"""
    stroke_options = []
    for stroke in df['Stroke'].unique():
        color = STROKE_COLORS.get(stroke, '#6C757D')
        stroke_options.append({
            'label': html.Span([
                html.Span('●', style={'color': color, 'fontSize': '16px', 'marginRight': '8px'}),
                stroke
            ], style={'display': 'flex', 'alignItems': 'center'}),
            'value': stroke
        })
    return stroke_options

def create_result_checklist():
    """Create result checklist with markers and colors"""
    result_markers = {
        'In': {'symbol': '●', 'color': '#28a745'},
        'Out': {'symbol': '✕', 'color': '#dc3545'}, 
        'Net': {'symbol': '▲', 'color': '#fd7e14'}
    }
    
    result_options = []
    for result in df['Result'].unique():
        marker_info = result_markers.get(result, {'symbol': '●', 'color': '#6C757D'})
        result_options.append({
            'label': html.Span([
                html.Span(marker_info['symbol'], 
                         style={'color': marker_info['color'], 'fontSize': '14px', 'marginRight': '8px', 'fontWeight': 'bold'}),
                result
            ], style={'display': 'flex', 'alignItems': 'center'}),
            'value': result
        })
    return result_options

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
                                options=create_stroke_checklist(),
                                value=df['Stroke'].unique().tolist(),
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
                                options=create_result_checklist(),
                                value=df['Result'].unique().tolist(),
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
        
        # Hidden components to maintain compatibility
            dcc.Store(id='shot-type-dropdown', data='all'),  # Hidden store for shot type (always 'all')
            dcc.Store(id='color-by', data='Stroke'),  # Hidden store for color by (always 'Stroke')
            dcc.Store(id='player-store')
        
    ], fluid=True, className="px-4 py-3")