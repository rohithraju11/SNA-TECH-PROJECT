import pickle
import networkx as nx
import matplotlib.pyplot as plt
import random

print("Loading graph...")
with open("data/processed/user_graph.pkl", "rb") as f:
    G = pickle.load(f)

print("Loading community partition...")
with open("data/processed/community_partition.pkl", "rb") as f:
    partition = pickle.load(f)

print("Selecting largest connected component...")

# Get largest connected component
largest_cc = max(nx.connected_components(G), key=len)
G_sub = G.subgraph(largest_cc).copy()

print("Nodes in largest component:", G_sub.number_of_nodes())

# Assign colors to communities
communities = list(set(partition.values()))
color_map = {}

for community in communities:
    color_map[community] = (random.random(), random.random(), random.random())

node_colors = [
    color_map[partition[node]] if node in partition else (0.5,0.5,0.5)
    for node in G_sub.nodes()
]

print("Drawing graph...")

plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G_sub, k=0.15, iterations=20)

nx.draw_networkx_nodes(
    G_sub,
    pos,
    node_color=node_colors,
    node_size=30,
    alpha=0.8
)

nx.draw_networkx_edges(
    G_sub,
    pos,
    alpha=0.2
)

plt.title("Technology Community Network (Largest Component)")
plt.axis("off")

plt.savefig("data/processed/community_network.png", dpi=300)
plt.show()

print("Visualization saved as community_network.png")