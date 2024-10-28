import tkinter as tk
from tkinter import ttk, messagebox
import requests

# URL del servidor Flask
BASE_URL = "http://127.0.0.1:5000"

# Función para cargar la lista de películas
def load_movies():
    try:
        response = requests.get(BASE_URL + "/movies")
        response.raise_for_status()
        movies = response.json()
        for movie in movies:
            movie_select_menu['values'] = (*movie_select_menu['values'], movie)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de conexión", f"No se pudo cargar la lista de películas: {e}")

# Función para obtener recomendaciones de películas
def get_recommendations():
    selected_movie = movie_select_menu.get()
    if not selected_movie:
        messagebox.showwarning("Selección de película", "Por favor, selecciona una película")
        return

    try:
        response = requests.get(f"{BASE_URL}/recommend", params={'movie': selected_movie, 'num': 5})
        response.raise_for_status()
        recommendations = response.json()

        # Limpiar la lista de recomendaciones
        recommendations_listbox.delete(0, tk.END)

        # Mostrar las recomendaciones
        for movie, similarity in recommendations.items():
            recommendations_listbox.insert(tk.END, f"{movie} (Similitud: {similarity:.2f})")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de conexión", f"No se pudo obtener recomendaciones: {e}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Recomendador de Películas")
root.geometry("500x500")

# Etiqueta y menú desplegable para seleccionar película
ttk.Label(root, text="Selecciona una película:").pack(pady=10)
movie_select_menu = ttk.Combobox(root)
movie_select_menu.pack(pady=5)

# Botón para obtener recomendaciones
recommend_button = ttk.Button(root, text="Obtener Recomendaciones", command=get_recommendations)
recommend_button.pack(pady=10)

# Lista de recomendaciones
ttk.Label(root, text="Recomendaciones:").pack(pady=10)
recommendations_listbox = tk.Listbox(root, width=50, height=10)
recommendations_listbox.pack(pady=10)

# Cargar películas al inicio
load_movies()

# Ejecutar la interfaz
root.mainloop()