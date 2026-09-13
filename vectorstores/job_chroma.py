from pathlib import Path

from langchain_chroma import Chroma


# ============================================================
# 路径
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

JOB_DB_PATH = BASE_DIR / "job_chroma_db"

COLLECTION_NAME = "jobs"


# ============================================================
# 创建岗位向量库
# ============================================================

def create_job_vectorstore(
    chunks,
    embeddings
):
    """
    创建岗位 Chroma 向量数据库。
    """

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(JOB_DB_PATH),
        collection_name=COLLECTION_NAME
    )

    return vectorstore


# ============================================================
# 加载岗位向量库
# ============================================================

def load_job_vectorstore(
    embeddings
):
    """
    加载已经存在的岗位 Chroma 向量数据库。
    """

    vectorstore = Chroma(
        persist_directory=str(JOB_DB_PATH),
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    return vectorstore