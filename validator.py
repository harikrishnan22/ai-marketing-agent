from openai import OpenAI
import json

client = OpenAI()

def validate_request(user_request):

	prompt = f"""
	You are a request validator.

	Decide if this request is relateed to a marketing assistant.

	Valid examples:
	- Create a campaign for Alice
	- Recommend products for Bob
	- Analyze customer behavior

	Invalid examples:
	- Tell me a joke
	- Random text
	- Weather today

	Return JSON only:

	{{
		"valid": true,
		"reason": "..."
	}}

	Request:
	
	{user_request}
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
