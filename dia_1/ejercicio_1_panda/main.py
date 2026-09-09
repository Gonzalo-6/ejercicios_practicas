import psycopg2
import json
import os

json_path = "config/config.json"
print("Existe archivo:", os.path.exists(json_path))

print("Ruta que se está usando:", json_path)

def open_connection(json_path):
    try:
        # Leer el fichero JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            config = json.load(file)

        # Crear conexión
        conn = psycopg2.connect(
            host=config["host"],
            database=config["database"],
            user=config["user"],
            password=config["password"],
            port=config["port"]
        )

        return conn

    except Exception as e:
        print("Error real: ", e)
        return None

conexion = open_connection("config/config.json")

if conexion:
    print("Conexión correcta")
    conexion.close()
else:
    print("Error en la conexión")