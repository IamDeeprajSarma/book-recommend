import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Load dataset
books = pd.read_csv("../data/books.csv", low_memory=False)

# Identify correct title column
print(books.columns)

# 👇 adjust if needed
TITLE_COL = "Book-Title"

books = books[[TITLE_COL]].dropna().drop_duplicates()

# TF-IDF
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(books[TITLE_COL])

# Save model
pickle.dump((books, tfidf, tfidf_matrix), open("model.pkl", "wb"))

print("Model rebuilt successfully")
