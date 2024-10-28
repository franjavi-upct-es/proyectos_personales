from flask import Flask, jsonify, request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Cargar el dataset de MovieLens
movies_df = pd.read_csv('../data/ml-100k/u.item', sep='|', encoding='ISO-8859-1', header=None)
ratings_df = pd.read_csv('../data/ml-100k/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])

# Preprocesamiento de datos
movies_df.columns = ['movie_id', 'title', 'release_date', 'video_release_date', 'IMDb_url',
                     'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
                     'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
                     'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

merged_df = pd.merge(ratings_df, movies_df[['movie_id', 'title']], on='movie_id')
user_movie_matrix = merged_df.pivot_table(index='user_id', columns='title', values='rating')
user_movie_matrix.fillna(0, inplace=True)
movie_similarity = cosine_similarity(user_movie_matrix.T)
movie_similarity_df = pd.DataFrame(movie_similarity, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)


# Endpoint de recomendaciones
@app.route('/recommend', methods=['GET'])
def recommend():
    movie_title = request.args.get('movie')
    num_recommendations = int(request.args.get('num', 5))

    # Verificar si la película está en el DataFrame de similitud
    if movie_title not in movie_similarity_df.columns:
        return jsonify({'error': 'Movie not found'}), 404

    # Obtener y ordenar por similitud
    similar_movies = movie_similarity_df[movie_title].sort_values(ascending=False)

    # Filtrar las recomendaciones más similares, excluyendo la película original
    similar_movies = similar_movies.iloc[1:num_recommendations + 1]

    # Devolver recomendaciones en el orden de similitud
    return jsonify(similar_movies.to_dict())


# Endpoint para listar películas
@app.route('/movies', methods=['GET'])
def movies():
    return jsonify(list(movies_df['title']))

if __name__ == '__main__':
    app.run(debug=True)