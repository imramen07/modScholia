# modScholia

modScholia is a modularized and enhanced version of the original Scholia-AI.  
It is a RAG-based QnA bot that generates responses based on the context of uploaded PDF documents.

---

## Why is it Different

- Uses hybrid retrieval with BM25 and FAISS vector search for efficient retrieval
- Uses reranking mechanisms for improved retrieval accuracy
- Rewrites queries for more precise and context aware responses
- Supports CUDA acceleration and caching
- Validates responses with proper sources and page numbers

---

## Installation

### Preferred Versions

- Python 3.10 – 3.11
- Streamlit 1.57
- Ollama 0.21

### Install Dependencies

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Ollama Setup

Requires `llama3` installed locally using Ollama.

### Install Ollama

- [Ollama Llama 3 Library](https://ollama.com/library/llama3)

### Pull and Run llama3

```bash
ollama pull llama3
ollama run llama3
```

---

## Pipeline

```text
PDF Upload
    ↓
PDF Loading
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Vector Database Storage
    ↓
Query Embedding
    ↓
Vector Similarity Search
    ↓
Reranking
    ↓
Context Selection
    ↓
LLM Prompting
    ↓
Response Generation
```

---

## Use Cases

- Academic PDF question answering
- Large document search and summarization
- Personalized local RAG experimentation
- Multiple PDF semantic retrieval

---

## Future Improvements

- Integrate FastAPI backend and reduce Streamlit dependency

---

## Author

Ramen
