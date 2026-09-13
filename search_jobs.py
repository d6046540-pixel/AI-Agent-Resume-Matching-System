import json
import re
import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer


# ============================================================
# 1. 配置
# ============================================================

EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"

RESUME_PATH = "resume.json"

# 综合评分
SKILL_WEIGHT = 0.60
SEMANTIC_WEIGHT = 0.40


# ============================================================
# 2. 技能标准化 / 同义词
# ============================================================

SKILL_ALIASES = {

    # -------------------------
    # Python
    # -------------------------

    "python": "python",
    "python3": "python",
    "python编程": "python",
    "py": "python",

    # -------------------------
    # Java
    # -------------------------

    "java": "java",

    # -------------------------
    # JavaScript
    # -------------------------

    "javascript": "javascript",
    "js": "javascript",

    # -------------------------
    # TypeScript
    # -------------------------

    "typescript": "typescript",
    "ts": "typescript",

    # -------------------------
    # Agent
    # -------------------------

    "agent": "agent",
    "ai agent": "agent",
    "aiagent": "agent",
    "智能体": "agent",
    "智能代理": "agent",
    "agent开发": "agent",
    "ai智能体": "agent",

    # -------------------------
    # LLM
    # -------------------------

    "llm": "llm",
    "large language model": "llm",
    "large language models": "llm",
    "大模型": "llm",
    "语言模型": "llm",
    "大型语言模型": "llm",

    # -------------------------
    # RAG
    # -------------------------

    "rag": "rag",
    "retrieval augmented generation": "rag",
    "retrieval-augmented generation": "rag",
    "检索增强生成": "rag",
    "检索增强": "rag",

    # -------------------------
    # LangChain
    # -------------------------

    "langchain": "langchain",
    "lang chain": "langchain",
    "langchain框架": "langchain",

    # -------------------------
    # LangGraph
    # -------------------------

    "langgraph": "langgraph",
    "lang graph": "langgraph",

    # -------------------------
    # LlamaIndex
    # -------------------------

    "llamaindex": "llamaindex",
    "llama index": "llamaindex",

    # -------------------------
    # 向量数据库
    # -------------------------

    "vector database": "vector_db",
    "vector db": "vector_db",
    "向量数据库": "vector_db",
    "向量库": "vector_db",

    "chroma": "vector_db",
    "chromadb": "vector_db",
    "milvus": "vector_db",
    "faiss": "vector_db",
    "pinecone": "vector_db",
    "weaviate": "vector_db",

    # -------------------------
    # Prompt
    # -------------------------

    "prompt": "prompt",
    "prompt engineering": "prompt",
    "提示词": "prompt",
    "提示词工程": "prompt",
    "提示工程": "prompt",

    # -------------------------
    # MCP
    # -------------------------

    "mcp": "mcp",
    "model context protocol": "mcp",

    # -------------------------
    # Tool Calling
    # -------------------------

    "tool calling": "tool_calling",
    "tool-calling": "tool_calling",
    "tool_calling": "tool_calling",
    "function calling": "tool_calling",
    "函数调用": "tool_calling",
    "工具调用": "tool_calling",

    # -------------------------
    # API
    # -------------------------

    "api": "api",
    "rest api": "api",
    "restful api": "api",
    "接口开发": "api",

    # -------------------------
    # Git
    # -------------------------

    "git": "git",
    "github": "git",

    # -------------------------
    # Docker
    # -------------------------

    "docker": "docker",
    "容器": "docker",
    "docker容器": "docker",

    # -------------------------
    # SQL
    # -------------------------

    "sql": "sql",
    "mysql": "mysql",
    "postgresql": "postgresql",
    "postgres": "postgresql",

    # -------------------------
    # DeepSeek
    # -------------------------

    "deepseek": "deepseek",
    "deep seek": "deepseek",

    # -------------------------
    # Qwen / 通义千问
    # -------------------------

    "qwen": "qwen",
    "通义千问": "qwen",
    "千问": "qwen",
}


# ============================================================
# 3. 加载 Embedding 模型
# ============================================================

print("正在加载 Embedding 模型...")

model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Embedding 模型加载完成")


# ============================================================
# 4. 文本处理
# ============================================================

def normalize_text(text):
    """
    统一文本格式。
    """

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
# 5. 技能标准化
# ============================================================

def normalize_skill(skill):
    """
    将技能转换为标准技能名称。
    """

    skill = normalize_text(skill)

    if not skill:
        return ""

    if skill in SKILL_ALIASES:
        return SKILL_ALIASES[skill]

    simplified = skill

    for suffix in [
        "开发",
        "编程",
        "技术",
        "框架",
        "工具",
        "能力",
    ]:

        if simplified.endswith(suffix):

            simplified = simplified[
                :-len(suffix)
            ]

    if simplified in SKILL_ALIASES:
        return SKILL_ALIASES[simplified]

    return simplified


# ============================================================
# 6. 从文本中提取技能
# ============================================================

def extract_skills(text):
    """
    从任意文本中识别技能。
    """

    text = normalize_text(text)

    found = set()

    if not text:
        return found

    for alias, canonical in SKILL_ALIASES.items():

        alias_normalized = normalize_text(
            alias
        )

        if not alias_normalized:
            continue

        # 英文多词技能
        if " " in alias_normalized:

            if alias_normalized in text:
                found.add(canonical)

            continue

        # 英文技能
        if re.search(
            r"(?<![a-zA-Z0-9])"
            + re.escape(alias_normalized)
            + r"(?![a-zA-Z0-9])",
            text
        ):

            found.add(canonical)

            continue

        # 中文技能
        if re.search(
            re.escape(alias_normalized),
            text
        ):

            found.add(canonical)

    return found


# ============================================================
# 7. 读取简历
# ============================================================

def load_resume(path):
    """
    读取 resume_parser.py 生成的 resume.json
    """

    resume_path = Path(path)

    if not resume_path.exists():

        raise FileNotFoundError(
            f"找不到简历文件：{resume_path}"
        )

    with open(
        resume_path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ============================================================
# 8. 简历 → 文本
# ============================================================

def resume_to_text(resume):
    """
    将结构化简历转换成语义匹配文本。
    """

    parts = []

    # 姓名
    if resume.get("name"):
        parts.append(
            str(resume["name"])
        )

    # 技能
    skills = resume.get(
        "skills",
        []
    )

    if isinstance(skills, list):

        parts.append(
            " ".join(
                str(x)
                for x in skills
            )
        )

    # 专业
    majors = resume.get(
        "majors",
        []
    )

    if isinstance(majors, list):

        parts.append(
            " ".join(
                str(x)
                for x in majors
            )
        )

    # 学历
    education = resume.get(
        "education",
        []
    )

    if isinstance(education, list):

        parts.append(
            " ".join(
                str(x)
                for x in education
            )
        )

    # 项目
    projects = resume.get(
        "projects",
        []
    )

    if isinstance(projects, list):

        for project in projects[:5]:

            if isinstance(project, dict):

                parts.append(
                    json.dumps(
                        project,
                        ensure_ascii=False
                    )
                )

            else:

                parts.append(
                    str(project)
                )

    # 实习
    internships = resume.get(
        "internships",
        []
    )

    if isinstance(internships, list):

        for internship in internships[:5]:

            if isinstance(
                internship,
                dict
            ):

                parts.append(
                    json.dumps(
                        internship,
                        ensure_ascii=False
                    )
                )

            else:

                parts.append(
                    str(internship)
                )

    # 其他字段
    for key in [
        "summary",
        "objective",
        "experience",
        "projects_text",
        "professional_skills",
    ]:

        value = resume.get(key)

        if value:

            if isinstance(
                value,
                list
            ):

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
# 9. 简历技能
# ============================================================

def extract_resume_skills(resume):
    """
    从结构化简历中提取标准化技能。
    """

    resume_text = resume_to_text(
        resume
    )

    return extract_skills(
        resume_text
    )


# ============================================================
# 10. HR 岗位技能
# ============================================================

def extract_job_skills(job_text):
    """
    从 HR 输入的岗位描述中提取岗位技能。
    """

    return extract_skills(
        job_text
    )


# ============================================================
# 11. 技能匹配
# ============================================================

def calculate_skill_match(
    resume_skills,
    job_skills
):
    """
    计算候选人与岗位技能匹配度。

    分母使用岗位技能数量。

    例如：

    岗位：
    Python
    LangChain
    RAG
    Agent

    候选人：
    Python
    LangChain
    RAG
    Agent
    MCP

    = 4 / 4 = 100%
    """

    if not job_skills:

        return (
            0.0,
            set(),
            set()
        )

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

    return (
        score,
        matched,
        missing
    )


# ============================================================
# 12. 语义匹配
# ============================================================

def calculate_semantic_score(
    resume_text,
    job_text
):
    """
    使用 Embedding 计算：

    候选人简历
        ↓
    岗位描述

    的语义相似度。
    """

    embeddings = model.encode(
        [
            resume_text,
            job_text
        ],
        normalize_embeddings=True
    )

    similarity = float(
        embeddings[0]
        @
        embeddings[1]
    )

    # cosine similarity
    # [-1, 1]
    #
    # 映射到 [0, 1]

    score = (
        similarity + 1
    ) / 2

    return max(
        0.0,
        min(
            score,
            1.0
        )
    )


# ============================================================
# 13. 综合评分
# ============================================================

def calculate_final_score(
    skill_score,
    semantic_score
):

    return (
        skill_score
        *
        SKILL_WEIGHT
        +
        semantic_score
        *
        SEMANTIC_WEIGHT
    )


# ============================================================
# 14. 匹配等级
# ============================================================

def get_match_level(score):

    if score >= 0.85:

        return (
            "★★★★★",
            "高度匹配",
            "建议：优先进入面试重点考察。"
        )

    if score >= 0.70:

        return (
            "★★★★",
            "较高匹配",
            "建议：可以进入面试，重点核实关键技能。"
        )

    if score >= 0.55:

        return (
            "★★★",
            "一般匹配",
            "建议：可以进入初筛，进一步判断岗位适配度。"
        )

    if score >= 0.40:

        return (
            "★★",
            "较低匹配",
            "建议：需要重点评估候选人的可迁移能力。"
        )

    return (
        "★",
        "低匹配",
        "建议：暂不作为优先候选人。"
    )


# ============================================================
# 15. HR 岗位输入
# ============================================================

def input_job_description():

    print()
    print("=" * 70)
    print("HR 岗位需求输入")
    print("=" * 70)

    print()
    print(
        "请输入当前正在招聘的岗位描述。"
    )

    print(
        "可以直接粘贴完整 JD。"
    )

    print()

    job_text = input(
        "HR 当前招聘岗位："
    ).strip()

    return job_text


# ============================================================
# 16. 展示匹配结果
# ============================================================

def display_match(
    resume,
    job_text
):

    print()
    print("=" * 70)
    print("候选人岗位匹配分析")
    print("=" * 70)

    candidate_name = (
        resume.get("name")
        or "未知候选人"
    )

    print()
    print(
        f"候选人：{candidate_name}"
    )

    # --------------------------------------------------------
    # 简历
    # --------------------------------------------------------

    resume_text = resume_to_text(
        resume
    )

    resume_skills = extract_resume_skills(
        resume
    )

    # --------------------------------------------------------
    # HR 岗位
    # --------------------------------------------------------

    job_skills = extract_job_skills(
        job_text
    )

    # --------------------------------------------------------
    # 技能匹配
    # --------------------------------------------------------

    (
        skill_score,
        matched_skills,
        missing_skills
    ) = calculate_skill_match(
        resume_skills,
        job_skills
    )

    # --------------------------------------------------------
    # 语义匹配
    # --------------------------------------------------------

    semantic_match = (
        calculate_semantic_score(
            resume_text,
            job_text
        )
    )

    # --------------------------------------------------------
    # 综合评分
    # --------------------------------------------------------

    final_score = calculate_final_score(
        skill_score,
        semantic_match
    )

    # --------------------------------------------------------
    # 匹配等级
    # --------------------------------------------------------

    (
        stars,
        level,
        suggestion
    ) = get_match_level(
        final_score
    )

    # ========================================================
    # HR 岗位
    # ========================================================

    print()
    print("=" * 70)
    print("HR 招聘岗位")
    print("=" * 70)

    print(job_text)

    # ========================================================
    # 候选人技能
    # ========================================================

    print()
    print("=" * 70)
    print("候选人技能")
    print("=" * 70)

    if resume_skills:

        print(
            ", ".join(
                sorted(resume_skills)
            )
        )

    else:

        print("未识别到技能")

    # ========================================================
    # 岗位技能
    # ========================================================

    print()
    print("=" * 70)
    print("岗位要求技能")
    print("=" * 70)

    if job_skills:

        print(
            ", ".join(
                sorted(job_skills)
            )
        )

    else:

        print(
            "未识别到明确技能要求"
        )

    # ========================================================
    # 匹配结果
    # ========================================================

    print()
    print("=" * 70)
    print("技能匹配分析")
    print("=" * 70)

    print()

    print(
        f"岗位要求技能："
        f"{len(job_skills)}"
    )

    print(
        f"候选人已有技能："
        f"{len(resume_skills)}"
    )

    print(
        f"匹配技能："
        f"{len(matched_skills)}"
    )

    print(
        f"缺失技能："
        f"{len(missing_skills)}"
    )

    print()

    print(
        "匹配技能："
        + (
            ", ".join(
                sorted(matched_skills)
            )
            if matched_skills
            else "无"
        )
    )

    print(
        "缺失技能："
        + (
            ", ".join(
                sorted(missing_skills)
            )
            if missing_skills
            else "无"
        )
    )

    print()

    print(
        f"技能匹配度："
        f"{skill_score * 100:.2f}%"
    )

    print(
        f"语义匹配度："
        f"{semantic_match * 100:.2f}%"
    )

    print(
        f"综合匹配度："
        f"{final_score * 100:.2f}%"
    )

    # ========================================================
    # HR 初步判断
    # ========================================================

    print()
    print("=" * 70)
    print("HR 初步判断")
    print("=" * 70)

    print()

    print(
        f"{stars} {level}"
    )

    print(
        suggestion
    )

    # ========================================================
    # 面试重点
    # ========================================================

    print()
    print("=" * 70)
    print("面试重点建议")
    print("=" * 70)

    if missing_skills:

        print()
        print(
            "建议重点确认以下岗位技能："
        )

        for skill in sorted(
            missing_skills
        ):

            print(
                f"• {skill}"
            )

    else:

        print()
        print(
            "候选人没有明显的技能缺口。"
        )

        print(
            "建议面试重点从以下方向验证："
        )

        print(
            "• 实际项目经验"
        )

        print(
            "• 技术深度"
        )

        print(
            "• 独立解决问题能力"
        )

        print(
            "• Agent / RAG 实际落地能力"
        )

    # ========================================================
    # 候选人摘要
    # ========================================================

    print()
    print("=" * 70)
    print("候选人基本信息")
    print("=" * 70)

    print()

    print(
        f"姓名："
        f"{resume.get('name') or '未知'}"
    )

    print(
        f"学历："
        f"{resume.get('education') or '未知'}"
    )

    print(
        f"专业："
        f"{resume.get('majors') or '未知'}"
    )

    preferred_cities = resume.get(
        "preferred_cities",
        []
    )

    if preferred_cities:

        print(
            "意向城市："
            + ", ".join(
                str(x)
                for x in preferred_cities
            )
        )

    # ========================================================
    # 项目
    # ========================================================

    projects = resume.get(
        "projects",
        []
    )

    if projects:

        print()
        print(
            "项目经历："
        )

        for project in projects[:3]:

            print(
                f"• {project}"
            )

    print()
    print("=" * 70)


# ============================================================
# 17. 主程序
# ============================================================

def main():

    print()
    print("=" * 70)
    print("AI 辅助 HR 候选人智能匹配系统")
    print("=" * 70)

    # --------------------------------------------------------
    # 读取简历
    # --------------------------------------------------------

    resume_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else RESUME_PATH
    )

    print()
    print(
        f"正在读取候选人简历："
        f"{resume_path}"
    )

    try:

        resume = load_resume(
            resume_path
        )

    except Exception as e:

        print()
        print(
            f"❌ 简历读取失败：{e}"
        )

        return

    print()
    print(
        "简历结构化数据读取成功。"
    )

    print(
        f"候选人："
        f"{resume.get('name') or '未知'}"
    )

    # --------------------------------------------------------
    # HR 输入岗位
    # --------------------------------------------------------

    while True:

        job_text = input_job_description()

        if not job_text:

            print()
            print(
                "⚠️ HR 岗位描述不能为空。"
            )

            print(
                "请重新输入。"
            )

            continue

        if job_text.lower() == "exit":

            print(
                "系统退出。"
            )

            return

        break

    # --------------------------------------------------------
    # 开始匹配
    # --------------------------------------------------------

    print()
    print(
        "正在匹配候选人..."
    )

    display_match(
        resume,
        job_text
    )


# ============================================================
# 18. 程序入口
# ============================================================

if __name__ == "__main__":

    main()