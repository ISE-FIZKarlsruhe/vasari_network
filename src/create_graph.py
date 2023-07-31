import networkx as nx
import matplotlib.pyplot as plt
import csv

with open("../data/sorted_pmi_table.csv", "r", encoding="utf-8") as f:
    data = list(csv.DictReader(f))

pmi_values = [float(row["pmi_yx"]) for row in data]
avg_pmi = sum(pmi_values)/len(pmi_values)

G = nx.Graph()
for row in data:
    if float(row["pmi_yx"])>=0:
        G.add_edge(row["x"], row["y"], weight=float(row["pmi_yx"]))

# centrality_dict=G.degree()
# sorted_centralities = sorted(centrality_dict, key=lambda tup: tup[1])[::-1]

# for n in range(10):
#   print(n+1, sorted_centralities[n][0],sorted_centralities[n][1])

# print("\n\n")

# betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
# sorted_centralities= sorted(betweenness_centrality.items(), key=lambda tup: tup[1])[::-1]

# for n in range(10):
#   print(n+1, sorted_centralities[n][0],sorted_centralities[n][1])




# graph_pos = nx.spring_layout(G)
# nx.draw_networkx_nodes(G, graph_pos, node_size=10, node_color='blue', alpha=0.3)
# nx.draw_networkx_edges(G, graph_pos)
# nx.draw_networkx_labels(G, graph_pos, font_size=8, font_family='sans-serif')

# plt.savefig("plot.png", dpi=1000)

nx.write_gexf(G, "../data/tlota-1.gexf")