import psycopg2
import os

# -------------------------------------------------------------------
# CONFIGURATION — EDIT THIS TO MATCH YOUR POSTGRES INSTANCE
# -------------------------------------------------------------------
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DB = "dbt_db"
PG_USER = "airflow"
PG_PASSWORD = "airflow"

DATA_DIR = "./"   # folder containing CSVs (change if needed)
# -------------------------------------------------------------------

RAW_TABLES = {
    "raw_customers": "raw_customers.csv",
    "raw_accounts": "raw_accounts.csv",
    "raw_products": "raw_products.csv",
    "raw_deposits": "raw_deposits.csv",
    "raw_transactions": "raw_transactions.csv",
    "raw_pricing": "raw_pricing.csv"
}


# -------------------------------------------------------------------
# SQL: Create raw tables
# -------------------------------------------------------------------
CREATE_TABLE_SQL = {
    "raw_customers": """
        CREATE TABLE IF NOT EXISTS raw_customers (
            customer_id INT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            signup_date DATE,
            risk_profile TEXT,
            marketing_opt_in BOOLEAN
        );
    """,

    "raw_accounts": """
        CREATE TABLE IF NOT EXISTS raw_accounts (
            account_id INT,
            customer_id INT,
            account_type TEXT,
            opened_date DATE,
            status TEXT
        );
    """,

    "raw_products": """
        CREATE TABLE IF NOT EXISTS raw_products (
            product_id INT,
            product_name TEXT,
            product_type TEXT,
            risk_level TEXT
        );
    """,

    "raw_deposits": """
        CREATE TABLE IF NOT EXISTS raw_deposits (
            deposit_id TEXT,
            account_id INT,
            amount NUMERIC,
            deposit_type TEXT,
            date DATE
        );
    """,

    "raw_transactions": """
        CREATE TABLE IF NOT EXISTS raw_transactions (
            txn_id TEXT,
            account_id INT,
            product_id INT,
            buy_sell TEXT,
            units NUMERIC,
            unit_price NUMERIC,
            txn_date DATE
        );
    """,

    "raw_pricing": """
        CREATE TABLE IF NOT EXISTS raw_pricing (
            product_id INT,
            date DATE,
            nav_price NUMERIC
        );
    """
}


# -------------------------------------------------------------------
# CONNECT TO POSTGRES
# -------------------------------------------------------------------
def get_connection():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )


# -------------------------------------------------------------------
# LOAD CSV USING COPY (FASTEST WAY)
# -------------------------------------------------------------------
def load_csv(cursor, table_name, csv_file):
    csv_path = os.path.join(DATA_DIR, csv_file)

    print(f"Loading {csv_file} into {table_name}...")

    with open(csv_path, "r", encoding="utf-8") as f:
        cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", f)


# -------------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------------
if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()

    print("Connected to Postgres.")

    # 1. Create raw tables
    for table_name, create_sql in CREATE_TABLE_SQL.items():
        print(f"Creating table {table_name}...")
        cur.execute(create_sql)

    # 2. Truncate existing content (optional)
    for table_name in RAW_TABLES.keys():
        cur.execute(f"TRUNCATE TABLE {table_name};")

    conn.commit()

    # 3. Load every CSV
    for table_name, csv_file in RAW_TABLES.items():
        load_csv(cur, table_name, csv_file)

    conn.commit()
    cur.close()
    conn.close()

    print("🎉 All raw data successfully loaded into Postgres!")
