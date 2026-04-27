import torch

CHUNK_SIZE = 300
CHUNK_OVERLAP = 80

EMBEDDING_MODEL = "BAAI/bge-small-en"
LLM_MODEL = "llama3"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

TOP_K = 5
FETCH_K = 10

torch.set_num_threads(4)
device = "cuda" if torch.cuda.is_available() else "cpu"