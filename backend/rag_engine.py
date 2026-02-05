from llama_index.llms.ollama import Ollama

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

from llama_index.core.postprocessor import (
    SimilarityPostprocessor,
    SentenceTransformerRerank
)

from .config import MODEL_NAME


# ---------- Retrieval Controls ----------

VECTOR_TOP_K = 12
SIMILARITY_CUTOFF = 0.55
RERANK_TOP_N = 5
CONFIDENCE_MIN_SCORE = 0.20


# ---------- Build Engine ----------

def build_query_engine(index):

    # ----- base retriever -----

    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=VECTOR_TOP_K
    )

    # ----- semantic similarity filter -----

    similarity_filter = SimilarityPostprocessor(
        similarity_cutoff=SIMILARITY_CUTOFF
    )

    # ----- cross-encoder reranker -----

    reranker = SentenceTransformerRerank(
        model="cross-encoder/ms-marco-MiniLM-L-6-v2",
        top_n=RERANK_TOP_N
    )

    # ----- LLM -----

    llm = Ollama(
        model=MODEL_NAME,
        temperature=0.2
    )

    # ----- query engine with hook chain -----

    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        llm=llm,
        node_postprocessors=[
            similarity_filter,   # semantic filter
            reranker             # rerank hook
        ],
        response_mode="compact"
    )

    return query_engine
