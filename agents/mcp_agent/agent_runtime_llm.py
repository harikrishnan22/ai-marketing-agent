import json
import asyncio
import os 
import time

from openai import OpenAI

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

client = OpenAI()

server_params = StdioServerParameters(
	command="/opt/homebrew/bin/python3",
	args=["-m", "mcp_servers.server"],
	env=os.environ.copy()
)

async def get_tools(session):

	tools = await session.list_tools()

	openai_tools = []

	for tool in tools.tools:

		openai_tools.append(
		{
			"type": "function",
			"name": tool.name,
			"description": tool.description,
			"parameters": tool.inputSchema
		}
	)

	return openai_tools

async def execute_tool(
	session,
	name,
	arguments
):

	print(f"Executing {name}")

	result = await session.call_tool(
		name,
		arguments
	)

	return result.content[0].text

async def run_agent_async(user_request):

	async with stdio_client(server_params) as (read, write):

		async with ClientSession(read, write) as session:

			print("1. MCP Connected")

			await session.initialize()

			print("2. MCP Initialized")

			tools = await get_tools(session)

			print("3. Tools Loaded")
			print(f"{len(tools)} tools found")

			print("4. Generating plan")

			print("Calling OpenAI for plan...")

			start = time.time()

			plan_response = client.responses.create(
				model="gpt-5-mini",
				input=f"""
				You are a planner.

				User Request:
				{user_request}

				Return ONLY valid JSON.

				To create campaigns:

				1. Find customer
				2. Retrieve campaign history
				3. Retrieve purchase history
				4. Retrieve product catalog
				5. Recommend product
				6. Choose channel
				7. Retieve similar campaigns
				8. Generate campaign
				9. Retrieve benchmarks
				10. Predict performance

				Schema:

				{{
					"steps": [
						"step1",
						"step2"
					]
				}}

				Do NOT create campaigns.
				Do NOT explain.
				Do NOT generate marketing content.
				Do NOT return context.
				Do NOT return assumptions.
				Do NOT return anything except the steps array.
				"""
			)

			print(
				"Planning took:",
				round(time.time() - start, 2),
				"second"
			)

			plan = json.loads(plan_response.output_text)

			print(f"Plan recieved, {plan}")

			response = client.responses.create(
				model="gpt-5",
				instructions="""
				You are an AI Marketing Agent.

				Follow this execution plan:

				{json.dumps(plan, indent=2)}

				You MUST use tools.
				Do not describe tool calls.
				Actually call them.

				Store intermediate results.
				""",
				input=user_request,
				tools=tools
			)

			context = {}

			while True:

				tool_calls = [
					item
					for item in response.output
					if item.type == "function_call"
				]

				if not tool_calls:

					return {
						"response": response.output_text,
						"context": context,
						"plan": plan,
					}

				outputs = []

				for call in tool_calls:

					print("\n" + "-" * 80)
					print("TOOL CALL")
					print("-" * 80)

					print("Tool:", call.name)
					print("Arguments:", call.arguments)

					args = json.loads(call.arguments)
				
					print("Calling tool...")

					result = await execute_tool(
						session,
						call.name,
						args
					)

					print("\nTool returned:")
					print(result)

					try:

						parsed = json.loads(result)

						context.update(parsed)

					except:

						pass

					outputs.append(
						{
							"type": "function_call_output",
							"call_id": call.call_id,
							"output": result
						}
					)

				response = client.responses.create(
					model="gpt-5",
					previous_response_id=response.id,
					input=outputs,
					tools=tools
				)

def run_agent(user_request):

	return asyncio.run(
		run_agent_async(user_request)
	)

if __name__ == "__main__":

	result = run_agent(
		"Create a campaign for Alice and assess its performance."
	)

	print("\n" + "=" * 80)
	print("FINAL RESPONSE")
	print("=" * 80)

	print(result["response"])

	print("\n" + "=" * 80)
	print("CONTEXT")
	print("=" * 80)

	print(json.dumps(
		result["context"],
		indent=2
	))

	print("\n" + "=" * 80)
	print("PLAN")
	print("=" * 80)

	print(json.dumps(
		result["plan"],
		indent=2
	))

