
# Anime Recommender System 

This Streamlit-based Anime Recommender System utilizes the anime.csv dataset to offer anime recommendations either by anime name or genre. It preprocesses the data by cleaning and vectorizing genres for cosine similarity calculations. Users can input an anime name to get recommendations based on similarity scores, or specify a genre to receive top recommendations. The interface provides user-friendly inputs and outputs through Streamlit's interactive components, ensuring easy navigation and clear presentation of results.

- Features
By Anime Name: Enter the name of an anime to get recommendations based on similarity.
By Genre: Enter a genre to get recommendations based on anime genres.

- Requirements
Python 3.x
Streamlit (pip install streamlit)
pandas (pip install pandas)
scikit-learn (pip install scikit-learn)

- Notes
Ensure the anime names in your input match the Japanese names used in the dataset.
The system uses cosine similarity on anime genres for recommendations.
Adjust the similarity cutoff (cutoff=0.2 in difflib.get_close_matches) as needed for anime name suggestions.tor-python)
