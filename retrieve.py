from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from ingestion import embeddings
from google import genai
from google.genai import types
from prompts import generate_fanout_system_prompt
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

input_query = input("> ")
# Query Translation Parallel Query Fanout

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="oop",
    url="http://localhost:6333",
)

# 1. Generate Queries by LLM

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=input_query,
    config=types.GenerateContentConfig(
        system_instruction=generate_fanout_system_prompt(input_prompt=input_query, doc="oop in c++"),
        response_mime_type="application/json",
        response_schema=list[str]
    ),
)

queries = response.parsed
searchResult = []
print(f"Queries Created: {queries}")

for query in queries:
    docs = qdrant.similarity_search(query)
    searchResult.extend(docs)

unique_docs = {doc.metadata["_id"]: doc for doc in searchResult}.values()
page_contents = [doc.page_content for doc in unique_docs]
print(f"Unique Response {unique_docs}")

# Fanout - End

system_prompt = f"""
You are an helpful AI assistant who will help users navigating with the docs.
You are given a context. Which you have to consider as a source of truth. Do not add anything from your own.
If you have relevant data then you can refine the answers.

Context:
{page_contents}
"""

config = types.GenerateContentConfig(
    system_instruction=system_prompt
)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=input_query,
    config=config,
)

print(f"Final Response {response.text}")