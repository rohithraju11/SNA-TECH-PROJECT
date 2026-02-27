import pickle
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

print("Loading user vectors...")

with open("data/processed/user_vectors.pkl", "rb") as f:
    user_vectors = pickle.load(f)

user_ids = list(user_vectors.keys())
user_matrix = np.array(list(user_vectors.values()))

print("Computing cosine similarity matrix...")
similarity_matrix = cosine_similarity(user_matrix)

print("Building user graph...")

G = nx.Graph()

# Add nodes
for user in user_ids:
    G.add_node(user)

# Similarity threshold
threshold = 0.25  # You can tune later

edge_count = 0

for i in range(len(user_ids)):
    for j in range(i + 1, len(user_ids)):
        sim = similarity_matrix[i][j]
        
        if sim > threshold:
            G.add_edge(user_ids[i], user_ids[j], weight=float(sim))
            edge_count += 1

print("Graph built successfully.")
print("Total nodes:", G.number_of_nodes())
print("Total edges:", edge_count)

# Save graph
with open("data/processed/user_graph.pkl", "wb") as f:
    pickle.dump(G, f)

print("Graph saved successfully.")