The Lenny Growth Assistant

A full-stack, transcript-grounded AI assistant for exploring insights from Lenny's Podcast.

The application retrieves relevant Lenny's Podcast transcript chunks from PostgreSQL + pgvector, generates grounded answers with a local Ollama model, supports a cloud-provider abstraction, and provides a Ship30 for 30 content mode with an in-app Artifact Viewer.

Features

Transcript-grounded Q&A using Lenny's Podcast transcripts

RAG retrieval with PostgreSQL and pgvector

Source attribution with episode, guest, and timestamp metadata

Exact insufficient-context response when relevant transcript information is unavailable

Ship30 for 30 mode for approximately 1,250-word actionable essays

Artifact Viewer for Markdown and sandboxed HTML/CSS artifacts

Local Ollama model support

Cloud LLM provider abstraction

Streaming responses using Server-Sent Events (SSE)

Session and message persistence

Health endpoint

Docker Compose support

Architecture

React / Next.js Frontend
        |
        | HTTP / SSE
        v
FastAPI Backend
   |        |        |
   v        v        v
PostgreSQL RAG    LLM Provider
+ pgvector        |
                  +-- Ollama (local)
                  +-- Cloud provider

Project Structure

lenny-growth-assistant/
├── .env.example
├── docker-compose.yml
├── README.md
├── docs/
│   ├── PRD.md
│   ├── architecture.md
│   └── design.md
├── agent_transcripts/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── scripts/
│   │   ├── download_transcripts.py
│   │   └── ingest.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── providers/
│   │   ├── rag/
│   │   ├── skills/
│   │   └── api/
│   └── tests/
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── tailwind.config.js
    ├── tsconfig.json
    └── src/
        ├── app/
        ├── components/
        ├── hooks/
        └── lib/

Tech Stack

Backend

Python 3.11+

FastAPI

Uvicorn

Pydantic v2

SQLAlchemy async

asyncpg

PostgreSQL

pgvector

sentence-transformers

Ollama

Frontend

React / Next.js

TypeScript

Tailwind CSS

react-markdown

remark-gfm

DOMPurify

Infrastructure

Docker

Docker Compose

PostgreSQL + pgvector

Ollama

Prerequisites

Install:

Python 3.11+

Node.js

Docker Desktop

Ollama

Pull the local model:

ollama pull llama3.2:3b

Verify:

ollama list

Environment Configuration

Create:

backend/.env

Example:

DATABASE_URL=postgresql+asyncpg://postgres:lenny_dev_password@127.0.0.1:5433/lenny_assistant

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

DEFAULT_LLM_PROVIDER=ollama

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

For the frontend:

NEXT_PUBLIC_API_URL=http://localhost:8000

Do not commit real API keys or secrets.

Transcript Ingestion

Transcript data is stored under:

data/

The ingestion pipeline:

Reads transcript Markdown/TXT files.

Extracts episode, guest, timestamp, and topic metadata.

Splits transcripts into overlapping chunks.

Generates embeddings.

Stores chunks and embeddings in PostgreSQL.

Uses pgvector similarity search during chat.

Run ingestion:

cd backend
python scripts/ingest.py

Run Locally

1. Start PostgreSQL + pgvector

From the project root:

docker compose up -d db

Check:

docker compose ps

The database is exposed on host port 5433 and maps to PostgreSQL container port 5432.

2. Start Ollama

Make sure Ollama is running:

ollama list

3. Start Backend

cd backend
python -m uvicorn app.main:app --reload --port 8000

Backend:

http://localhost:8000

Swagger API documentation:

http://localhost:8000/docs

Health:

http://localhost:8000/api/health

4. Start Frontend

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:3000

Docker Compose

Build and start the services:

docker compose up --build

Check:

docker compose ps

Logs:

docker compose logs -f backend

For Docker-to-host Ollama communication, the backend container may need:

http://host.docker.internal:11434

instead of:

http://localhost:11434

API Endpoints

Create Session

POST /api/sessions

Example:

{
  "title": "Lenny Growth Assistant"
}

Get Session

GET /api/sessions/{session_id}

Chat

POST /api/chat

Example:

{
  "session_id": "SESSION_UUID",
  "message": "How can a startup find product-market fit?",
  "mode": "default",
  "provider": "ollama"
}

Supported modes:

default
ship30

Supported providers:

ollama
openai

The chat response is streamed using Server-Sent Events.

Health

GET /api/health

Grounded Q&A

The default mode:

Embeds the user's question.

Performs vector similarity search.

Retrieves relevant transcript chunks.

Applies the relevance threshold.

Builds a transcript-grounded prompt.

Sends the retrieved context to the selected model.

Streams the answer.

Persists the response and sources.

Citation format:

[Episode: Guest Name, Timestamp/Topic]

If relevant information cannot be retrieved, the assistant returns:

I do not have sufficient information in Lenny's podcast archive to answer this

Ship30 for 30 Mode

Ship30 mode transforms retrieved Lenny transcript insights into a long-form article.

The prompt targets:

Approximately 1,250 words

Strong curiosity-driven or outcome-focused hook

Markdown H2/H3 headings

Short, skimmable paragraphs

Bold anchor words

Useful bullet points

Correct source attribution

A practical framework or checklist at the end

The essay remains grounded in the retrieved transcript context.

Artifact Viewer

The frontend provides a side-by-side Artifact Viewer.

Supported types:

markdown
html

Markdown artifacts are rendered with:

react-markdown + remark-gfm

HTML artifacts are sanitized with DOMPurify and rendered in a sandboxed iframe.

The iframe uses:

sandbox="allow-scripts"

and does not grant allow-same-origin.

Local and Cloud Providers

The provider layer allows runtime provider selection.

Local

Ollama
llama3.2:3b

Cloud

A cloud provider implementation is included and can use the configured cloud API key/model.

The local Ollama provider is the primary demo path.

Testing

From backend/:

pytest -v

The test suite covers API, retrieval, and provider behavior.

Demo Flow

Grounded Q&A

How should a startup find product-market fit?

Verify the generated answer, retrieved sources, guest, episode, and timestamps.

Follow-up

Can you turn those product-market-fit insights into practical steps for a startup?

Ship30 Essay

Switch to Ship30 Essay:

Write a Ship 30 for 30 essay explaining how startups can find product-market fit, using the insights from the relevant Lenny podcast guests. Include a practical framework at the end.

Artifact

Create a Markdown checklist that helps a startup evaluate whether it is moving toward product-market fit, based only on the retrieved Lenny podcast insights.

Insufficient Context

Switch back to Grounded Q&A:

What is the chemical formula of water?

Expected:

I do not have sufficient information in Lenny's podcast archive to answer this

Troubleshooting

Database connection fails

Check:

docker compose ps

The current host mapping is:

ports:
  - "5433:5432"

Therefore the Windows host connects through:

127.0.0.1:5433

Ollama connection fails

Check:

ollama list

Make sure:

llama3.2:3b

is installed and Ollama is running on port 11434.

Frontend "Failed to fetch"

Verify:

http://localhost:8000/api/health

Then verify:

NEXT_PUBLIC_API_URL=http://localhost:8000

Also ensure the backend CORS configuration allows:

http://localhost:3000

No relevant sources

Run:

cd backend
python scripts/ingest.py

Then restart the backend and test with a question related to the transcript corpus.

Documentation

Additional project documentation:

docs/PRD.md
docs/architecture.md
docs/design.md

Development/agent notes:

agent_transcripts/

Security

Transcript-grounded prompting limits unsupported responses.

Retrieval uses a similarity threshold.

Generated HTML is sanitized before rendering.

HTML artifacts are isolated in a sandboxed iframe.

API keys are provided through environment variables.

Database access uses async SQLAlchemy sessions.

Sessions and messages are persisted separately.

Generated artifacts are persisted separately from messages.

Design Summary

The application is designed around the core take-home requirements:

Lenny's Podcast transcript grounding

RAG with pgvector

Local Ollama inference

Cloud provider abstraction

Ship30 content generation

Side-by-side Artifact Viewer

Persistent sessions and messages

Streaming chat responses

Docker-based deployment

Health and operational visibility