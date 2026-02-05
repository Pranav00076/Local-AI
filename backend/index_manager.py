import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from .config import DATA_DIR, STORAGE_DIR, EMBED_MODEL

Settings.node_parser = SentenceSplitter(
    chunk_size=700,
    chunk_overlap=200
)

embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)
Settings.embed_model = embed_model


def load_docs():
    return SimpleDirectoryReader(DATA_DIR).load_data()


def load_or_build():

    if os.path.exists(STORAGE_DIR) and os.listdir(STORAGE_DIR):
        storage = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
        return load_index_from_storage(storage)

    docs = load_docs()

    index = VectorStoreIndex.from_documents(
        docs,
        embed_model=embed_model
    )

    index.storage_context.persist(STORAGE_DIR)
    return index


def rebuild():
    docs = load_docs()

    index = VectorStoreIndex.from_documents(
        docs,
        embed_model=embed_model
    )

    index.storage_context.persist(STORAGE_DIR)
    return index
