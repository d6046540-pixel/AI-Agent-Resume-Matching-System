from chains.query_rewrite import create_query_rewriter
from langchain_openai import ChatOpenAI
import os


llm = ChatOpenAI(

    model="deepseek-chat",

    api_key=os.getenv(
        "DEEPSEEK_API_KEY"
    ),

    base_url="https://api.deepseek.com",

    temperature=0

)


rewriter = create_query_rewriter(
    llm
)


result = rewriter.invoke(
    {
        "question":
        "我的背景适合AI Agent开发岗位吗？"
    }
)


print(result.content)