import pandas as pd
import math

class ForexArbitrage:
    def __init__(self, currencies):
        self.currencies = currencies
        self.graph = {cur: {} for cur in currencies}

    def update(self, base, quote, rate):
        if rate and rate != 0 and not math.isnan(rate):
            self.graph[base][quote] = -math.log(rate)
            self.graph[quote][base] = -math.log(1 / rate)

    def is_arbitrage_possible(self):
        dist = {cur: float('inf') for cur in self.currencies}
        pred = {cur: None for cur in self.currencies}
        source = self.currencies[0]
        dist[source] = 0

        for _ in range(len(self.currencies) - 1):
            for u in self.graph:
                for v, w in self.graph[u].items():
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        pred[v] = u

        for u in self.graph:
            for v, w in self.graph[u].items():
                if dist[u] + w < dist[v]:
                    return True
        return False

    def find_arbitrage_opportunity(self):
        dist = {cur: float('inf') for cur in self.currencies}
        pred = {cur: None for cur in self.currencies}
        source = self.currencies[0]
        dist[source] = 0

        for _ in range(len(self.currencies) - 1):
            for u in self.graph:
                for v, w in self.graph[u].items():
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        pred[v] = u

        for u in self.graph:
            for v, w in self.graph[u].items():
                if dist[u] + w < dist[v]:
                    cycle = [v]
                    visited = set()
                    while u not in visited:
                        visited.add(u)
                        cycle.append(u)
                        u = pred[u]
                        if u is None:
                            return None, None
                    cycle.append(u)
                    cycle = cycle[cycle.index(u):]
                    cycle.reverse()

                    profit = 1
                    valid = True
                    for i in range(len(cycle) - 1):
                        a, b = cycle[i], cycle[i + 1]
                        if b in self.graph.get(a, {}):
                            rate = math.exp(-self.graph[a][b])
                        elif a in self.graph.get(b, {}):
                            rate = 1 / math.exp(-self.graph[b][a])
                        else:
                            valid = False
                            break
                        profit *= rate

                    if valid and profit > 1.00001:
                        return cycle, profit
        return None, None




# Load forex data
df = pd.read_csv("../data/merged_all.csv")  # Adjust path if needed
currency_pairs = df.columns[1:]  # Skip timestamp

results = []

for _, row in df.iterrows():
    currencies = set()
    for pair in currency_pairs:
        currencies.add(pair[:3])
        currencies.add(pair[3:])
    currencies = list(currencies)

    forex = ForexArbitrage(currencies)

    for pair in currency_pairs:
        base, quote = pair[:3], pair[3:]
        rate = row[pair]
        forex.update(base, quote, rate)

    cycle, profit = forex.find_arbitrage_opportunity()

    if cycle:
        results.append({
            "timestamp": row["Timestamp"],
            "cycle": "/".join(cycle),
            "profit": profit
        })

# Save results
results_df = pd.DataFrame(results)
results_df["timestamp"] = pd.to_datetime(results_df["timestamp"])
results_df = results_df.sort_values(by="timestamp")
results_df.to_csv("../data/bellman_output.csv", index=False)

