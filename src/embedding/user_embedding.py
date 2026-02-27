import pandas as pd
import pickle
import numpy as np

print("Loading cleaned dataset...")
df = pd.read_csv("data/processed/clean_data.csv")

print("Loading TF-IDF matrix...")
with open("data/processed/tfidf_matrix.pkl", "rb") as f:
    tfidf_matrix = pickle.load(f)

print("Creating user embeddings...")

user_vectors = {}

# Get unique users
unique_users = df["user_id"].unique()

for user in unique_users:
    
    # Get indices of rows for this user
    user_indices = df[df["user_id"] == user].index.tolist()
    
    if len(user_indices) == 0:
        continue

    # Get TF-IDF vectors for this user's posts
    user_tfidf = tfidf_matrix[user_indices].toarray()

    # Get upvotes for weighting
    user_upvotes = df.loc[user_indices, "upvotes"].values

    # Compute weights using log scaling
    weights = np.log1p(user_upvotes)

    # Replace zero weights with 1 (avoid zero division)
    weights[weights == 0] = 1

    # Safety check
    if weights.sum() == 0:
        weights = np.ones(len(weights))

    # Compute weighted average vector
    weighted_avg = np.average(user_tfidf, axis=0, weights=weights)

    # Store user vector
    user_vectors[user] = weighted_avg

print("Total users:", len(user_vectors))

# Save user vectors
with open("data/processed/user_vectors.pkl", "wb") as f:
    pickle.dump(user_vectors, f)

print("User embeddings saved successfully.")