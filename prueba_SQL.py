import oracledb
import pandas as pd

# Activa el modo thick con la ruta del cliente
oracledb.init_oracle_client(lib_dir=r"C:\Users\fcoja\Downloads\instantclient_23_7")

# Leer la consulta desde el archivo .sql
with open("prueba_SQL.sql", "r") as file:
    sql_query = file.read()

# Conectar a Oracle
conn = oracledb.connect(
    user="SYSTEM",
    password="1234",
    host="localhost",
    port=1521,
    service_name="XE"
)

# Ejecutar consulta y cargar resultados en DataFrame
df = pd.read_sql(sql_query, con=conn)

# Mostrar datos
df.to_excel("prueba.xlsx", index=False, engine="openpyxl")

# Cerrar conexión
conn.close()
