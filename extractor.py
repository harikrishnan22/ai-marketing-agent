from openai import OpenAI
import json

client = OpenAI()

def extract_entities(user_request):

	prompt = f"""
		Extract entities from the request.

		Request:
		{user_request}

		Return JSON only.

		{{
			"customer_name": "Alice"
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
