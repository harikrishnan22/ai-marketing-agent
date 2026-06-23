from registry.tool_registry import TOOLS
from agent_core.planner import create_plan
from agent_core.extractor import extract_entities
from agent_core.validator import validate_request
from agent_core.dependency_expander import expand_plan

#user_request = input("How can I help?")

def run_agent(user_request):

	check = validate_request(user_request)

	if not check["valid"]:
		print(f"Request rejected: {check['reason']}")
		exit()
	
	context = {
		"feedback": None
	}
	context.update(
		extract_entities(user_request)
	)

	raw_plan = create_plan(user_request)

	#print("\nRAW PLAN")
	#print(raw_plan)

	expanded_plan = expand_plan(raw_plan["steps"])

	#print("\nEXPANDED PLAN")
	#print(expanded_plan)

	for tool_name in expanded_plan:
	
		tool = TOOLS[tool_name]

		inputs = tool["inputs"]

		args = {}

		for input_name in inputs:
			args[input_name] = context[input_name]

		result = tool["function"](**args)

		if "error" in result:
			print("\nERROR:")
			print(result["error"])
			break
	
		context.update(result)

		#print(f"\nRan {tool_name}")
		#print("Input:", inputs)
		#print("Output:", result)

	#print("\nFINAL CONTEXT")
	#print(context)

	return {
		"raw_plan": raw_plan,
		"expanded_plan": expanded_plan,
		"context": context
	}
