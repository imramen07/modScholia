import torch
import os
from dotenv import load_dotenv

# use env variables instead of hardcoding values
load_dotenv()

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))

# todo - try bge large with mistral or phi3
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
RERANK_MODEL = os.getenv("RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")

# 3 - X
# 4 - very less context
# 5 - fine
# 6 - slight out of context
# 7 - X
TOP_K = int(os.getenv("TOP_K", "5"))

# get atleast double more of tops to handle explanation and non matching queries
FETCH_K = int(os.getenv("FETCK_K", "10"))

env_device = os.getenv("DEVICE", "auto")
if env_device == "auto":
    device = "cuda" if torch.cuda.is_available() else "cpu"
else:
    # handle exceptional returns
    device = env_device if env_device in ("cuda", "cpu") else "cpu"

# added - v2
# simple / nltk
BM25_TOK = os.getenv("BM25_TOK", "simple")
# use 0.5 if longer context usecase
THRESHOLD_RERANK = float(os.getenv("THRESHOLD_RERANK", "0.6"))
OLLAMA_BASEURL = os.getenv("OLLAMA_BASEURL", "http://localhost:11434")