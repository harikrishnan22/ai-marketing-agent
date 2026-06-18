import pandas as pd
from openai import OpenAI

client = OpenAI()

# Load data
df = pd.read_csv("campaigns.csv")

# Calculate metrics
df["CTR"] = df["clicks"] / df["impressions"] * 100
df["conversion_rate"] = df["conversions"] / df["clicks"] * 100
df["ROAS"] = df["revenue"] / df["spend"]

# Convert data to text for GPT
summary = df[["campaign", "CTR", "conversion_rate", "ROAS"]].to_string(index=False)

prompt = f"""
You are a senior marketing analyst.

Here is the campaign performance data:

{summary}

Give:
1. Key insights
2. Best performing campaign
3. What to improve
4. Simple recommendation for budget allocation
"""

response = client.responses.create(
	model="gpt-4o-mini",
	input=prompt
)

print("\n=== AI INSIGHTS ===\n")
print(response.output_text)
