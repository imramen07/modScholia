from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def split_docs(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
        # add - basic separators
        separators = ["\n\n", "\n", ". ", " ", ""],
        length_function = len
    )
    chunks = splitter.split_documents(pages)
    #add - filter out very small chunks (<50)
    # check behaviour
    chunks = [c for c in chunks if len(c.page_content.strip()) > 50]
    return chunks