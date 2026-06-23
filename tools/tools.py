import pandas as pd
from openai import OpenAI
import json
import sqlite3
from datetime import date
from agent_core.build_vector_store import search_similar_campaigns
from core.config import MARKETING_DB_PATH
 
client = OpenAI()

def get_campaign_data():
	df = pd.read_csv("campaigns.csv")

	df["CTR"] = df["clicks"] / df["impressions"] * 100
	df["conversion_rate"] = df["conversions"] / df["clicks"] * 100
	df["ROAS"] = df["revenue"] / df["spend"]

	return df

def get_customer_by_name(customer_name):
	
	conn = sqlite3.connect(MARKETING_DB_PATH)

	customer_record = pd.read_sql_query(
			f"""
			SELECT *
			FROM customers
			WHERE name = ?
			""",
			conn,
			params = [customer_name]
		)
	conn.close()

	if len(customer_record) == 0:
		return {
			"error": f"Customer '{customer_name}' not found"
		}

	customer_record_dict = customer_record.iloc[0].to_dict()

	return {
		"customer": customer_record_dict,
		"segment": customer_record_dict["segment"]
	}

def get_purchase_history(customer):
	
	customer_id = customer["customer_id"]
	
	conn = sqlite3.connect(MARKETING_DB_PATH)

	purchases = pd.read_sql_query(
		"""
		SELECT *
		FROM purchases
		WHERE customer_id = ?
		""",
		conn,
		params=[customer_id]
	)

	conn.close()

	return {
		"purchase_history": purchases["product"].tolist()
	}

def get_campaign_history(customer):

	conn = sqlite3.connect(MARKETING_DB_PATH)

	history = pd.read_sql_query(
		"""
		SELECT *
		FROM campaign_history
		WHERE customer_id = ?
		""",
		conn,
		params=[customer["customer_id"]]
	)

	conn.close()

	return {
		"campaign_history": history.to_dict(orient="records")
	}

def get_product_catalog(segment):
	
	conn = sqlite3.connect(MARKETING_DB_PATH)

	catalog = pd.read_sql_query(
		"""
		SELECT *
		FROM products
		WHERE segment = ?
		""",
		conn,
		params=[segment]
	)

	conn.close()

	return {
		"product_catalog": catalog["product"].tolist()
	}

def recommend_product(customer, purchase_history, campaign_history, product_catalog):

	prompt = f"""
		You are a luxury jewelry marketing strategist.
		
		Customer Profile:
		{json.dumps(customer, indent=2)}
		
		Purchase History:
		{json.dumps(purchase_history, indent=2)}

		Previous Campaigns:
		{json.dumps(campaign_history, indent=2)}
		
		Available Products:
		{json.dumps(product_catalog, indent=2)}

		Recommend ONE jewelry product that this customer is most likely to buy next.
	
		Rules:
		- Consider previous purchases.
		- Consider the customer's segment.
		- Do NOT recommend products already purhcased.
		- Do NOT recommend products already promoted in previous campaigns.
		- Only recommend products from Available Products.
		- Recommend the next logical product.
		- Return JSON only.
		
		Example:

		{{
			"product": "Diamond Bracelet"
		}}
		"""

	response = client.responses.create(
		model="gpt-4o-mini",
		input=prompt
	)

	cleaned = response.output_text
	
	cleaned = cleaned.replace("```json", "")
	cleaned = cleaned.replace("```", "")
	cleaned = cleaned.strip()

	return json.loads(cleaned)

def choose_channel(customer, purchase_history, product):

	prompt = f"""
		You are a marketing strategist.
		
		Customer:
		{json.dumps(customer, indent=2)}

		Purchase History:
		{json.dumps(purchase_history, indent=2)}

		Product:
		{product}

		Choose ONE channel:

		- Email
		- SMS
		- Push Notification
		- Whatsapp

		Return JSON only:

		{{
			"channel": "Email"
		}}
		"""

	response = client.responses.create(
		model="gpt-4o-mini",
		input=prompt
		)

	cleaned = response.output_text

	cleaned = cleaned.replace("```json", "")
	cleaned = cleaned.replace("```", "")
	cleaned = cleaned.strip()

	return json.loads(cleaned)

def retrieve_similar_campaigns(customer, product, segment):

	query = f"""
	Segment: {segment}

	Product: {product}
	"""

	similar_campaigns = search_similar_campaigns(
		query
	)

	return {
		"similar_campaigns": similar_campaigns
	}

def generate_campaign(customer, product, segment, channel, similar_campaigns, feedback=None):
	
	prompt = f"""
	You are a senior marketing strategist.

	Customer:
	{json.dumps(customer, indent=2)}

	Segment:
	{segment}

	Recommended Product:
	{product}

	Channel:
	{channel}

	Similar Campaigns:
	{json.dumps(similar_campaigns, indent=2)}

	Create a personalized marketing campaign.

	The campaign must be optimized for the selected channel.

	Examples:
	- Email: include a subject line and longer message.
	- SMS: short concise message.
	- WhatsApp: conversational tone.
	- Push Notification: very short attention-grabbing message.

	User Revision Request:
	{feedback}

	IMPORTANT:
	The user has rejected the previous campaign.

	You MUST apply the user's revision request.

	Return JSON only:
	
	{{
		"subject": "...",
		"message": "...",
		"cta": "..."
	}}
	"""
	
	response = client.responses.create(
		model="gpt-4o-mini",
		input=prompt
		)

	cleaned = response.output_text

	cleaned = cleaned.replace("```json", "")
	cleaned = cleaned.replace("```", "")
	cleaned = cleaned.strip()

	return json.loads(cleaned)

def save_campaign(customer, product, channel, subject, message):
	
	conn = sqlite3.connect(MARKETING_DB_PATH)

	conn.execute(
		"""
		INSERT INTO campaign_history
		(
			customer_id,
			product,
			channel,
			subject,
			message,
			campaign_date
		)
		VALUES (?, ?, ?, ?, ?, ?)
		""",
		(
			customer["customer_id"],
			product,
			channel,
			subject,
			message,
			str(date.today())
		)
	)
		
	conn.commit()
	conn.close()
	
	return {
		"campaign_saved": True
	}

def get_campaign_benchmarks(segment, channel):
	
	conn = sqlite3.connect(MARKETING_DB_PATH)
	
	campaign_benchmarks = pd.read_sql_query(
		"""
		SELECT *
		FROM campaign_results
		WHERE segment = ?
		AND channel = ?
		""",
		conn,
		params=[segment, channel]
	)

	conn.close()

	if len(campaign_benchmarks) == 0:
		return {
			"campaign_benchmarks": None
		}

	campaign_benchmarks_dict = campaign_benchmarks.iloc[0].to_dict()

	return {
		"campaign_benchmarks": campaign_benchmarks_dict
	}
		

def predict_campaign_performance(customer, product, channel, message, campaign_benchmarks):
	
	prompt = f"""
	You are a marketing analytics expert.

	Customer:
	{json.dumps(customer, indent=2)}

	Product:
	{product}

	Channel:
	{channel}

	Historical Benchmarks:
	{json.dumps(campaign_benchmarks, indent=2)}
	
	Campaign Message:
	{message}

	Analyze the campaign message and estimate whether performance
	will be above, below, or equal to the benchmark.
	
	Return realistic predicitons.

	Do not simply copy the benchmark values.
	
	Example:

	Benchmark:
	CTR = 3.4
	Conversion Rate = 1.2
	ROAS = 2.0

	Campaign Message:
	"Limited-time offer on our most popular products. Shop today and save 20%."

	Analysis:
	The message has a clear offer, urgency, and call-to-action.
	Performance is expected to be slightly above benchmark.

	Use the benchmark values as a starting point.

	Adjust prediction up or down based on:
	- messgae quality
	- personalization
	- strength of call-to-action
	- product relevance
	- channel effectiveness

	Predictions should typically remain within +/- 30% of benchmarks values
	unless there is a strong reason otherwise.
	
	Return JSON only.

	Expected Ouput:

	{{
		"predicted_ctr": 0.00,
		"predicted_conversion_rate": 0.00,
		"predicted_roas": 0.0
	}}
	"""

	response = client.responses.create(
		model="gpt-4o-mini",
		input=prompt
		)

	cleaned = response.output_text
	
	cleaned = cleaned.replace("```json", "")
	cleaned = cleaned.replace("```", "")
	cleaned = cleaned.strip()
	
	return json.loads(cleaned)
