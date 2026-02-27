import pandas as pd
import re
import spacy
from bs4 import BeautifulSoup

print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

print("Loading dataset...")
df = pd.read_csv("data/raw/stack_overflow_raw.csv")

def clean_text(text):
    if pd.isna(text):
        return ""

    # Remove HTML
    text = BeautifulSoup(text, "html.parser").get_text()

    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove special characters
    text = re.sub(r'[^a-zA-Z ]', ' ', text)

    text = text.lower()

    # Lemmatization
    doc = nlp(text)
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and token.is_alpha and len(token) > 2
    ]

    return " ".join(tokens)

print("Merging title and body...")
df["full_text"] = df["question_title"] + " " + df["question_body"]

print("Cleaning text...")
df["clean_text"] = df["full_text"].apply(clean_text)

# Remove empty rows
df = df[df["clean_text"].str.strip() != ""]

print("Saving cleaned data...")
df.to_csv("data/processed/clean_data.csv", index=False)

print("Cleaning completed.")
print("Final rows:", len(df))
