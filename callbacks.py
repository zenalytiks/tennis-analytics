from dash import Input, Output, callback, callback_context
import plotly.graph_objects as go
import plotly.express as px
from utils.graphs import create_tennis_court_shapes, add_shot_data, create_placement_analysis, create_speed_analysis, COURT_LENGTH
from utils.data_reader import read_data

df = read_data()

df = df[~df['Stroke'].isin(['Feed','Serve'])]

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
     Input('spin-filter', 'value'),
     Input('player-store','data'),
     Input('shot-spin-switch','value')],
     prevent_initial_call=True
)
# Replace this section in your callbacks.py update_charts function

def update_charts(selected_strokes, selected_results, selected_spins, selected_player, shot_spin_view):
    """
    Updated callback to handle single player perspective and modern UI controls
    """
    player_perspective = selected_player['player_perspective']
    # Filter data to show only the selected player's shots
    filtered_df = df[(df['Player'] == player_perspective) & (df['Spin'].isin(selected_spins))].copy()

    # PROPER PERSPECTIVE TRANSFORMATION
    # Transform coordinates to show receiving player's perspective
    def transform_to_player_perspective(row):
        x, y, result = row['Bounce (x)'], row['Bounce (y)'], row['Result']
        
        # Handle net shots - clamp them to the net line
        if result == 'Net':
            return x, COURT_LENGTH  # Place all net shots at the net line
        
        # If shot is on the opposite side of the net (y > COURT_LENGTH)
        if y > COURT_LENGTH:
            # Transform both coordinates for proper perspective
            new_x = -x  # Mirror across center line
            new_y = (2 * COURT_LENGTH) - y  # Flip across net line
            
            # DON'T clamp - let shots go beyond baseline if they were deep on opponent's side
            # This preserves the true perspective of how deep/short the shot appeared
            
            return new_x, new_y
        else:
            # Shot is already on player's side, no transformation needed
            return x, y
    
    # Apply transformation
    transformed_coords = filtered_df.apply(transform_to_player_perspective, axis=1, result_type='expand')
    filtered_df['Bounce (x)'] = transformed_coords[0]
    filtered_df['Bounce (y)'] = transformed_coords[1]
    
    # Rest of your existing filtering logic...
    if selected_strokes and len(selected_strokes) < len(df['Stroke'].unique()):
        filtered_df = filtered_df[filtered_df['Stroke'].isin(selected_strokes)]
    
    if selected_results and len(selected_results) > 0:
        filtered_df = filtered_df[filtered_df['Result'].isin(selected_results)]
    
    # Create court visualization
    shapes, annotations = create_tennis_court_shapes()
    
    court_fig = go.Figure(data=[], layout=go.Layout(
        shapes=shapes,
        annotations=annotations,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        xaxis=dict(range=[-8,8],showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-5, COURT_LENGTH + 3],showgrid=False, zeroline=False, visible=False),
        height=600,
        margin=dict(l=0, r=0, t=0, b=0)
    ))
    court_fig = add_shot_data(court_fig, filtered_df, shot_spin_view)
    
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
    
    
    options = []
    for stroke in df['Stroke'].unique():
        color = df.loc[df['Stroke'] == stroke, 'color'].iloc[0]
        
        # Add checkmark for selected strokes
        if selected_strokes and stroke in selected_strokes:
            label = html.Span([
                html.Span('●', style={'color': color, 'fontSize': '24px', 'marginRight': '8px'}),
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
        'In': {'symbol': '⚫', 'color': '#000'},
        'Out': {'symbol': '⚪', 'color': '#000'},
    }
    
    options = []
    for result in df[~df['Result'].isin(['Net'])]['Result'].unique():
        marker_info = result_markers.get(result, {'symbol': '●', 'color': '#6C757D'})
        
        # Add checkmark for selected results
        if selected_results and result in selected_results:
            label = html.Span([
                html.Span(marker_info['symbol'], 
                         style={'color': marker_info['color'], 'fontSize': '20px', 'marginRight': '8px', 'fontWeight': 'bold'}),
                result
            ], style={'display': 'flex', 'alignItems': 'center'})
        else:
            label = html.Span([
                html.Span(marker_info['symbol'], 
                         style={'color': marker_info['color'], 'fontSize': '20px', 'marginRight': '8px', 
                                'fontWeight': 'bold', 'opacity': '0.4'}),
                result
            ], style={'display': 'flex', 'alignItems': 'center', 'opacity': '0.6'})
            
        options.append({'label': label, 'value': result})
    
    return options


@callback(
    Output('spin-filter', 'options'),
    Input('spin-filter', 'value')
)
def update_spin_options(selected_spins):
    """
    Update spin options with visual feedback and opacity changes
    """
    from dash import html
    
    # Spin markers and colors
    spin_markers = {
        'Topspin': {'symbol': '▲', 'color': '#000'},
        'Slice': {'symbol': '◆', 'color': '#000'},
        'Flat': {'symbol': '■', 'color': '#000'},
    }
    
    options = []
    for spin in df['Spin'].unique():
        marker_info = spin_markers.get(spin, {'symbol': '●', 'color': '#6C757D'})

        # Add checkmark for selected spins
        if selected_spins and spin in selected_spins:
            label = html.Span([
                html.Span(marker_info['symbol'], 
                         style={'color': marker_info['color'], 'fontSize': '20px', 'marginRight': '8px', 'fontWeight': 'bold'}),
                spin
            ], style={'display': 'flex', 'alignItems': 'center'})
        else:
            label = html.Span([
                html.Span(marker_info['symbol'], 
                         style={'color': marker_info['color'], 'fontSize': '20px', 'marginRight': '8px', 
                                'fontWeight': 'bold', 'opacity': '0.4'}),
                spin
            ], style={'display': 'flex', 'alignItems': 'center', 'opacity': '0.6'})

        options.append({'label': label, 'value': spin})

    return options