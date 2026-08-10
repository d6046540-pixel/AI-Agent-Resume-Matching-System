from langchain_chroma import Chroma


JOB_DB_PATH = "./job_chroma_db"



def create_job_vectorstore(
        chunks,
        embeddings
):

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=JOB_DB_PATH
    )


    return vectorstore



def load_job_vectorstore(
        embeddings
):

    vectorstore = Chroma(
        persist_directory=JOB_DB_PATH,
        embedding_function=embeddings
    )


    return vectorstore