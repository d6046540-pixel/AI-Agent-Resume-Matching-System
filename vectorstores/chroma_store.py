from langchain_chroma import Chroma
import os


def load_vectorstore(
    embedding_model
):

    BASE_DIR = os.path.dirname(
        os.path.dirname(__file__)
    )


    DB_PATH = os.path.join(
        BASE_DIR,
        "resume_chroma_db"
    )


    #print(
        #"加载简历库路径:",
        #DB_PATH
    #)


    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model
    )


    return vectorstore