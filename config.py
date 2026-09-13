import os
from dotenv import load_dotenv


# =========================
# 项目根目录
# =========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# =========================
# 加载 .env
# =========================

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)


# =========================
# DeepSeek
# =========================

DEEPSEEK_API_KEY = os.getenv(
    "DEEPSEEK_API_KEY"
)

DEEPSEEK_BASE_URL = os.getenv(
    "DEEPSEEK_BASE_URL",
    "https://api.deepseek.com"
)


# =========================
# LLM
# =========================

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "deepseek-v4-flash"
)

LLM_TEMPERATURE = float(
    os.getenv(
        "LLM_TEMPERATURE",
        "0"
    )
)


# =========================
# Embedding
# =========================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-large-zh-v1.5"
)

EMBEDDING_DIMENSION = int(
    os.getenv(
        "EMBEDDING_DIMENSION",
        "1024"
    )
)