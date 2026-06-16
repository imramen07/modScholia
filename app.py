import sys
import subprocess
import streamlit as st
import hashlib
import os

from collections import defaultdict

import config.settings as config

from core.embeddings import init_and_load_embeddings
from core.llm import load_llm
from core.reranker import load_reranker

from ingestion.loader import pdf_loader
from ingestion.splitter import split_docs

from pipeline.context_builder import build_chat_context
from pipeline.intent import detect_intent
from pipeline.prompt_builder import build_prompt
from pipeline.query_rewriter import rewrite_query

from retrieval.rerank import rerank_docs
from retrieval.retriever import retrieve_docs
from retrieval.bm25_store import BM25Store

import utils.cuda as cuda
from utils.deduplication import deduplicate_docs
from utils.extract_relevance import extract_relevant_sentences
from utils.hashing import hash_files
from utils.ensure_gpu import ensure_gpu
from utils.render import initandrender_chat

from vectorstore.faiss_store import load_index, create_index

# init userdata for storing indexed files
# todo - check and maintain size of userdata
# like delete old files
os.makedirs("userdata", exist_ok = True)

@st.cache_data
# pull ollama version for ui/debug
def get_ollama_version():
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output = True,
            text = True
        )
        return result.stdout.strip()
    except Exception:
        return "Ollama not found"

# pull python version for ui/debug
python_version = sys.version.split(" ")[0]
# same for st
streamlit_version = st.__version__
# may affect performance
# keep after debug
if sys.version_info < (3, 10) or sys.version_info >= (3, 12):
    st.warning("Use Python 3.10 or 3.11 for best compatibility")

# page config
st.set_page_config(
    page_title = "Scholia AI",
    page_icon = "🥀",
    layout = "wide"
)
st.title("Scholia AI")

st.sidebar.title("Upload Document")
uploaded_files = st.sidebar.file_uploader(
    "Choose a PDF",
    type = "pdf",
    accept_multiple_files = True
)
# cpu/gpu
# shows cpu only
# todo - debug and optim gpu switch
st.sidebar.write(f"Device: {config.device}")

# init chat state
if "messages" not in st.session_state:
    st.session_state.messages = []
initandrender_chat()

# refactor - if else ref
# flow changed from v1
if not uploaded_files:
    st.info("Upload a PDF to start chat")
    st.stop()

# proceed with uploaded files
# hash all files to use as unique index
# sort of caching docs
fdata = [(f.name, f.read()) for f in uploaded_files]
fhash = hash_files(fdata)
newhash = hashlib.sha256(
    "".join(sorted(fhash.values())).encode()
    ).hexdigest()
# save in dir
index_dir = f"userdata/faiss_index_{newhash}"
# def file is changed
fileischanged = (
    "processed_file" not in st.session_state or
    st.session_state.processed_file != newhash
)

# init embedding loader
# and cache
@st.cache_resource
def C_init_and_load_embeddings(device):
    return init_and_load_embeddings(device)
embeddings = C_init_and_load_embeddings(config.device)

if fileischanged:
    with st.spinner("Indexing Document..."):
        # try pdfloader
        try:
            all_pages = []
            for name, data in fdata:
                all_pages.extend(pdf_loader(name, data))

        # pdfloader fallback
        # if add ocr, mod here
        except Exception as e:
            st.error(f"Error loading pdf: {e}")
            st.stop()

        # chunking
        chunks = split_docs(all_pages)
        st.sidebar.write(f"Total pages: {len(all_pages)}")
        st.sidebar.write(f"Chunks: {len(chunks)}")

        # init db
        db = create_index(chunks, embeddings, index_dir)
        st.session_state.db = db
        # set processed file as newhash
        # current file is now in session
        st.session_state.processed_file = newhash
        # clear chat context for new doc
        st.session_state.messages = []

        bm25_store = BM25Store(chunks)
        st.session_state.bm25 = bm25_store
        # save current chunks in state
        st.session_state.thischunks = chunks
        # gpu switch if avail
        st.session_state.db = ensure_gpu(st.session_state.db)
# index exists
# pull indexed file
else:
    # add - bm25 pulling
    if "db" not in st.session_state or "bm25" not in st.session_state:
        temp_db = load_index(embeddings, index_dir)
        if temp_db:
            # rebuild bm25 if faiss exists
            if "thischunks" in st.session_state:
                st.session_state.bm25 = BM25Store(st.session_state.thischunks)
            if st.session.state.db:
                st.session_state.db = ensure_gpu(st.session_state.db)
            else:
                st.error("Error State recovery, lost chunk refs")
                st.stop()
        # fallback - index not found
        else:
            st.error("Error Failed loading index. Try reupload")
            st.stop()
# atp db and processed file exists
st.sidebar.success("Document Ready");
st.sidebar.markdown("Built with 💗 by Ramen")
st.sidebar.markdown("---")
# show version
st.sidebar.caption(
    f"Python {python_version} | "
    f"Streamlit {streamlit_version} | "
    f"{get_ollama_version()}"
)

# llm, reranker loaders
# with caching
@st.cache_resource
def load_llm_cached():
    return load_llm()
llm = load_llm_cached()
@st.cache_resource
def load_reranker_cached(device):
    return load_reranker(device)
reranker = load_reranker_cached(config.device)

# chat input
query = st.chat_input("Ask Scholia")
if not query:
    st.stop()
query = query.strip()
if not query:
    st.stop()

# query pipeline
st.session_state.messages.append({"role": "user", "content": query})
st.chat_message("user").write(query)

# rewrite and retrieve
primary_query, query_variants = rewrite_query(query)     
db = st.session_state.db
all_docs = []
bm25_store = st.session_state.bm25

for q in query_variants:
    faiss_docs = retrieve_docs(db, q) or []
    bm25_docs = bm25_store.search(q, k = 5)
    all_docs.extend(faiss_docs)
    all_docs.extend(bm25_docs)
        
# retriever fallback
if not all_docs:
    # print(f"Retriever fail")
    response = "Not found in document"
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
    st.stop()

# context
top_docs = deduplicate_docs(all_docs)
# fallback - dedup fail
if not top_docs:
    # print(f"Dedup fail")
    response = "Not found in document"
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
    st.stop()

# rerank
rerank_query = query;
top_docs = rerank_docs(reranker, rerank_query, top_docs)

context, pages_used = extract_relevant_sentences(top_docs, primary_query)

# no context - fallback
# first doc - first page, 500chars
if not pages_used:
    top_doc = top_docs[0]
    page = top_doc.metadata.get("page", 0)
    source = top_doc.metadata.get("source", "Unknown")
    context = f"[{source} - Page {page}]\n{top_doc.page_content}"
    pages_used = [(source, page)]
        
#chat history, intent
chat_history = build_chat_context(st.session_state.messages)
intent = detect_intent(primary_query)
extra = {
    "summary": "Give a concise summary.",
    "explain": "Explain in simple terms.",
    "definition": "Give a clear definition."
}.get(intent, "")

#prompt
prompt = build_prompt(context, primary_query, extra, chat_history)

#llm response
with st.spinner("Thinking..."):
    response_placeholder = st.empty()
    full_response = ""

    try:
        for chunk in llm.stream(prompt):
            full_response += chunk
            response_placeholder.write(full_response)
            
    except Exception as e:
        st.error(f"LLM error: {e}")
        st.stop()

st.session_state.messages.append(
    {"role": "assistant", "content": full_response}
)

# copy response
with st.expander("Copy Latest Response"):
    st.text_area("Response", full_response, height = 150)
# show most relevant chunk
best_doc = top_docs[0]
source = best_doc.metadata.get("source", "Unknown")
best_page = best_doc.metadata.get("page", 0)
st.markdown("Most Relevant")
st.write(f"{source} - Page {best_page}")
st.write(best_doc.page_content[:300] + "...")

#sources, grouped
st.markdown("Sources")
grouped = defaultdict(list)
for src, pg in pages_used:
    grouped[src].append(pg)
for src in grouped:
    pages = sorted(grouped[src])
    st.write(f"{src}: Pages {', '.join(map(str, pages))}")