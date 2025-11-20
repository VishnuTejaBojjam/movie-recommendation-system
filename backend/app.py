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

# Google Drive File ID (NOT the full link)
FILE_ID = "1PiQZV4Ua6_1Jm71xbd3iWzqi8jzupASP"


# ----------------------------------------------------
#  DOWNLOAD LARGE FILE FROM GOOGLE DRIVE (Correct way)
# ----------------------------------------------------
def download_file_from_google_drive(id, destination):
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={"id": id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)


# ----------------------------------------------------
#  DOWNLOAD MODEL IF NOT EXISTS
# ----------------------------------------------------
if not os.path.exists(MODEL_PATH):
    print("⚠ Model not found! Downloading from Google Drive...")
    os.makedirs(MODEL_DIR, exist_ok=True)

    download_file_from_google_drive(FILE_ID, MODEL_PATH)

    print("✅ Model downloaded successfully!")


# ----------------------------------------------------
#  LOAD MODEL
# ----------------------------------------------------
print("📦 Loading model...")
with open(MODEL_PATH, "rb") as f:
    data = pickle.load(f)

movies = data["movies"]
similarity = data["similarity"]

movies = movies.reset_index(drop=True)
titles = movies["title"].values


# ----------------------------------------------------
#  ROUTES
# ----------------------------------------------------
@app.route("/")
def home():
    return "Backend is running successfully!"


@app.route("/movies")
def get_movies():
    return jsonify(list(titles))


@app.route("/recommend")
def recommend():
    movie = request.args.get("movie", "").strip().lower()

    matches = movies[movies["title"].str.lower() == movie]

    if matches.empty:
        return jsonify({"error": "Movie not found"}), 404

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


# ----------------------------------------------------
#  START APP
# ----------------------------------------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

