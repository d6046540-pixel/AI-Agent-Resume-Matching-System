# AI-Agent-Resume-Matching-System

基于 LangGraph + RAG 构建的 AI Agent 岗位匹配系统。

该项目模拟真实招聘场景，通过 Agent 自动理解用户需求，调用简历知识库和岗位知识库，实现：

- 个人能力分析
- 技能画像生成
- AI岗位检索
- 岗位匹配度分析
- 求职方向推荐


## 项目背景

传统求职过程中，用户通常需要：

- 手动阅读大量岗位JD
- 对比自身技能与岗位要求
- 分析能力差距

本项目通过 AI Agent 自动完成：


用户需求
↓
Agent任务理解
↓
调用检索工具
↓
RAG知识库查询
↓
岗位匹配分析
↓
生成求职建议



# 核心功能

## 1. 简历知识库

将个人简历转换为向量数据库。

支持：

- 技术技能查询
- 项目经历分析
- 教育背景查询
- Agent能力评估


技术：

- BGE-small-zh-v1.5 Embedding
- Chroma Vector Database


---

## 2. 岗位知识库

构建AI岗位数据库。

支持：

- 岗位搜索
- 技能要求分析
- 城市筛选
- 岗位类别筛选


岗位信息包含：

- 岗位名称
- 公司
- 城市
- 技术要求
- 工作描述


---

## 3. RAG检索增强生成


完整RAG流程：


用户问题

↓

Query Understanding

↓

Query Rewrite

↓

Embedding向量化

↓

Chroma相似度检索

↓

Rerank重新排序

↓

LLM生成回答



使用技术：

- Embedding模型：
  BAAI/bge-small-zh-v1.5

- Reranker：
  BAAI/bge-reranker-base

- Vector Database：
  Chroma


---

# Agent架构


             User

              |

              ↓

      LangGraph Agent

              |

    ------------------

    |                |

    ↓                ↓

resume_search job_search

简历知识库 岗位知识库

    |

    ↓


job_match Tool


    |

    ↓


 LLM分析生成

    |

    ↓


最终求职建议


---

# Agent设计

## Agent核心能力


### Tool Calling

设计多个Agent工具：

### resume_search

功能：

查询个人简历信息。

例如：


分析我的Agent开发能力



---

### job_search

功能：

搜索目标岗位。

例如：


杭州AI Agent开发实习



---

### job_match

功能：

分析：

- 技能匹配度
- 项目匹配度
- 能力差距
- 学习建议



---

# 技术栈


## AI Agent

- LangGraph
- LangChain


## LLM

- DeepSeek API


## RAG

- Chroma
- BGE Embedding
- BGE Reranker


## Development

- Python
- Git
- VS Code



---

# 项目亮点


## 1. Agent系统设计

基于LangGraph实现：

- Agent状态管理
- Tool调用
- 工作流编排


## 2. 完整RAG链路

实现：

- 文档处理
- Embedding
- 向量检索
- Query Rewrite
- Multi Query Retrieval
- Rerank


## 3. 面向真实场景

不是简单Demo，而是针对：

> AI求职岗位匹配场景

设计完整Agent应用。



---

# 项目运行


## 安装依赖

```bash
pip install -r requirements.txt
启动
python test_agent.py
示例

用户：

分析我的Agent开发能力

Agent：

查询简历知识库

↓

检索Agent技能

↓

分析项目经验

↓

生成能力评价
Future Improvements

计划增加：

多Agent协作
长期记忆
Web岗位实时搜索
FastAPI接口
Streamlit可视化界面
Agent监控与日志系统
Author

AI Agent Developer Intern Candidate


---

# 二、项目架构图

在项目根目录新建：

```text
docs
 └── architecture.md

写：

# System Architecture


             User

              |

              v

      LangGraph Agent

              |

    ------------------

    |                |

    v                v

Resume Tool Job Tool

    |                |

    v                v

Resume VectorDB Job VectorDB

    \              /

      \          /

         v

    Job Match Tool


         |

         v


      LLM


         |

         v


    Final Response


## RAG Pipeline



Document

↓

Text Split

↓

Embedding

↓

Chroma

User Query

↓

Query Rewrite

↓

Retriever

↓

Reranker

↓

Context

↓

LLM
