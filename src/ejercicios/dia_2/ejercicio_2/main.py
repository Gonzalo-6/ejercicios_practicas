import pandas as pd
import os
import sys
print(sys.path)


print("Working dir:", os.getcwd())


from src.ejercicios.dia_1.ejercicio_1_panda.main import open_connection

json_path = "config/config.json"
print("Existe archivo:", os.path.exists(json_path))
json_path = "config/config.json"
print("Existe archivo:", os.path.exists(json_path))

def get_order_total(json_path, order_id):
    conn = open_connection(json_path)

    if not conn:
        return None

    query = f"""
        SELECT 
            order_id,
            SUM(unit_price * quantity * (1 - discount)) AS total_price
        FROM order_details
        WHERE order_id = {order_id}
        GROUP BY order_id;
    """

    try:
        df = pd.read_sql(query, conn)
        return df

    except Exception as e:
        print("Error en la query:", e)
        return None

    finally:
        conn.close()


df = get_order_total("config/config.json", 10248)

print(df)


