import sqlite3
import pandas as pd

customers = pd.read_csv("customers.csv")
purchases = pd.read_csv("purchases.csv")
campaign_history = pd.read_csv("campaign_history.csv")
products = pd.read_csv("products.csv")
campaign_results = pd.read_csv("campaign_results.csv")

conn = sqlite3.connect("marketing.db")

customers.to_sql(
	"customers",
	conn,
	if_exists="replace",
	index=False
)

purchases.to_sql(
	"purchases",
	conn,
	if_exists="replace",
	index=False
)

conn.execute("""
	CREATE TABLE campaign_history(
	campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INTEGER,
	product TEXT,
	channel TEXT,
	subject TEXT,
	message TEXT,
	campaign_date TEXT
	)
""")

campaign_history.to_sql(
	"campaign_history",
	conn,
	if_exists="append",
	index=False
)

products.to_sql(
	"products",
	conn,
	if_exists="replace",
	index=False
)

campaign_results.to_sql(
	"campaign_results",
	conn,
	if_exists="replace",
	index=False
)

conn.close()

print("Database created")
