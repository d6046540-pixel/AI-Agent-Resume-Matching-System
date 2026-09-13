import sys
import json
import re
from pathlib import Path

import fitz  # PyMuPDF
from pydantic import BaseModel, Field


# ============================================================
# 1. 简历结构
# ============================================================

class ResumeData(BaseModel):
    name: str = ""
    phone: str = ""
    email: str = ""

    education: list[str] = Field(default_factory=list)
    schools: list[str] = Field(default_factory=list)
    majors: list[str] = Field(default_factory=list)

    skills: list[str] = Field(default_factory=list)

    projects: list[str] = Field(default_factory=list)
    internships: list[str] = Field(default_factory=list)

    raw_text: str = ""


# ============================================================
# 2. PDF 文本提取
# ============================================================

def extract_pdf_text(pdf_path: str) -> str:
    """
    从 PDF 中提取全部文本。
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"找不到简历文件：{path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("目前只支持 PDF 简历")

    doc = fitz.open(path)

    pages = []

    for page in doc:
        text = page.get_text("text")
        pages.append(text)

    doc.close()

    text = "\n".join(pages)

    # 清理多余空白
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ============================================================
# 3. 基础信息解析
# ============================================================

def extract_phone(text: str) -> str:
    """
    提取中国大陆手机号。
    """

    pattern = r"(?<!\d)1[3-9]\d{9}(?!\d)"

    match = re.search(pattern, text)

    return match.group(0) if match else ""


def extract_email(text: str) -> str:
    """
    提取邮箱。
    """

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    return match.group(0) if match else ""


def extract_name(text: str) -> str:
    """
    简历姓名的启发式解析。

    第一版不追求 100% 准确，
    后续接 LLM 后再升级。
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # 常见情况：
    # 第一行就是姓名
    if lines:
        first_line = lines[0]

        # 排除明显不是姓名的内容
        excluded = [
            "个人简历",
            "简历",
            "resume",
            "curriculum vitae",
        ]

        if (
            first_line.lower() not in excluded
            and len(first_line) <= 10
            and not re.search(r"\d", first_line)
            and "@" not in first_line
        ):
            return first_line

    return ""


# ============================================================
# 4. 教育经历
# ============================================================

def extract_education(text: str) -> list[str]:
    """
    根据关键词提取教育相关内容。
    """

    education_keywords = [
        "本科",
        "硕士",
        "博士",
        "专科",
        "大专",
        "研究生",
        "大学",
        "学院",
        "专业",
        "学历",
    ]

    results = []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines:

        if any(keyword in line for keyword in education_keywords):

            if line not in results:
                results.append(line)

    return results[:10]


# ============================================================
# 5. 学校解析
# ============================================================

def extract_schools(text: str) -> list[str]:

    school_keywords = [
        "大学",
        "学院",
        "学校",
    ]

    results = []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines:

        if any(keyword in line for keyword in school_keywords):

            # 避免把整个句子全部当学校
            if len(line) <= 40:

                if line not in results:
                    results.append(line)

    return results[:10]


# ============================================================
# 6. 专业解析
# ============================================================

def extract_majors(text: str) -> list[str]:

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    keywords = [
        "专业",
        "计算机",
        "软件工程",
        "人工智能",
        "数据科学",
        "信息管理",
        "信息系统",
        "统计学",
        "应用统计",
    ]

    results = []

    for line in lines:

        if any(keyword in line for keyword in keywords):

            if len(line) <= 50:

                if line not in results:
                    results.append(line)

    return results[:10]


# ============================================================
# 7. 技能解析
# ============================================================

SKILL_DICTIONARY = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "TypeScript",

    "SQL",
    "MySQL",
    "PostgreSQL",
    "Redis",

    "Git",
    "Docker",
    "Linux",

    "FastAPI",
    "Flask",
    "Django",

    "LangChain",
    "LangGraph",
    "LlamaIndex",

    "RAG",
    "Agent",
    "AI Agent",
    "MCP",
    "Tool Calling",

    "Prompt Engineering",
    "Prompt",

    "OpenAI",
    "Qwen",
    "DeepSeek",
    "Kimi",

    "PyTorch",
    "TensorFlow",

    "Pandas",
    "NumPy",

    "Chroma",
    "FAISS",

    "机器学习",
    "深度学习",
    "自然语言处理",
    "大模型",
    "LLM",
]


def extract_skills(text: str) -> list[str]:

    text_lower = text.lower()

    results = []

    for skill in SKILL_DICTIONARY:

        if skill.lower() in text_lower:

            if skill not in results:
                results.append(skill)

    return results


# ============================================================
# 8. 项目经历
# ============================================================

def extract_projects(text: str) -> list[str]:

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    project_keywords = [
        "项目",
        "project",
        "系统",
        "平台",
        "开发",
        "搭建",
        "实现",
    ]

    results = []

    for line in lines:

        if any(keyword.lower() in line.lower()
               for keyword in project_keywords):

            if len(line) <= 100:

                if line not in results:
                    results.append(line)

    return results[:20]


# ============================================================
# 9. 实习经历
# ============================================================

def extract_internships(text: str) -> list[str]:

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    keywords = [
        "实习",
        "实习生",
        "intern",
        "internship",
        "工作经历",
        "工作经验",
    ]

    results = []

    for line in lines:

        if any(keyword.lower() in line.lower()
               for keyword in keywords):

            if len(line) <= 100:

                if line not in results:
                    results.append(line)

    return results[:20]


# ============================================================
# 10. 完整解析
# ============================================================

def parse_resume(pdf_path: str) -> ResumeData:

    print("正在读取 PDF 简历...")

    text = extract_pdf_text(pdf_path)

    if not text:
        raise ValueError(
            "PDF 中没有提取到文字。\n"
            "如果这是扫描版简历，需要下一步加入 OCR。"
        )

    print("PDF 文本提取完成")

    resume = ResumeData(
        name=extract_name(text),
        phone=extract_phone(text),
        email=extract_email(text),

        education=extract_education(text),
        schools=extract_schools(text),
        majors=extract_majors(text),

        skills=extract_skills(text),

        projects=extract_projects(text),
        internships=extract_internships(text),

        raw_text=text,
    )

    return resume


# ============================================================
# 11. 保存 JSON
# ============================================================

def save_resume(resume: ResumeData, output_path: str):

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            resume.model_dump(),
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"\n结构化简历已保存：{output_path}")


# ============================================================
# 12. 命令行入口
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "用法：\n"
            "python resume_parser.py 简历.pdf\n\n"
            "例如：\n"
            "python resume_parser.py resume.pdf"
        )

        sys.exit(1)

    pdf_path = sys.argv[1]

    try:

        resume = parse_resume(pdf_path)

        print("\n")
        print("=" * 70)
        print("简历结构化解析结果")
        print("=" * 70)

        print(
            json.dumps(
                resume.model_dump(),
                ensure_ascii=False,
                indent=2
            )
        )

        output_path = (
            Path(pdf_path).with_suffix(".json")
        )

        save_resume(
            resume,
            str(output_path)
        )

    except Exception as e:

        print(f"\n解析失败：{e}")

        sys.exit(1)