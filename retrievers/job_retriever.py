def create_job_retriever(
        vectorstore
):

    retriever = vectorstore(
        search_kwargs={
            "k": 10
        }
    )

    return retriever