from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver


from tools.job_tool import create_job_tool
from tools.resume_tool import create_resume_tool
from tools.match_tool import create_match_tool
from tools.hr_analysis_tool import create_hr_analysis_tool
from tools.interview_tool import create_interview_tool


from prompts.agent_prompt import SYSTEM_PROMPT


from vectorstores.chroma_store import load_vectorstore
from vectorstores.job_chroma import load_job_vectorstore


from rerankers.reranker import Reranker
from embeddings.embedding import get_embeddings


from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    LLM_MODEL,
    LLM_TEMPERATURE
)


def create_agent_instance():

    # =========================
    # 1. 初始化 LLM
    # =========================

    if not DEEPSEEK_API_KEY:
        raise ValueError(
            "未检测到 DEEPSEEK_API_KEY，请检查 .env 文件。"
        )

    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,

        # DeepSeek 当前不依赖 response_format
        disabled_params={
            "response_format": True
        }
    )

    # =========================
    # 2. Embedding
    # =========================

    embedding_model = get_embeddings()

    # =========================
    # 3. 加载简历向量库
    # =========================

    resume_vectorstore = load_vectorstore(
        embedding_model
    )

    # =========================
    # 4. 加载岗位向量库
    # =========================

    job_vectorstore = load_job_vectorstore(
        embedding_model
    )

    # =========================
    # 5. Reranker
    # =========================

    reranker = Reranker()

    # =========================
    # 6. 创建五个 Tool
    # =========================

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

    hr_candidate_analysis = create_hr_analysis_tool(
        llm
    )

    generate_interview_plan = create_interview_tool(
        llm
    )

    tools = [
        resume_search,
        job_search,
        job_match,
        hr_candidate_analysis,
        generate_interview_plan
    ]

    # =========================
    # 7. Memory
    # =========================

    memory = MemorySaver()

    # =========================
    # 8. 创建 Agent
    # =========================

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory
    )

    return agent