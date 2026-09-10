from dotenv import load_dotenv
import requests
import pandas as pd
import os


load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
print("API_KEY:", API_KEY)

# Función: obtener coordenadas
def get_coords(direccion):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    params = {
        "address": direccion,
        "key": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    print("STATUS:", data.get("status"))
    print("FULL RESPONSE:", data)

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
    
    response = requests.get(url, params=params)
    data = response.json()

    if not data.get("results"):
        raise ValueError("No se encontraron restaurantes")
    
    return data["results"]


# Función: convertir a dataframe
def to_dataframe(restaurantes):
    data = []
    
    for r in restaurantes:
        data= [
             {
            "nombre": r.get("name"),
            "direccion": r.get("vicinity")
        }
        ]
        
    if not data:
            raise ValueError("No se encontraron resultados") 
    
    return pd.DataFrame(data)


# Función principal
def ejercicio_restaurantes():
    direccion = "Av. Manoteras 26, Madrid, Spain"
    
    lat, lng = get_coords(direccion)
    restaurantes = get_restaurantes(lat, lng)
    df = to_dataframe(restaurantes)
    
    return df

    
if __name__ == "__main__":
    df = ejercicio_restaurantes()
    print(df)