import asyncio
import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def parse_tool_results(result):
	return json.loads(result.content[0].text)

async def main():

	server_params = StdioServerParameters(
		command="/opt/homebrew/bin/python3",
		args=[
			"mcp_servers/marketing_server.py"
		],
		env=os.environ.copy()
	)

	async with stdio_client(server_params) as (read, write):

		async with ClientSession(read, write) as session:

			await session.initialize()

			tools = await session.list_tools()

			print("Available Tools:")

			for tool in tools.tools:
				print("-", tool)

			customer = parse_tool_results(
				await session.call_tool(
					"get_customer_by_name",
					{
						"customer_name": "Alice"
					}
				)
			)

			campaign_history = parse_tool_results(
				await session.call_tool(
					"get_campaign_history",
					{
						"customer": customer["customer"]
					}
				)
			)

			purchase_history = parse_tool_results(
				await session.call_tool(
					"get_purchase_history",
					{
						"customer": customer["customer"]
					}
				)
			)

			product_catalog = parse_tool_results(
				await session.call_tool(
					"get_product_catalog",
					{
						"segment": customer["segment"]
					}
				)
			)

			product = parse_tool_results(
				await session.call_tool(
					"recommend_product",
					{
						"customer": customer["customer"],
						"purchase_history": purchase_history["purchase_history"],
						"campaign_history": campaign_history["campaign_history"],
						"product_catalog": product_catalog["product_catalog"]
					}
				)
			)

			channel = parse_tool_results(
				await session.call_tool(
					"choose_channel",
					{
						"customer": customer["customer"],
						"purchase_history": purchase_history["purchase_history"],
						"product": product["product"]
					}
				)
			)

			similar_campaigns = parse_tool_results(
				await session.call_tool(
					"retrieve_similar_campaigns",
					{
						"customer": customer["customer"],
						"product": product["product"],
						"segment": customer["segment"]
					}
				)
			)

			campaign = parse_tool_results(
				await session.call_tool(
					"generate_campaign",
					{
						"customer": customer["customer"],
						"product": product["product"],
						"segment": customer["segment"],
						"channel": channel["channel"],
						"similar_campaigns": similar_campaigns["similar_campaigns"]
					}
				)
			)
			
			campaign_benchmarks = parse_tool_results(
				await session.call_tool(
					"get_campaign_benchmarks",
					{
						"segment": customer["segment"],
						"channel": channel["channel"]
					}
				)
			)

			campaign_performance = parse_tool_results(
				await session.call_tool(
					"predict_campaign_performance",
					{
						"customer": customer["customer"],
						"product": product["product"],
						"channel": channel["channel"],
						"message": campaign["message"],
						"campaign_benchmarks": campaign_benchmarks["campaign_benchmarks"]
					}
				)
			)		

			result = parse_tool_results(
				await session.call_tool(
					"save_campaign",
					{
						"customer": customer["customer"],
						"product": product["product"],
						"channel": channel["channel"],
						"subject": campaign["subject"],
						"message": campaign["message"]
					}
				)
			)

			print("\nTool Results:")
			print("\nCustomer:")
			print(customer)
			print("\nCampaign History:")
			print(campaign_history)
			print("\nPurchase History:")
			print(purchase_history)
			print("\nGet Product Catalog:")
			print(product_catalog)
			print("\nProduct:")
			print(product)
			print("\nChannel:")
			print(channel)
			print("\nSimilar Campaigns:")
			print(similar_campaigns)
			print("\nCampaign:")
			print(campaign)
			print("\nCampaign Benchmarks:")
			print(campaign_benchmarks)
			print("\nCampaign Performance:")
			print(campaign_performance)
			print("\nSave Campaign:")
			print(result)

if __name__ == "__main__":
	asyncio.run(main())
