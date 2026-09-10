import requests
from datetime import datetime, timedelta


# funcion para obetener el precio en la api de fakestoreapi.com

def get_product_price():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    data = response.json()
    
    for product in data:
        if product["title"] == "Rain Jacket Women Windbreaker Striped Climbing Raincoats":
            return product["price"]
    
    return None

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


# precio de eth con la api CoinGecko

def get_eth_price_yesterday():
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%d-%m-%Y")  # formato CoinGecko
    
    url = f"https://api.coingecko.com/api/v3/coins/ethereum/history?date={date_str}"
    
    response = requests.get(url)
    data = response.json()
    
    return data["market_data"]["current_price"]["usd"]



# timeline de las conversiones

def timeline_conversiones():
    price_usd = get_product_price()

    # compra en rub 2020
    rub_2020 = convert_currency(price_usd, "USD", "RUB", "2020-01-26")

    # venta en rub 2022
    rub_2022 = convert_currency(price_usd, "RUB", "USD", "2022-03-03")

    # cambio rub-huf 2024
    huf_2024 = convert_currency(rub_2022, "RUB", "HUF", "2024-09-01")

    # cambio huf-eth ayer
    eth_price = get_eth_price_yesterday()
    eth_amount = huf_2024 / eth_price

    return {
        "rub_paid_2020": rub_2020,
        "rub_recibe_2022": rub_2022,
        "huf_2024": huf_2024,
        "eth_yesterday": eth_amount
    }

# resultado final del dinero en eth que tienes

result = timeline_conversiones()
print(f"""
1- RUB pagados en 2020: {result['rub_paid_2020']}
2- RUB recibidas en 2022: {result['rub_recibe_2022']}
3- HUF obtenidas en 2024: {result['huf_2024']}
4- ETH obtenidas ayer: {result['eth_yesterday']}
""")