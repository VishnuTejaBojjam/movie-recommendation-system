# Movie Recommendation System

This repository contains a Flask-based ML backend and a simple frontend. This `README` adds instructions to run a Node.js server that serves the `frontend/` folder and proxies API calls to the Flask backend.

## Local setup

1. Ensure Python and Node.js are installed.

2. Python backend

- Create and activate a venv and install requirements:

```powershell
cd backend
python -m venv venv; .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- Start the Flask backend (default: runs on port 5000):

```powershell
python app.py
```

3. Node server (serves static frontend and proxies API)

- Install Node packages:

```powershell
cd ..  # go back to repo root
npm install
```

- Start the Node server and open `http://localhost:3000` in your browser:

```powershell
npm start
```

The Node server will proxy `/movies` and `/recommend` to the Flask backend running at `http://127.0.0.1:5000` by default. You can change the backend URL by setting the `BACKEND_URL` environment variable before starting the server.

## GitHub instructions

1. Initialize a git repository (if not already done):

```powershell
git init
```

2. Create a GitHub repo and add it as remote (replace URL if different):

```powershell
git remote add origin https://github.com/VishnuTejaBojjam/movie-recommendation-system.git
```

3. Stage, commit, and push:

```powershell
git add .
git commit -m "Add Node server to serve frontend and proxy to Flask backend"
git branch -M main
git push -u origin main
```

Note: If you hit a locked index error, delete `.git/index.lock` and try again.
