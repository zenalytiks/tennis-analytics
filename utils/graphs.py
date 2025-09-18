import plotly.graph_objects as go
import plotly.express as px

# Tennis court dimensions (standard court)
COURT_LENGTH = 78  # feet
COURT_WIDTH = 36   # feet
NET_HEIGHT = 3     # feet

def create_tennis_court():
    """Create tennis court layout"""
    fig = go.Figure()
    
    # Court outline
    fig.add_shape(type="rect", x0=-COURT_WIDTH/2, y0=0, x1=COURT_WIDTH/2, y1=COURT_LENGTH,
                  line=dict(color="white", width=3), fillcolor="rgba(34,139,34,0.3)")
    
    # Service boxes
    fig.add_shape(type="line", x0=-COURT_WIDTH/2, y0=COURT_LENGTH/2, x1=COURT_WIDTH/2, y1=COURT_LENGTH/2,
                  line=dict(color="white", width=2))  # Net line
    fig.add_shape(type="line", x0=0, y0=COURT_LENGTH/2-21, x1=0, y1=COURT_LENGTH/2+21,
                  line=dict(color="white", width=2))  # Center service line
    fig.add_shape(type="line", x0=-COURT_WIDTH/2+4.5, y0=COURT_LENGTH/2-21, x1=COURT_WIDTH/2-4.5, y1=COURT_LENGTH/2-21,
                  line=dict(color="white", width=2))  # Service line near
    fig.add_shape(type="line", x0=-COURT_WIDTH/2+4.5, y0=COURT_LENGTH/2+21, x1=COURT_WIDTH/2-4.5, y1=COURT_LENGTH/2+21,
                  line=dict(color="white", width=2))  # Service line far
    
    # Singles sidelines
    fig.add_shape(type="line", x0=-COURT_WIDTH/2+4.5, y0=0, x1=-COURT_WIDTH/2+4.5, y1=COURT_LENGTH,
                  line=dict(color="white", width=2))
    fig.add_shape(type="line", x0=COURT_WIDTH/2-4.5, y0=0, x1=COURT_WIDTH/2-4.5, y1=COURT_LENGTH,
                  line=dict(color="white", width=2))
    
    # Baselines
    fig.add_shape(type="line", x0=-COURT_WIDTH/2, y0=0, x1=COURT_WIDTH/2, y1=0,
                  line=dict(color="white", width=3))
    fig.add_shape(type="line", x0=-COURT_WIDTH/2, y0=COURT_LENGTH, x1=COURT_WIDTH/2, y1=COURT_LENGTH,
                  line=dict(color="white", width=3))
    
    # Add zone labels
    fig.add_annotation(x=-9, y=10, text="Ad Court", showarrow=False, 
                      font=dict(color="white", size=12), bgcolor="rgba(0,0,0,0.5)")
    fig.add_annotation(x=9, y=10, text="Deuce Court", showarrow=False,
                      font=dict(color="white", size=12), bgcolor="rgba(0,0,0,0.5)")
    fig.add_annotation(x=0, y=39, text="Net", showarrow=False,
                      font=dict(color="white", size=14, family="Arial Black"), bgcolor="rgba(0,0,0,0.7)")
    
    fig.update_layout(
        plot_bgcolor='rgba(34,139,34,0.8)',
        paper_bgcolor='rgba(34,139,34,0.8)',
        xaxis=dict(range=[-20, 20], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-5, 83], showgrid=False, zeroline=False, visible=False),
        showlegend=True,
        height=800,
        # width=600,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig

def add_shot_data(fig, filtered_df, shot_type="all", color_by="Player"):
    """Add shot placement data to court"""
    if filtered_df.empty:
        return fig
    
    # Color mapping
    colors = px.colors.qualitative.Set1
    if color_by == "Player":
        unique_vals = filtered_df['Player'].unique()
        color_map = {val: colors[i % len(colors)] for i, val in enumerate(unique_vals)}
        filtered_df['color'] = filtered_df['Player'].map(color_map)
    elif color_by == "Direction":
        unique_vals = filtered_df['Direction'].unique()
        color_map = {val: colors[i % len(colors)] for i, val in enumerate(unique_vals)}
        filtered_df['color'] = filtered_df['Direction'].map(color_map)
    else:
        filtered_df['color'] = colors[0]
    
    # Add bounce points
    for _, row in filtered_df.iterrows():
        # Convert coordinates to court scale
        bounce_x = row['Bounce (x)'] * 3  # Scale factor
        bounce_y = row['Bounce (y)'] * 2.5
        
        # Determine marker size based on speed
        marker_size = max(8, min(20, row['Speed (MPH)'] / 3))
        
        # Determine marker symbol based on result
        marker_symbol = 'circle' if row['Result'] == 'In' else 'x'
        
        fig.add_trace(go.Scatter(
            x=[bounce_x],
            y=[bounce_y],
            mode='markers',
            marker=dict(
                size=marker_size,
                color=row['color'],
                symbol=marker_symbol,
                line=dict(width=2, color='white')
            ),
            name=f"{row['Player']} - {row['Stroke']}",
            hovertemplate=(
                f"<b>{row['Player']}</b><br>"
                f"Stroke: {row['Stroke']}<br>"
                f"Speed: {row['Speed (MPH)']} MPH<br>"
                f"Direction: {row['Direction']}<br>"
                f"Result: {row['Result']}<br>"
                f"Spin: {row['Spin']}<br>"
                "<extra></extra>"
            ),
            showlegend=False
        ))
    
    return fig

def create_placement_analysis(df):
    """Create placement analysis charts"""
    # Deep vs Short analysis
    depth_counts = df['Bounce Depth'].value_counts()
    
    # Cross vs Line analysis  
    direction_counts = df['Direction'].value_counts()
    
    fig1 = px.pie(values=depth_counts.values, names=depth_counts.index, 
                  title="Shot Depth Distribution", color_discrete_sequence=px.colors.qualitative.Set3)
    
    fig2 = px.pie(values=direction_counts.values, names=direction_counts.index,
                  title="Shot Direction Distribution", color_discrete_sequence=px.colors.qualitative.Set2)
    
    return fig1, fig2

def create_speed_analysis(df):
    """Create speed analysis by player and stroke type"""
    fig = px.box(df, x='Player', y='Speed (MPH)', color='Stroke',
                 title="Speed Distribution by Player and Stroke Type")
    fig.update_layout(
        plot_bgcolor="#fff",
    )
    fig.update_xaxes(gridcolor='rgba(61,61,61,0.2)',zerolinecolor='rgb(61,61,61,0.2)',zeroline=True,zerolinewidth=1)
    fig.update_yaxes(gridcolor='rgba(61,61,61,0.2)',zerolinecolor='rgb(61,61,61,0.2)',zeroline=True,zerolinewidth=1)
    return fig