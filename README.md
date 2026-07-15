# simple-chatbot (Django + React + Claude )🚀
A minimal chatbot with a Django backend, React frontend, and Claude API integration (Need an Anthropic API key with a funded credit balance( Hope you have it own your own or like me, you can use a friend's API key - No, i did not annoy him :) ) — built end-to-end, one concept at a time, as a learning project.

## 📌 Motivation & Purpose
I built this to get hands-on practice bridging my existing backend/Django background and build a chatbot using the Anthropic Messages API — as part of learning.

## 🛠️ Tech Stack & Concepts (Existing Knowledge + Learning Re-Enforcement)
- **Backend**: Django 6, Django REST Framework, `anthropic` Python SDK
- **Frontend**: React 18 + Vite
- **Tools**: Docker, Docker Compose, `uv` (Rust-based pip/venv replacement), Git
- **Key New Concepts Learned**:
  - The Anthropic Messages API shape — `role`/`content` list, `system` prompt as a separate parameter, `stop_reason`, token usage accounting, and the fact that the API itself has no memory between calls

## 🔮 Could Add / To-Do
- [ ] Could Add a `Conversation`/`Message` model + Postgres for persistent chat history
- [ ] Could Add a simple UI for selecting different models or adjusting temperature
- [ ] Could Make the system configured to do a specific task such as a coding assistant or a tutor
- [ ] Could Write tests for the serializer and view error paths
- [ ] Could Pin dependency versions deliberately (currently unpinned — picked up Django 6 unexpectedly on install)
