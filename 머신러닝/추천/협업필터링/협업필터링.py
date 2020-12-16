import pandas as pd

rating_data = pd.read_csv('./ratings.csv')
movie_data = pd.read_csv('./movies.csv')
# print(movie_data.head())
# print(rating_data.head())
# print(movie_data.shape)
# print(rating_data.shape)
rating_data.drop('timestamp', axis=1, inplace=True)
movie_data.drop('genres', axis=1, inplace=True)
user_movie_data = pd.merge(rating_data, movie_data, on='movieId')
# print(user_movie_data.head())
# print(user_movie_data.shape)
user_movie_rating = user_movie_data.pivot_table(
    'rating', index='userId', columns='title').fillna(0)

movie_user_rating = user_movie_rating.values.T
print(user_movie_rating.shape)
print(movie_user_rating.shape)
