import pandas as pd



def read_data():

    df = pd.read_excel('./data/SwingVision-match-2025-08-29 at 16.40.52.xlsx',sheet_name='Shots')
    
    # Convert numeric columns
    numeric_cols = ["Speed (MPH)", "Point", "Game", "Set", "Bounce (x)", "Bounce (y)", 
                   "Hit (x)", "Hit (y)", "Hit (z)"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df