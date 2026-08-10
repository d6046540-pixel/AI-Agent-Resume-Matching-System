# AI-Agent-Resume-Matching-System Architecture

## System Architecture

```mermaid
flowchart TD

A[User Query] --> B[FastAPI API]

B --> C[LangGraph Agent]

C --> D[Query Understanding]

C --> E[Query Rewrite]

C --> F[Resume Tool]

C --> G[Job Search Tool]

C --> H[Match Tool]

F --> I[Resume Vector Database]

G --> J[Job Vector Database]

I --> K[BGE Embedding]

J --> K

K --> L[Vector Retrieval]

L --> M[BGE Reranker]

M --> N[DeepSeek LLM]

N --> O[Career Analysis Report]
Agent Workflow
User Input

↓

Query Understanding

↓

Query Rewrite

↓

Multi Query Retrieval

↓

Vector Database Search

↓

Document Retrieval

↓

BGE Reranker

↓

LangGraph Agent Reasoning

↓

Tool Calling

↓

LLM Generation

↓

Career Analysis Report
Core Components
1. Agent Layer
   LangGraph Agent Workflow
   ReAct Agent Architecture
   Tool Calling
   Memory Checkpoint
   State Management
2. RAG Retrieval Layer
   Resume Knowledge Base
   Job Knowledge Base
   Document Loading
   Text Splitting
   BGE Embedding
   Chroma Vector Database
   Similarity Retrieval
   Query Rewrite
   Multi Query Search
   BGE Reranker
3. Tool Layer
Resume Tool

负责：

简历信息检索
用户技能分析
项目经验提取
Job Search Tool

负责：

岗位信息检索
JD分析
技能需求匹配
Match Tool

负责：

用户能力与岗位需求对比
匹配度分析
职业建议生成
4. LLM Layer

Model:

DeepSeek API

负责：

Agent推理
信息整合
最终职业分析报告生成
5. Data Layer
Resume PDF

↓

PDF Loader

↓

Text Splitter

↓

Embedding Model

↓

Chroma Vector Database
Job Dataset

↓

Job Loader

↓

Text Processing

↓

Embedding Model

↓

Job Vector Database
Technology Stack
Category	            Technology
Programming Language	Python
Agent Framework	        LangGraph
LLM Framework	        LangChain
Vector Database	        ChromaDB
Embedding	            BGE         Embedding
Reranker	            BGE Reranker
API Framework	        FastAPI
Data Validation	        Pydantic
LLM API	                DeepSeek
Project Design Highlights:
  End-to-end Agent application development
  RAG + Agent combination architecture
  Vector retrieval optimization
  Query rewriting strategy
  Reranking improvement
  Persistent Agent memory
  Modular project architecture
  Future Improvements
  Multi-Agent collaboration
  Long-term memory system
  Agent evaluation framework
  LangSmith/Langfuse observability
  Production deployment