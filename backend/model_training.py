import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import ast

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIE_PATH = os.path.join(BASE_DIR, "model", "tmdb_5000_movies.csv")
CREDITS_PATH = os.path.join(BASE_DIR, "model", "tmdb_5000_credits.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "content_model.pkl")

print("Loading datasets...")
movies = pd.read_csv(MOVIE_PATH)
credits = pd.read_csv(CREDITS_PATH)

print("Merging...")
movies = movies.merge(credits, on='title')

movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

def convert_names(x):
    L = []
    for i in ast.literal_eval(x):
        L.append(i['name'])
    return L

def get_director(x):
    L = []
    for i in ast.literal_eval(x):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

movies['genres'] = movies['genres'].apply(convert_names)
movies['keywords'] = movies['keywords'].apply(convert_names)
movies['cast'] = movies['cast'].apply(lambda x: convert_names(x)[:5])
movies['crew'] = movies['crew'].apply(get_director)

movies['overview'] = movies['overview'].fillna("").apply(lambda x: x.split())

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

print("Vectorizing...")
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

print("Computing similarity...")
similarity = cosine_similarity(vectors)

data = {
    "movies": movies,
    "similarity": similarity
}

with open(MODEL_PATH, "wb") as f:
    pickle.dump(data, f)

print("✔ Model saved at:", MODEL_PATH)
