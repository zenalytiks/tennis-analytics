from dash import Input, Output, callback, State, callback_context
import plotly.graph_objects as go
import plotly.express as px
from utils.graphs import create_tennis_court_half, add_shot_data_half_court, create_placement_analysis, create_speed_analysis
from utils.data_reader import read_data

df = read_data()

@callback(
    Output('player-store','data'),
    Output('player-1','style'),
    Output('player-2','style'),
    [
        Input('player-1','n_clicks'),
        Input('player-2','n_clicks'),
        Input('player-1', 'value'),
        Input('player-2', 'value'),
    ]
)
def update_player_click(n_click_player_1, n_click_player_2, player1, player2):
    player_perspective = df['Player'].unique()[0]
    player1_style = {}
    player2_style = {}
    if player_perspective == player1:
        player1_style = {'background-color': 'darkgray'}
        player2_style = {'background-color': 'lightgray'}
    else:
        player1_style = {'background-color': 'lightgray'}
        player2_style = {'background-color': 'darkgray'}

    if callback_context.triggered_id == 'player-1':
        player_perspective = player1
        player1_style = {'background-color': 'darkgray'}
        player2_style = {'background-color': 'lightgray'}
    elif callback_context.triggered_id == 'player-2':
        player_perspective = player2
        player1_style = {'background-color': 'lightgray'}
        player2_style = {'background-color': 'darkgray'}
    return {'player_perspective': player_perspective}, player1_style, player2_style


@callback(
    [Output('tennis-court-half', 'figure'),
     Output('depth-analysis', 'figure'),
     Output('direction-analysis', 'figure'),
     Output('speed-analysis', 'figure')],
    [
     Input('stroke-dropdown', 'value'),
     Input('result-filter', 'value'),
     Input('player-store','data')],
     prevent_initial_call=True
)
def update_charts(selected_strokes, selected_results, selected_player):
    """
    Updated callback to handle single player perspective and modern UI controls
    """
    player_perspective = selected_player['player_perspective']
    # Filter data to show only the selected player's shots
    filtered_df = df[df['Player'] == player_perspective].copy()
    
    # Filter by selected strokes
    if selected_strokes and len(selected_strokes) < len(df['Stroke'].unique()):
        filtered_df = filtered_df[filtered_df['Stroke'].isin(selected_strokes)]
    
    # Filter by selected results  
    if selected_results and len(selected_results) > 0:
        filtered_df = filtered_df[filtered_df['Result'].isin(selected_results)]
    
    # Shot type is always 'all' in the new design - no filtering needed
    # Color by is always 'Stroke' in the new design
    color_by = 'Stroke'
    
    # Create court visualization for single player
    court_fig = create_tennis_court_half(player_perspective)
    court_fig = add_shot_data_half_court(court_fig, filtered_df, player_perspective, color_by=color_by)
    
    # Create analysis charts
    depth_fig, direction_fig = create_placement_analysis(filtered_df)
    speed_fig = create_speed_analysis(filtered_df)
    
    return court_fig, depth_fig, direction_fig, speed_fig


# Remove the player options callback since we're using radio buttons now
# Additional callback to handle dynamic stroke selection updates
@callback(
    Output('stroke-dropdown', 'options'),
    Input('stroke-dropdown', 'value')
)
def update_stroke_options(selected_strokes):
    """
    Update stroke options with visual feedback and maintain colors
    """
    from dash import html

    colors = px.colors.qualitative.Set2
    unique_vals = df['Stroke'].unique()
    color_map = {val: colors[i % len(colors)] for i, val in enumerate(unique_vals)}
    df['color'] = df['Stroke'].map(color_map)
    
    # Stroke colors for consistency
    # STROKE_COLORS = {
    #     'Forehand': '#FF6B6B',
    #     'Backhand': '#4ECDC4', 
    #     'Serve': '#45B7D1',
    #     'Return': '#96CEB4',
    #     'Volley': '#FFEAA7',
    #     'Smash': '#DDA0DD'
    # }
    
    options = []
    for stroke in df['Stroke'].unique():
        color = df.loc[df['Stroke'] == stroke, 'color'].iloc[0]
        
        # Add checkmark for selected strokes
        if selected_strokes and stroke in selected_strokes:
            label = html.Span([
                html.Span('●', style={'color': color, 'fontSize': '24px', 'marginRight': '8px'}),
                # html.Span('✓', style={'color': '#28a745', 'fontSize': '12px', 'marginRight': '4px'}),
                stroke
            ], style={'display': 'flex', 'alignItems': 'center'})
        else:
            label = html.Span([
                html.Span('●', style={'color': color, 'fontSize': '24px', 'marginRight': '8px', 'opacity': '0.4'}),
                stroke
            ], style={'display': 'flex', 'alignItems': 'center', 'opacity': '0.6'})
            
        options.append({'label': label, 'value': stroke})
    
    return options

# Callback to provide real-time feedback on result selections
@callback(
    Output('result-filter', 'options'),
    Input('result-filter', 'value')
)
def update_result_options(selected_results):
    """
    Update result options with visual feedback and opacity changes
    """
    from dash import html
    
    # Result markers and colors
    result_markers = {
        'In': {'symbol': '●', 'color': '#000'},
        'Out': {'symbol': '✕', 'color': '#000'}, 
        'Net': {'symbol': '▲', 'color': '#000'}
    }
    
    options = []
    for result in df['Result'].unique():
        marker_info = result_markers.get(result, {'symbol': '●', 'color': '#6C757D'})
        
        # Add checkmark for selected results
        if selected_results and result in selected_results:
            label = html.Span([
                html.Span(marker_info['symbol'], 
                         style={'color': marker_info['color'], 'fontSize': '14px', 'marginRight': '8px', 'fontWeight': 'bold'}),
                # html.Span('✓', style={'color': '#28a745', 'fontSize': '12px', 'marginRight': '4px'}),
                result
            ], style={'display': 'flex', 'alignItems': 'center'})
        else:
            label = html.Span([
                html.Span(marker_info['symbol'], 
                         style={'color': marker_info['color'], 'fontSize': '14px', 'marginRight': '8px', 
                                'fontWeight': 'bold', 'opacity': '0.4'}),
                result
            ], style={'display': 'flex', 'alignItems': 'center', 'opacity': '0.6'})
            
        options.append({'label': label, 'value': result})
    
    return options