import pandas as pd
import math

# Load your merged forex dataset
df = pd.read_csv("../data/merged_all.csv")  # Adjust path

currency_pairs = df.columns[1:]  # All columns except Timestamp

# Build currency graph for one timestamp
def build_graph(row):
    graph = {}
    for pair in currency_pairs:
        base, quote = pair[:3], pair[3:]
        rate = row[pair]
        if not (math.isnan(rate) or rate == 0):
            graph.setdefault(base, {})[quote] = rate
            graph.setdefault(quote, {})[base] = 1 / rate
    return graph

# Convert rates to log space for arbitrage detection
def graph_to_log(graph):
    return {c: {nbr: -math.log(w) for nbr, w in edges.items()} for c, edges in graph.items()}

# Bellman-Ford algorithm to find negative cycles
def bellman_ford(graph):
    log_graph = graph_to_log(graph)
    nodes = list(log_graph.keys())
    dist = {c: float('inf') for c in nodes}
    pred = {c: None for c in nodes}

    source = nodes[0]
    dist[source] = 0

    for _ in range(len(nodes) - 1):
        for u in log_graph:
            for v, w in log_graph[u].items():
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    pred[v] = u

    for u in log_graph:
        for v, w in log_graph[u].items():
            if dist[u] + w < dist[v]:
                cycle = [v]
                while u not in cycle:
                    cycle.append(u)
                    u = pred[u]
                cycle.append(u)
                cycle.reverse()
                return cycle
    return None

# Process all rows
results = []
for _, row in df.iterrows():
    graph = build_graph(row)
    cycle = bellman_ford(graph)
    
    if cycle:
        profit = 1
        valid = True
        for i in range(len(cycle) - 1):
            a, b = cycle[i], cycle[i + 1]
            if b in graph.get(a, {}):
                rate = graph[a][b]
            elif a in graph.get(b, {}):
                rate = 1 / graph[b][a]
            else:
                valid = False
                break
            profit *= rate
        
        if valid and profit > 1.00001:  # Only consider meaningful arbitrage
            results.append({
                "timestamp": row["Timestamp"],
                "cycle": "/".join(cycle),
                "profit": profit
            })

# Final DataFrame, sorted by timestamp
results_df = pd.DataFrame(results)
results_df["timestamp"] = pd.to_datetime(results_df["timestamp"])
results_df = results_df.sort_values(by="timestamp")

# Save and preview
results_df.to_csv("../data/bellman_output.csv", index=False)
print(results_df.head(10))
