import pandas as pd
import streamlit as st
# import plotly.express as px
import altair as alt
import json
import datetime
import numpy as np

# Import gemeinde_id
with open('data/gemeinde_data.json', 'r') as f:
    gemeinde = json.load(f)


filename = 'data/Zaehldaten_Q3_2025.xlsx'
df = pd.read_excel(filename)

header1, header2 = st.columns([4, 1])

header1.title('Bus 670')
header2.image("assets/Salzburg-Verkehr-Logo.png")


with st.sidebar:
    st.header("🔍 Filters")

    # Tagesart (multi-select)
    tagesarten = sorted(df['Tagesart'].dropna().unique())
    selected_tagesarten = st.multiselect("Tagesart", options=tagesarten, default=tagesarten[:1])

    # Linie (selectbox)
    linien = sorted(df['Linie'].dropna().unique())
    selected_linie = st.selectbox("Linie (Bus Line)", options=linien, index=1)

    # Linienrichtung (selectbox)
    richtung_map = {}
    for linie in linien:
        sub = df[df['Linie'] == linie]
        for richtung in sorted(sub['Linienrichtung'].dropna().unique()):
            if 'Haltestellenabfolge' in sub.columns:
                first_stop = sub.loc[sub['Linienrichtung'] == richtung, 'HaltestelleName'].iloc[0]
                last_stop = sub.loc[sub['Linienrichtung'] == richtung, 'HaltestelleName'].iloc[-1]
                richtung_map[(linie, richtung)] = f"{first_stop} → {last_stop}"
            else:
                richtung_map[(linie, richtung)] = f"Direction {richtung}"

    verfuegbare_richtungen = [
        (richtung, richtung_map[(selected_linie, richtung)])
        for richtung in sorted(df[df['Linie'] == selected_linie]['Linienrichtung'].dropna().unique())
    ]
    selected_richtung_label = st.selectbox(
        "Linienrichtung",
        options=[label for _, label in verfuegbare_richtungen],
        index=0
    )
    selected_richtung = [r for r, label in verfuegbare_richtungen if label == selected_richtung_label][0]

    # Month (multi-select)
    months = sorted(df['Betriebstag'].dt.month.unique())
    selected_months = st.multiselect(
        "Month",
        options=months,
        default=[months[1]],
        format_func=lambda x: datetime.date(1900, x, 1).strftime('%B')
    )


# Top row (you can leave empty or put something)
col1, col2 = st.columns(2)
col1.write("Chart1")   # optional
col2.write("Chart2")  # optional

# Bottom row with the two charts
col3, col4 = st.columns(2)


# df = df[df['Tagesart'] == 'Mo-Fr Ferien']
df = df[df['Linie'] == 670] # Filter for line 670
df = df[df['Linienrichtung'] == 1] # Filter for Linierichtung 1
df = df[df['Betriebstag'].dt.month == 8]
df['weekday'] = df['Betriebstag'].dt.weekday
df['is_weekend'] = df['weekday'].isin([5,6]).astype(bool)


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
col3.subheader("Tourist Ridership per Trip")

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
col4.subheader("Actual vs Estimated Tourists")

# Actual scanned line
actual_line = alt.Chart(daily_sum).mark_line(color='blue', point=True).encode(
    x=alt.X('Betriebstag:T', title='Betriebstag'),
    y=alt.Y('Einsteiger:Q', title='Number of Einsteiger'),
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

