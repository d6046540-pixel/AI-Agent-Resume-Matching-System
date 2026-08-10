from langchain_core.prompts import ChatPromptTemplate


def create_query_rewriter(llm):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
你是一个Query Rewrite模块。

任务：
把用户问题改写成适合向量数据库检索的关键词。

严格规则：

- 只输出检索关键词
- 每行一个query
- 最多3个
- 不要解释
- 不要 Markdown
- 不要编号
- 不要回答用户问题

示例：

用户：
分析我的Agent开发能力

输出：
Agent开发技能
Agent项目经验
LangGraph项目经验
"""
            ),
            (
                "human",
                "{query}"
            )
        ]
    )

    return prompt | llm