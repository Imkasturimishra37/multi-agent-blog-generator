def retrieve_context(vector_store, query: str, k: int = 4):
    """
    Retrieve the most relevant chunks from the vector store.
    """

    docs = vector_store.similarity_search(
        query,
        k=k
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context
