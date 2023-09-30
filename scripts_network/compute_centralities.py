import networkx as nx
import matplotlib.pyplot as plt
import csv
import glob
import sys
import re


maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def main():
    for file_name in glob.glob("../results/pmi_tables/*.csv"):
        with open(file_name, "r") as f:
            data = list(csv.DictReader(f))
            file_num = re.match(r".*?(\d+).*?", file_name).group(1)

        pmi_values = [float(row["pmi_yx"]) for row in data]
        avg_pmi = sum(pmi_values)/len(pmi_values)

        G = nx.Graph()
        for row in data:
            if float(row["pmi_yx"])>=1:
                G.add_edge(row["x"], row["y"], weight=float(row["pmi_yx"]))

        with open("../results/centralities/"+file_num+".txt", "w") as f:
            centrality_dict=G.degree()
            sorted_centralities = sorted(centrality_dict, key=lambda tup: tup[1])[::-1]
            f.write("\nDegree Centrality Ranks: \n")
            for n in range(10):
                f.write(str(n+1)+ ": "+sorted_centralities[n][0] + " score: "+ str(sorted_centralities[n][1])+"\n")
            betweenness_centrality = nx.betweenness_centrality(G)
            sorted_centralities= sorted(betweenness_centrality.items(), key=lambda tup: tup[1])[::-1]
            f.write("\nBetweenness Centrality Ranks: \n")
            for n in range(10):
                f.write(str(n+1)+ ": "+sorted_centralities[n][0] + " score: "+ str(sorted_centralities[n][1])+"\n")
            eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=600)
            sorted_centralities= sorted(eigenvector_centrality.items(), key=lambda tup: tup[1])[::-1]
            f.write("\nEigenvector Centrality Ranks: \n")
            for n in range(10):
                f.write(str(n+1)+ ": "+sorted_centralities[n][0] + " score: "+ str(sorted_centralities[n][1])+"\n")
        
main()