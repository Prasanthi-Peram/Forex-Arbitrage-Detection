import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

df = pd.read_csv("../data/bellman_output.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

plt.figure(figsize=(10, 6))
plt.scatter(df["date"], df["profit"] - 1, s=1, alpha=0.5, label="Raw Profit")

daily_median = df.groupby("date")["profit"].median() - 1
rolling_median = daily_median.rolling(window=3, center=True).median()

plt.plot(rolling_median.index, rolling_median.values, color="orange", linewidth=2, label="3-day Rolling Median")

plt.yscale("log")
plt.ylim(1e-6, 1e3)

plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
plt.gcf().autofmt_xdate()

plt.title("Net Profit by Date (3-day Rolling Median)")
plt.xlabel("Date")
plt.ylabel("Net Profit (Profit - 1, log scale)")
plt.legend()
plt.grid(True)

plt.savefig("net_profit.jpg", format='jpg', bbox_inches='tight', dpi=300)
plt.close()
