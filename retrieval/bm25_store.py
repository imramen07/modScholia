# major changes
# using nltk for better tokenization
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from rank_bm25 import BM25Okapi
from utils.deduplication import deduplicate_docs

# set stopwords using nltk
swords = set(stopwords.words('english'))

class BM25Store:
    
    def __init__(self, docs):
        self.docs = deduplicate_docs(docs)
        self.corpus = [self.thisTokenize(doc.page_content) for doc in self.docs]
        self.bm25 = BM25Okapi(self.corpus)
    
    # add - tokenizer
    def thisTokenize(self, text):
        toks = word_tokenize(text.lower())
        return[
            t for t in toks if t.isalnum() and
            t not in swords
        ]

    def search(self, query, k = 5):
        #tokenized_query = query.lower().split()
        tokedQuery = self.thisTokenize(query)
        scores = self.bm25.get_scores(tokedQuery)

        ranked = sorted(
            zip(self.docs, scores),
            key = lambda x: x[1],
            reverse = True
        )

        return [doc for doc, _ in ranked[:k]]