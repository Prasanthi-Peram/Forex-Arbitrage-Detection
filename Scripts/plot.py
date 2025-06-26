import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

merged_df = pd.read_csv("../data/merged_all.csv")
merged_df["Timestamp"] = pd.to_datetime(merged_df["Timestamp"])

target_time = "2025-05-01 00:16:00"
row = merged_df[merged_df["Timestamp"] == target_time]

if not row.empty:
    row = row.iloc[0]
    G = nx.DiGraph()
    for col in merged_df.columns:
        if col != "Timestamp":
            rate = row[col]
            if not pd.isna(rate) and len(col) == 6:
                base, quote = col[:3], col[3:]
                G.add_edge(base, quote, weight=rate)

    pos = nx.circular_layout(G)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1500)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, edgelist=edges, arrowsize=20)
    edge_labels = {(u, v): f"{d['weight']:.4f}" for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=10)
    plt.title(f"Forex Graph at {target_time}", fontsize=15)
    plt.axis('off')
    plt.savefig("graph.jpg", format='jpg', bbox_inches='tight', dpi=300)
    plt.close()
