from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches


app = Flask(__name__)
CORS(
    app,
    resources={r"/recommend": {"origins": "http://localhost:5173"}},
    methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"]
)

# Load ML assets
books, tfidf, tfidf_matrix = pickle.load(open("../model/model.pkl", "rb"))
TITLE_COL = books.columns[0]

def recommend(book_title, n=5):
    matches = books.index[books[TITLE_COL] == book_title]
    if len(matches) == 0:
        return []

    idx = matches[0]

    similarity_scores = cosine_similarity(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()

    similar_indices = similarity_scores.argsort()[::-1][1:n+1]

    return books.iloc[similar_indices][TITLE_COL].tolist()

@app.route("/recommend", methods=["POST", "OPTIONS"])
def get_recommendations():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.json
    book_name = data.get("book", "").strip()

    if book_name not in books["Book-Title"].values:
        matches = get_close_matches(
            book_name,
            books["Book-Title"].values,
            n=1,
            cutoff=0.6
        )

        if not matches:
            return jsonify({"recommendations": []})

        book_name = matches[0]

    recommendations = recommend(book_name)
    return jsonify({"recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)
