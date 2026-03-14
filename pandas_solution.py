import sqlite3
import pandas as pd
import logging
import os

DB_PATH = "data/database.db"
OUTPUT_PATH = "output/pandas_output.csv"

logging.basicConfig(level=logging.INFO)

def load_tables(conn):
    customers = pd.read_sql("SELECT * FROM Customer", conn)
    sales = pd.read_sql("SELECT * FROM Sales", conn)
    orders = pd.read_sql("SELECT * FROM Orders", conn)
    items = pd.read_sql("SELECT * FROM Items", conn)

    return customers, sales, orders, items


def transform_data(customers, sales, orders, items):
    # Join Customer -> Sales
    df = sales.merge(customers, on="customer_id")

    # Join Sales -> Orders
    df = df.merge(orders, on="sales_id")

    # Join Orders -> Items
    df = df.merge(items, on="item_id")

    # Filter age range
    df = df[(df["age"] >= 18) & (df["age"] <= 35)]

    # Remove NULL quantities
    df = df[df["quantity"].notna()]

    # Aggregate quantities
    result = (
        df.groupby(["customer_id", "age", "item_name"], as_index=False)
        .agg({"quantity": "sum"})
    )

    # Remove zero totals
    result = result[result["quantity"] > 0]

    # Rename columns to match example #doing this because I had to recreate DB
    result = result.rename(columns={
        "customer_id": "Customer",
        "age": "Age",
        "item_name": "Item",
        "quantity": "Quantity"
    })
    # Ensure integer quantities, becuase : (The company doesn’t sell half of an item ;) )
    result["Quantity"] = result["Quantity"].astype(int) 
    # Sort output, matching order in example
    result = result.sort_values(["Customer", "Item"])
    return result


def export_csv(df):
    os.makedirs("output", exist_ok=True)
    df.to_csv(OUTPUT_PATH,index=False,sep=";") #not sure if example meant to store query or query result as ; seperated, so doing both
    logging.info(f"Output exported to {OUTPUT_PATH}")

def main():
    try:
        conn = sqlite3.connect(DB_PATH)
        customers, sales, orders, items = load_tables(conn)
        result = transform_data(customers, sales, orders, items)
        export_csv(result)
        conn.close()
        logging.info("Pandas solution completed successfully.")
    except Exception as e:
        logging.error(f"Process failed: {e}")

if __name__ == "__main__":
    main()