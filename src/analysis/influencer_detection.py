import pickle
import networkx as nx
import pandas as pd

print("Loading graph...")

with open("data/processed/user_graph.pkl", "rb") as f:
    G = pickle.load(f)

print("Calculating centrality measures...")

degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
pagerank = nx.pagerank(G, weight='weight')

print("Combining influence scores...")

influence_data = []

for node in G.nodes():
    influence_score = (
        0.4 * pagerank[node] +
        0.3 * betweenness_centrality[node] +
        0.3 * degree_centrality[node]
    )
    
    influence_data.append({
        "user_id": node,
        "degree": degree_centrality[node],
        "betweenness": betweenness_centrality[node],
        "pagerank": pagerank[node],
        "influence_score": influence_score
    })

df_influence = pd.DataFrame(influence_data)

df_influence = df_influence.sort_values(
    by="influence_score",
    ascending=False
)

df_influence.to_csv(
    "data/processed/influencer_ranking.csv",
    index=False
)

print("Top 10 Influencers:")
print(df_influence.head(10))

print("Influencer ranking saved successfully.")