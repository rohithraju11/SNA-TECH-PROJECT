import pickle
from collections import Counter

print("Loading community partition...")

with open("data/processed/community_partition.pkl", "rb") as f:
    partition = pickle.load(f)

community_counts = Counter(partition.values())

print("Top 10 Largest Communities:")

for community, size in community_counts.most_common(10):
    print(f"Community {community}: {size} users")

print("\nTotal Communities:", len(community_counts))