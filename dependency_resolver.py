from tool_registry import TOOLS

def resolve_dependencies(plan):
	
	available_data = {"customer_name"}

	final_plan = []

	remaining_tools = plan.copy()

	while remaining_tools:
		
		progress = False

		for tool_name in remaining_tools[:]:

			tool = TOOLS[tool_name]

			required_inputs = set(tool["inputs"])

			if required_inputs.issubset(available_data):
	
				final_plan.append(tool_name)

				available_data.update(tool["outputs"])

				remaining_tools.remove(tool_name)

				progress = True

		if not progress:
			raise Exception(
				 "Cannot resolve dependencies: {remaining_tools}"
			)

	return final_plan 
