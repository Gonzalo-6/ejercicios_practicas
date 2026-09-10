import pandas as pd
import requests
from src.db.connection import open_connection

# Llamar a la base de datos
def get_products(conn):
    
    query = "SELECT product_id, product_name, unit_price FROM products"
    
    df = pd.read_sql(query, conn)
    
    conn.close()
    
    return df

# Leer el archivo Excel
def read_compra_excel(path):
    df = pd.read_excel(path)
    df.columns = df.columns.str.lower()
    return df

# Calcular el total de la compra
def calcular_total(products_df, compra_df):

    print(products_df.head())
    print(compra_df.head())

    df = compra_df.merge( 
        products_df, 
        on = "product_id"
        )
    
    df["total"] = df["quantity"] * df["unit_price"]
    
    return df["total"].sum()


# Convertir de USD a GBP
def convertir_a_gbp(total_usd):
    url = f"https://api.exchangerate.host/convert?from=USD&to=GBP&amount={total_usd}"
    
    response = requests.get(url)
    data = response.json()
    
    return data.get("result", 0)


#Función principal
def main():
    conn = open_connection("config/config.json")
    
    if conn is None:
        raise ValueError("Error conexión BD")
    
    products_df = get_products(conn)
    compra_df = read_compra_excel("data/compra.xlsx")
    
    total_usd = calcular_total(products_df, compra_df)
    total_gbp = convertir_a_gbp(total_usd)
    
    conn.close()
    
    return float(total_usd), float(total_gbp)

# Resultado
if __name__ == "__main__":
    total_usd, total_gbp = main()
    print(f"Total en USD: {total_usd:.2f}")
    print(f"Total en GBP: {total_gbp:.2f}")