from mcp.server.fastmcp import FastMCP

from mcp_servers.customer.tools import register_customer_tools
from mcp_servers.marketing.tools import register_marketing_tools
from mcp_servers.analytics.tools import register_analytics_tools

mcp = FastMCP("marketing-agent")

register_customer_tools(mcp)
register_marketing_tools(mcp)
register_analytics_tools(mcp)

if __name__ == "__main__":
	mcp.run()
