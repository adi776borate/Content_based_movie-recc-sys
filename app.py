import streamlit as st
import pickle
import pandas as pd
import requests

movies_data = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_data)
sim = pickle.load(open('sim.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=637815ed1d46d2472aa86e081a0d95b6&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):  
    index = movies.loc[movies['title'] == movie].index[0]
    dist = sim[index]
    movie_list = sorted(list(enumerate(dist)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies =[]
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies.append(movies.iloc[i[0]]['title'])
        #poster fetching
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters



st.title('Movie Recommender System')
selected_name = st.selectbox(
    "Select the movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_name)
    print(posters)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])


