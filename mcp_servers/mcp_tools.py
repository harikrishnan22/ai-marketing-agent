import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP
from tools.tools import (
	get_customer_by_name as get_customer_by_name_tool,
	get_purchase_history as get_purchase_history_tool,
	get_campaign_history as get_campaign_history_tool,
	get_product_catalog as get_product_catalog_tool,
	recommend_product as recommend_product_tool,
	choose_channel as choose_channel_tool,
	retrieve_similar_campaigns as retrieve_similar_campaigns_tool,
	generate_campaign as generate_campaign_tool,
	get_campaign_benchmarks as get_campaign_benchmarks_tool,
	predict_campaign_performance as predict_campaign_performance_tool,
	save_campaign as save_campaign_tool
)

mcp = FastMCP("marketing")

@mcp.tool(
	description=
	"""
	Retrieve customer profile information including
	customer ID and  segment using the customer's name.
	"""
)
def get_customer_by_name(customer_name: str):

	return get_customer_by_name_tool(customer_name)

@mcp.tool(
	description=
	"""
	Retrieve products previously purchased by a customer.
	Used for personalization and recommendation.
	"""	
)
def get_purchase_history(customer: dict):

	return get_purchase_history_tool(customer)

@mcp.tool(
	description=
	"""
	Retrieve previous marketing campaigns sent to a specific customer.
	Used to avoid repeating previous promotions.
	"""
)
def get_campaign_history(customer: dict):

	return get_campaign_history_tool(customer)

@mcp.tool(
	description=
	"""
	Retrieve available products for a customer segment.
	Used when selecting products for campaigns.
	"""
)
def get_product_catalog(segment: str):

	return get_product_catalog_tool(segment)

@mcp.tool(
	description=
	"""
	Recommend the next best product for a customer
	using purchase history, campaign history, customer segment,
	and available products.
	"""
)
def recommend_product(
	customer:dict,
	purchase_history: list,
	campaign_history: list,
	product_catalog: list
	):

	return recommend_product_tool(
		customer,
		purchase_history,
		campaign_history,
		product_catalog
	)

@mcp.tool(
	description=
	"""
	Choose the best marketing channel (Email, SMS,
	Push Notification, or Whatsapp) for a customer and product.
	"""
)
def choose_channel(
	customer: dict,
	purchase_history: list,
	product: str
	):

	return choose_channel_tool(
		customer,
		purchase_history,
		product
	)

@mcp.tool(
	description=
	"""
	Search previous successful campaigns similar to
	a proposed product and customer segment using vector similarity.
	"""
)
def retrieve_similar_campaigns(
	customer: dict,
	product: str,
	segment: str
	):

	return retrieve_similar_campaigns_tool(
		customer,
		product,
		segment
	)

@mcp.tool(
	description=
	"""
	Generate a personalized marketing campaign message
	including subject, message, and call-to-action based on customer,
	product, channel, and similar campaigns.
	"""
)
def generate_campaign(
	customer: dict,
	product: str,
	segment: str,
	channel: str,
	similar_campaigns: dict,
	feedback: str | None = None
	):

	return generate_campaign_tool(
		customer,
		product,
		segment,
		channel,
		similar_campaigns,
		feedback
	)

@mcp.tool(
	description=
	"""
	Retrieve historical campaign performance performance benchmarks
	such as CTR, conversion rate, and ROAS for a segment and channel.
	"""
)
def get_campaign_benchmarks(
	segment: str,
	channel: str
	):

	return get_campaign_benchmarks_tool(
		segment,
		channel
	)

@mcp.tool(
	description=
	"""
	Predict expected campaign performance metrics including CTR,
	conversion rate, and ROAS based on message quality and historical benchmarks.
	"""
)
def predict_campaign_performance(
	customer: dict,
	product: str,
	channel: str,
	message: str,
	campaign_benchmarks: dict
	):

	return predict_campaign_performance_tool(
		customer,
		product,
		channel,
		message,
		campaign_benchmarks
	)
	

@mcp.tool(
	description=
	"""
	Save a generated marketing campaign into campaign history
	for future reference.
	"""
)
def save_campaign(
	customer: dict,
	product: str,
	channel: str,
	subject: str,
	message: str,
):

	return save_campaign_tool(
		customer,
		product=product,
		channel=channel,
		subject=subject,
		message=message
	)


if __name__ == "__main__":
    mcp.run()
