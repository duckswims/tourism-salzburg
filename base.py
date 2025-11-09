# base.py
import pandas as pd
import json

# Load main Excel file
Q3_2025_df = pd.read_excel('data/Zaehldaten_Q3_2025.xlsx')

# Load gemeinde data
with open('data/gemeinde_data.json', 'r') as f:
    gemeinde = json.load(f)
