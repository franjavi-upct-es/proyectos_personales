import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import gc
import os

# Función para limpiar la memoria del archivo
def clear_cache():
    plt.close('all')  # Close all figures
    gc.collect()  # Force garbage collection to free memory

clear_cache()
data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data/housing.csv'))
df = pd.DataFrame(data)
data = df.rename(columns={'MEDV': 'PRICE'})

sns.pairplot(data[['PRICE', 'RM', 'LSTAT', 'PTRATIO']])
plt.show()

X = data.drop('PRICE', axis=1)
y = data['PRICE']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Media y desviación estándar de cada columna de X
stats = X_train.describe()
print(stats)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse}")
print(f"R2 Score: {r2}")

# Número de muestras sintéticas que quiero generar
num_samples = 1000

# Generar un DataFrame con valores aleatorios basados en la media y desviación estándar de X_train
synthetic_data = pd.DataFrame({
    col: np.random.normal(loc=stats.loc['mean', col], scale=stats.loc['std', col], size=num_samples)
    for col in X_train.columns
})

# Hay que asegurarse de que los valores estén dentro de los rangos realistas (por ejemplo, no negativos)
synthetic_data = synthetic_data.clip(lower=X_train.min(), upper=X_train.max(), axis=1)

# Predecir el precio para cada fila en synthetic_data
synthetic_data['PRICE'] = model.predict(synthetic_data) + np.random.normal(0, 1, num_samples)

# Combinamos los datos sintéticos con el conjunto de entrenamiento orginal
X_train_augmented = pd.concat([X_train, synthetic_data.drop(columns=['PRICE'])], ignore_index=True)
y_train_augmented = pd.concat([y_train, synthetic_data['PRICE']], ignore_index=True)

# Reentrenamos el modelo con los datos aumentados
model.fit(X_train_augmented, y_train_augmented)

# Evaluamos el modelo nuevamente en el conjunto de prueba para ver si el rendimiento ha mejorado
y_pred = model.predict(X_test)
mse_2 = mean_squared_error(y_test, y_pred)
r2_2 = r2_score(y_test, y_pred)

print(f"MSE después de aumentar datos: {mse_2}")
print(f"R2 Score después de aumentar datos: {r2_2}")

print(f"Diferencia MSE: {mse_2 - mse}")
print(f"Diferencia R2 Score: {r2_2 - r2}")