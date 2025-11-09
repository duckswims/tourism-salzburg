# components/sidebar.py
import streamlit as st
import datetime
import pandas as pd

def render_sidebar(df: pd.DataFrame):
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

    return {
        "selected_tagesarten": selected_tagesarten,
        "selected_linie": selected_linie,
        "selected_richtung": selected_richtung,
        "selected_months": selected_months
    }
