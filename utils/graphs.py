import plotly.graph_objects as go
import plotly.express as px
from utils.data_reader import read_data


df = read_data()

# Tennis court dimensions (standard court)
COURT_LENGTH = 78  # feet
COURT_WIDTH = 36   # feet
NET_HEIGHT = 3     # feet

def analyze_data_bounds(df):
    """Analyze the data to determine precise court scaling"""
    bounce_x_min, bounce_x_max = df['Bounce (x)'].min(), df['Bounce (x)'].max()
    bounce_y_min, bounce_y_max = df['Bounce (y)'].min(), df['Bounce (y)'].max()
    
    # Calculate scaling factors to map data to tennis court dimensions
    # Tennis court: Width = 36ft (27ft singles + 4.5ft alleys each side), Half Length = 39ft
    data_x_range = bounce_x_max - bounce_x_min
    data_y_range = bounce_y_max - bounce_y_min
    
    # Scale to fit within court bounds with some padding
    x_scale = 30 / data_x_range if data_x_range > 0 else 1  # 30ft to account for court width
    y_scale = 35 / data_y_range if data_y_range > 0 else 1  # 35ft for half court length
    
    return {
        'x_min': bounce_x_min, 'x_max': bounce_x_max,
        'y_min': bounce_y_min, 'y_max': bounce_y_max,
        'x_scale': x_scale, 'y_scale': y_scale,
        'x_offset': 0, 'y_offset': 0
    }

# Analyze data bounds
data_bounds = analyze_data_bounds(df)

# Tennis court dimensions (half court)
COURT_LENGTH = 39  # Half court length (from net to baseline)
COURT_WIDTH = 36   # feet
SINGLES_WIDTH = 27  # Singles court width
NET_HEIGHT = 3     # feet

def transform_coordinates(x, y, player_perspective, data_bounds):
    """Transform data coordinates to court coordinates with proper scaling and orientation"""
    # Apply scaling
    scaled_x = x * data_bounds['x_scale']
    scaled_y = y * data_bounds['y_scale']
    
    # Center the x-coordinate
    court_x = scaled_x
    
    # Handle y-coordinate based on player perspective
    if player_perspective == "Kamran Khan":
        # Net at bottom (y=0), baseline at top (y=39)
        # Positive y values in data should map to higher court positions
        court_y = abs(scaled_y)
    else:  # Alex MacDonald
        # Net at top (y=39), baseline at bottom (y=0) 
        # Positive y values in data should map to lower court positions
        court_y = COURT_LENGTH - abs(scaled_y)
    
    # Clamp to court bounds
    court_x = max(-COURT_WIDTH/2, min(COURT_WIDTH/2, court_x))
    court_y = max(0, min(COURT_LENGTH, court_y))
    
    return court_x, court_y

def create_tennis_court_half(player_perspective="Kamran Khan"):
    """Create half tennis court layout with proper orientation"""
    fig = go.Figure()
    
    # Determine court orientation and title
    if player_perspective == "Kamran Khan":
        court_title = "Where Kamran Khan's shots land (Alex MacDonald's side)"
        net_y = 0
        baseline_y = COURT_LENGTH
        service_line_y = 21
        net_label_y = -2
        baseline_label_y = COURT_LENGTH + 2
    else:  # Alex MacDonald
        court_title = "Where Alex MacDonald's shots land (Kamran Khan's side)"
        net_y = COURT_LENGTH
        baseline_y = 0
        service_line_y = COURT_LENGTH - 21
        net_label_y = COURT_LENGTH + 2
        baseline_label_y = -2
    
    # Court outline (half court)
    fig.add_shape(type="rect", x0=-COURT_WIDTH/2, y0=0, x1=COURT_WIDTH/2, y1=COURT_LENGTH,
                  line=dict(color="white", width=3), fillcolor="rgba(34,139,34,0.3)")
    
    # Net line
    fig.add_shape(type="line", x0=-COURT_WIDTH/2, y0=net_y, x1=COURT_WIDTH/2, y1=net_y,
                  line=dict(color="white", width=4))
    
    # Service boxes
    fig.add_shape(type="line", x0=0, y0=min(net_y, service_line_y), x1=0, y1=max(net_y, service_line_y),
                  line=dict(color="white", width=2))  # Center service line
    fig.add_shape(type="line", x0=-SINGLES_WIDTH/2, y0=service_line_y, x1=SINGLES_WIDTH/2, y1=service_line_y,
                  line=dict(color="white", width=2))  # Service line
    
    # Singles sidelines
    fig.add_shape(type="line", x0=-SINGLES_WIDTH/2, y0=0, x1=-SINGLES_WIDTH/2, y1=COURT_LENGTH,
                  line=dict(color="white", width=2))
    fig.add_shape(type="line", x0=SINGLES_WIDTH/2, y0=0, x1=SINGLES_WIDTH/2, y1=COURT_LENGTH,
                  line=dict(color="white", width=2))
    
    # Doubles sidelines (alleys)
    fig.add_shape(type="line", x0=-COURT_WIDTH/2, y0=0, x1=-COURT_WIDTH/2, y1=COURT_LENGTH,
                  line=dict(color="white", width=2))
    fig.add_shape(type="line", x0=COURT_WIDTH/2, y0=0, x1=COURT_WIDTH/2, y1=COURT_LENGTH,
                  line=dict(color="white", width=2))
    
    # Baseline
    fig.add_shape(type="line", x0=-COURT_WIDTH/2, y0=baseline_y, x1=COURT_WIDTH/2, y1=baseline_y,
                  line=dict(color="white", width=3))
    
    # Create 6 vertical zones for placement analysis
    zone_width = SINGLES_WIDTH / 6  # Singles court width divided into 6 zones
    start_x = -SINGLES_WIDTH/2  # Start from left singles sideline
    
    for i in range(1, 6):  # Create 5 vertical lines to make 6 zones
        x_pos = start_x + (zone_width * i)
        fig.add_shape(type="line", x0=x_pos, y0=0, x1=x_pos, y1=COURT_LENGTH,
                      line=dict(color="yellow", width=1, dash="dot"), opacity=0.6)
    
    # Create horizontal depth line at service line (modified section)
    # Use service_line_y instead of mid_y for depth analysis
    # Extend line to full court width (including doubles alleys)
    fig.add_shape(type="line", x0=-COURT_WIDTH/2, y0=service_line_y, x1=COURT_WIDTH/2, y1=service_line_y,
                  line=dict(color="yellow", width=2, dash="dot"), opacity=0.8)
    
    # Add court labels
    fig.add_annotation(x=-9, y=COURT_LENGTH/4, text="Ad Court", showarrow=False, 
                      font=dict(color="white", size=12), bgcolor="rgba(0,0,0,0.5)")
    fig.add_annotation(x=9, y=COURT_LENGTH/4, text="Deuce Court", showarrow=False,
                      font=dict(color="white", size=12), bgcolor="rgba(0,0,0,0.5)")
    fig.add_annotation(x=0, y=net_label_y, text="Net", showarrow=False,
                      font=dict(color="white", size=14, family="Arial Black"), bgcolor="rgba(0,0,0,0.7)")
    fig.add_annotation(x=0, y=baseline_label_y, text="Baseline", showarrow=False,
                      font=dict(color="white", size=12), bgcolor="rgba(0,0,0,0.5)")
    
    # Initialize zone percentage labels (will be updated by add_shot_data)
    zone_labels_x = [start_x + (zone_width * (i + 0.5)) for i in range(6)]
    zone_names = ["Wide Ad", "Ad Court", "Ad Center", "Deuce Center", "Deuce Court", "Wide Deuce"]
    
    for i, (x_pos, zone_name) in enumerate(zip(zone_labels_x, zone_names)):
        fig.add_annotation(x=x_pos, y=COURT_LENGTH + 3, text=f"{zone_name}<br>0%", showarrow=False,
                          font=dict(color="yellow", size=9), bgcolor="rgba(0,0,0,0.7)",
                          name=f"zone_{i}")
    
    # Initialize depth zone labels - positioned relative to service line
    if player_perspective == "Kamran Khan":
        short_y = service_line_y * 0.5  # Between net and service line
        deep_y = service_line_y + (COURT_LENGTH - service_line_y) * 0.5  # Between service line and baseline
    else:  # Alex MacDonald
        deep_y = service_line_y * 0.5  # Between baseline and service line  
        short_y = service_line_y + (COURT_LENGTH - service_line_y) * 0.5  # Between service line and net
    
    fig.add_annotation(x=15, y=short_y, text="Short Zone<br>0%", showarrow=False,
                      font=dict(color="lightblue", size=10), bgcolor="rgba(0,0,0,0.7)", name="short_zone")
    fig.add_annotation(x=15, y=deep_y, text="Deep Zone<br>0%", showarrow=False,
                      font=dict(color="lightblue", size=10), bgcolor="rgba(0,0,0,0.7)", name="deep_zone")
    
    fig.update_layout(
        title=dict(text=court_title, x=0.5, font=dict(size=16, color='white')),
        plot_bgcolor='rgba(34,139,34,0.8)',
        paper_bgcolor='rgba(34,139,34,0.8)',
        xaxis=dict(range=[-22, 22], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-5, 45], showgrid=False, zeroline=False, visible=False),
        showlegend=True,
        height=800,
        # width=800,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

def add_shot_data_half_court(fig, filtered_df, player_perspective, color_by="Stroke"):
    """Add shot placement data to half court with precise scaling and zone calculations"""
    if filtered_df.empty:
        return fig
    
    # Color mapping
    colors = px.colors.qualitative.Set1
    if color_by == "Stroke":
        unique_vals = filtered_df['Stroke'].unique()
        color_map = {val: colors[i % len(colors)] for i, val in enumerate(unique_vals)}
        filtered_df['color'] = filtered_df['Stroke'].map(color_map)
    elif color_by == "Direction":
        unique_vals = filtered_df['Direction'].unique()
        color_map = {val: colors[i % len(colors)] for i, val in enumerate(unique_vals)}
        filtered_df['color'] = filtered_df['Direction'].map(color_map)
    elif color_by == "Result":
        result_colors = {'In': 'green', 'Out': 'red', 'Net': 'orange'}
        filtered_df['color'] = filtered_df['Result'].map(result_colors)
    else:
        filtered_df['color'] = colors[0]
    
    # Calculate zone statistics
    zone_width = SINGLES_WIDTH / 6  # 6 vertical zones
    start_x = -SINGLES_WIDTH/2
    zone_counts = [0] * 6  # 6 zones
    depth_counts = {"short": 0, "deep": 0}  # 2 depth zones
    total_shots = 0
    
    # Get service line position based on player perspective
    if player_perspective == "Kamran Khan":
        service_line_y = 21
    else:
        service_line_y = COURT_LENGTH - 21
    
    # Add bounce points and calculate zone statistics
    for _, row in filtered_df.iterrows():
        # Transform coordinates using precise scaling
        court_x, court_y = transform_coordinates(
            row['Bounce (x)'], row['Bounce (y)'], 
            player_perspective, data_bounds
        )
        
        # Determine which horizontal zone (0-5)
        if -SINGLES_WIDTH/2 <= court_x <= SINGLES_WIDTH/2:  # Within singles court
            zone_index = int((court_x - start_x) / zone_width)
            zone_index = max(0, min(5, zone_index))  # Clamp to valid range
            zone_counts[zone_index] += 1
            
            # Determine depth zone based on service line position
            if player_perspective == "Kamran Khan":
                # For Kamran Khan: short = between net (0) and service line (21)
                # deep = between service line (21) and baseline (39)
                if court_y <= service_line_y:
                    depth_counts["short"] += 1
                else:
                    depth_counts["deep"] += 1
            else:  # Alex MacDonald
                # For Alex MacDonald: deep = between baseline (0) and service line (18)
                # short = between service line (18) and net (39)
                if court_y <= service_line_y:
                    depth_counts["deep"] += 1
                else:
                    depth_counts["short"] += 1
            
            total_shots += 1
        
        # Determine marker size based on speed
        marker_size = max(8, min(20, row['Speed (MPH)'] / 3))
        
        # Determine marker symbol based on result
        if row['Result'] == 'In':
            marker_symbol = 'circle'
        elif row['Result'] == 'Out':
            marker_symbol = 'x'
        else:  # Net
            marker_symbol = 'triangle-up'
        
        fig.add_trace(go.Scatter(
            x=[court_x],
            y=[court_y],
            mode='markers',
            marker=dict(
                size=marker_size,
                color=row['color'],
                symbol=marker_symbol,
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
    
    # Clear existing annotations and add updated ones
    fig.layout.annotations = []
    
    # Re-add basic court labels
    net_y = 0 if player_perspective == "Kamran Khan" else COURT_LENGTH
    baseline_y = COURT_LENGTH if player_perspective == "Kamran Khan" else 0
    net_label_y = -2 if player_perspective == "Kamran Khan" else COURT_LENGTH + 2
    baseline_label_y = COURT_LENGTH + 2 if player_perspective == "Kamran Khan" else -2
    
    fig.add_annotation(x=-9, y=COURT_LENGTH/4, text="Ad Court", showarrow=False, 
                      font=dict(color="white", size=12), bgcolor="rgba(0,0,0,0.5)")
    fig.add_annotation(x=9, y=COURT_LENGTH/4, text="Deuce Court", showarrow=False,
                      font=dict(color="white", size=12), bgcolor="rgba(0,0,0,0.5)")
    fig.add_annotation(x=0, y=net_label_y, text="Net", showarrow=False,
                      font=dict(color="white", size=14, family="Arial Black"), bgcolor="rgba(0,0,0,0.7)")
    fig.add_annotation(x=0, y=baseline_label_y, text="Baseline", showarrow=False,
                      font=dict(color="white", size=12), bgcolor="rgba(0,0,0,0.5)")
    
    # Add updated zone percentages (6 zones)
    zone_labels_x = [start_x + (zone_width * (i + 0.5)) for i in range(6)]
    zone_names = ["Wide Ad", "Ad Court", "Ad Center", "Deuce Center", "Deuce Court", "Wide Deuce"]
    
    if total_shots > 0:
        for i, (x_pos, zone_name, count) in enumerate(zip(zone_labels_x, zone_names, zone_counts)):
            percentage = (count / total_shots) * 100
            fig.add_annotation(
                x=x_pos, 
                y=COURT_LENGTH + 3, 
                text=f"{zone_name}<br>{percentage:.1f}%<br>({count})",
                showarrow=False,
                font=dict(color="yellow", size=9, family="Arial Bold"), 
                bgcolor="rgba(0,0,0,0.8)",
                bordercolor="yellow",
                borderwidth=1
            )
        
        # Add depth zone percentages - positioned relative to service line
        if player_perspective == "Kamran Khan":
            short_y = service_line_y * 0.5  # Between net and service line
            deep_y = service_line_y + (COURT_LENGTH - service_line_y) * 0.5  # Between service line and baseline
        else:  # Alex MacDonald
            deep_y = service_line_y * 0.5  # Between baseline and service line  
            short_y = service_line_y + (COURT_LENGTH - service_line_y) * 0.5  # Between service line and net
        
        fig.add_annotation(
            x=15, y=short_y,
            text=f"Short Zone<br>{(depth_counts['short']/total_shots)*100:.1f}%<br>({depth_counts['short']})",
            showarrow=False,
            font=dict(color="lightblue", size=10, family="Arial Bold"),
            bgcolor="rgba(0,0,0,0.8)",
            bordercolor="lightblue",
            borderwidth=1
        )
        
        fig.add_annotation(
            x=15, y=deep_y,
            text=f"Deep Zone<br>{(depth_counts['deep']/total_shots)*100:.1f}%<br>({depth_counts['deep']})",
            showarrow=False,
            font=dict(color="lightblue", size=10, family="Arial Bold"),
            bgcolor="rgba(0,0,0,0.8)",
            bordercolor="lightblue",
            borderwidth=1
        )
        
        # Add total shots counter
        fig.add_annotation(
            x=-17, y=COURT_LENGTH + 3,
            text=f"Total Shots: {total_shots}",
            showarrow=False,
            font=dict(color="white", size=12, family="Arial Bold"),
            bgcolor="rgba(0,0,0,0.8)",
            bordercolor="white",
            borderwidth=1
        )
    
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