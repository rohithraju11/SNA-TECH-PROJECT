import pickle
import networkx as nx
import community as community_louvain

print("Loading graph...")

with open("data/processed/user_graph.pkl", "rb") as f:
    G = pickle.load(f)

print("Running Louvain community detection...")

partition = community_louvain.best_partition(G, weight='weight')

# Number of communities
communities = set(partition.values())

print("Total communities detected:", len(communities))

# Compute modularity
modularity = community_louvain.modularity(partition, G, weight='weight')

print("Modularity score:", round(modularity, 4))

# Save partition
with open("data/processed/community_partition.pkl", "wb") as f:
    pickle.dump(partition, f)

print("Community detection completed and saved.")
