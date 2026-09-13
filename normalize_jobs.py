import json
import re
from pathlib import Path


# =========================================================
# 1. 配置
# =========================================================

INPUT_PATH = Path("./job.json")
OUTPUT_PATH = Path("./normalized_jobs.json")


# =========================================================
# 2. 中国城市标准化
# =========================================================

CITY_MAP = {
    "北京": ("北京市", "北京市"),
    "北京市": ("北京市", "北京市"),

    "上海": ("上海市", "上海市"),
    "上海市": ("上海市", "上海市"),

    "广州": ("广东省", "广州市"),
    "广州市": ("广东省", "广州市"),

    "深圳": ("广东省", "深圳市"),
    "深圳市": ("广东省", "深圳市"),

    "杭州": ("浙江省", "杭州市"),
    "杭州市": ("浙江省", "杭州市"),

    "南京": ("江苏省", "南京市"),
    "南京市": ("江苏省", "南京市"),

    "苏州": ("江苏省", "苏州市"),
    "苏州市": ("江苏省", "苏州市"),

    "成都": ("四川省", "成都市"),
    "成都市": ("四川省", "成都市"),

    "武汉": ("湖北省", "武汉市"),
    "武汉市": ("湖北省", "武汉市"),

    "西安": ("陕西省", "西安市"),
    "西安市": ("陕西省", "西安市"),

    "重庆": ("重庆市", "重庆市"),
    "重庆市": ("重庆市", "重庆市"),

    "天津": ("天津市", "天津市"),
    "天津市": ("天津市", "天津市"),

    "厦门": ("福建省", "厦门市"),
    "厦门市": ("福建省", "厦门市"),

    "长沙": ("湖南省", "长沙市"),
    "长沙市": ("湖南省", "长沙市"),

    "郑州": ("河南省", "郑州市"),
    "郑州市": ("河南省", "郑州市"),

    "合肥": ("安徽省", "合肥市"),
    "合肥市": ("安徽省", "合肥市"),

    "青岛": ("山东省", "青岛市"),
    "青岛市": ("山东省", "青岛市"),

    "济南": ("山东省", "济南市"),
    "济南市": ("山东省", "济南市"),

    "宁波": ("浙江省", "宁波市"),
    "宁波市": ("浙江省", "宁波市"),

    "东莞": ("广东省", "东莞市"),
    "东莞市": ("广东省", "东莞市"),
}


def normalize_city(city):
    """
    将各种城市写法统一成：
    province + city
    """

    if not city:
        return "", ""

    city = str(city).strip()

    # 直接匹配
    if city in CITY_MAP:
        province, standard_city = CITY_MAP[city]
        return province, standard_city

    # 模糊匹配
    for key, value in CITY_MAP.items():
        if key in city:
            return value

    return "", city


# =========================================================
# 3. 岗位级别标准化
# =========================================================

def normalize_level(title, level):
    text = f"{title} {level}".lower()

    if any(x in text for x in [
        "实习",
        "intern",
        "internship"
    ]):
        return "实习"

    if any(x in text for x in [
        "应届",
        "校招",
        "graduate",
        "entry level"
    ]):
        return "应届"

    if any(x in text for x in [
        "junior",
        "初级"
    ]):
        return "初级"

    if any(x in text for x in [
        "senior",
        "高级"
    ]):
        return "高级"

    if any(x in text for x in [
        "lead",
        "负责人",
        "主管"
    ]):
        return "负责人"

    if any(x in text for x in [
        "manager",
        "经理"
    ]):
        return "经理"

    return level or ""


# =========================================================
# 4. 岗位类别标准化
# =========================================================

def normalize_category(title, category):
    text = f"{title} {category}".lower()

    if any(x in text for x in [
        "agent",
        "ai开发",
        "ai developer",
        "算法",
        "python开发",
        "大模型",
        "llm",
        "rag"
    ]):
        return "AI开发"

    if any(x in text for x in [
        "产品经理",
        "ai产品",
        "product manager"
    ]):
        return "AI产品"

    if any(x in text for x in [
        "数据分析",
        "data analyst",
        "数据科学",
        "data scientist"
    ]):
        return "数据"

    if any(x in text for x in [
        "测试",
        "qa",
        "test engineer"
    ]):
        return "测试"

    if any(x in text for x in [
        "后端",
        "backend"
    ]):
        return "后端开发"

    if any(x in text for x in [
        "前端",
        "frontend"
    ]):
        return "前端开发"

    if any(x in text for x in [
        "运维",
        "devops"
    ]):
        return "运维"

    return category or "其他"


# =========================================================
# 5. 工作模式标准化
# =========================================================

def normalize_work_mode(value):
    if not value:
        return ""

    text = str(value).lower()

    if "remote" in text or "远程" in text:
        return "远程"

    if "hybrid" in text or "混合" in text:
        return "混合办公"

    if "office" in text or "现场" in text:
        return "现场办公"

    return value


# =========================================================
# 6. 技能标准化
# =========================================================

def normalize_skills(skills):
    if not skills:
        return []

    if isinstance(skills, str):

        # 支持：
        # Python, RAG, LangChain
        # Python、RAG、LangChain

        skills = re.split(r"[,，、;；|]", skills)

    result = []

    for skill in skills:

        skill = str(skill).strip()

        if skill and skill not in result:
            result.append(skill)

    return result


# =========================================================
# 7. 经验年限标准化
# =========================================================

def normalize_experience(value):

    if value is None:
        return None

    if isinstance(value, int):
        return value

    text = str(value)

    match = re.search(r"(\d+)", text)

    if match:
        return int(match.group(1))

    return None


# =========================================================
# 8. 单条岗位标准化
# =========================================================

def normalize_job(job, index):

    title = str(
        job.get("title", "")
    ).strip()

    content = str(
        job.get("content", "")
    ).strip()

    company = str(
        job.get("company", "")
    ).strip()

    # -----------------------------------------------------
    # 城市
    # -----------------------------------------------------

    raw_city = (
        job.get("city")
        or job.get("location")
        or ""
    )

    province, city = normalize_city(raw_city)

    # -----------------------------------------------------
    # 基础字段
    # -----------------------------------------------------

    category = normalize_category(
        title,
        job.get("category", "")
    )

    level = normalize_level(
        title,
        job.get("level", "")
    )

    employment_type = job.get(
        "employment_type",
        ""
    )

    work_mode = normalize_work_mode(
        job.get("work_mode", "")
    )

    skills = normalize_skills(
        job.get("skills", [])
    )

    experience_min = normalize_experience(
        job.get("experience_years_min")
    )

    # -----------------------------------------------------
    # 生成岗位 ID
    # -----------------------------------------------------

    job_id = (
        job.get("job_id")
        or f"job_{index:06d}"
    )

    # -----------------------------------------------------
    # 标准岗位对象
    # -----------------------------------------------------

    normalized_job = {

        "job_id": job_id,

        "title": title,

        "company": company,

        "city": city,

        "province": province,

        "district": job.get(
            "district",
            ""
        ),

        "category": category,

        "level": level,

        "employment_type": employment_type,

        "work_mode": work_mode,

        "education": job.get(
            "education",
            ""
        ),

        "experience_years_min": experience_min,

        "experience_years_max": job.get(
            "experience_years_max"
        ),

        "skills": skills,

        "description": content,

        "salary_min": job.get(
            "salary_min"
        ),

        "salary_max": job.get(
            "salary_max"
        ),

        "salary_unit": job.get(
            "salary_unit",
            ""
        ),

        "url": job.get(
            "url",
            ""
        ),

        "source": job.get(
            "source",
            "manual"
        ),

        "posted_at": job.get(
            "posted_at",
            ""
        ),

        "status": job.get(
            "status",
            "active"
        )
    }

    return normalized_job


# =========================================================
# 9. 主程序
# =========================================================

def main():

    print("=" * 70)
    print("真实岗位 → 标准化岗位数据")
    print("=" * 70)

    # -----------------------------------------------------
    # 读取原始岗位
    # -----------------------------------------------------

    if not INPUT_PATH.exists():

        raise FileNotFoundError(
            f"找不到岗位文件：{INPUT_PATH}"
        )

    with open(
        INPUT_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        jobs = json.load(f)

    if not isinstance(jobs, list):

        raise ValueError(
            "job.json 必须是岗位数组 []"
        )

    print(
        f"读取原始岗位：{len(jobs)} 条"
    )

    # -----------------------------------------------------
    # 标准化
    # -----------------------------------------------------

    normalized_jobs = []

    for index, job in enumerate(
        jobs,
        start=1
    ):

        normalized_job = normalize_job(
            job,
            index
        )

        normalized_jobs.append(
            normalized_job
        )

    # -----------------------------------------------------
    # 保存
    # -----------------------------------------------------

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            normalized_jobs,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"标准化岗位：{len(normalized_jobs)} 条"
    )

    print(
        f"输出文件：{OUTPUT_PATH}"
    )

    print("=" * 70)

    # -----------------------------------------------------
    # 展示前几条
    # -----------------------------------------------------

    for job in normalized_jobs[:5]:

        print("\n岗位：", job["title"])
        print("公司：", job["company"])
        print("城市：", job["city"])
        print("省份：", job["province"])
        print("类别：", job["category"])
        print("级别：", job["level"])
        print("技能：", job["skills"])

    print("\n标准化完成。")


if __name__ == "__main__":
    main()