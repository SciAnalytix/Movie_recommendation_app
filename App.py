import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Function to download the similarity.pkl file from Google Drive
def download_similarity_file():
    url = "https://drive.google.com/uc?id=15B5i0wsuL2fDDWhCZeZgQb5pn1Z7zguO"
    output_file = "similarity.pkl"
    
    if not os.path.exists(output_file):
        response = requests.get(url)
        with open(output_file, 'wb') as f:
            f.write(response.content)

# Download similarity.pkl if not exists
download_similarity_file()

# Load the data
movies = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))  

# Streamlit app UI
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

st.markdown('<div class="title">🎥 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Find your next favorite movie!</div>', unsafe_allow_html=True)

movie_list = movies['title'].values
selected_movie = st.selectbox("Choose a movie you like", movie_list)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_movies = [movies.iloc[i[0]].title for i in movie_list]
    return recommended_movies

if st.button("🎯 Recommend"):
    recommendations = recommend(selected_movie)
    st.subheader("📌 Recommended Movies:")
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f'<div class="movie-box">{i}. {rec}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("Made with ❤️ by Prakhar Sharma")
