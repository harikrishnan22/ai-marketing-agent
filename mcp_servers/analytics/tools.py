from mcp.server.fastmcp import FastMCP
from tools.tools import (
	get_campaign_benchmarks as get_campaign_benchmarks_tool,
	predict_campaign_performance as predict_campaign_performance_tool,
)

def register_analytics_tools(mcp):

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
