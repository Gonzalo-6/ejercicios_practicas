import psycopg2
import json


def open_connection(json_path):
    try:
        # Leer el fichero JSON
        with open(json_path, 'r') as file:
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
        print("Error al conectar a la base de datos:", e)
        return None

conexion = open_connection("config.json")

if conexion:
    print("Conexión correcta")
    conexion.close()
else:
    print("Error en la conexión")