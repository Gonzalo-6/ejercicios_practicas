from dotenv import load_dotenv
from src.db.connection import open_connection
import requests
import pandas as pd
import os
import math
import psycopg2



load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Calcular distancia

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  # km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

# Función: obtener coordenadas
def get_coords(direccion):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    params = {
        "address": direccion,
        "key": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    
    if not data.get("results"):
        raise ValueError("No se encontraron coordenadas para la dirección")
    
    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]


# Función: obtener restaurantes
def get_restaurantes(lat, lng):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "location": f"{lat},{lng}",
        "radius": 1000,
        "type": "restaurant",
        "key": API_KEY
    }
    
    data = requests.get(url, params=params).json()

    if data.get("status") != "OK":
        raise ValueError(f"Error API Google: {data.get('status')}")
    
    return data.get("results", [])




# Función: convertir a dataframe
def to_dataframe(restaurantes, origen_lat, origen_lng, ):
    data = []
    
    for r in restaurantes:
        lat = r["geometry"]["location"]["lat"]
        lng = r["geometry"]["location"]["lng"]
        
        distancia = calcular_distancia(origen_lat, origen_lng, lat, lng)
        
        data.append({
            "nombre": r.get("name"),
            "direccion": r.get("vicinity"),
            "rating": r.get("rating"),
            "distancia_km": distancia
        })
    
    return pd.DataFrame(data)

# Obtener los mejores restaurantes
def obtener_mejores(df):
    mas_cercano = df.loc[df["distancia_km"].idxmin()]
    mejor_valorado = df.loc[df["rating"].idxmax()]
    
    return mas_cercano, mejor_valorado

# Guardar en PostgreSQL
def guardar_en_bd(df):
    conn = open_connection("config/config1.json")

    if conn is None: 
        raise ValueError("No se puede conectar a as base de datos")
       
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO api_google.restaurantes (nombre, direccion, rating, distancia_km)
            VALUES (%s, %s, %s, %s)
        """, (row["nombre"], row["direccion"], row["rating"], row["distancia_km"]))
    
    conn.commit()
    cursor.close()
    conn.close()


# Función principal
def ejercicio_restaurantes():
    direccion = "Av. Manoteras 26, Madrid, Spain"
    
    lat, lng = get_coords(direccion)
    restaurantes = get_restaurantes(lat, lng)
    
    df = to_dataframe(restaurantes, lat, lng)
    
    mas_cercano, mejor_valorado = obtener_mejores(df)
    
    print("\nMás cercano:\n", mas_cercano)
    print("\nMejor valorado:\n", mejor_valorado)
    
    guardar_en_bd(df)
    
    return df

if __name__ == "__main__":
    df = ejercicio_restaurantes()
    print(df)

