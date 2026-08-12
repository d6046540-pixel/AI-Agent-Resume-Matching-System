# ================================
# 创建 Agent 实例
# ================================


from langchain_openai import ChatOpenAI


from tools.job_tool import create_job_tool
from tools.resume_tool import create_resume_tool

from prompts.agent_prompt import SYSTEM_PROMPT



from vectorstores.chroma_store import load_vectorstore
from vectorstores.job_chroma import load_job_vectorstore

from rerankers.reranker import Reranker
from embeddings.embedding import get_embeddings

from tools.match_tool import create_match_tool


from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL
)

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver



def create_agent_instance():


    # ================================
    # 1. 初始化LLM
    # ================================


    llm = ChatOpenAI(

        model="deepseek-v4-flash",

        temperature=0,

        api_key="sk-a40d383a6ad343f1a9847f2254f5ea61",

        base_url="https://api.deepseek.com"

    )



    # ================================
    # 2. embedding
    # ================================


    embedding_model = get_embeddings()



    # ================================
    # 3. 加载向量库
    # ================================


    #print(
        #"加载已有简历向量库..."
    #)


    resume_vectorstore = load_vectorstore(

        embedding_model

    )


    print(
        "加载已有岗位向量库..."
    )


    job_vectorstore = load_job_vectorstore(

        embedding_model

    )



    # ================================
    # 4. 初始化reranker
    # ================================


    reranker = Reranker()



    # ================================
    # 5. 创建工具
    # ================================


    resume_search = create_resume_tool(

        resume_vectorstore,
        llm,
        reranker

    )



    job_search = create_job_tool(

        llm,

        job_vectorstore,

        reranker

    )

    job_match = create_match_tool(
    llm,
    resume_vectorstore,
    job_vectorstore,
    reranker
)


    tools=[
  
    job_search,
    resume_search,
    job_match
    ]


    



    # ================================
    # 6. Memory
    # ================================


    

    memory = MemorySaver()

#7. 创建Agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=memory,
        prompt=SYSTEM_PROMPT
    )


    return agent