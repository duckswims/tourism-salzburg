import pandas as pd
import streamlit as st
# import plotly.express as px
import altair as alt
import json
import datetime

# Import gemeinde_id
with open('data/gemeinde_data.json', 'r') as f:
    gemeinde = json.load(f)


filename = 'data/Zaehldaten_Q3_2025.xlsx'
df = pd.read_excel(filename)

df = df[df['Tagesart'] == 'Mo-Fr Ferien']
df = df[df['Linie'] == 670] # Filter for line 670
df = df[df['Linienrichtung'] == 1] # Filter for Linierichtung 1
df = df[df['Betriebstag'].dt.month == 8]
# df = df[df['Kurs'] < 200]


# Group by Kurs and Betriebstag
df_grouped = df.groupby(['Betriebstag', 'Kurs'])['Einsteiger'].sum().reset_index()
df_grouped['Kurs'] = df_grouped['Kurs'].astype(int)

# Calculate predicted values using median per Kurs
scan_rate = 0.3
quantile_per_kurs = df_grouped.groupby('Kurs')['Einsteiger'].quantile(0.75).reset_index()
quantile_per_kurs['predicted'] = quantile_per_kurs['Einsteiger'] / scan_rate

# Merge predicted values back to df_grouped (optional, for plotting)
df_predicted = quantile_per_kurs[['Kurs', 'predicted']]

# Streamlit Altair scatter plot
st.title("Einsteiger per Kurs for Each Betriebstag with Predicted")

# Original scatter
scatter_chart = alt.Chart(df_grouped).mark_circle(size=60).encode(
    x=alt.X('Kurs:O', title='Kurs'),
    y=alt.Y('Einsteiger:Q', title='Sum of Einsteiger'),
    # color=alt.Color('Betriebstag:T', title='Betriebstag'),
    tooltip=['Betriebstag:T', 'Kurs', 'Einsteiger']
)

# Predicted line/points
predicted_chart = alt.Chart(df_predicted).mark_line(color='red', strokeWidth=2).encode(
    x=alt.X('Kurs:O'),
    y=alt.Y('predicted:Q')
)

# Overlay charts
final_chart = scatter_chart + predicted_chart

st.altair_chart(final_chart, use_container_width=True)