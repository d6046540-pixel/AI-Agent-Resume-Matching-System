from langchain_core.documents import Document

from langchain_chroma import Chroma
from embeddings.embedding import get_embeddings


JOB_DB_PATH="./job_chroma_db"
import os
import shutil


if os.path.exists(JOB_DB_PATH):
    shutil.rmtree(JOB_DB_PATH)

# 模拟岗位数据
jobs = [

{
"title":"AI应用开发实习生",
"company":"杭州某人工智能公司",
"city":"杭州",
"level":"实习",
"category":"AI开发",
"skills":"Python, LangChain, Agent, RAG, 大模型应用",
"description":"负责基于大语言模型的应用开发，包括Agent系统搭建、知识库问答、RAG流程优化。"
},


{
"title":"大模型应用开发实习生",
"company":"杭州AI创业公司",
"city":"杭州",
"level":"实习",
"category":"AI开发",
"skills":"Python, OpenAI API, LangChain, Prompt Engineering",
"description":"参与LLM应用开发，设计Prompt流程，实现智能助手和自动化Agent。"
},


{
"title":"Agent开发实习生",
"company":"杭州智能科技有限公司",
"city":"杭州",
"level":"实习",
"category":"AI开发",
"skills":"Python, LangGraph, Tool Calling, MCP, RAG",
"description":"负责智能Agent开发，包括工具调用、多Agent协作和任务规划。"
},


{
"title":"机器学习算法实习生",
"company":"杭州互联网企业",
"city":"杭州",
"level":"实习",
"category":"算法",
"skills":"Python, PyTorch, sklearn, 数据分析",
"description":"参与机器学习模型训练、数据处理和算法优化工作。"
},


{
"title":"NLP算法实习生",
"company":"杭州人工智能研究院",
"city":"杭州",
"level":"实习",
"category":"自然语言处理",
"skills":"Python, NLP, Transformer, BERT",
"description":"参与文本分类、语义理解、大模型微调相关研究。"
},


{
"title":"AI产品经理实习生",
"company":"杭州科技公司",
"city":"杭州",
"level":"实习",
"category":"AI产品",
"skills":"AI产品设计, Prompt, 用户需求分析",
"description":"参与AI产品规划、需求分析以及大模型应用场景设计。"
},


{
"title":"RAG应用开发实习生",
"company":"杭州大模型公司",
"city":"杭州",
"level":"实习",
"category":"AI开发",
"skills":"Python, Chroma, Embedding, Vector Database",
"description":"负责企业知识库构建，实现RAG检索增强生成系统。"
},


{
"title":"计算机视觉算法实习生",
"company":"杭州视觉AI公司",
"city":"杭州",
"level":"实习",
"category":"CV算法",
"skills":"Python, OpenCV, PyTorch, 深度学习",
"description":"参与图像识别、目标检测和视觉算法开发。"
},


{
"title":"AI Agent工程师实习生",
"company":"杭州大模型创业公司",
"city":"杭州",
"level":"实习",
"category":"AI开发",
"skills":"LangGraph, LangChain, MCP, Agent",
"description":"开发企业级Agent应用，实现自动任务执行和智能决策。"
},


{
"title":"Python后端开发实习生",
"company":"杭州软件公司",
"city":"杭州",
"level":"实习",
"category":"后端开发",
"skills":"Python, FastAPI, MySQL, API",
"description":"参与后台服务开发，为AI应用提供接口支持。"
}

]



documents=[]


for job in jobs:

    doc=Document(

        page_content=job["description"],

        metadata={

            "title":job["title"],

    "company":job["company"],

    "city":job["city"],

    "level":job["level"],

    "category":job["category"],

    "skills":job["skills"]

        }

    )


    documents.append(doc)




print(
    "岗位数量:",
    len(documents)
)



embedding_model = get_embeddings()



vectorstore=Chroma.from_documents(

    documents=documents,

    embedding=embedding_model,

    persist_directory=JOB_DB_PATH

)



print("岗位库创建完成")
