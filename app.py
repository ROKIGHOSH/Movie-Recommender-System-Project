import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_posters(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7fa674895c673b9261e2f1b7c55237b3"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    else:
        return "https://via.placeholder.com/500"  
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']  
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_posters.append(fetch_posters(movie_id))
    
    return recommended_movies, recommended_posters

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Choose a movie name:',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movies, recommended_posters = recommend(selected_movie_name)
    columns = st.columns(5)  # Create 5 columns for layout
    for col, movie, poster in zip(columns, recommended_movies, recommended_posters):
        with col:
            st.text(movie)
            st.image(poster)
