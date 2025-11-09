# main_app.py
import streamlit as st
import altair as alt
import numpy as np
from base import Q3_2025_df, gemeinde
from components.sidebar import render_sidebar

# Header
header1, header2 = st.columns([4, 1])
header1.title('Bus 670')
header2.image("assets/Salzburg-Verkehr-Logo.png")

# Sidebar
with st.sidebar:
    filters = render_sidebar(Q3_2025_df)

# Filter dataframe
df = Q3_2025_df.copy()
df = df[df['Linie'] == filters['selected_linie']]
df = df[df['Linienrichtung'] == filters['selected_richtung']]
df = df[df['Betriebstag'].dt.month.isin(filters['selected_months'])]

# Add weekday and weekend flags
df['weekday'] = df['Betriebstag'].dt.weekday
df['is_weekend'] = df['weekday'].isin([5,6])


# Top row with image
st.image("assets/bus_route.png")

# Bottom row with the two charts
col3, col4 = st.columns(2)



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
col3.subheader("Tourist Ridership")

# Original scatter
scatter_chart = alt.Chart(df_grouped).mark_circle(size=60).encode(
    x=alt.X('Kurs:O', title='Route'),
    y=alt.Y('Einsteiger:Q', title='Passengers boarded'),
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

col3.altair_chart(final_chart, use_container_width=True)





# Sum Einsteiger per day (actual scanned)
daily_sum = df.groupby('Betriebstag').agg(
    Einsteiger=('Einsteiger', 'sum'),
    is_weekend=('is_weekend', 'first')  # or 'max'
).reset_index()
daily_sum = daily_sum.sort_values('Betriebstag')

# Different scan rates
weekday_rate = 0.2  
weekend_rate = weekday_rate * .75  

# Apply conditional estimated occupancy
daily_sum['estimated'] = np.where(
    daily_sum['is_weekend'],
    daily_sum['Einsteiger'] / weekend_rate,
    daily_sum['Einsteiger'] / weekday_rate
)

# Streamlit Altair plot
col4.subheader("Tourists Projection")

# Actual scanned line
actual_line = alt.Chart(daily_sum).mark_line(color='blue', point=True).encode(
    x=alt.X('Betriebstag:T', title='Date'),
    y=alt.Y('Einsteiger:Q', title='Passengers boarded'),
    tooltip=['Betriebstag:T', 'Einsteiger', 'is_weekend']
)

# Estimated total line
estimated_line = alt.Chart(daily_sum).mark_line(color='red', point=True).encode(
    x=alt.X('Betriebstag:T'),
    y=alt.Y('estimated:Q'),
    tooltip=['Betriebstag:T', 'estimated', 'is_weekend']
)

# Combine charts
chart = actual_line + estimated_line

col4.altair_chart(chart.interactive(), use_container_width=True)

