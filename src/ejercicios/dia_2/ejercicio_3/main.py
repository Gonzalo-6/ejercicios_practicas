import requests



from src.db.connection import open_connection
from src.ejercicios.dia_2.ejercicio_2.main import get_order_total

def best_crypto(total_usd):
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    params = {
        "ids": "bitcoin,ethereum,solana,cardano",
        "vs_currencies": "usd"
    }

    response = requests.get(url, params=params)
    data = response.json()

    best_coin = None
    max_amount = 0

    for coin, values in data.items():
        price_usd = values["usd"]
        amount = total_usd / price_usd

        if amount > max_amount:
            max_amount = amount
            best_coin = coin

    return best_coin, float(max_amount)

df = get_order_total("config/config.json", 10248)

if df is not None:
    total_usd = df["total_price"].iloc[0]

    result = best_crypto(total_usd)
    print(result)