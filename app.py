import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

anime_data = pd.read_csv('anime.csv')

anime_data['genre'] = anime_data['genre'].fillna('')
anime_data['name'] = anime_data['name'].str.lower().str.replace(' ', '')

count_vectorizer = CountVectorizer(stop_words='english')
count_matrix = count_vectorizer.fit_transform(anime_data['genre'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)

# Function to get recommendations based on anime name
def get_recommendations(anime_name, cosine_sim=cosine_sim):
    anime_name = anime_name.lower().replace(' ', '')
    try:
        idx = anime_data[anime_data['name'] == anime_name].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:]
        recommendations = []
        for score in sim_scores:
            if anime_name not in anime_data['name'].iloc[score[0]]:
                recommendations.append(score)
            if len(recommendations) == 5:
                break
        anime_indices = [i[0] for i in recommendations]
        return anime_data[['name', 'genre', 'rating']].iloc[anime_indices]
    except IndexError:
        return pd.DataFrame(columns=['name', 'genre', 'rating'])

# Function to get recommendations based on genre
def get_recommendations_by_genre(genre, cosine_sim=cosine_sim):
    filtered_anime = anime_data[anime_data['genre'].str.contains(genre, case=False, na=False)]
    filtered_indices = filtered_anime.index
    sim_scores = cosine_sim[filtered_indices]
    mean_sim_scores = sim_scores.mean(axis=0)
    sorted_indices = mean_sim_scores.argsort()[::-1]
    return anime_data[['name', 'genre', 'rating']].iloc[sorted_indices[:5]]

# Streamlit interface
st.title('Anime Recommender System')
st.markdown("""
    Welcome to the Anime Recommender System! You can get recommendations based on your favorite anime or genre.
    Simply select your preferred method and input the required details to get started.
    Please ensure to put only Japanese name of the anime in Search box.
""")

option = st.selectbox('Choose your recommendation method:', ('By Anime Name', 'By Genre'))

if option == 'By Anime Name':
    anime_name_input = st.text_input('Enter the name of an anime:')
    if anime_name_input:
        suggestions = difflib.get_close_matches(anime_name_input.lower().replace(' ', ''), anime_data['name'], n=5, cutoff=0.2)
        if suggestions:
            anime_name = st.selectbox('Did you mean:', suggestions)
            if anime_name:
                recommendations = get_recommendations(anime_name)
                if not recommendations.empty:
                    st.write('Top 5 recommendations based on the anime you provided:')
                    st.write(recommendations)
                else:
                    st.write('Anime not found. Please check the name and try again.')
        else:
            st.write('No similar anime found. Please check the name and try again.')
else:
    genre = st.text_input('Enter a genre:')
    if genre:
        recommendations_by_genre = get_recommendations_by_genre(genre)
        if not recommendations_by_genre.empty:
            st.write('Top 5 recommendations based on the genre you provided:')
            st.write(recommendations_by_genre)
        else:
            st.write('No animes found for the given genre. Please check the genre and try again.')

st.markdown("""
    by anmera
""")