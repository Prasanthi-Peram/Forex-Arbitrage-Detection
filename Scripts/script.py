import os
import pandas as pd
from functools import reduce

data_dir = "csv_data"  
output_file = "../data/merged_all.csv"

dfs = []

for file in os.listdir(data_dir):
    if not file.endswith(".csv"):
        continue

    parts = file.split("_")
    if len(parts) < 4:
        continue
    pair = parts[2]

    filepath = os.path.join(data_dir, file)
    print(f"Reading {filepath} as pair: {pair}")

    df = pd.read_csv(filepath, header=None,
                     names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"])

    df["Timestamp"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%Y.%m.%d %H:%M")
    df = df[["Timestamp", "Close"]].rename(columns={"Close": pair})
    
    dfs.append(df)

# Full Outer Join on Timestamp
merged_df = reduce(lambda left, right: pd.merge(left, right, on="Timestamp", how="outer"), dfs)

merged_df = merged_df.sort_values("Timestamp").reset_index(drop=True)

# Save the final merged dataset
os.makedirs(os.path.dirname(output_file), exist_ok=True)
merged_df.to_csv(output_file, index=False)

print(f"\n✅ Merged dataset with all timestamps saved to: {output_file}")
print(merged_df.head())
print(f"\nTotal columns (including timestamp): {merged_df.shape[1]}")
