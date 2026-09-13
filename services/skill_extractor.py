import re


# 常见技术技能词表
# 用于从真实岗位描述中提取技能要求
SKILL_LEXICON = [
    "Python",
    "Java",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "Go",
    "Rust",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "Redis",
    "MongoDB",

    "Spring",
    "Spring Boot",
    "Django",
    "Flask",
    "FastAPI",

    "Vue",
    "React",
    "Node.js",

    "Docker",
    "Kubernetes",
    "Linux",
    "Git",

    "AWS",
    "Azure",
    "GCP",

    "LangChain",
    "LangGraph",
    "RAG",
    "Agent",
    "MCP",

    "PyTorch",
    "TensorFlow",

    "Pandas",
    "NumPy",

    "机器学习",
    "深度学习",
    "自然语言处理",
    "计算机视觉",
    "数据分析",
    "数据挖掘",
]


def extract_skills(text: str) -> list[str]:

    if not text:
        return []

    text = str(text)

    found = []

    for skill in SKILL_LEXICON:

        pattern = (
            rf"(?<![A-Za-z0-9+#])"
            rf"{re.escape(skill)}"
            rf"(?![A-Za-z0-9+#])"
        )

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        ):

            found.append(skill)

    return found