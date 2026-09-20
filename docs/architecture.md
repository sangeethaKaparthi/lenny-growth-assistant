# Architecture Specification
# The Lenny Growth Assistant

## 1. Architecture Overview

The Lenny Growth Assistant uses a full-stack architecture consisting of:

- React/Next.js frontend
- FastAPI backend
- PostgreSQL database
- pgvector for vector similarity search
- Ollama for local LLM inference
- Optional cloud LLM provider
- Docker Compose for deployment

The backend is responsible for API requests, retrieval, LLM provider
selection, persistence, and artifact generation.

The frontend is responsible for the chat interface, streaming responses,
provider selection, session history, and artifact rendering.

---

## 2. High-Level Architecture

```text
                    ┌──────────────────────┐
                    │      User            │
                    │  Growth Product PM   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React / Next.js    │
                    │      Frontend        │
                    └──────────┬───────────┘
                               │ HTTP / SSE
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │ RAG Engine  │  │ LLM Router  │  │ Persistence │
       └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
              │                │                │
              ▼                ▼                ▼
       ┌─────────────┐   ┌─────────────┐  ┌─────────────┐
       │ PostgreSQL  │   │   Ollama    │  │ PostgreSQL  │
       │ + pgvector  │   │    Local    │  │   Sessions  │
       └─────────────┘   └──────┬──────┘  │   Messages  │
                                │         │  Artifacts  │
                                ▼         └─────────────┘
                         ┌─────────────┐
                         │ Cloud LLM   │
                         │  Optional   │
                         └─────────────┘