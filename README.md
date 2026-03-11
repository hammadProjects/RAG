# Basic RAG Pipeline – Indexing, Retrieval, Generation

This project demonstrates a minimal **Retrieval-Augmented Generation (RAG)** pipeline built using **LangChain**, **Google Gemini embeddings**, and **Qdrant** as the vector database.

The system implements the three fundamental stages of a RAG architecture:

1. Document ingestion and indexing
2. Vector similarity retrieval
3. Context-based generation

A PDF document is ingested, split into chunks, embedded using the Gemini embedding model, and stored in a Qdrant vector database. When a user submits a query, the system retrieves the most relevant chunks using vector similarity search.

This repository focuses on demonstrating the **core infrastructure of a RAG system** in a clean and simple implementation.

---

## System Overview

The pipeline works as follows:

1. A PDF document is loaded into the system.
2. The document is split into manageable chunks.
3. Each chunk is converted into embeddings using Gemini embeddings.
4. The embeddings are stored inside a Qdrant vector database.
5. A user query is embedded using the same embedding model.
6. The vector database performs similarity search.
7. Relevant document chunks are returned as context.

This architecture forms the foundation for building more advanced retrieval-based AI systems.

---

## Architecture

The system consists of three primary layers.

### Document Ingestion

Responsible for:

- Loading source documents
- Splitting text into chunks
- Generating embeddings
- Storing vectors in Qdrant

### Vector Database

Qdrant stores vector representations of document chunks and enables fast similarity search using cosine distance.

### Retrieval Layer

The retrieval layer takes user queries, generates embeddings, and searches the vector database for the most relevant document chunks.

---

## Tech Stack

### Language

- Python 3.11+

### LLM and Embeddings

- Google Gemini API
- langchain-google-genai

### RAG Framework

- LangChain

### Vector Database

- Qdrant

### Containerization

- Docker
- Docker Compose

---

## Project Structure

```
.
├── ingestion.py
├── retrieve.py
├── docker-compose.yml
├── requirements.txt
├── oop.pdf
├── qdrant_storage/
└── .gitignore
```

### File Descriptions

**ingestion.py**

Responsible for the indexing pipeline.

- Loads the PDF document
- Splits text into chunks
- Generates embeddings
- Stores vectors in Qdrant

**retrieve.py**

Handles query-time retrieval.

- Accepts a user query
- Performs similarity search
- Returns relevant document chunks

**docker-compose.yml**

Runs a local Qdrant vector database instance.

**oop.pdf**

Example document used for indexing.

---

## Environment Variables

Create a `.env` file in the project root.

```
GOOGLE_API_KEY=your_google_api_key
```

This key is used for generating embeddings and interacting with the Gemini API.

---

## Running Qdrant

Start the Qdrant vector database using Docker.

```bash
docker compose up -d
```

Qdrant will run at:

```
http://localhost:6333
```

Vector database data is persisted in:

```
./qdrant_storage
```

---

## Installation

Clone the repository and install dependencies.

```bash
git clone https://github.com/hammadProjects/RAG
cd RAG

pip install -r requirements.txt
```

---

## Step 1: Index the Document

Run the ingestion pipeline to load the PDF and store embeddings in Qdrant.

```bash
python ingestion.py
```

This step performs:

- PDF loading
- Document chunking
- Embedding generation
- Vector storage

The Qdrant collection created is named:

```
rag-genai
```

---

## Step 2: Run Retrieval

After indexing the document, run the retrieval script.

```bash
python retrieve.py
```

You will be prompted for a query.

Example:

```
> What is polymorphism?
```

The system will return the most relevant document chunks retrieved from the vector database.

---

## Document Processing Details

### Chunking Strategy

| Parameter     | Value           |
| ------------- | --------------- |
| Chunk Size    | 1000 characters |
| Chunk Overlap | 200 characters  |

Overlapping chunks help preserve context between sections and improve retrieval accuracy.

### Embedding Model

```
gemini-embedding-001
```

### Vector Distance Metric

```
Cosine similarity
```

---

## Future Improvements

Potential improvements for this project include:

- Query translation
- Query routing
- Hybrid retrieval (BM25 + vector search)
- Cross-encoder reranking
- Citation enforcement
- CI-gated evaluation pipeline
- Domain-specific "Ask My Docs" system
- RAG evaluation using RAGAS

---

## License

MIT License
