from langchain_core.documents import Document
from langchain_chroma import Chroma

from embeddings.embedding import get_embeddings


import os

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

RESUME_DB_PATH = os.path.join(
    BASE_DIR,
    "resume_chroma_db"
)

# =========================
# 我的简历数据
# =========================

resume = """
姓名：XXX

教育背景：
徐州工程学院
本科
大三学生

专业：
信息资源管理与信息系统


技术技能：

Python：
熟悉Python基础开发，能够进行AI应用开发。

大模型应用开发：
了解LLM API调用流程。
掌握Prompt Engineering。
理解System Prompt、Temperature、Token等概念。

Agent开发：
掌握LangChain、LangGraph。
理解Agent工作流程。
了解Tool Calling、多Agent协作。

RAG技术：
掌握RAG基本流程。
包括：
- 文档切分
- Embedding向量化
- Chroma向量数据库
- 相似度检索
- Query Rewrite
- Multi Query Retrieval
- Rerank


项目经历：

项目名称：
AI Agent岗位匹配系统


项目描述：

基于LangGraph构建AI招聘Agent系统。

系统包含：

1. 简历知识库

将个人简历转换为向量数据，
支持自然语言查询个人能力。


2. 岗位知识库

构建岗位数据库，
支持AI岗位检索。


3. RAG检索系统

使用BGE-small-zh-v1.5作为Embedding模型。

使用BGE-reranker进行结果重排序。


4. Agent工具调用

设计多个Tool：

resume_search：
查询个人简历信息。

job_search：
查询岗位信息。

job_match：
分析岗位匹配程度。


项目技术栈：

Python
LangChain
LangGraph
Chroma
BGE Embedding
Reranker
DeepSeek API


求职方向：

AI Agent开发实习生

大模型应用开发实习生

RAG应用开发实习生

AI应用工程师实习生

"""


# =========================
# 创建Document
# =========================


documents = [

    Document(
        page_content=resume,
        metadata={
            "name":"resume",
            "category":"personal"
        }
    )

]


print(
    "简历文档数量:",
    len(documents)
)



# =========================
# embedding
# =========================


embedding_model = get_embeddings()



# =========================
# 创建向量库
# =========================


from langchain_chroma import Chroma
import shutil
import os


RESUME_DB_PATH = "./resume_chroma_db"


# 如果旧库存在，先删除
if os.path.exists(RESUME_DB_PATH):
    shutil.rmtree(RESUME_DB_PATH)


print("开始创建简历向量库...")


vectorstore = Chroma.from_documents(

    documents=documents,

    embedding=embedding_model,

    persist_directory=RESUME_DB_PATH

)


print(
    "向量数量:",
    vectorstore._collection.count()
)


print("简历向量库创建完成")