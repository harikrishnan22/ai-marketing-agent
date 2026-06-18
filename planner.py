from openai import OpenAI
import json

client = OpenAI()

def create_plan(user_request):
	available_tools = [
		"generate_campaign",
		"predict_campaign_performance"
		]

	prompt = f"""
		You are an AI workflow planner.

		Available tools:
		
		{available_tools}

		Rules:

		- If the user wants to create, generate, build, or launch a campaign,
		return:
		"generate_campaign"

		- If the user wants to predict campaign performance, estimate results,
		forecast CTR, forecast conversion rate, forecast ROAS,
		or determine how well a campaign might perform,
		return:
		"predict_campaign_performance"

		- If the user says evaluate, analyze, assess, review, predict,
		forecast, or estimate campaign performance,
		return:
		"predict_campaign_performance"

		User Request:
		
		{user_request}

		Return JSON only.

		Examples:
	
		User:
		Create a campaign for Alice

		{{
			"steps": [
				"generate_campaign",
				]
		}}

		User:
		Predict campaign performance for Alice

		Output:
		{{
			"steps": [
				"predict_campaign_performance"
			]
		}}
		"""

	response = client.responses.create(
			model="gpt-4o-mini",
			input=prompt
			)

	cleaned = response.output_text

	cleaned = cleaned.replace("```json", "")
	cleaned = cleaned.replace("```", "")
	cleaned = cleaned.strip()

	return json.loads(cleaned)
