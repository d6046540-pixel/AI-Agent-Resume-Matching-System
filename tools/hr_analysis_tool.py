from langchain_core.tools import tool

from chains.hr_analysis_chain import (
    create_hr_analysis_chain
)


def create_hr_analysis_tool(llm):

    # ========================================================
    # 创建 HR 分析 Chain
    # ========================================================

    chain = create_hr_analysis_chain(
        llm
    )

    # ========================================================
    # Tool
    # ========================================================

    @tool
    def hr_candidate_analysis(
        resume: str,
        job: str,
        matching_result: str = ""
    ) -> str:
        """
        对候选人与当前招聘岗位进行深度 HR 招聘辅助分析。

        注意：

        本工具不会重新计算匹配分数。

        它负责解释：
        - 系统匹配结果
        - 简历证据
        - 项目证据
        - 技能缺口
        - 风险
        - 面试重点
        - 招聘建议
        """

        # ====================================================
        # 1. 调用分析 Chain
        # ====================================================

        result = chain.invoke(
            {
                "resume": resume,
                "job": job,
                "matching_result": matching_result
            }
        )

        # ====================================================
        # 2. 获取模型输出
        # ====================================================

        if hasattr(
            result,
            "content"
        ):
            return result.content

        return str(result)

    # ========================================================
    # 返回 Tool
    # ========================================================

    return hr_candidate_analysis