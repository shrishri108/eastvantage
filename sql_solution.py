import sqlite3
import pandas as pd
import logging
import os

DB_PATH = "data/database.db"
OUTPUT_PATH = "output/sql_output.csv"

logging.basicConfig(level=logging.INFO)

def load_tables(conn):
    try:
        output = pd.read_sql("""SELECT c.customer_id AS Customer,
                                        c.age AS Age,
                                        i.item_name AS Item,
                                        SUM(o.quantity) AS Quantity
                                    FROM Customer c
                                    JOIN Sales s ON c.customer_id = s.customer_id
                                    JOIN Orders o ON s.sales_id = o.sales_id
                                    JOIN Items i ON o.item_id = i.item_id
                                    WHERE
                                        c.age BETWEEN 18 AND 35
                                        AND o.quantity IS NOT NULL
                                    GROUP BY
                                        c.customer_id,
                                        c.age,
                                        i.item_name
                                    HAVING SUM(o.quantity) > 0
                                    ORDER BY
                                        c.customer_id,
                                        i.item_name;""", conn)
        
        # logging.info("Tables loaded and query executed successfully.")
    except Exception as e:
        logging.error(f"Error loading tables: {e}")
        raise   
    return output

def export_csv(df):
    os.makedirs("output", exist_ok=True)
    df.to_csv(OUTPUT_PATH,index=False,sep=";") #not sure if example meant to store query or query result as ; seperated, so doing both
    logging.info(f"Output exported to {OUTPUT_PATH}")

def main():
    try:
        conn = sqlite3.connect(DB_PATH)
        result = load_tables(conn)
        export_csv(result)
        conn.close()
        logging.info("SQL solution completed successfully.")
    except Exception as e:
        logging.error(f"Process failed: {e}")

if __name__ == "__main__":
    main()