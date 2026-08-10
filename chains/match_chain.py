from langchain_core.prompts import ChatPromptTemplate


def create_match_chain(
    llm,
    resume_vectorstore,
    job_vectorstore,
    reranker
    ):

    prompt = ChatPromptTemplate.from_template(
        """
你是一名AI招聘专家。

根据候选人简历和岗位要求，
分析岗位匹配程度。

输出：

1. 综合匹配评分（0-100）
2. 匹配优势
3. 技能不足
4. 改进建议


候选人简历：

{resume}


岗位信息：

{job}


请用Markdown格式回答。
"""
    )


    chain = prompt | llm


    return chain