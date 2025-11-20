from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import os
import requests

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "content_model.pkl")

# Direct Google Drive download link
MODEL_URL = "https://drive.google.com/uc?export=download&id=1PiQZV4Ua6_1Jm71xbd3iWzqi8jzupASP"

# -----------------------
# DOWNLOAD MODEL IF MISSING
# -----------------------
if not os.path.exists(MODEL_PATH):
    print("Model NOT found! Downloading from Google Drive...")
    os.makedirs(MODEL_DIR, exist_ok=True)

    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(response.content)

    print("Model downloaded successfully!")

# -----------------------
# LOAD MODEL
# -----------------------
print("Loading model...")
with open(MODEL_PATH, "rb") as f:
    data = pickle.load(f)

movies = data["movies"]
similarity = data["similarity"]

movies = movies.reset_index(drop=True)
titles = movies["title"].values

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/movies")
def get_movies():
    return jsonify(list(titles))

@app.route("/recommend")
def recommend():
    movie = request.args.get("movie", "").strip().lower()

    matches = movies[movies["title"].str.lower() == movie]

    if matches.empty:
        return jsonify({"error": "Movie not found", "recommendations": []}), 404

    index = matches.index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:11]

    recommendations = [{
        "title": movies.iloc[i]["title"],
        "score": float(score)
    } for i, score in movie_list]

    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
