# modScholia

A modular Retrieval-Augmented Generation (RAG) system designed for scalable, context-aware document querying.

---

## Overview

modScholia enables efficient document understanding by combining semantic retrieval with local language models.

The system follows a modular architecture, allowing independent development, testing, and optimization of each component.

---

## Architecture

```
Ingestion → Vector Store → Retrieval → Pipeline → App
```

* Ingestion: Document loading and preprocessing
* Vector Store: Embedding storage using FAISS
* Retrieval: Context fetching via similarity search
* Pipeline: Orchestration of end-to-end flow
* App: Streamlit-based interface

---

## Project Structure

```
modScholia/
│── config/         
│── core/           
│── ingestion/      
│── retrieval/      
│── vectorstore/    
│── pipeline/       
│── utils/          
│── app.py          
│── requirements.txt
```

---

## Tech Stack

* Python
* FAISS (vector similarity search)
* Ollama (llama3 local LLM)
* Streamlit (interface)

---

## Installation

```bash
git clone https://github.com/imramen07/modScholia.git
cd modScholia
pip install -r requirements.txt
```

Prerequisite: Ollama with the `llama3` model running locally.

---

## Usage

```bash
streamlit run app.py
```

---

## How It Works

1. Documents are ingested and preprocessed
2. Text is converted into embeddings and stored in FAISS
3. User query is embedded into vector space
4. Relevant documents are retrieved via similarity search
5. Retrieved context and query are passed to the LLM
6. The generated response is returned through the interface

---

## Use Cases

* Educational assistants for querying notes and study material
* Internal knowledge bases for organizations
* Document question-answering systems
* Context aware chatbots grounded in data
* Semantic search over custom datasets

---

## Target Users

* Students exploring AI, ML, or NLP
* Developers building LLM-based applications
* Startups creating internal tools
* Researchers handling large document collections

---

## Features

* Modular RAG architecture
* Local LLM integration (no external API dependency)
* Efficient vector similarity search using FAISS
* Lightweight Streamlit interface

---

## Example

Query:
What is retrieval-augmented generation?

Response:
Retrieval-Augmented Generation combines information retrieval with language models to produce context-grounded and accurate responses.

---

## Future Improvements

* Add FastAPI backend for production deployment
* Improve retrieval ranking and relevance
* Introduce evaluation metrics
* Add logging and monitoring

---

## Author

https://github.com/imramen07
