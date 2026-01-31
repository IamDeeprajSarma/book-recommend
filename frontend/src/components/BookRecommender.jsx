import { useState } from "react";

function BookRecommender() {
  const [book, setBook] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  const getRecommendations = async () => {
    const res = await fetch("http://127.0.0.1:5000/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ book }),
    });

    const data = await res.json();
    setRecommendations(data.recommendations || []);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>📚 Book Recommendation System</h1>

      <input
        type="text"
        placeholder="Enter a book name"
        value={book}
        onChange={(e) => setBook(e.target.value)}
      />

      <button onClick={getRecommendations}>Recommend</button>

      <ul>
        {recommendations.map((b, i) => (
          <li key={i}>{b}</li>
        ))}
      </ul>
    </div>
  );
}

export default BookRecommender;
