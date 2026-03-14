import sqlite3
import pandas as pd
import logging
import os

if not os.path.exists("output"):
    os.makedirs("output")

DB_PATH = "data/database.db"
OUTPUT_PATH = "output/pandas_output.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        logging.info("Connected to database.")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection failed: {e}")
        raise

def extract_data(conn):
    try:
        query = """
        SELECT
            c.customer_id,
            c.age,
            i.item_name,
            o.quantity
        FROM Customer c
        JOIN Sales s ON c.customer_id = s.customer_id
        JOIN Orders o ON s.sales_id = o.sales_id
        JOIN Items i ON o.item_id = i.item_id
        WHERE c.age BETWEEN 18 AND 35
        """
        df = pd.read_sql_query(query, conn)
        logging.info("Data extracted successflly.")
        return df
    except Exception as e:
        logging.error(f"Data extraction failed: {e}")
        raise


def transform_data(df):
    """
    1. Ignore NULL quantities
    2. Aggregate totals per customer/item
    3. Remove zero totals
    """
    try:
        df = df.dropna(subset=["quantity"]) #drop all rows with NULL quantity

        df["quantity"] = df["quantity"].astype(int) # because no half of an item sold ;)
        
        #aggregate total quantity per customer/item combination
        result = (df.groupby(["customer_id", "age", "item_name"], as_index=False).agg({"quantity": "sum"}))

        result = result[result["quantity"] > 0] #filter on > 0
        result = result.rename(columns={"customer_id": "Customer","age": "Age","item_name": "Item","quantity": "Quantity"})
        result = result.sort_values(["Customer", "Item"])

        logging.info("Data transformation complete.")
        return result

    except Exception as e:
        logging.error(f"Transformation failed: {e}")
        raise

def export_csv(df, output_path):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, sep=";",index=False) # use ; seperator
        logging.info(f"CSV exported successfully to {output_path}")
    except Exception as e:
        logging.error(f"CSV export failed: {e}")
        raise

def main():
    try:
        conn = create_connection(DB_PATH)
        raw_data = extract_data(conn)
        transformed = transform_data(raw_data)
        export_csv(transformed, OUTPUT_PATH)
        conn.close()
        logging.info("Pandas solution completed successfully.")
    except Exception as e:
        logging.error(f"Process failed with error: {e}")

if __name__ == "__main__":
    main()