import requests

# Funcion generica para llamar a la API de FreeCurrencyAPI

API_KEY = "fca_live_Rzl47fBD06wWF5aDQWpVyqfmGTbVqBY0rf0peyEC"  

def call_freecurrency(endpoint, params=None):
    base_url = "https://api.freecurrencyapi.com/v1/"
    
    headers = {
        "apikey": API_KEY
    }
    
    url = base_url + endpoint
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error API: {response.status_code} - {response.text}")
    
    return response.json()

# Funcion para convertir monedas usando la API de FreeCurrencyAPI

def convert_currency(amount, from_currency, to_currency, date):
    params = {
        "base_currency": from_currency,
        "currencies": to_currency,
        "date": date
    }
    
    data = call_freecurrency("historical", params)
    
    rate = data["data"][date][to_currency]
    
    return amount * rate


# Comprar rupias 

inr_amount = convert_currency(
    amount=200,
    from_currency="TRY",
    to_currency="INR",
    date="2023-01-01"
)

print("Rupias compradas:", inr_amount)


# Comprar liras 

try_amount = convert_currency(
    amount=inr_amount,
    from_currency="INR",
    to_currency="TRY",
    date="2024-03-04"
)

print("Liras finales:", try_amount)


# resumen final
print(f"""
Inicial: 200 TRY
Después de comprar INR (2023-01-01): {inr_amount}
Después de vender (2024-03-04): {try_amount}
""")