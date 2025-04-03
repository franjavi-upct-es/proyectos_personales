import cx_Oracle

# Conexión a la base de datos
username = 'SYSTEM'
password = '1234'
dsn = 'localhost/XE'

# Conexión a la base de datos
connection = cx_Oracle.connect(username, password, dsn)

# Creación de un cursor
cursor = connection.cursor()

# Ejecución de una consulta
cursor.execute('SELECT * FROM ACTIVIDAD')

# Recuperación de los resultados
for result in cursor:
    print(result)

# Cierre de la conexión
cursor.close()
connection.close()