import pandas as pd

df = pd.read_csv("../data/bellman_output.csv")  # Adjust filename if needed


df["Profit"] = df["profit"].astype(float)
df["Cycle"] = df["cycle"].str.split("/")
df["Timestamp"] = df["timestamp"]

# Extract Base Currency
df["Base Currency"] = df["Cycle"].apply(lambda i: i[0])


rates_df = pd.read_csv("../data/merged_all.csv")  # Where your exchange rates live
rates_df = rates_df.set_index("Timestamp")

# Map Base to USD
base_to_usd = []
for idx, row in df.iterrows():
    timestamp = row["Timestamp"]
    base = row["Base Currency"]
    try:
        rates_row = rates_df.loc[timestamp]
        if base == "USD":
            base_to_usd.append(1.0)
        elif f"{base}USD" in rates_row:
            base_to_usd.append(rates_row[f"{base}USD"])
        elif f"USD{base}" in rates_row:
            base_to_usd.append(1 / rates_row[f"USD{base}"])
        else:
            base_to_usd.append(float('nan'))
    except:
        base_to_usd.append(float('nan'))

df["Base to USD"] = base_to_usd

last_seen = {}
for idx in reversed(df.index):
    base = df.loc[idx, "Base Currency"]
    value = df.loc[idx, "Base to USD"]
    if pd.notna(value):
        last_seen[base] = value
    elif base in last_seen:
        df.loc[idx, "Base to USD"] = last_seen[base]

# Cycle Length
df["Cycle Length"] = df["Cycle"].apply(lambda x: len(x)-1)

# USD Adjusted Profit
df["USD Adjusted Profit"] = (df["Profit"] - 1) * df["Base to USD"]

# Sort by Timestamp
df = df.sort_values(by="Timestamp")

# Final Output Format
df = df[["Profit", "Cycle", "Timestamp", "Base to USD", "Base Currency", "Cycle Length", "USD Adjusted Profit"]]

print(df.head())
df.to_csv("../arb_analysis.csv", index=False)
