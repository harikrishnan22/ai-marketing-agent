import sqlite3
import pandas as pd

def get_purchase_history(customer_id):
	
	conn = sqlite3.connect("marketing.db")

	purchases = pd.read_sql_query(
		f"""
		SELECT *
		FROM purchases
		WHERE customer_id = {customer_id}
		""",
		conn
		)

	conn.close()

	return{
		"purchase_history":
		purchases["product"].tolist()
		}
