import sqlite3
import logging
import os

DB_PATH = "data/database.db"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def create_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        logging.info("Connected to SQLite database.")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Connection failed: {e}")
        raise

def create_tables(conn):
    try:
        cursor = conn.cursor()

        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Customer (
            customer_id INTEGER PRIMARY KEY,
            age INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Items (
            item_id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Sales (
            sales_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
        );

        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY,
            sales_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER,
            FOREIGN KEY (sales_id) REFERENCES Sales(sales_id),
            FOREIGN KEY (item_id) REFERENCES Items(item_id)
        );
        """)

        conn.commit()
        logging.info("Tables created successfully.")

    except sqlite3.Error as e:
        logging.error(f"Table creation failed: {e}")
        raise

def insert_data(conn):
    try:
        cursor = conn.cursor()

        # Customers
        customers = [
            (1, 21),
            (2, 23),
            (3, 35)
        ]

        # Items
        items = [
            (1, "x"),
            (2, "y"),
            (3, "z")
        ]

        # Sales transactions
        sales = [
            (1, 1),  # customer 1
            (2, 1),  # customer 1
            (3, 2),  # customer 2
            (4, 3),  # customer 3
            (5, 3)   # customer 3
        ]

        # Orders (all items recorded per sale)
        orders = [
            # Sale 1 (customer 1)
            (1, 1, 1, 5),
            (2, 1, 2, None),
            (3, 1, 3, None),

            # Sale 2 (customer 1)
            (4, 2, 1, 5),
            (5, 2, 2, None),
            (6, 2, 3, None),

            # Sale 3 (customer 2)
            (7, 3, 1, 1),
            (8, 3, 2, 1),
            (9, 3, 3, 1),

            # Sale 4 (customer 3)
            (10, 4, 1, None),
            (11, 4, 2, None),
            (12, 4, 3, 1),

            # Sale 5 (customer 3)
            (13, 5, 1, None),
            (14, 5, 2, None),
            (15, 5, 3, 1)
        ]

        cursor.executemany(
            "INSERT INTO Customer (customer_id, age) VALUES (?, ?)",
            customers
        )

        cursor.executemany(
            "INSERT INTO Items (item_id, item_name) VALUES (?, ?)",
            items
        )

        cursor.executemany(
            "INSERT INTO Sales (sales_id, customer_id) VALUES (?, ?)",
            sales
        )

        cursor.executemany(
            "INSERT INTO Orders (order_id, sales_id, item_id, quantity) VALUES (?, ?, ?, ?)",
            orders
        )

        conn.commit()

        cursor.executemany(
            "INSERT INTO Items (item_id, item_name) VALUES (?, ?)",
            items
        )

        cursor.executemany(
            "INSERT INTO Sales (sales_id, customer_id) VALUES (?, ?)",
            sales
        )

        cursor.executemany(
            """
            INSERT INTO Orders (order_id, sales_id, item_id, quantity)
            VALUES (?, ?, ?, ?)
            """,
            orders
        )
        conn.commit()
        logging.info("Sample data inserted successfully.")

    except sqlite3.Error as e:
        logging.error(f"Data insertion failed: {e}")
        raise

def main():
    try:
        os.makedirs("data", exist_ok=True)

        conn = create_connection(DB_PATH)

        create_tables(conn)
        insert_data(conn)

        conn.close()

        logging.info("Database setup completed.")

    except Exception as e:
        logging.error(f"Database setup failed: {e}")


if __name__ == "__main__":
    main()