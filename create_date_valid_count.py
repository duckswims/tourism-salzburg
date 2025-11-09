import os
import pandas as pd

filename = 'data/ausgegebene_Tickets.csv'

# Create DataFrame
df = pd.read_csv(filename,  sep="\t")
df["valid_from"] = pd.to_datetime(df["valid_from"])
df["valid_to"] = pd.to_datetime(df["valid_to"])

# Expand each ticket to one row per day
df_expanded = (
    df
    .assign(date=lambda x: x.apply(lambda r: pd.date_range(r.valid_from, r.valid_to, freq="D"), axis=1))
    .explode("date")
)

# Count how many tickets are valid per day in each region
df_daily_counts = (
    df_expanded
    .groupby(["partner_id", "date"])
    .size()
    .reset_index(name="ticket_count")
)

df_daily_counts.to_csv('data/ticket_valid_dates.csv', index=False)