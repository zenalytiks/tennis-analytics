from dash import Input, Output, callback
import plotly.graph_objects as go
from utils.graphs import create_tennis_court_half, add_shot_data_half_court, create_placement_analysis, create_speed_analysis
from utils.data_reader import read_data


df = read_data()

@callback(
    [Output('tennis-court-half', 'figure'),
     Output('depth-analysis', 'figure'),
     Output('direction-analysis', 'figure'),
     Output('speed-analysis', 'figure')],
    [Input('player-perspective', 'value'),
     Input('stroke-dropdown', 'value'),
     Input('shot-type-dropdown', 'value'),
     Input('color-by', 'value'),
     Input('result-filter', 'value')]
)
def update_charts(player_perspective, selected_stroke, selected_shot_type, color_by, selected_results):
    # Filter data to show only the selected player's shots
    filtered_df = df[df['Player'] == player_perspective].copy()
    
    if selected_stroke != 'all':
        filtered_df = filtered_df[filtered_df['Stroke'] == selected_stroke]
    
    if selected_shot_type != 'all':
        filtered_df = filtered_df[filtered_df['Type'] == selected_shot_type]
        
    if selected_results:
        filtered_df = filtered_df[filtered_df['Result'].isin(selected_results)]
    
    # Create half court visualization with precise scaling
    court_fig = create_tennis_court_half(player_perspective)
    court_fig = add_shot_data_half_court(court_fig, filtered_df, player_perspective, color_by=color_by)
    
    # Create analysis charts
    depth_fig, direction_fig = create_placement_analysis(filtered_df)
    speed_fig = create_speed_analysis(filtered_df)
    
    return court_fig, depth_fig, direction_fig, speed_fig