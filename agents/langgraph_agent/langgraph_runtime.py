from typing import TypedDict, Annotated
from operator import add
import uuid
from agent_core.extractor import extract_entities
from agent_core.validator import validate_request
from agent_core.planner import create_plan
from agent_core.dependency_expander import expand_plan
from agent_core.executor import execute_plan
from langgraph.graph import StateGraph, END
from registry.tool_registry import TOOLS
from langgraph.checkpoint.sqlite import SqliteSaver
from core.config import AGENT_MEMORY_DB_PATH

class AgentState(TypedDict):

	user_request: str
	valid: bool
	reason: str
	raw_plan: dict
	expanded_plan: list
	context: dict
	approved: bool
	feedback: str
	messages: Annotated[list, add]

def validate_node(state):

	result = validate_request(
		state["user_request"]
	)

	state["valid"] = result["valid"]

	state["reason"] = result.get("reason", "")

	return state

def inspect_memory_node(state):

	print("\n===== STATE DEBUG =====")

	print("\nRequest:")
	print(state.get("user_request"))

	print("\nMessages:")	
	for msg in state.get("messages", [])[-3:]:
		print(msg)

	print("\nContext Keys:")
	print(list(state.get("context", {}).keys()))

	print("\n=======================")

	return state

def error_node(state):

	print(f"Validation failed: {state['reason']}")

	return state

def validation_router(state):

	if state["valid"]:
		return "extractor"

	return "error"

def extractor_node(state):

	extracted = extract_entities(
		state["user_request"]
	)

	state["context"].update(extracted)

	return state

def planner_node(state):

	state["raw_plan"] = create_plan(
		state["user_request"]
	)

	return state

def dependency_node(state):

	state["expanded_plan"] = expand_plan(
		state["raw_plan"]["steps"]
	)

	return state

def executor_node(state):

	state["context"] = execute_plan(
		state["expanded_plan"],
		state["context"]
	)

	return state

def approval_node(state):

	campaign = state["context"]

	print("\nCampaign Generated:")
	print("---------------------")

	print(
		campaign.get("subject")
	)

	print(
		campaign.get("message")
	)

	answer = input(
		"\nApprove campaign? (yes/no):"
	)

	state["approved"] = (
		answer.lower() == "yes"
	)

	if "messages" not in state:
		state["messages"] = []

	state["messages"].append(
		f"""
		Campaign:
		{campaign.get("subject")}

		Approved:
		{state["approved"]}
		"""
	)

	return state

def approval_router(state):

	if state["approved"]:
		return "save"
	
	return "regenerate"

def save_node(state):

	result = TOOLS["save_campaign"]["function"](
		customer=state["context"]["customer"],
		product=state["context"]["product"],
		channel=state["context"]["channel"],
		subject=state["context"]["subject"],
		message=state["context"]["message"]
	)

	state["context"].update(result)

	return state

def regenerate_node(state):

	feedback = input(
		"What should change? "
	)

	state["context"]["feedback"] = feedback

	state["context"].pop("subject", None)
	state["context"].pop("message", None)
	state["context"].pop("cta", None)

	return state

def generate_campaign_node(state):

	tool = TOOLS["generate_campaign"]

	inputs = tool["inputs"]

	args = {}

	for input_name in inputs:
		args[input_name] = state["context"][input_name]

	result = tool["function"](**args)

	state["context"].update(result)
	print(state["context"])
	return state

graph = StateGraph(AgentState)

graph.add_node("validator", validate_node)
graph.add_node("inspect_memory_node", inspect_memory_node)
graph.add_node("error", error_node)
graph.add_node("extractor", extractor_node)
graph.add_node("planner", planner_node)
graph.add_node("dependencies", dependency_node)
graph.add_node("executor", executor_node)
graph.add_node("approval", approval_node)
graph.add_node("save", save_node)
graph.add_node("regenerate", regenerate_node)
graph.add_node("generate_campaign", generate_campaign_node)

graph.set_entry_point("inspect_memory_node")

graph.add_edge("inspect_memory_node", "validator")

graph.add_conditional_edges(
	"validator",
	validation_router,
	{
		"extractor": "extractor",
		"error": "error"
	}
)

graph.add_edge("error", END)
graph.add_edge("extractor", "planner")
graph.add_edge("planner", "dependencies")
graph.add_edge("dependencies", "executor")
graph.add_edge("executor", "approval")

graph.add_conditional_edges(
	"approval",
	approval_router,
	{
		"save": "save",
		"regenerate": "regenerate"
	}
)

graph.add_edge("save", END)
graph.add_edge("regenerate", "generate_campaign")
graph.add_edge("generate_campaign", "approval")

user_request = input("How can I help?")

with SqliteSaver.from_conn_string(
	str(AGENT_MEMORY_DB_PATH)
) as memory:

	app = graph.compile(
		checkpointer=memory
	)

	thread_id = "marketing_session"

	result = app.invoke(
		{
			"user_request": user_request,
			"context": {
				"feedback": None
			}
		},
		config={
			"configurable": {
				"thread_id": thread_id
			}
		},
	)

print(result)
