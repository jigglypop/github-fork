from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
movies = pd.read_csv('./tmdb_5000_movies.csv')
# print(movies.shape)
# print(movies.head(1))
movies_df = movies[['id', 'title', 'genres', 'vote_average',
                    'vote_count', 'popularity', 'keywords', 'overview']]
pd.set_option('max_colwidth', 100)
# print(movies_df[['genres', 'keywords']][:1])
movies_df['genres'] = movies_df['genres'].apply(literal_eval)
movies_df['keywords'] = movies_df['keywords'].apply(literal_eval)
movies_df['genres'] = movies_df['genres'].apply(
    lambda x: [y['name'] for y in x])
movies_df['keywords'] = movies_df['keywords'].apply(
    lambda x: [y['name'] for y in x])
# print(movies_df[['genres', 'keywords']][:1])

# 장르 유사도 콘텐츠 측정
movies_df['genres_literal'] = movies_df['genres'].apply(
    lambda x: (' ').join(x))
count_vect = CountVectorizer(min_df=0, ngram_range=(1, 2))
genre_mat = count_vect.fit_transform(movies_df['genres_literal'])
# print(genre_mat.shape)

# 코사인 유사도 벡터 생성
genre_sim = cosine_similarity(genre_mat, genre_mat)
# print(genre_sim.shape)
# print(genre_sim[:1])
genre_sim_sorted = genre_sim.argsort()[:, ::-1]


def find_sim_movies(movies_df, genre_sim_sorted, title, top_n=10):
    title_movie = movies_df[movies_df['title'] == title]
    title_index = title_movie.index.values
    similar_indexes = genre_sim_sorted[title_index, :(top_n)]
    print(similar_indexes)
    similar_indexes = similar_indexes.reshape(-1)
    return movies_df.iloc[similar_indexes]


similar_movies = find_sim_movies(
    movies_df, genre_sim_sorted, 'The Godfather', 10)

print(similar_movies[['title', 'vote_average']])
