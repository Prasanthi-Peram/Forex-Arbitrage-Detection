import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

full_df = pd.read_csv("../data/merged_all.csv")
full_df["Date"] = pd.to_datetime(full_df["Timestamp"]).dt.date

arb_df = pd.read_csv("../data/bellman_output.csv")
arb_df["Date"] = pd.to_datetime(arb_df["timestamp"]).dt.date

total_counts = full_df["Date"].value_counts().sort_index()
arb_counts = arb_df["Date"].value_counts().sort_index()

arb_density = (arb_counts / total_counts) * 100

plt.figure(figsize=(10, 6))
plt.plot(arb_density.index, arb_density.values, color="green")
plt.title("Arbitrage Density by Day")
plt.xlabel("Date")
plt.ylabel("Arbitrage Opportunities / # of Timestamps (%)")
plt.grid(True)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.gcf().autofmt_xdate()
plt.savefig("arb_density.jpg", format='jpg', bbox_inches='tight', dpi=300)
plt.close()
