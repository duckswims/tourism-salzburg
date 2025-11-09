import pandas as pd
import streamlit as st
import altair as alt
import json
import datetime

# Import gemeinde_id
with open('data/gemeinde_data.json', 'r') as f:
    gemeinde = json.load(f)

filename = 'data/Zaehldaten_Q3_2025.xlsx'
df = pd.read_excel(filename)

df['Betriebstag'] = pd.to_datetime(df['Betriebstag'])

# === Sidebar: Filter Options ===
st.sidebar.header("🔍 Filter Options")

# Tagesart (multi-select)
tagesarten = sorted(df['Tagesart'].dropna().unique())
selected_tagesarten = st.sidebar.multiselect(
    "Tagesart",
    options=tagesarten,
    default=tagesarten[:1]
)

# Linie
linien = sorted(df['Linie'].dropna().unique())
selected_linie = st.sidebar.selectbox("Linie (Bus Line)", options=linien, index=0)

# Mapping for Linienrichtung
richtung_map = {}
for linie in linien:
    sub = df[df['Linie'] == linie]
    for richtung in sorted(sub['Linienrichtung'].dropna().unique()):
        subset = sub[sub['Linienrichtung'] == richtung]
        if 'Haltestellenabfolge' in subset.columns:
            # get first and last stop names
            first_stop = subset.loc[subset['Haltestellenabfolge'].idxmin(), 'HaltestelleName']
            last_stop = subset.loc[subset['Haltestellenabfolge'].idxmax(), 'HaltestelleName']
            richtung_map[(linie, richtung)] = f"{first_stop} → {last_stop}"
        else:
            richtung_map[(linie, richtung)] = f"Direction {richtung}"

# Available directions for the selected line
verfuegbare_richtungen = [
    (richtung, richtung_map[(selected_linie, richtung)])
    for richtung in sorted(df[df['Linie'] == selected_linie]['Linienrichtung'].dropna().unique())
]

selected_richtung_label = st.sidebar.selectbox(
    "Linienrichtung",
    options=[label for _, label in verfuegbare_richtungen],
    index=0
)
selected_richtung = [r for r, label in verfuegbare_richtungen if label == selected_richtung_label][0]

# Month (multi-select)
months = sorted(df['Betriebstag'].dt.month.unique())
selected_months = st.sidebar.multiselect(
    "Month",
    options=months,
    default=[months[0]],
    format_func=lambda x: datetime.date(1900, x, 1).strftime('%B')
)

# Filters
filtered_df = df[
    (df['Tagesart'].isin(selected_tagesarten)) &
    (df['Linie'] == selected_linie) &
    (df['Linienrichtung'] == selected_richtung) &
    (df['Betriebstag'].dt.month.isin(selected_months))
]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    df_grouped = (
        filtered_df
        .groupby(['Betriebstag', 'Kurs'])['Einsteiger']
        .sum()
        .reset_index()
    )
    df_grouped['Kurs'] = df_grouped['Kurs'].astype(int)

    # === Predicted values ===
    scan_rate = 0.3
    quantile_per_kurs = df_grouped.groupby('Kurs')['Einsteiger'].quantile(0.75).reset_index()
    quantile_per_kurs['predicted'] = quantile_per_kurs['Einsteiger'] / scan_rate
    df_predicted = quantile_per_kurs[['Kurs', 'predicted']]

    # === Visualization ===
    st.title(f"Einsteiger per Kurs")

    scatter_chart = alt.Chart(df_grouped).mark_circle(size=60, opacity=0.8).encode(
        x=alt.X('Kurs:O', title='Kurs'),
        y=alt.Y('Einsteiger:Q', title='Sum of Einsteiger'),
        color=alt.Color('Betriebstag:T', title='Betriebstag', scale=alt.Scale(scheme='viridis')),
        tooltip=['Betriebstag:T', 'Kurs', 'Einsteiger']
    )

    predicted_chart = alt.Chart(df_predicted).mark_line(
        color='red',
        strokeWidth=2
    ).encode(
        x=alt.X('Kurs:O'),
        y=alt.Y('predicted:Q'),
        tooltip=['Kurs', 'predicted']
    )
    # Overlay charts
    final_chart = scatter_chart + predicted_chart
    st.altair_chart(final_chart.interactive(), use_container_width=True)