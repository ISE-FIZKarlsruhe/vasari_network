import csv
import re
from pyvis.network import Network
import glob

for file_name in glob.glob(".../results/pmi_tables/*.csv"):
    with open(file_name, "r", encoding="utf-8") as f:
        result_data=list(csv.DictReader(f))
        file_num = re.match(r".*?(\d+).*?", file_name).group(1)
    net = Network()
    list_of_names=[]
    for row in result_data:
        list_of_names.append(row["x"])
        list_of_names.append(row["y"])
    unique_names=list(set(list_of_names))
    net.add_nodes(unique_names)
    for row in result_data:
        net.add_edge(row["x"], row["y"], weight=row["pmi_yx"])
    net.show('.../results/networks/network'+file_num+'.html', notebook=False)