from urllib import response

import requests
import os

API_KEY = os.getenv("AEMET_API_KEY")
print("API_KEY:", API_KEY)


# Obtener los datos de la localización

def get_estaciones():
    url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"
    
    response = requests.get(url, params={"api_key": API_KEY})
    data = response.json()

    if "datos" not in data:
        print("Error AEMET:", data)
        return None
    

    estaciones = requests.get(data["datos"]).json()
    
    for est in estaciones:
        if "GETAFE" in est["nombre"].upper():
            return est["indicativo"] 

        
# Obtener los datos de la temperatura

def get_aemet_data(idema):
    url = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2024-08-22T00:00:00UTC/fechafin/2024-08-23T23:59:59UTC/estacion/{idema}"
    
    # request 1
    response = requests.get(url, params={"api_key": API_KEY})
    data = response.json()
    
    # request 2 (la clave)
    if "datos" not in data:
        print("Error AEMET:", data)
        return None
    final_response = requests.get(data["datos"])
    
    return final_response.json()

# calcular temperatura media

def calcular_media(datos):
    temps = []
    
    for d in datos:
        if d.get("tmed"):
            temps.append(float(d["tmed"].replace(",", ".")))
    
    return sum(temps) / len(temps)

# resultado final

idema = get_estaciones()

if idema:
    datos = get_aemet_data(idema)

    if datos:
        media = calcular_media(datos)
        print(f"Temperatura media en Getafe el 22 y 23 de agosto de 2024: {media:.2f} °C")

    else:
        print("No se pudieron obtener los datos")

else:
    print("No se encontro estación")        
