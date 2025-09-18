from dash import Input, Output, callback
import plotly.graph_objects as go
from utils.graphs import create_tennis_court, add_shot_data, create_placement_analysis, create_speed_analysis
from utils.data_reader import read_data


df = read_data()

@callback(
    [Output('tennis-court', 'figure'),
     Output('depth-analysis', 'figure'),
     Output('direction-analysis', 'figure'),
     Output('speed-analysis', 'figure')],
    [Input('player-dropdown', 'value'),
     Input('stroke-dropdown', 'value'),
     Input('color-by', 'value'),
     Input('result-filter', 'value')]
)
def update_charts(selected_player, selected_stroke, color_by, selected_results):
    # Filter data
    filtered_df = df.copy()
    
    if selected_player != 'all':
        filtered_df = filtered_df[filtered_df['Player'] == selected_player]
    
    if selected_stroke != 'all':
        filtered_df = filtered_df[filtered_df['Stroke'] == selected_stroke]
        
    if selected_results:
        filtered_df = filtered_df[filtered_df['Result'].isin(selected_results)]
    
    # Create court visualization
    court_fig = create_tennis_court()
    court_fig = add_shot_data(court_fig, filtered_df, color_by=color_by)
    
    # Create analysis charts
    if not filtered_df.empty:
        depth_fig, direction_fig = create_placement_analysis(filtered_df)
        speed_fig = create_speed_analysis(filtered_df)
    else:
        # Empty figures if no data
        depth_fig = go.Figure().add_annotation(text="No data available", showarrow=False)
        direction_fig = go.Figure().add_annotation(text="No data available", showarrow=False)
        speed_fig = go.Figure().add_annotation(text="No data available", showarrow=False)
    
    return court_fig, depth_fig, direction_fig, speed_fig