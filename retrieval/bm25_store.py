from rank_bm25 import BM25Okapi
from utils.deduplication import deduplicate_docs

class BM25Store:
    
    def __init__(self, docs):
        self.docs = deduplicate_docs(docs)
        self.corpus = [doc.page_content.lower().split() for doc in self.docs]
        self.bm25 = BM25Okapi(self.corpus)
    
    def search(self, query, k = 5):
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            zip(self.docs, scores),
            key = lambda x: x[1],
            reverse = True
        )

        return [doc for doc, _ in ranked[:k]]