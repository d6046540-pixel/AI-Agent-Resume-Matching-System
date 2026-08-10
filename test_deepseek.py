from langchain_openai import ChatOpenAI
import os




llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


response = llm.invoke(
    "你好，请介绍一下你自己"
)


print(response.content)