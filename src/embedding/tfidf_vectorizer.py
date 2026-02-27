import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

print("Loading cleaned dataset...")
df = pd.read_csv("data/processed/clean_data.csv")

print("Creating TF-IDF vectorizer...")

vectorizer = TfidfVectorizer(
    max_features=8000,
    ngram_range=(1,2),
    min_df=3,
    max_df=0.85
)

tfidf_matrix = vectorizer.fit_transform(df["clean_text"])

print("TF-IDF matrix shape:", tfidf_matrix.shape)

# Save TF-IDF matrix
with open("data/processed/tfidf_matrix.pkl", "wb") as f:
    pickle.dump(tfidf_matrix, f)

# Save vectorizer
with open("data/processed/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("TF-IDF vectors saved successfully.")