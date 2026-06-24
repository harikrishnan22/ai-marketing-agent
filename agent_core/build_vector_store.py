import sqlite3
import pandas as pd
from openai import OpenAI
import chromadb
from core.config import MARKETING_DB_PATH
from core.config import CHROMA_PATH

client = chromadb.PersistentClient(
	path=CHROMA_PATH
)

collection = client.get_or_create_collection(
	name="campaigns"
)

client_openai = OpenAI()

conn = sqlite3.connect(MARKETING_DB_PATH)

campaigns = pd.read_sql_query(
	"""
	SELECT *
	FROM campaign_history
	""",
	conn
)

for _, row in campaigns.iterrows():

	text = f"""
	Subject:
	{row['subject']}

	Message:
	{row['message']}
	"""

	embedding = client_openai.embeddings.create(
		model="text-embedding-3-small",
		input=text
	).data[0].embedding

	collection.add(
		ids=[
			str(row["campaign_id"])
		],
		documents=[
			text
		],
		embeddings=[
			embedding
		]
	)

def search_similar_campaigns(query):
	
	query_embedding = client_openai.embeddings.create(
		model="text-embedding-3-small",
		input=query
	).data[0].embedding

	results = collection.query(
		query_embeddings=[
			query_embedding
		],
		n_results=3
	)

	return results
