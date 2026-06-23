from registry.tool_registry import TOOLS

def execute_plan(plan, context):

    for tool_name in plan:

        tool = TOOLS[tool_name]

        inputs = tool["inputs"]

        args = {}

        for input_name in inputs:
            args[input_name] = context[input_name]

        result = tool["function"](**args)

        if "error" in result:
            raise Exception(result["error"])

        context.update(result)

    return context
