import streamlit as st
import pickle
import pandas as pd
import requests
import os

# ✅ Function to download from Google Drive (handles large files too)
def download_from_gdrive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)

    # Check for confirmation token (for large files)
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    token = get_confirm_token(response)
    if token:
        response = session.get(URL, params={'id': file_id, 'confirm': token}, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# ✅ Download similarity.pkl from Google Drive only if it doesn't exist
if not os.path.exists("similarity.pkl"):
    download_from_gdrive("15B5i0wsuL2fDDWhCZeZgQb5pn1Z7zguO", "similarity.pkl")

# ✅ Load the data
movies = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ✅ Streamlit UI Setup
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")

st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #FF4B4B;
        }
        .sub {
            text-align: center;
            font-size: 18px;
            color: #777;
            margin-bottom: 30px;
        }
        .movie-box {
            background-color: #f0f2f6;
            padding: 10px 20px;
            border-radius: 10px;
            margin: 10px 0;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Title
st.markdown('<div class="title">🎥 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Find your next favorite movie!</div>', unsafe_allow_html=True)

# ✅ Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox("Choose a movie you like", movie_list)

# ✅ Recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_movies = [movies.iloc[i[0]].title for i in movie_list]
    return recommended_movies

# ✅ Trigger recommendations
if st.button("🎯 Recommend"):
    recommendations = recommend(selected_movie)
    st.subheader("📌 Recommended Movies:")
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f'<div class="movie-box">{i}. {rec}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("Made with ❤️ by Prakhar Sharma")
