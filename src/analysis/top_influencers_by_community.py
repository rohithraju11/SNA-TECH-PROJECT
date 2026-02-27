import pickle
import pandas as pd
from collections import Counter

print("Loading community partition...")
with open("data/processed/community_partition.pkl", "rb") as f:
    partition = pickle.load(f)

print("Loading influencer ranking...")
df_influence = pd.read_csv("data/processed/influencer_ranking.csv")

# Add community info
df_influence["community"] = df_influence["user_id"].map(partition)

# Count community sizes
community_sizes = Counter(partition.values())

# Focus on top 10 largest communities
largest_communities = [c for c, _ in community_sizes.most_common(10)]

print("\nTop Influencer in Each Major Community:\n")

for community in largest_communities:
    community_df = df_influence[df_influence["community"] == community]
    
    if not community_df.empty:
        top_user = community_df.iloc[0]
        print(f"Community {community} (Size: {community_sizes[community]})")
        print(f"Top Influencer: {top_user['user_id']}")
        print(f"Influence Score: {round(top_user['influence_score'], 5)}")
        print("-" * 40)