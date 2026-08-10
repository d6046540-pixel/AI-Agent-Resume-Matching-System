from langchain_core.documents import Document


def search_with_filter(
        vectorstore,
        query,
        metadata_filter=None
):


    docs = vectorstore.similarity_search(
        query,
        k=10,
        filter=metadata_filter
    )


    return docs