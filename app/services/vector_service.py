import chromadb

from sentence_transformers import (
    SentenceTransformer
)

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="study_documents"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embedding(text: str):
    embedding = embedding_model.encode(
        text
    )

    return embedding.tolist()


def add_document_chunk(
    chunk_id: str,
    content: str,
    document_id: int
):
    embedding = create_embedding(
        content
    )

    collection.add(
        ids=[chunk_id],
        documents=[content],
        embeddings=[embedding],
        metadatas=[
            {
                "document_id": document_id
            }
        ]
    )


def search_similar_chunks(
    query: str,
    document_id: int,
    limit: int = 3
):
    query_embedding = create_embedding(
        query
    )

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=limit,
        where={
            "document_id": document_id
        }
    )

    return results["documents"][0]