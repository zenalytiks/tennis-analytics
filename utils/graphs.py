import plotly.graph_objects as go
import plotly.express as px

# Tennis court dimensions (half court)
COURT_LENGTH = 11.89  # meters (baseline to net)
COURT_WIDTH = 10.97   # meters (full width)
# Service boxes
service_line_y = 5.49  # 5.49m from baseline (18 feet)
singles_width = 8.23   # 8.23m singles court width
# Create 6 vertical zones for placement analysis
zone_width = singles_width / 3  # Singles court width divided into 3 zones
start_x = -singles_width/2  # Start from left singles sideline

# Function to create tennis court lines
def create_tennis_court_shapes():
    """Create shapes for half tennis court layout"""
    shapes = []
    annotations = []
    
    # Court boundaries (half court from baseline to net)
    # Outer boundary
    shapes.append({
        'type': 'rect',
        'x0': COURT_WIDTH/2, 'y0': COURT_LENGTH,
        'x1': -COURT_WIDTH/2, 'y1': 0,
        'line': {'color': 'darkgray', 'width': 4},
        'layer': 'below'
    })
    
    # Baseline (back of court)
    shapes.append({
        'type': 'line',
        'x0': COURT_WIDTH/2, 'y0': 0,
        'x1': -COURT_WIDTH/2, 'y1': 0,
        'line': {'color': 'darkgray', 'width': 3}
    })
    
    # Net line
    shapes.append({
        'type': 'line',
        'x0': COURT_WIDTH/2, 'y0': 0,
        'x1': COURT_WIDTH/2, 'y1': COURT_LENGTH,
        'line': {'color': 'darkgray', 'width': 4}
    })
    
    # Side lines
    shapes.append({
        'type': 'line',
        'x0': COURT_WIDTH/2, 'y0': COURT_LENGTH + 1,
        'x1': COURT_WIDTH/2, 'y1': 0,
        'line': {'color': 'darkgray', 'width': 4}
    })
    
    shapes.append({
        'type': 'line',
        'x0': -COURT_WIDTH/2, 'y0': COURT_LENGTH + 1,
        'x1': -COURT_WIDTH/2, 'y1': 0,
        'line': {'color': 'darkgray', 'width': 4}
    })
    
    
    
    # Service line
    shapes.append({
        'type': 'line',
        'x0': singles_width/2, 'y0': service_line_y,
        'x1': -singles_width/2, 'y1': service_line_y,
        'line': {'color': 'darkgray', 'width': 2}
    })
    
    # Center service line
    shapes.append({
        'type': 'line',
        'x0': 0, 'y0': COURT_LENGTH + 1,
        'x1': 0, 'y1': service_line_y,
        'line': {'color': 'darkgray', 'width': 2}
    })
    
    # Singles sidelines
    shapes.append({
        'type': 'line',
        'x0': singles_width/2, 'y0': COURT_LENGTH + 1,
        'x1': singles_width/2, 'y1': 0,
        'line': {'color': 'darkgray', 'width': 2}
    })
    
    shapes.append({
        'type': 'line',
        'x0': -singles_width/2, 'y0': COURT_LENGTH + 1,
        'x1': -singles_width/2, 'y1': 0,
        'line': {'color': 'darkgray', 'width': 2}
    })

    shapes.append({
        'type': 'line',
        'x0': 0, 'y0': 0,
        'x1': 0, 'y1': 0.3,
        'line': {'color': 'darkgray', 'width': 2}
    })

     
    
    for i in range(1, 3):  # Create 2 vertical lines to make 3 zones
        x_pos = start_x + (zone_width * i)
        shapes.append({'type': 'line', 'x0': x_pos, 'y0': 0 - 1, 'x1': x_pos, 'y1': COURT_LENGTH + 1,
                      'line':{'color': "lightgray", 'width':2, 'dash':'dot'}, 'opacity': 0.6})
    
    # Create horizontal depth line at service line (modified section)
    # Use service_line_y instead of mid_y for depth analysis
    # Extend line to full court width (including doubles alleys)
    shapes.append({'type': 'line', 'x0': (singles_width/2) + 2, 'y0': service_line_y, 'x1': (-singles_width/2) - 2, 'y1': service_line_y,
                  'line': {'color': 'lightgray', 'width': 2, 'dash': 'dot'}, 'opacity':0.8})
    
    # Add court labels
    annotations.append({'x': 0, 'y': COURT_LENGTH + 0.5, 'text': "Net", 'showarrow': False,
                      'font': {'color': 'darkgray', 'size': 14, 'family': 'Arial Black'}})
    annotations.append({'x': 0, 'y': -0.5, 'text': 'Baseline', 'showarrow': False,
                      'font': {'color': 'darkgray', 'size': 12}})
    
    return shapes,annotations

def add_shot_data(fig, filtered_df, df):
    if filtered_df.empty:
        return fig

    # Calculate zone statistics (only for shots within singles court)
    zone_counts = [0] * 3  # 3 zones
    depth_counts = {"short": 0, "deep": 0}  # 2 depth zones
    total_shots = 0
    shots_in_analysis_area = 0  # For zone percentage calculations

    # Add bounce points - PLOT ALL SHOTS, not just those in singles court
    for _, row in filtered_df.iterrows():
        court_x, court_y = row['Bounce (x)'], row['Bounce (y)']
        
        # Plot ALL shots regardless of position
        marker_size = max(8, min(20, row['Speed (MPH)'] / 3))
        
        # Determine marker symbol based on result
        if row['Result'] == 'In':
            marker_symbol = 'circle'
        elif row['Result'] == 'Out':
            marker_symbol = 'x'
        else:  # Net
            marker_symbol = 'triangle-up'
        
        # Add trace for this shot
        fig.add_trace(go.Scatter(
            x=[court_x],
            y=[court_y],
            mode='markers',
            marker=dict(
                size=marker_size,
                symbol=marker_symbol,
                color=row['color'],
                line=dict(width=2, color='white'),
                opacity=0.8
            ),
            name=f"{row['Stroke']} - {row['Direction']}",
            hovertemplate=(
                f"<b>{row['Player']}</b><br>"
                f"Stroke: {row['Stroke']}<br>"
                f"Speed: {row['Speed (MPH)']} MPH<br>"
                f"Direction: {row['Direction']}<br>"
                f"Result: {row['Result']}<br>"
                f"Spin: {row['Spin']}<br>"
                f"Shot Type: {row['Type']}<br>"
                f"Court Position: ({court_x:.1f}, {court_y:.1f})<br>"
                "<extra></extra>"
            ),
            showlegend=False
        ))
        
        total_shots += 1
        
        # Only count for zone analysis if within singles court bounds AND valid court length AND not a net shot
        if (row['Result'] != 'Net' and 
            -singles_width/2 <= court_x <= singles_width/2 and 
            0 <= court_y <= COURT_LENGTH):
            
            # Determine which horizontal zone (0-2)
            zone_index = int((court_x - start_x) / zone_width)
            zone_index = max(0, min(2, zone_index))  # Clamp to valid range
            zone_counts[zone_index] += 1

            # Depth analysis
            if court_y >= service_line_y:
                depth_counts["deep"] += 1
            else:
                depth_counts["short"] += 1
            
            shots_in_analysis_area += 1
    
    # Add zone percentages (only for shots in analysis area)
    zone_labels_x = [start_x + (zone_width * (i + 0.5)) for i in range(3)]
    zone_names = ["Ad", "Center", "Deuce"]
    
    if shots_in_analysis_area > 0:  # Use shots_in_analysis_area instead of total_shots
        for i, (x_pos, zone_name, count) in enumerate(zip(zone_labels_x, zone_names, zone_counts)):
            percentage = (count / shots_in_analysis_area) * 100
            fig.add_annotation(
                x=x_pos, 
                y=COURT_LENGTH + 1.5, 
                text=f"{percentage:.1f}%",
                showarrow=False,
                font=dict(color="darkgray", size=12, family="Arial Bold")
            )
        
        # Add depth zone percentages
        short_y = service_line_y * 0.5
        deep_y = service_line_y + (COURT_LENGTH - service_line_y) * 0.5
        
        fig.add_annotation(
            x=6.5, y=short_y,
            text=f"{(depth_counts['short']/shots_in_analysis_area)*100:.1f}%",
            showarrow=False,
            font=dict(color="darkgray", size=12, family="Arial Bold")
        )
        
        fig.add_annotation(
            x=6.5, y=deep_y,
            text=f"{(depth_counts['deep']/shots_in_analysis_area)*100:.1f}%",
            showarrow=False,
            font=dict(color="darkgray", size=12, family="Arial Bold")
        )

    return fig

def create_placement_analysis(df):
    """Create placement analysis charts"""
    # Deep vs Short analysis
    depth_counts = df['Bounce Depth'].value_counts()
    
    # Cross vs Line analysis  
    direction_counts = df['Direction'].value_counts()
    
    fig1 = px.pie(values=depth_counts.values, names=depth_counts.index, color_discrete_sequence=px.colors.qualitative.Set2)
    fig1.update_layout(legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"),margin=dict(l=20, r=20, t=20, b=20))
    
    fig2 = px.pie(values=direction_counts.values, names=direction_counts.index, color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_layout(legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"),margin=dict(l=20, r=20, t=20, b=20))
    
    return fig1, fig2

def create_speed_analysis(df):
    """Create speed analysis by player and stroke type"""
    fig = px.box(df, x='Stroke', y='Speed (MPH)', color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(
        plot_bgcolor="#fff",
        legend=dict(orientation="h", y=1.2, x=0.5, xanchor="center"),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    fig.update_xaxes(gridcolor='rgba(61,61,61,0.2)',zerolinecolor='rgb(61,61,61,0.2)',zeroline=True,zerolinewidth=1)
    fig.update_yaxes(gridcolor='rgba(61,61,61,0.2)',zerolinecolor='rgb(61,61,61,0.2)',zeroline=True,zerolinewidth=1)
    return fig