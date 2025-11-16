import pandas as pd
import random
import uuid
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# --------------------
# 1. Customers
# --------------------
def generate_customers(n=1000):
    customers = []
    for i in range(1, n+1):
        customers.append({
            "customer_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "signup_date": fake.date_between(start_date="-3y", end_date="today"),
            "risk_profile": random.choice(["Low","Medium","High"]),
            "marketing_opt_in": random.choice([True, False])
        })
    return pd.DataFrame(customers)

# --------------------
# 2. Accounts
# --------------------
def generate_accounts(customers):
    accounts = []
    account_types = ["GIA", "ISA", "LISA", "SIPP"]
    for i in range(1, 3000):
        cust = random.choice(customers["customer_id"])
        accounts.append({
            "account_id": i,
            "customer_id": cust,
            "account_type": random.choice(account_types),
            "opened_date": fake.date_between(start_date="-3y", end_date="today"),
            "status": random.choice(["Open","Closed"])
        })
    return pd.DataFrame(accounts)

# --------------------
# 3. Products
# --------------------
def generate_products():
    product_list = [
        ("Global Shares", "ETF", "High"),
        ("Balanced Portfolio", "Fund", "Medium"),
        ("Defensive Portfolio", "Fund", "Low"),
        ("Technology Leaders", "ETF", "High"),
        ("Emerging Markets", "ETF", "Medium")
    ]
    products = []
    for i, p in enumerate(product_list, 1):
        products.append({
            "product_id": i,
            "product_name": p[0],
            "product_type": p[1],
            "risk_level": p[2]
        })
    return pd.DataFrame(products)

# --------------------
# 4. Deposits
# --------------------
def generate_deposits(accounts, n=20000):
    deposits = []
    for _ in range(n):
        acc = random.choice(accounts["account_id"])
        deposits.append({
            "deposit_id": str(uuid.uuid4()),
            "account_id": acc,
            "amount": round(random.uniform(1.0, 100.0), 2),
            "deposit_type": random.choice(["Roundup", "OneOff", "Monthly"]),
            "date": fake.date_between(start_date="-2y", end_date="today")
        })
    return pd.DataFrame(deposits)

# --------------------
# 5. Investment Transactions
# --------------------
def generate_investment_txns(accounts, products, n=50000):
    txns = []
    for _ in range(n):
        acc = random.choice(accounts["account_id"])
        prod = random.choice(products["product_id"])
        price = round(random.uniform(0.5, 5.0), 2)
        units = round(random.uniform(1, 50), 3)

        txns.append({
            "txn_id": str(uuid.uuid4()),
            "account_id": acc,
            "product_id": prod,
            "buy_sell": random.choice(["BUY","SELL"]),
            "units": units,
            "unit_price": price,
            "txn_date": fake.date_between(start_date="-2y", end_date="today")
        })
    return pd.DataFrame(txns)

# --------------------
# 6. Daily Pricing
# --------------------
def generate_pricing(products):
    rows = []
    start_dt = datetime(2022,1,1)
    end_dt = datetime.today()
    delta = timedelta(days=1)

    while start_dt <= end_dt:
        for p in products["product_id"]:
            base = random.uniform(1.0, 2.5)
            rows.append({
                "product_id": p,
                "date": start_dt.date(),
                "nav_price": round(base + random.uniform(-0.2, 0.2), 3)
            })
        start_dt += delta

    return pd.DataFrame(rows)

# --------------------
# EXECUTION
# --------------------
if __name__ == "__main__":
    customers = generate_customers()
    accounts = generate_accounts(customers)
    products = generate_products()
    deposits = generate_deposits(accounts)
    txns = generate_investment_txns(accounts, products)
    pricing = generate_pricing(products)

    customers.to_csv("raw_customers.csv", index=False)
    accounts.to_csv("raw_accounts.csv", index=False)
    products.to_csv("raw_products.csv", index=False)
    deposits.to_csv("raw_deposits.csv", index=False)
    txns.to_csv("raw_transactions.csv", index=False)
    pricing.to_csv("raw_pricing.csv", index=False)

    print("RAW MONEYBOX-like data generated successfully!")
