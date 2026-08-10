import os
from dotenv import load_dotenv


# ======================
# 环境变量
# ======================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


load_dotenv(
    os.path.join(BASE_DIR, ".env")
)



# ======================
# DeepSeek
# ======================

DEEPSEEK_API_KEY = os.getenv(
    "sk-a40d383a6ad343f1a9847f2254f5ea61"
)

DEEPSEEK_BASE_URL = (
    "https://api.deepseek.com"
)



# ======================
# SiliconFlow
# ======================

SILICONFLOW_API_KEY = os.getenv(
    "sk-xtnxbdydsyfxdvpenkjwutwnkhtlfffuxdwjmvheqsofaxju"
)

SILICONFLOW_BASE_URL = (
    "https://api.siliconflow.cn/v1"
)



# ======================
# Embedding配置
# ======================

EMBEDDING_MODEL = (
    "BAAI/bge-large-zh-v1.5"
)


# 向量维度
EMBEDDING_DIMENSION = 1024