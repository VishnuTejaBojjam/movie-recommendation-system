// Backend API - ALWAYS use Render backend online
const API_BASE = 'https://movie-backend-844x.onrender.com';

// Your TMDB API Key
const TMDB_KEY = "a30becae90c7150eaf2276b2846ad2b0";

// ---------------------------------------------
// Load movie list from BACKEND → <datalist>
// ---------------------------------------------
async function fetchMovies() {
    const datalist = document.getElementById("moviesList");
    datalist.innerHTML = "<option>Loading movies...</option>";

    try {
        const res = await fetch(`${API_BASE}/movies`);
        const movies = await res.json();
        datalist.innerHTML = "";

        movies.forEach(title => {
            let op = document.createElement("option");
            op.value = title;
            datalist.appendChild(op);
        });

    } catch (err) {
        datalist.innerHTML = "<option>Error loading movies</option>";
    }
}

// ---------------------------------------------
// Fetch POSTER from TMDB
// ---------------------------------------------
async function getPoster(title) {
    try {
        const url = `https://api.themoviedb.org/3/search/movie?api_key=${TMDB_KEY}&query=${encodeURIComponent(title)}`;
        const response = await fetch(url);
        const data = await response.json();

        if (data.results?.length > 0 && data.results[0].poster_path) {
            return "https://image.tmdb.org/t/p/w500" + data.results[0].poster_path;
        }
    } catch { }

    return "https://via.placeholder.com/200x300?text=No+Image";
}

// ---------------------------------------------
// Get recommendations from backend & display cards
// ---------------------------------------------
async function getRecommendations() {
    const q = document.getElementById("movieInput").value.trim();
    const results = document.getElementById("results");

    if (!q) {
        alert("Please type a movie name.");
        return;
    }

    results.innerHTML = "<p style='color:#ccc;'>Loading...</p>";

    try {
        const res = await fetch(`${API_BASE}/recommend?movie=${encodeURIComponent(q)}`);

        if (!res.ok) {
            results.innerHTML = "<p style='color:red;'>Movie not found</p>";
            return;
        }

        const data = await res.json();
        results.innerHTML = "";  // clear

        for (let m of data) {
            const poster = await getPoster(m.title);

            let card = document.createElement("div");
            card.className = "movie-card";

            card.innerHTML = `
                <img class="poster" src="${poster}">
                <h4>${m.title}</h4>
                <p>Score: ${m.score.toFixed(3)}</p>
            `;

            results.appendChild(card);
        }

    } catch (err) {
        results.innerHTML = "<p style='color:red;'>Backend not reachable.</p>";
    }
}

// EVENT LISTENER
document.getElementById("findBtn").addEventListener("click", getRecommendations);

// Load movies when page loads
fetchMovies();
