import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=2f9cbfa773d73187f02651cc5f1ef529&language=en-US')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
                            

movies_dict= pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6] #Check below cell for o/p
    
    recommended_movie=[]
    recommended_movie_poster=[]
    for i in movies_list:
       movie_id = movies.iloc[i[0]].movie_id     #To fetch the poster using id
       #fetch poster from API
#         print(i[0])  #So this will return index but we want name of movie check below o/p
       recommended_movie_poster.append(fetch_poster(movie_id))
       recommended_movie.append(movies.iloc[i[0]].title)
    return recommended_movie,recommended_movie_poster

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'Please select movie for suggestions',
movies['title'].values)

if st.button('Recommend Movies'):
    names , poster = recommend(selected_movie_name)
    col1, col2, col3, col4 , col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])
