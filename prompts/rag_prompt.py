from langchain_core.prompts import ChatPromptTemplate


rag_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
你是一个专业的AI职业规划助手。

请根据提供的简历内容回答问题。

要求：
1. 只能依据提供的资料回答
2. 不要编造经历
3. 分析优势和不足
4. 给出改进建议

参考资料:
{context}
"""
        ),
        (
            "human",
            "{question}"
        )
    ]
)