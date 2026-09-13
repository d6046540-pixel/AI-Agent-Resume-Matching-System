# AI-Agent-Resume-Matching-System

> 基于 LangGraph + RAG + Tool Calling 构建的 AI 招聘辅助 Agent，面向企业 HR 招聘场景，实现候选人简历检索、岗位检索、岗位匹配、招聘风险分析与结构化面试方案生成。

## 项目简介

AI-Agent-Resume-Matching-System 是一个面向 HR 招聘场景的大模型 Agent 应用。

系统假设候选人已经进入招聘流程，HR 可以直接向 Agent 提出自然语言问题，Agent 根据当前任务自主选择合适的工具，对候选人的简历信息和岗位要求进行检索、匹配与分析，并最终生成招聘辅助结果。

核心业务流程：

候选人简历
→ 简历结构化
→ 简历知识库
→ HR 提问
→ Agent 判断任务
→ Tool Calling
→ 简历 / 岗位检索
→ Reranker 重排
→ 岗位匹配
→ 招聘风险分析
→ 结构化面试方案
→ HR 决策辅助

最终招聘决定由真人 HR 完成。

---

# Project Overview

传统简历筛选通常依赖关键词匹配，容易出现以下问题：

- 简历中的项目经验难以被充分利用
- 技能与岗位要求之间缺乏结构化比较
- 简历中的能力证据与技能标签可能不完全对应
- 候选人的风险点需要人工进一步判断
- 面试问题缺乏针对性

本项目使用 LLM Agent + RAG + Reranker + 确定性匹配引擎，将候选人信息、岗位信息和 HR 招聘任务结合起来。

系统不仅回答“这个候选人是否匹配”，还进一步回答：

- 为什么匹配？
- 哪些能力有明确证据？
- 哪些能力缺少证据？
- 哪些风险需要面试验证？
- 面试应该重点验证什么？

---

# System Architecture

![Architecture](docs/architecture.png)

核心架构：

```text
                         HR
                          │
                          ▼
                ┌──────────────────┐
                │   LangGraph      │
                │   AI Agent       │
                └────────┬─────────┘
                         │
                    Tool Calling
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
 resume_search       job_search       job_match
        │                │                │
        ▼                ▼                ▼
 Resume Vector DB   Job Vector DB   Match Engine
        │                │                │
        └────────────┬───┴────────────────┘
                     │
                  Reranker
                     │
                     ▼
             HR Candidate Analysis
                     │
                     ▼
          Generate Interview Plan
                     │
                     ▼
               HR Decision
Agent Workflow

Agent 根据 HR 的自然语言问题动态选择工具。

典型流程：

HR Question
     │
     ▼
Agent Intent Understanding
     │
     ▼
Tool Calling
     │
     ├── resume_search
     │       ↓
     │   Resume Knowledge Base
     │
     ├── job_search
     │       ↓
     │   Job Knowledge Base
     │
     ├── job_match
     │       ↓
     │   Deterministic Match Engine
     │
     ├── hr_candidate_analysis
     │       ↓
     │   Risk / Evidence Analysis
     │
     └── generate_interview_plan
             ↓
       Structured Interview Plan
             │
             ▼
        Final HR Response

Agent 并不是固定执行所有工具，而是根据 HR 当前任务选择需要的工具。

Core Features
1. LangGraph Agent

使用 LangGraph 构建 Agent 的任务编排与状态管理。

Agent 可以根据 HR 的自然语言问题：

理解当前任务
调用简历检索工具
调用岗位检索工具
执行岗位匹配
分析候选人风险
生成结构化面试方案
维护多轮对话状态

核心能力：

Agent Workflow
Tool Calling
State Management
Memory Checkpoint
Multi-step Task Execution
2. Resume RAG

针对候选人简历建立独立知识库。

RAG Pipeline：

Resume PDF
    ↓
Document Loader
    ↓
Text Splitting
    ↓
Embedding
    ↓
Chroma Vector Database
    ↓
Similarity Retrieval
    ↓
Query Rewrite
    ↓
Multi Query Retrieval
    ↓
Reranker
    ↓
Relevant Resume Evidence

支持：

PDF 简历解析
文本切分
Embedding
Chroma 向量数据库
相似度检索
Query Rewrite
Multi Query Retrieval
Reranking
3. Job RAG

针对岗位信息建立独立岗位知识库。

Job Information
    ↓
Normalization
    ↓
Document Processing
    ↓
Embedding
    ↓
Job Vector Database
    ↓
Similarity Retrieval
    ↓
Reranker
    ↓
Relevant Job Requirements

用于检索：

岗位职责
技术要求
技能要求
学历要求
工作经验要求
岗位方向
4. Query Rewrite

对于 HR 输入的复杂自然语言问题，系统首先进行查询改写，使其更加适合知识库检索。

例如：

HR：
分析这个候选人的 Agent 开发能力

可以转换为多个检索方向：

Agent 开发技能
Agent 项目经验
LangChain / LangGraph 项目经验
RAG 实践经验
Tool Calling 实践经验

然后执行 Multi Query Retrieval，提高复杂问题下的信息召回能力。

5. Reranking

向量检索主要负责召回候选文档，但召回结果不一定完全符合当前问题。

因此系统在向量检索之后增加 BGE Reranker：

Query
  ↓
Vector Retrieval
  ↓
Candidate Documents
  ↓
BGE Reranker
  ↓
Top Relevant Evidence

Reranker 使用 Query 与 Document 的语义相关性进行二次排序，使最终交给 Agent 的证据更加集中。

6. Agent Tool Calling

系统设计了 5 个核心工具。

Resume Search Tool

resume_search

用于从候选人简历知识库中检索相关证据。

主要功能：

查询候选人技能
查询项目经验
查询技术栈
查询简历中的具体经历
Job Search Tool

job_search

用于从岗位知识库中检索当前岗位要求。

主要功能：

查询岗位职责
查询技能要求
查询技术要求
查询学历与经验要求
Match Tool

job_match

用于完成候选人与岗位之间的匹配。

系统并不是简单让 LLM 直接给出一个分数，而是结合：

技能匹配
岗位职责匹配
项目证据
经验
学历
语义相关性

进行结构化匹配。

匹配结果可以进一步解释：

匹配点
不足
证据
风险
建议
HR Candidate Analysis Tool

hr_candidate_analysis

用于从 HR 招聘角度分析候选人。

重点关注：

候选人的主要优势
能力证据是否充分
技能深度风险
项目贡献真实性
简历信息缺口
需要在面试中进一步验证的信息

核心原则：

没有明确证据 ≠ 候选人一定不会，而是需要进一步验证。

Interview Plan Tool

generate_interview_plan

根据：

候选人简历
当前岗位要求
岗位匹配结果
风险信息

生成结构化面试方案。

包括：

面试维度
面试问题
验证目标
评分标准
风险验证点
面试时间建议
7. Deterministic Match Engine

岗位匹配中的核心评分不完全依赖 LLM。

系统通过 services/match_engine.py 实现确定性的匹配逻辑。

LLM 负责：

理解
分析
解释
生成报告

确定性程序负责：

匹配计算

这样做的优势：

结果更加可解释
降低 LLM 随机性对评分的影响
更容易调试
更适合招聘辅助场景
8. Memory & State Management

使用 LangGraph Checkpointer：

MemorySaver
     ↓
Thread ID
     ↓
Conversation State

支持：

多轮对话
Agent 状态保存
Workflow 状态管理
同一招聘任务下的上下文保持

例如 HR 可以先问：

这个候选人适合这个岗位吗？

然后继续问：

他的主要风险是什么？

Agent 可以基于同一个会话状态继续完成分析。

9. Streamlit Web Interface

项目提供 Streamlit Web 界面。

启动：

python -m streamlit run app.py

访问：

http://localhost:8501

HR 可以直接在聊天界面输入招聘问题。

例如：

请分析当前候选人的背景是否适合这个岗位，并说明主要匹配点和不足。

或者：

请重点分析这个候选人的招聘风险，以及哪些信息需要在面试中进一步验证。

或者：

请根据候选人的简历和当前岗位，设计一套结构化面试方案。
Evaluation

项目提供基础 Agent Evaluation。

测试重点：

Agent 是否正确选择工具
工具调用链是否符合预期
是否能够生成最终回答

测试场景：

Test Case	Result
候选人岗位匹配	✅
招聘风险分析	✅
结构化面试方案	✅

最终测试结果：

Evaluation Result

通过：3/3

✅ 全部测试通过

典型工具调用结果：

候选人岗位匹配：

resume_search
job_search
job_match
hr_candidate_analysis

结构化面试任务：

resume_search
job_search
job_match
hr_candidate_analysis
generate_interview_plan

Evaluation 主要用于验证 Agent 的基本工具选择能力与端到端执行能力，并不代表模型在真实招聘数据上的绝对准确率。

Technology       Stack
Category	     Technology
Language	     Python
Agent Framework	 LangGraph
LLM Framework	 LangChain
LLM	DeepSeek
Vector Database	 Chroma
Embedding	BGE  Embedding
Reranker	BGE  Reranker
Data Validation	 Pydantic
Web Interface	 Streamlit
Agent Memory	 LangGraph Checkpointer
Retrieval	     RAG
Agent Capability Tool Calling
Model Provider	 DeepSeek API
Project Structure
AI-Agent-Resume-Matching-System/
│
├── agents/
│   └── Agent相关逻辑
│
├── api/
│   └── 接口相关模块
│
├── chains/
│   ├── hr_analysis_chain.py
│   ├── interview_chain.py
│   ├── match_chain.py
│   ├── query_rewriter.py
│   ├── query_understanding.py
│   └── rag_chain.py
│
├── embeddings/
│   └── Embedding相关模块
│
├── evaluation/
│   ├── evaluate.py
│   └── test_cases.json
│
├── factories/
│   └── agent_factory.py
│
├── loaders/
│   └── 文档加载
│
├── memory/
│   └── Agent状态与记忆
│
├── models/
│   └── 模型相关模块
│
├── pipelines/
│   └── RAG Pipeline
│
├── prompts/
│   └── Prompt模板
│
├── rerankers/
│   └── reranker.py
│
├── retrievers/
│   └── 检索模块
│
├── schemas/
│   └── Pydantic数据结构
│
├── services/
│   ├── match_engine.py
│   └── skill_extractor.py
│
├── splitters/
│   └── 文本切分
│
├── states/
│   └── LangGraph State
│
├── tools/
│   ├── resume_tool.py
│   ├── job_tool.py
│   ├── match_tool.py
│   ├── hr_analysis_tool.py
│   └── interview_tool.py
│
├── vectorstores/
│   └── Chroma Vector Store
│
├── app.py
├── main.py
├── config.py
├── requirements.txt
├── .env
└── README.md
Installation
1. Clone Repository
git clone https://github.com/d6046540-pixel/AI-Agent-Resume-Matching-System.git

cd AI-Agent-Resume-Matching-System
2. Create Virtual Environment
python -m venv .venv

Windows:

.\.venv\Scripts\Activate.ps1
3. Install Dependencies
python -m pip install -r requirements.txt
4. Configure Environment Variables

创建 .env：

DEEPSEEK_API_KEY=your_api_key
HF_TOKEN=your_huggingface_token

请勿将真实 API Key 或 Token 提交到 GitHub。

5. Build Knowledge Base

根据项目数据执行：

python build_resume_db.py

以及：

python build_job_db.py
6. Run CLI Agent
python main.py
7. Run Web Application
python -m streamlit run app.py

然后访问：

http://localhost:8501
Example
HR Question
请分析当前候选人的背景是否适合这个岗位，并说明主要匹配点和不足。
Agent
1. 理解 HR 当前任务
2. 检索候选人简历
3. 检索岗位要求
4. 执行岗位匹配
5. 分析匹配点与不足
6. 输出 HR 招聘辅助结果
Engineering Highlights
Agent Orchestration

不是简单的单轮 LLM 问答，而是：

User Query
    ↓
Agent
    ↓
Tool Selection
    ↓
Multiple Tools
    ↓
Evidence Retrieval
    ↓
Analysis
    ↓
Final Response
Evidence-based Analysis

系统尽可能基于简历和岗位检索结果进行分析，而不是完全依赖模型记忆。

Deterministic Matching

匹配计算由程序逻辑完成，LLM 主要负责理解和解释，提高结果的可解释性。

RAG + Reranking

使用：

Embedding Retrieval
        +
BGE Reranker

提升招聘信息检索的相关性。

Human-in-the-loop

系统定位为：

AI Decision Support

而不是：

AI Automated Hiring

最终招聘决定由 HR 做出。

Project Status

当前项目已经完成：

✅ LLM API
✅ Prompt Engineering
✅ Agent Development
✅ LangGraph
✅ Tool Calling
✅ Agent Memory
✅ Resume RAG
✅ Job RAG
✅ Embedding
✅ Chroma Vector Database
✅ Query Rewrite
✅ Multi Query Retrieval
✅ BGE Reranker
✅ Deterministic Match Engine
✅ HR Risk Analysis
✅ Structured Interview Generation
✅ Streamlit Web Interface
✅ Agent Evaluation

Evaluation：

3 / 3 Passed
Future Improvements

后续可进一步优化：

LangSmith / Langfuse Observability
更完善的 Agent Evaluation
更细粒度的招聘指标体系
更丰富的岗位数据
Production Deployment
权限管理
招聘数据脱敏与隐私保护
更完善的 HR Dashboard
Disclaimer

本项目用于展示 AI Agent、RAG、Tool Calling 和招聘辅助系统的工程实现。

系统输出仅作为 HR 的辅助参考，不应作为自动化招聘决策的唯一依据。

招聘过程中应避免基于敏感个人信息进行不当决策，并结合人工面试与实际业务要求进行综合判断。