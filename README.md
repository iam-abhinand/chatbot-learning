# simple-chatbot (Django + React + Claude )🚀
A minimal chatbot with a Django backend, React frontend, and Claude API integration (Need an Anthropic API key with a funded credit balance( Hope you have it own your own or like me, you can use a friend's API key - No, i did not annoy him :) ) — built end-to-end, one concept at a time, as a learning project.

## 📌 Motivation & Purpose
I built this to get hands-on practice bridging my existing backend/Django background and build a chatbot using the Anthropic Messages API — as part of learning.

## 🛠️ Tech Stack & Concepts (Existing Knowledge + Learning Re-Enforcement)
- **Backend**: Django 6, Django REST Framework, `anthropic` Python SDK
- **Frontend**: React 18 + Vite
- **ML/AI**: PyTorch, sentence-transformers, scikit-learn, CUDA support
- **Tools**: Docker, Docker Compose, `uv` (Rust-based pip/venv replacement), Git
- **Key New Concepts Learned**:
  - The Anthropic Messages API shape — `role`/`content` list, `system` prompt as a separate parameter, `stop_reason`, token usage accounting, and the fact that the API itself has no memory between calls
  - **Conversation Management**: Sliding window strategy to manage context window size, maintaining conversation history across turns
  - **Tool/Function Calling**: Implementing Claude's tool calling protocol with custom Python functions, handling multi-turn tool execution loops
  - **RAG (Retrieval-Augmented Generation)**: Building semantic search with sentence embeddings, cosine similarity for document retrieval, context injection into prompts
  - **Embeddings**: Using sentence-transformers (all-MiniLM-L6-v2) for semantic similarity, understanding vector representations of text
  - **Token Counting**: Using Anthropic's count_tokens API for cost estimation and context management
  - **Agentic Loops**: Extending tool-use into multi-tool chains where Claude autonomously sequences calls (e.g. reverse text, then count the result) without hardcoded step order; added a hard iteration cap (`MAX_TOOL_ITERATIONS`) since an agent that decides its own step count can otherwise loop indefinitely, billing every round
  - **MCP (Model Context Protocol)**: Built a standalone MCP server (`step_mcp_server.py`) exposing tools via the decorator-based API, and a client (`step_mcp_client.py`) that discovers tools dynamically at runtime via `list_tools()` rather than importing a hardcoded list — proof-of-concept only, not wired into the Django app itself

## 🔮 Could Add / To-Do
- [x] ~~Could Add a simple UI for selecting different models~~ (✅ Implemented - model dropdown added)
- [ ] Could Add a `Conversation`/`Message` model + Postgres for persistent chat history
- [ ] Could Add more tools beyond count_words (e.g., web search, file operations)
- [ ] Could Make the system configured to do a specific task such as a coding assistant or a tutor
- [ ] Could Write tests for the serializer and view error paths
- [ ] Could Pin dependency versions deliberately (currently unpinned — picked up Django 6 unexpectedly on install)
