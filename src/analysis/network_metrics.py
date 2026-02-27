import pickle
import networkx as nx

print("Loading graph...")

with open("data/processed/user_graph.pkl", "rb") as f:
    G = pickle.load(f)

print("Computing network metrics...")

density = nx.density(G)
avg_clustering = nx.average_clustering(G)
components = nx.number_connected_components(G)

print("Total Nodes:", G.number_of_nodes())
print("Total Edges:", G.number_of_edges())
print("Graph Density:", round(density, 6))
print("Average Clustering Coefficient:", round(avg_clustering, 4))
print("Connected Components:", components)
