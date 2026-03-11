from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from ingestion import embeddings
from google import genai
from google.genai import types
import os
input_query = input("> ")

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="rag-genai",
    url="http://localhost:6333",
)

searchResult = qdrant.similarity_search(input_query)
# print(searchResult)

page_contents = [res.page_content for res in searchResult]
print(page_contents)

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

print(response.text)