from mcp.server.fastmcp import FastMCP
from tools.tools import (
	get_customer_by_name as get_customer_by_name_tool,
	get_purchase_history as get_purchase_history_tool,
	get_campaign_history as get_campaign_history_tool,
	get_product_catalog as get_product_catalog_tool,
)

def register_customer_tools(mcp):

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
