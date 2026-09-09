import psycopg2
import json

def open_connection(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            config = json.load(file)

        conn = psycopg2.connect(
            host=config["host"],
            database=config["database"],
            user=config["user"],
            password=config["password"],
            port=config["port"]
        )

        return conn

    except Exception as e:
        print("Error en la conexión:", e)
        return None