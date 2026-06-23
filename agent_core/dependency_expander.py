from registry.tool_registry import TOOLS

def find_tool_that_produces(output_name):

	for tool_name, tool in TOOLS.items():
	
		if output_name in tool["outputs"]:
			return tool_name

	return None

def expand_tool(tool_name, expanded):
	
	tool = TOOLS[tool_name]
	for required_input in tool["inputs"]:
	
		producer = find_tool_that_produces(required_input)

		if producer:
			expand_tool(producer, expanded)

	if tool_name not in expanded:
		expanded.append(tool_name)

def expand_plan(plan):
	
	expanded = []

	for tool_name in plan:
		expand_tool(tool_name, expanded)

	return expanded
