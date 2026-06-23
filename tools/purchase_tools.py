import sqlite3
import pandas as pd
from core.config import MARKETING_DB_PATH

def get_purchase_history(customer_id):
	
	conn = sqlite3.connect(MARKETING_DB_PATH)

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
