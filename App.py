import streamlit as st
import pickle
import os
import requests

# Load the movies data (already in repo)
movies = pickle.load(open('df.pkl', 'rb'))

# Handle similarity.pkl from Google Drive
file_id = "15B5i0wsuL2fDDWhCZeZgQb5pn1Z7zguO"
download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
filename = "similarity.pkl"

if not os.path.exists(filename):
    with st.spinner("Downloading similarity.pkl from Google Drive..."):
        response = requests.get(download_url)
        with open(filename, "wb") as f:
            f.write(response.content)
        st.success("similarity.pkl downloaded successfully!")

# Load the similarity matrix
similarity = pickle.load(open(filename, 'rb'))

# Set page config
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")

# Custom styling
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

# Title
st.markdown('<div class="title">🎥 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Find your next favorite movie!</div>', unsafe_allow_html=True)

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("Choose a movie you like", movie_list)

# Recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_movies = [movies.iloc[i[0]].title for i in movie_list]
    return recommended_movies

# Button to trigger recommendation
if st.button("
