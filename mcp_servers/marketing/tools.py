from mcp.server.fastmcp import FastMCP
from tools.tools import (
	recommend_product as recommend_product_tool,
	choose_channel as choose_channel_tool,
	retrieve_similar_campaigns as retrieve_similar_campaigns_tool,
	generate_campaign as generate_campaign_tool,
	save_campaign as save_campaign_tool
)

def register_marketing_tools(mcp):

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
