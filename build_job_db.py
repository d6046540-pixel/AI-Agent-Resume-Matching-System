import json
import shutil
from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ============================================================
# 1. 路径
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

JOB_JSON_PATH = BASE_DIR / "job.json"
CHROMA_DB_PATH = BASE_DIR / "job_chroma_db"


# ============================================================
# 2. 读取岗位
# ============================================================

if not JOB_JSON_PATH.exists():
    raise FileNotFoundError(
        f"找不到岗位文件：{JOB_JSON_PATH}"
    )

with open(JOB_JSON_PATH, "r", encoding="utf-8") as f:
    jobs = json.load(f)

if not isinstance(jobs, list):
    raise ValueError(
        "job.json 最外层必须是 JSON 数组，例如：[{}, {}]"
    )

print(f"读取真实岗位：{len(jobs)} 条")


# ============================================================
# 3. 清除旧数据库
# ============================================================

if CHROMA_DB_PATH.exists():
    shutil.rmtree(CHROMA_DB_PATH)
    print("旧岗位数据库已清除")


# ============================================================
# 4. 岗位标准化 + Document
# ============================================================

documents = []

for index, job in enumerate(jobs):

    # ---------- 基础字段 ----------

    job_id = job.get("job_id") or f"job_{index + 1:05d}"

    title = job.get("title", "")
    company = job.get("company", "")

    city = job.get("city", "")
    province = job.get("province", "")
    district = job.get("district", "")

    category = job.get("category", "")
    level = job.get("level", "")

    employment_type = job.get("employment_type", "")
    work_mode = job.get("work_mode", "")

    education = job.get("education", "")

    experience_min = job.get("experience_years_min")
    experience_max = job.get("experience_years_max")

    skills = job.get("skills", [])
    if not isinstance(skills, list):
        skills = []

    skills = [
        str(skill).strip()
        for skill in skills
        if str(skill).strip()
    ]

    description = job.get("description", "")

    salary_min = job.get("salary_min")
    salary_max = job.get("salary_max")
    salary_unit = job.get("salary_unit", "")

    url = job.get("url", "")
    source = job.get("source", "")

    posted_at = job.get("posted_at", "")
    status = job.get("status", "active")


    # ========================================================
    # 5. 构造用于向量检索的文本
    # ========================================================

    skills_text = ", ".join(skills)

    page_content = f"""
岗位名称：{title}

公司：{company}

城市：{city}

省份：{province}

区县：{district}

岗位类别：{category}

岗位级别：{level}

岗位类型：{employment_type}

工作模式：{work_mode}

学历要求：{education}

最低经验：{experience_min} 年

最高经验：{experience_max} 年

技能要求：{skills_text}

薪资：{salary_min}-{salary_max} {salary_unit}

岗位描述：
{description}
""".strip()


    # ========================================================
    # 6. metadata
    # ========================================================

    metadata = {
        "job_id": str(job_id),
        "title": str(title),
        "company": str(company),

        "city": str(city),
        "province": str(province),
        "district": str(district),

        "category": str(category),
        "level": str(level),

        "employment_type": str(employment_type),
        "work_mode": str(work_mode),

        "education": str(education),

        "experience_years_min": (
            experience_min if experience_min is not None else -1
        ),

        "experience_years_max": (
            experience_max if experience_max is not None else -1
        ),

        # Chroma metadata 不适合直接保存 list
        "skills": skills_text,

        "salary_min": (
            salary_min if salary_min is not None else -1
        ),

        "salary_max": (
            salary_max if salary_max is not None else -1
        ),

        "salary_unit": str(salary_unit),

        "url": str(url),
        "source": str(source),
        "posted_at": str(posted_at),
        "status": str(status),
    }


    documents.append(
        Document(
            page_content=page_content,
            metadata=metadata
        )
    )


# ============================================================
# 7. Embedding
# ============================================================

print("正在加载 Embedding 模型...")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True
    }
)

print("Embedding 模型加载完成")


# ============================================================
# 8. 创建 Chroma
# ============================================================

print("正在创建岗位向量数据库...")

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory=str(CHROMA_DB_PATH),
    collection_name="jobs"
)


# ============================================================
# 9. 数据库健康检查
# ============================================================

actual_count = vectorstore._collection.count()

print()
print("=" * 60)
print("岗位数据库健康检查")
print("=" * 60)

print(f"JSON 岗位数量：{len(documents)}")
print(f"Chroma 实际数量：{actual_count}")
print(f"Collection：jobs")
print(f"数据库位置：{CHROMA_DB_PATH}")


if actual_count != len(documents):

    raise RuntimeError(
        f"""
岗位数据库写入失败！

JSON 岗位数量：{len(documents)}
Chroma 实际数量：{actual_count}

请不要启动 Agent。
"""
    )


if actual_count == 0:

    raise RuntimeError(
        "Chroma 数据库为空，禁止继续运行。"
    )


print()
print("✅ 岗位向量数据库健康")
print("✅ 岗位已经成功写入 Chroma")
print("=" * 60)