from langchain_core.prompts import ChatPromptTemplate


def create_match_chain(
    llm,
    resume_vectorstore=None,
    job_vectorstore=None,
    reranker=None
):

    prompt = ChatPromptTemplate.from_template(
        """
你是一名专业的企业招聘辅助 AI。

你的任务是：
根据候选人简历、真实岗位信息以及程序计算出的基础匹配结果，
对候选人与岗位之间的匹配关系进行解释。

注意：

1. 不允许虚构候选人的技能。

2. 不允许虚构岗位要求。

3. 不允许修改程序计算出的基础匹配评分。

4. 没有明确证据时：
   必须说“没有明确证据”。

5. 没有证据不代表候选人不会，
   应该建议通过面试验证。

6. 不要因为候选人拥有岗位之外的额外技能而扣分。

7. 最终招聘决定属于真人 HR。

请分析：

- 岗位核心要求
- 候选人对应证据
- 技能匹配情况
- 技能不足
- 项目相关性
- 需要面试验证的部分

候选人简历：

{resume}

真实岗位信息：

{job}

程序计算出的基础匹配结果：

{matching_result}

请用 Markdown 输出。

不要重新计算匹配评分。
"""
    )

    return prompt | llm