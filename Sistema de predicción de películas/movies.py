import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Cargar el dataset de MovieLens
movies_df = pd.read_csv('data/ml-100k/u.item', sep='|', encoding='ISO-8859-1', header=None)
ratings_df = pd.read_csv('data/ml-100k/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])

# Agregar nombres de columnas al archivo de películas
movies_df.columns = ['movie_id', 'title', 'release_date', 'video_release_date', 'IMDb_url',
                     'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
                     'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
                     'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

# Mostrar los primeros registros de cada dataset para verificar
print("Movies Data:")
print(movies_df.head())
print("Ratings Data:")
print(ratings_df.head())

# Paso 2: Preprocesamiento de los Datos

# Unir el DataFrame de valoraciones con el DataFrame de películas
merged_df = pd.merge(ratings_df, movies_df[['movie_id', 'title']], on='movie_id')

# Crear una tabla de usuario-pelicula
user_movie_matrix = merged_df.pivot_table(index='user_id', columns='title', values='rating')

# Llenar los valores NaN con 0
user_movie_matrix.fillna(0.0, inplace=True)

# Paso 3: Implementación del Sistema de Recomendación basado en ítems
movie_similarity = cosine_similarity(user_movie_matrix.T) # Transponemos para similitud entre películas
movie_similarity_df = pd.DataFrame(movie_similarity, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)

# Función para recomendar películas similares
def get_movie_recommendations(movie_title, num_recommendations=5):
    # Obtener las puntuaciones de similitud de la película solicitada
    similar_movies = movie_similarity_df[movie_title]

    # Ordenar las películas en orden descendente de similitud
    similar_movies = similar_movies.sort_values(ascending=False)

    # Retornar las películas más similares, excluyendo la misma película
    return similar_movies.iloc[1:num_recommendations + 1]

# Ejemplo de recomendación
movie_to_recommend = "Copycat (1995)"
recommendations = get_movie_recommendations(movie_to_recommend)
print(f"Películas recomendadas para '{movie_to_recommend}':")
print(recommendations)

"""
Explicación del Código:
1.  Unión y Pivot: Unimos las tablas de `ratings` y `movies` y creamos una matriz `user_movie_matrix`, donde cada fila es
    un usuario y cada columna es una película con el valor de la calificación dada.
2.  Similitud coseno: Calculamos la similitud coseno entre las columnas (películas) para obtener una matriz de similitud
    de películas.
3.  Función de Recomendación: Definimos `get_movie_recommendations`, que toma una película y devuelve las más similares 
    según la similitud de puntuación.

"""