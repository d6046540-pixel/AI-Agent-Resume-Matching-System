from langchain_core.tools import tool

from services.match_engine import MatchEngine
from services.skill_extractor import extract_skills


def create_match_tool(
    llm,
    resume_vectorstore,
    job_vectorstore,
    reranker
):

    engine = MatchEngine()

    @tool
    def job_match(
        resume: str,
        job: str
    ) -> str:
        """
        根据候选人简历和真实岗位要求，
        计算可解释的岗位匹配结果。

        匹配技能来自真实岗位文本，
        不使用固定岗位技能。
        """

        # ==========================================
        # 1. 从真实岗位文本中提取技能要求
        # ==========================================

        required_skills = extract_skills(
            job
        )

        # ==========================================
        # 2. 如果岗位没有识别出技能
        # ==========================================

        if not required_skills:

            return (
                "无法从当前岗位信息中识别出明确的技术技能要求，"
                "暂时无法进行技能维度匹配。"
            )

        # ==========================================
        # 3. MatchEngine 确定性计算
        # ==========================================

        result = engine.calculate(
            required_skills=required_skills,
            candidate_text=resume,
            job_text=job
        )

        # ==========================================
        # 4. 返回结构化结果
        # ==========================================

        return result.model_dump_json(
            ensure_ascii=False,
            indent=2
        )

    return job_match