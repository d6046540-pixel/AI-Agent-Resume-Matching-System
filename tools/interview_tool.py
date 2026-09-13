from langchain_core.tools import tool

from chains.interview_chain import (
    create_interview_chain
)


def create_interview_tool(llm):

    chain = create_interview_chain(
        llm
    )

    @tool
    def generate_interview_plan(
        resume: str,
        job: str,
        matching_result: str = ""
    ) -> str:
        """
        根据候选人简历、岗位要求和匹配结果，
        生成结构化HR面试方案。
        """

        result = chain.invoke(
            {
                "resume": resume,
                "job": job,
                "matching_result": matching_result
            }
        )

        return result.model_dump_json(
            ensure_ascii=False,
            indent=2
        )

    return generate_interview_plan