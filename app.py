import sys
import subprocess
import streamlit as st
import hashlib

from collections import defaultdict

import config.settings as config

from core.embeddings import load_embeddings
from core.llm import load_llm
from core.reranker import load_reranker

from ingestion.loader import load_pdf
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
from utils.render import render_chat

from vectorstore.faiss_store import load_index, create_index

@st.cache_data
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

python_version = sys.version.split(" ")[0]
streamlit_version = st.__version__

if sys.version_info < (3, 10) or sys.version_info >= (3, 12):
    st.warning("Use Python 3.10 or 3.11 for best compatibility")

st.set_page_config(
    page_title = "Scholia AI",
    page_icon = "🥀",
    layout = "wide"
)
st.title("Scholia AI")

#get files
st.sidebar.title("Upload Document")
uploaded_files = st.sidebar.file_uploader(
    "Choose a PDF",
    type = "pdf",
    accept_multiple_files = True
)

st.sidebar.write(f"Device: {config.device}")

#chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

render_chat()

if uploaded_files:
    file_data = [(f.name, f.read()) for f in uploaded_files]

    file_hashes = hash_files(file_data)
    combined_hash = hashlib.sha256(
        "".join(sorted(file_hashes.values())).encode()
        ).hexdigest()

    index_dir = f"faiss_index_{combined_hash}"

    file_changed = (
        "processed_file" not in st.session_state or
        st.session_state.processed_file != combined_hash
    )

    #loader
    @st.cache_resource
    def load_embeddings_cached(device):
        return load_embeddings(device)
    
    embeddings = load_embeddings_cached(config.device)

    if file_changed:
        with st.spinner("Indexing Document..."):
            try:
                all_pages = []

                for name, data in file_data:
                    all_pages.extend(load_pdf(name, data))

            except Exception as e:
                st.error(f"Error loading pdf: {e}")
                st.stop()

            chunks = split_docs(all_pages)

            st.sidebar.write(f"Total pages: {len(all_pages)}")
            st.sidebar.write(f"Chunks: {len(chunks)}")

            db = create_index(chunks, embeddings, index_dir)

            st.session_state.db = db
            st.session_state.processed_file = combined_hash
            st.session_state.messages = []

            bm25_store = BM25Store(chunks)
            st.session_state.bm25 = bm25_store

            st.session_state.db = ensure_gpu(st.session_state.db)

    else:
        if "db" not in st.session_state:
            st.session_state.db = load_index(embeddings, index_dir)

            st.session_state.db = ensure_gpu(st.session_state.db)

    st.sidebar.success("Document Ready");
    st.sidebar.markdown("Built with 💗 by Ramen")

    st.sidebar.markdown("---")
    st.sidebar.caption(
        f"Python {python_version} | "
        f"Streamlit {streamlit_version} | "
        f"{get_ollama_version()}"
    )

    #loaders
    @st.cache_resource
    def load_llm_cached():
        return load_llm()
    llm = load_llm_cached()

    @st.cache_resource
    def load_reranker_cached(device):
        return load_reranker(device)
    reranker = load_reranker_cached(config.device)

    #input
    query = st.chat_input("Ask Scholia")

    if not query:
        st.stop()

    query = query.strip()
    if not query:
        st.stop()

    #query pipeline
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        st.chat_message("user").write(query)

        primary_query, query_variants = rewrite_query(query)

        if "db" not in st.session_state:
            st.warning("Please upload and index a PDF first.")
            st.stop()
        
        db = st.session_state.db

        #multiquery retrieval
        all_docs = []

        bm25_store = st.session_state.bm25

        for q in query_variants:
            faiss_docs = retrieve_docs(db, q) or []
            bm25_docs = bm25_store.search(q, k = 5)

            all_docs.extend(faiss_docs)
            all_docs.extend(bm25_docs)

        #not retrieved
        if not all_docs:
            response = "Not found in document"
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
            st.stop()

        #context
        top_docs = deduplicate_docs(all_docs)

        #fallback
        if not top_docs:
            response = "Not found in document"
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
            st.stop()

        #rerank
        rerank_query = query;
        top_docs = rerank_docs(reranker, rerank_query, top_docs)

        context, pages_used = extract_relevant_sentences(top_docs, primary_query)

        #not context / fallaback
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

        #llm
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

        #output
        with st.expander("Copy Latest Response"):
            st.text_area("Response", full_response, height = 150)

        best_doc = top_docs[0]
        source = best_doc.metadata.get("source", "Unknown")
        best_page = best_doc.metadata.get("page", 0) + 1

        st.markdown("Most Relevant")
        st.write(f"{source} - Page {best_page}")
        st.write(best_doc.page_content[:300] + "...")

        #sources
        st.markdown("Sources")
        grouped = defaultdict(list)
        for src, pg in pages_used:
            grouped[src].append(pg)
        
        for src in grouped:
            pages = sorted(grouped[src])
            st.write(f"{src}: Pages {', '.join(map(str, pages))}")

else:
    st.info("Upload a PDF to start chat")