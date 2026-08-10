# AI-Agent-Resume-Matching-System

> 基于 LangGraph + RAG + Tool Calling 构建的大模型 Agent 应用系统

一个面向复杂信息检索与智能分析场景的 LLM Agent 项目。

本项目通过 Agent 工作流编排、知识库检索、工具调用和大模型推理，实现从用户需求理解、信息检索到智能分析生成的完整流程。

项目以「个人能力分析与岗位匹配」作为业务 Demo 场景，用于验证大模型 Agent 在真实任务中的应用能力。


---

# ✨ 项目亮点

- 🚀 基于 LangGraph 构建 Agent 工作流
- 🔍 完整实现 RAG（Retrieval-Augmented Generation）流程
- 🛠 支持 Agent Tool Calling 工具调用
- 🧠 支持 Memory 对话状态管理
- 📚 构建个人知识库与业务知识库
- 🔄 实现 Query Understanding 与 Query Rewrite
- 🎯 支持向量检索 + Rerank 优化
- 🏗 采用模块化工程结构设计


---

# 🏗 系统架构

```
                         用户输入

                            |
                            v

                  Query Understanding

                            |
                            v

                     Query Rewrite

                            |
                            v

                    LangGraph Agent

                            |

        ------------------------------------------------

        |                    |                         |

        v                    v                         v

  Resume Tool          Job Search Tool          Match Tool


        |                    |                         |

        v                    v                         v


 Resume Vector DB     Job Vector DB          Match Chain


        |
        v

    Embedding

        |
        v

 Vector Retrieval

        |
        v

    Reranker

        |
        v

       LLM

        |
        v

    Final Response

```


---

# 🚀 核心功能


## 1. Agent 工作流

基于 LangGraph 实现 Agent 状态管理和任务编排。

整体流程：

```
用户问题

↓

任务理解

↓

Agent决策

↓

调用工具

↓

获取知识库信息

↓

结果分析

↓

生成最终回答

```


Agent 可以根据任务需求自动完成：

- 查询个人信息
- 查询岗位信息
- 分析能力匹配度
- 生成职业建议


---

# 2. RAG 检索增强生成系统

项目实现完整 RAG Pipeline：


```
Document

↓

Loader

↓

Text Splitter

↓

Embedding

↓

Vector Database

↓

Retriever

↓

Reranker

↓

LLM Generation

```


技术组件：

- BGE-small-zh-v1.5 Embedding
- Chroma Vector Database
- BGE Reranker


实现能力：

- 文档解析
- 文本切分
- 向量化
- 相似度检索
- Query Rewrite
- Multi Query Retrieval
- Rerank 优化


---

# 3. Query Understanding & Query Rewrite


用户输入自然语言问题：

例如：

```
分析我的Agent开发能力
```


系统自动理解用户需求，并生成适合向量检索的 Query：

```
Agent开发技能

Agent项目经验

智能体开发经验
```


提升复杂问题下的检索准确率。


---

# 4. Agent Tool Calling


Agent 通过工具调用完成任务。


当前设计工具：


## resume_search

个人知识库检索工具。

功能：

- 查询个人技能
- 查询项目经历
- 查询技术栈


---

## job_search

岗位知识库检索工具。

功能：

- 查询目标岗位
- 获取岗位技能要求
- 分析岗位方向


---

## job_match

岗位匹配分析工具。

功能：

- 对比用户能力和岗位要求
- 输出匹配结果
- 提供能力提升建议


---

# 5. Memory 状态管理


基于 LangGraph Checkpointer 实现 Agent 状态保存。


支持：

- 多轮对话
- 上下文保持
- Agent 状态管理


---

# 🛠 技术栈


## Large Language Model

- DeepSeek API


## Agent Framework

- LangChain
- LangGraph


## RAG

- Chroma
- BGE Embedding
- BGE Reranker


## Backend

- Python
- FastAPI


## Development

- Git
- Virtual Environment


---

# 📂 项目结构


```
AI-Agent-Resume-Matching-System

├── agents
│   └── Agent核心逻辑

├── api
│   └── API接口

├── chains
│   └── LLM流程链

├── tools
│   └── Agent工具

├── retrievers
│   └── 检索模块

├── vectorstores
│   └── Chroma向量数据库

├── embeddings
│   └── Embedding模块

├── rerankers
│   └── 重排序模块

├── memory
│   └── 状态管理

├── loaders
│   └── 文档加载

├── pipelines
│   └── RAG流程

├── prompts
│   └── Prompt模板

├── schemas
│   └── 数据结构

└── main.py

```


---

# ▶️ 项目运行


## 安装依赖

```bash
pip install -r requirements.txt
```


## 启动项目

```bash
python main.py
```


---

# 💡 Demo 示例


用户输入：

```
分析我的Agent开发能力
```


Agent执行流程：

```
1. 理解用户需求

2. Rewrite检索关键词

3. 查询个人知识库

4. 获取Agent相关经历

5. 分析技术能力

6. 生成能力报告

```


---

# 📊 技术能力覆盖


| 技术方向 | 实现 |
|---|---|
| LLM API调用 | ✅ |
| Prompt Engineering | ✅ |
| Agent开发 | ✅ |
| LangGraph | ✅ |
| Tool Calling | ✅ |
| Memory | ✅ |
| RAG | ✅ |
| Embedding | ✅ |
| Vector Database | ✅ |
| Query Rewrite | ✅ |
| Reranker | ✅ |


---

# 🌱 Future Work


计划继续优化：

- 多 Agent 协作
- Agent 自动规划
- 长期记忆系统
- Agent 可观测性
- Web 前端展示
- 服务部署


---

# 👨‍💻 Author

AI Agent Developer