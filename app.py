import pickle
import streamlit as st
import requests
import gdown
import os

# ================== GOOGLE DRIVE FILE IDs ==================
# 🔴 YAHAN movies.pkl KA FILE ID DALO
MOVIES_FILE_ID = "1lbWg0zsgHHIzQ0SSUO-FP648wjwXFWvb"

# 🔴 YAHAN similarity.pkl KA FILE ID DALO
SIMILARITY_FILE_ID = "1aLL459Glq4ZYYu93QjcW7M_vwJC0Ee5Q"

# Download movies.pkl if not exists
if not os.path.exists("movies.pkl"):
    gdown.download(f"https://drive.google.com/uc?id={MOVIES_FILE_ID}", "movies.pkl", quiet=False)

# Download similarity.pkl if not exists
if not os.path.exists("similarity.pkl"):
    gdown.download(f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}", "similarity.pkl", quiet=False)


# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="FlixMind | AI Movie Magic",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================== ADVANCED NEON-NETFLIX CSS ==================
st.markdown("""
<style>
/* Pure Black Background */
.stApp {
    background-color: #000000;
}

/* Custom Font Import */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@300;700&display=swap');

/* ---------- LOGO SECTION ---------- */
.logo-container {
    text-align: center;
    padding: 20px 0px;
}

.main-logo {
    font-family: 'Bebas Neue', cursive;
    font-size: 90px;
    color: #E50914;
    text-shadow: 0px 0px 15px rgba(229, 9, 20, 0.4);
    letter-spacing: 4px;
    margin-bottom: -10px;
}

.tagline {
    font-family: 'Roboto', sans-serif;
    color: #8c8c8c;
    font-size: 18px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* ---------- SEARCH BOX ---------- */
div[data-baseweb="select"] > div {
    background-color: #1a1a1a !important;
    border: 1px solid #333 !important;
    border-radius: 4px !important;
    height: 50px !important;
}

div[data-baseweb="select"] input {
    color: #ffffff !important;
    font-size: 18px !important;
}

div[data-baseweb="select"] div[aria-selected="true"] {
    color: #ffffff !important;
}

div[role="listbox"] {
    background-color: #1a1a1a !important;
}

div[role="option"] {
    color: white !important;
    transition: 0.2s;
}

div[role="option"]:hover {
    background-color: #E50914 !important;
}

/* ---------- BUTTON ---------- */
.stButton > button {
    background-color: #E50914;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 12px 20px;
    font-size: 20px;
    font-weight: bold;
    font-family: 'Roboto', sans-serif;
    width: 100%;
    box-shadow: 0 4px 15px rgba(229, 9, 20, 0.3);
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #ff0a16;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(229, 9, 20, 0.5);
    color: white;
}

/* ---------- MOVIE CARD ---------- */
.movie-card-container {
    background: #141414;
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.4s;
    cursor: pointer;
    border: 1px solid #222;
}

.movie-card-container:hover {
    transform: scale(1.08);
    border: 1px solid #E50914;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.8);
    z-index: 99;
}

.movie-title-text {
    padding: 10px;
    font-size: 14px;
    font-weight: 700;
    color: #e5e5e5;
    text-align: center;
    font-family: 'Roboto', sans-serif;
}

.section-header {
    font-family: 'Roboto', sans-serif;
    font-size: 26px;
    color: #ffffff;
    border-left: 5px solid #E50914;
    padding-left: 15px;
    margin: 40px 0 20px 0;
}

</style>
""", unsafe_allow_html=True)


# ================== LOAD DATA ==================
@st.cache_data
def load_data():
    movies = pickle.load(open("movies.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity


movies, similarity = load_data()


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8"
        data = requests.get(url, timeout=5).json()
        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    except:
        pass
    return "https://via.placeholder.com/500x750/141414/FFFFFF?text=Poster+Unavailable"


def recommend(movie_title):
    idx = movies[movies["title"] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])[1:7]

    names, posters = [], []
    for i in distances:
        movie_id = movies.iloc[i[0]].id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return names, posters


# ================== UI ==================
st.markdown("""
<div class="logo-container">
    <div class="main-logo">FLIXMIND</div>
    <div class="tagline">Your Personal AI Cinema Scout</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie = st.selectbox(
        "What's on your mind?",
        movies['title'].values,
        index=None,
        placeholder="Type a movie you love...",
        label_visibility="collapsed"
    )
    btn = st.button("DISCOVER MOVIES")

if btn and selected_movie:
    names, posters = recommend(selected_movie)

    st.markdown(f'<div class="section-header">Based on your interest in "{selected_movie}"</div>',
                unsafe_allow_html=True)

    cols = st.columns(6)
    for i in range(len(names)):
        with cols[i]:
            st.markdown(f"""
            <div class="movie-card-container">
                <img src="{posters[i]}" style="width:100%">
                <div class="movie-title-text">{names[i]}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)
https://drive.google.com/file/d//view?usp=drive_link