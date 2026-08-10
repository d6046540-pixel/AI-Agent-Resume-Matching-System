from langchain_core.runnables import RunnablePassthrough


def create_rag_chain(
        retriever,
        prompt,
        llm
):

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        |
        prompt
        |
        llm
    )

    return chain