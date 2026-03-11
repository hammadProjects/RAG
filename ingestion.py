from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from pprint import pp
import os
import time
load_dotenv()
# To prevent hitting rate limit - process big docs in batches
batch_size = 50
chunk_load_size = 80 # How many chunks of the splitted docs should load

# init api key & quadrant client
# get the file path
api_key = os.getenv("GOOGLE_API_KEY")
filePath = Path(__file__).parent / "oop.pdf"
quadrant_client = QdrantClient("localhost", port=6333)

# load and split the pdf into chunks
loader = PyPDFLoader(file_path=filePath)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(loader.load()[:chunk_load_size])

# create embedder for the qdrant_db - qdrant will automatically create embeddings and store
embeddings = GoogleGenerativeAIEmbeddings(
    api_key = api_key,
    model="gemini-embedding-001",
)

# Get size of embeddings of current model
vector_size = len(embeddings.embed_query("dummy query"))
if not quadrant_client.collection_exists("rag-genai"):
    quadrant_client.create_collection(
        "rag-genai", 
        vectors_config=VectorParams(size=vector_size,distance=Distance.COSINE)
    )

# qdrant vector store init
vector_store = QdrantVectorStore(
    collection_name="rag-genai",
    embedding=embeddings,
    client=quadrant_client,
)

for i in range(0, len(docs), batch_size):
    batch = docs[i:i+batch_size]
    vector_store.add_documents(batch)
    time.sleep(60)
