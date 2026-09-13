import json
import re
from pathlib import Path


# ============================================================
# 1. 路径配置
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

RESUME_PATH = BASE_DIR / "resume.json"
JOB_PATH = BASE_DIR / "job.json"


# ============================================================
# 2. 技能标准化
# ============================================================

SKILL_ALIASES = {

    # Python
    "python": "python",
    "python3": "python",
    "python编程": "python",
    "py": "python",

    # Agent
    "agent": "agent",
    "ai agent": "agent",
    "aiagent": "agent",
    "智能体": "agent",
    "智能代理": "agent",
    "agent开发": "agent",

    # LLM
    "llm": "llm",
    "大模型": "llm",
    "大语言模型": "llm",
    "大型语言模型": "llm",
    "语言模型": "llm",

    # RAG
    "rag": "rag",
    "检索增强生成": "rag",
    "检索增强": "rag",

    # LangChain
    "langchain": "langchain",
    "lang chain": "langchain",

    # LangGraph
    "langgraph": "langgraph",
    "lang graph": "langgraph",

    # MCP
    "mcp": "mcp",
    "model context protocol": "mcp",

    # Tool Calling
    "tool calling": "tool_calling",
    "tool-calling": "tool_calling",
    "tool calling": "tool_calling",
    "工具调用": "tool_calling",

    # Vector DB
    "vector database": "vector_db",
    "vector db": "vector_db",
    "向量数据库": "vector_db",
    "向量库": "vector_db",

    "chroma": "vector_db",
    "chromadb": "vector_db",
    "milvus": "vector_db",
    "faiss": "vector_db",
    "pinecone": "vector_db",

    # Prompt
    "prompt": "prompt",
    "prompt engineering": "prompt",
    "提示词": "prompt",
    "提示词工程": "prompt",

    # Git
    "git": "git",
    "github": "git",

    # Docker
    "docker": "docker",
    "容器": "docker",

    # SQL
    "sql": "sql",
    "mysql": "mysql",
    "postgresql": "postgresql",
    "postgres": "postgresql",

    # API
    "api": "api",
    "rest api": "api",
    "restful api": "api",
}


# ============================================================
# 3. 文本标准化
# ============================================================

def normalize_text(text):
    if text is None:
        return ""

    text = str(text).lower().strip()

    text = re.sub(
        r"[，,、；;|/]+",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ============================================================
# 4. 单个技能标准化
# ============================================================

def normalize_skill(skill):

    skill = normalize_text(skill)

    if not skill:
        return ""

    if skill in SKILL_ALIASES:
        return SKILL_ALIASES[skill]

    return skill


# ============================================================
# 5. 从文本中提取技能
# ============================================================

def extract_skills_from_text(text):

    text = normalize_text(text)

    found = set()

    for alias, canonical in SKILL_ALIASES.items():

        alias_normalized = normalize_text(alias)

        if not alias_normalized:
            continue

        if " " in alias_normalized:

            if alias_normalized in text:
                found.add(canonical)

        else:

            if re.search(
                r"(?<![a-zA-Z0-9])"
                + re.escape(alias_normalized),
                text
            ):
                found.add(canonical)

            elif alias_normalized in text:
                found.add(canonical)

    return found


# ============================================================
# 6. 读取 JSON
# ============================================================

def load_json(path):

    if not path.exists():

        raise FileNotFoundError(
            f"找不到文件：{path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ============================================================
# 7. 简历转文本
# ============================================================

def resume_to_text(resume):

    parts = []

    for key in [
        "name",
        "education",
        "majors",
        "skills",
        "projects",
        "internships",
        "courses",
        "summary",
        "experience",
    ]:

        value = resume.get(key)

        if value:

            if isinstance(value, list):

                parts.append(
                    " ".join(
                        str(x)
                        for x in value
                    )
                )

            else:

                parts.append(
                    str(value)
                )

    return " ".join(parts)


# ============================================================
# 8. 岗位转文本
# ============================================================

def job_to_text(job):

    parts = []

    for key in [
        "title",
        "category",
        "level",
        "employment_type",
        "work_mode",
        "education",
        "skills",
        "description",
    ]:

        value = job.get(key)

        if value:

            if isinstance(value, list):

                parts.append(
                    " ".join(
                        str(x)
                        for x in value
                    )
                )

            else:

                parts.append(
                    str(value)
                )

    return " ".join(parts)


# ============================================================
# 9. 获取简历技能
# ============================================================

def get_resume_skills(resume):

    skills = resume.get(
        "skills",
        []
    )

    result = set()

    if isinstance(skills, list):

        for skill in skills:

            normalized = normalize_skill(skill)

            if normalized:
                result.add(normalized)

    # 再从整个简历文本中补充识别
    resume_text = resume_to_text(resume)

    result.update(
        extract_skills_from_text(
            resume_text
        )
    )

    return result


# ============================================================
# 10. 获取岗位技能
# ============================================================

def get_job_skills(job):

    skills = job.get(
        "skills",
        []
    )

    result = set()

    if isinstance(skills, list):

        for skill in skills:

            normalized = normalize_skill(skill)

            if normalized:
                result.add(normalized)

    elif isinstance(skills, str):

        raw_skills = re.split(
            r"[,，、;/|]+",
            skills
        )

        for skill in raw_skills:

            normalized = normalize_skill(skill)

            if normalized:
                result.add(normalized)

    # 从岗位描述中补充识别
    job_text = job_to_text(job)

    result.update(
        extract_skills_from_text(
            job_text
        )
    )

    return result


# ============================================================
# 11. 技能匹配
# ============================================================

def calculate_skill_match(
    resume_skills,
    job_skills
):

    if not job_skills:

        return {
            "score": 0.0,
            "matched": set(),
            "missing": set(),
        }

    matched = (
        resume_skills
        &
        job_skills
    )

    missing = (
        job_skills
        -
        resume_skills
    )

    score = (
        len(matched)
        /
        len(job_skills)
    )

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
    }


# ============================================================
# 12. 教育背景匹配
# ============================================================

def calculate_education_match(
    resume,
    job
):

    job_education = normalize_text(
        job.get(
            "education",
            ""
        )
    )

    resume_education = normalize_text(
        str(
            resume.get(
                "education",
                ""
            )
        )
    )

    if not job_education:

        return 1.0

    if not resume_education:

        return 0.5

    education_keywords = [
        "本科",
        "硕士",
        "研究生",
        "博士",
        "大专",
    ]

    for keyword in education_keywords:

        if (
            keyword in job_education
            and keyword in resume_education
        ):

            return 1.0

    return 0.5


# ============================================================
# 13. 专业匹配
# ============================================================

def calculate_major_match(
    resume,
    job
):

    resume_text = normalize_text(
        resume_to_text(resume)
    )

    job_text = normalize_text(
        job_to_text(job)
    )

    # AI / 计算机 / 信息类岗位的相关专业关键词
    related_keywords = [
        "计算机",
        "软件",
        "人工智能",
        "信息",
        "数据",
        "统计",
        "数学",
        "电子",
        "通信",
    ]

    resume_related = any(
        keyword in resume_text
        for keyword in related_keywords
    )

    job_related = any(
        keyword in job_text
        for keyword in related_keywords
    )

    if resume_related and job_related:
        return 1.0

    return 0.5


# ============================================================
# 14. 项目匹配
# ============================================================

def calculate_project_match(
    resume,
    job
):

    resume_text = normalize_text(
        resume_to_text(resume)
    )

    job_text = normalize_text(
        job_to_text(job)
    )

    project_keywords = (
        extract_skills_from_text(
            resume_text
        )
        &
        extract_skills_from_text(
            job_text
        )
    )

    if not project_keywords:

        return 0.0

    # 有项目相关技能，认为存在项目相关性
    return min(
        len(project_keywords) / 5,
        1.0
    )


# ============================================================
# 15. 综合评分
# ============================================================

def calculate_final_score(
    skill_score,
    education_score,
    major_score,
    project_score
):

    return (
        skill_score * 0.50
        +
        education_score * 0.15
        +
        major_score * 0.15
        +
        project_score * 0.20
    )


# ============================================================
# 16. 候选人匹配分析
# ============================================================

def match_candidate(
    resume,
    job
):

    resume_skills = get_resume_skills(
        resume
    )

    job_skills = get_job_skills(
        job
    )

    skill_result = calculate_skill_match(
        resume_skills,
        job_skills
    )

    education_score = (
        calculate_education_match(
            resume,
            job
        )
    )

    major_score = (
        calculate_major_match(
            resume,
            job
        )
    )

    project_score = (
        calculate_project_match(
            resume,
            job
        )
    )

    final_score = calculate_final_score(
        skill_result["score"],
        education_score,
        major_score,
        project_score
    )

    return {

        "candidate_name":
            resume.get(
                "name",
                "未知"
            ),

        "job_title":
            job.get(
                "title",
                "未知岗位"
            ),

        "resume_skills":
            sorted(resume_skills),

        "job_skills":
            sorted(job_skills),

        "matched_skills":
            sorted(
                skill_result["matched"]
            ),

        "missing_skills":
            sorted(
                skill_result["missing"]
            ),

        "skill_score":
            skill_result["score"],

        "education_score":
            education_score,

        "major_score":
            major_score,

        "project_score":
            project_score,

        "final_score":
            final_score,
    }


# ============================================================
# 17. HR 评估建议
# ============================================================

def generate_hr_recommendation(
    result
):

    score = result[
        "final_score"
    ]

    missing = result[
        "missing_skills"
    ]

    matched = result[
        "matched_skills"
    ]

    if score >= 0.80:

        recommendation = (
            "强烈建议进入下一轮面试"
        )

    elif score >= 0.65:

        recommendation = (
            "建议进入面试，重点验证项目真实性与实际能力"
        )

    elif score >= 0.50:

        recommendation = (
            "可以考虑面试，但存在明显能力缺口"
        )

    else:

        recommendation = (
            "岗位匹配度较低，不建议作为优先候选人"
        )

    return {

        "recommendation":
            recommendation,

        "strengths":
            matched,

        "risks":
            missing,
    }


# ============================================================
# 18. 输出报告
# ============================================================

def display_result(
    result
):

    recommendation = (
        generate_hr_recommendation(
            result
        )
    )

    print()
    print("=" * 70)

    print(
        "AI 招聘 Agent · 候选人评估"
    )

    print("=" * 70)

    print(
        f"\n候选人："
        f"{result['candidate_name']}"
    )

    print(
        f"应聘岗位："
        f"{result['job_title']}"
    )

    print(
        f"\n综合匹配度："
        f"{result['final_score'] * 100:.2f}%"
    )

    print(
        f"技能匹配度："
        f"{result['skill_score'] * 100:.2f}%"
    )

    print(
        f"学历匹配度："
        f"{result['education_score'] * 100:.2f}%"
    )

    print(
        f"专业匹配度："
        f"{result['major_score'] * 100:.2f}%"
    )

    print(
        f"项目匹配度："
        f"{result['project_score'] * 100:.2f}%"
    )

    print("\n候选人技能：")

    print(
        ", ".join(
            result["resume_skills"]
        )
    )

    print("\n岗位要求技能：")

    print(
        ", ".join(
            result["job_skills"]
        )
    )

    print("\n匹配技能：")

    print(
        ", ".join(
            result["matched_skills"]
        )
        or "无"
    )

    print("\n技能缺口：")

    print(
        ", ".join(
            result["missing_skills"]
        )
        or "无明显技能缺口"
    )

    print("\nHR 建议：")

    print(
        recommendation[
            "recommendation"
        ]
    )

    print("=" * 70)


# ============================================================
# 19. 主程序
# ============================================================

def main():

    print()
    print("=" * 70)
    print("AI 招聘 Agent · 候选人岗位匹配系统")
    print("=" * 70)

    print(
        "\n当前模式："
        "真人 HR + 候选人简历 + 岗位 JD"
    )

    resume = load_json(
        RESUME_PATH
    )

    jobs = load_json(
        JOB_PATH
    )

    # job.json 允许：
    #
    # 1. 单个岗位对象
    # 2. 岗位数组

    if isinstance(jobs, dict):

        jobs = [jobs]

    if not isinstance(jobs, list):

        raise ValueError(
            "job.json 必须是岗位对象或岗位数组"
        )

    if not jobs:

        raise ValueError(
            "job.json 中没有岗位数据"
        )

    print(
        f"\n候选人："
        f"{resume.get('name', '未知')}"
    )

    print(
        f"岗位数量："
        f"{len(jobs)}"
    )

    # ========================================================
    # 如果有多个岗位
    # ========================================================

    results = []

    for job in jobs:

        result = match_candidate(
            resume,
            job
        )

        results.append(
            result
        )

    # 综合排序
    results.sort(
        key=lambda x:
        x["final_score"],
        reverse=True
    )

    # 输出
    for result in results:

        display_result(
            result
        )


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":

    main()