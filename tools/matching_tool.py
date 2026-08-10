from langchain_core.tools import tool

from pydantic import BaseModel

from langchain_core.output_parsers import PydanticOutputParser



# =========================
# 1. 定义输出结构
# =========================

class CareerReport(BaseModel):

    score: int

    strengths: list[str]

    weaknesses: list[str]

    suggestions: list[str]




# =========================
# 2. 创建Tool
# =========================


def create_matching_tool(llm):


    parser = PydanticOutputParser(
        pydantic_object=CareerReport
    )



    @tool(
        description="分析候选人的简历和岗位要求，输出岗位匹配评分、优势、不足和建议"
    )
    def matching_analysis(
        resume_info: str,
        job_info: str
    ):


        """
        根据简历和岗位要求，
        生成结构化职业匹配报告。
        """



        prompt = f"""

你是一名专业AI招聘专家。


请根据候选人信息和岗位要求进行分析。


候选人:

{resume_info}



岗位:

{job_info}



请严格返回JSON。


格式必须如下：

{{
    "score": 80,
    "strengths": [
        "优势1",
        "优势2"
    ],
    "weaknesses": [
        "不足1",
        "不足2"
    ],
    "suggestions": [
        "建议1",
        "建议2"
    ]
}}


不要输出解释文字。
不要输出markdown。
不要输出代码块。


"""


        response = llm.invoke(
            prompt
        )



        result = parser.parse(
            response.content
        )



        return result.model_dump()



    return matching_analysis