# Product Requirements Document
# The Lenny Growth Assistant

## 1. Product Overview

The Lenny Growth Assistant is an AI-powered growth assistant that allows Growth
Product Managers to ask questions and receive actionable, source-attributed
answers based on Lenny's Podcast transcripts.

The goal is to help users extract useful growth and product insights without
having to listen to more than 200 hours of podcast content.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant
transcript sections before generating an answer.

---

## 2. Target Persona

### Growth Product Manager

The primary user is a Growth PM who:

- Needs actionable product and growth tactics.
- Does not have time to listen to 200+ hours of podcast episodes.
- Wants answers grounded in real podcast discussions.
- Needs to know which episode and section support an answer.
- Wants practical frameworks and tactics that can be applied immediately.

---

## 3. Problem Statement

Lenny's Podcast contains a large amount of valuable product and growth
knowledge distributed across many episodes.

Finding a specific insight manually requires listening to or searching through
large amounts of content.

The Lenny Growth Assistant solves this problem by allowing users to ask
natural-language questions and retrieve relevant information from the
transcript archive.

---

## 4. Goals

### Primary Goals

1. Provide grounded answers using Lenny's Podcast transcripts.
2. Provide citations for retrieved information.
3. Acknowledge when the transcript archive does not contain sufficient
   information to answer a question.
4. Support local inference using Ollama.
5. Support a cloud LLM provider.
6. Allow users to switch between model providers.
7. Generate approximately 1,250-word "Ship 30 for 30" essays.
8. Provide a Claude-style artifact viewer.
9. Safely render Markdown and HTML artifacts.
10. Provide a deployable Docker-based application.

---

## 5. Core Features

### 5.1 Grounded Question Answering

Users can ask questions about product, growth, leadership, and other topics
covered by the podcast transcripts.

The system will:

1. Convert the user's question into an embedding.
2. Search the vector database.
3. Retrieve the most relevant transcript chunks.
4. Provide those chunks to the LLM.
5. Generate a grounded response.
6. Include source citations.

---

### 5.2 Source Citations

Generated answers must use the following citation format:

[Episode: Guest Name, Timestamp/Topic]

The citations should allow the user to understand where the information came
from.

---

### 5.3 Insufficient Information Handling

If retrieved information does not meet the required relevance threshold, the
assistant should respond:

"I do not have sufficient information in Lenny's podcast archive to answer
this"

The system must avoid presenting unsupported information as if it came from
the podcast archive.

---

### 5.4 Ship 30 for 30 Content Engine

The assistant will support generation of approximately 1,250-word essays.

Generated essays should include:

- A strong headline and hook.
- A curiosity gap, outcome promise, or counterintuitive insight.
- Short paragraphs of approximately 1–3 sentences.
- Clear Markdown headings.
- Bold key ideas.
- Bullet lists.
- Clear transitions.
- A concrete framework, checklist, or operational tactic.

---

### 5.5 Artifact Viewer

The application will provide a side-by-side artifact experience.

Supported artifact types:

- Markdown
- HTML/CSS

Markdown artifacts will be rendered using the frontend Markdown renderer.

HTML/CSS artifacts will be displayed inside a sandboxed iframe.

The iframe will use:

`sandbox="allow-scripts"`

and will omit:

`allow-same-origin`

to prevent the artifact from accessing the parent application's storage
and cookies.

---

### 5.6 Multi-Provider LLM Support

The application will support:

- Ollama for local inference.
- A cloud provider such as Anthropic or OpenAI.

The default provider will be configurable through an environment variable:

`DEFAULT_LLM_PROVIDER=ollama`

The frontend will provide a provider selector.

---

## 6. Success Metrics

### Retrieval Citation Accuracy

Target:

**>= 90%**

Answers should correctly reference relevant transcript sources.

### Local Inference Latency

Target:

**< 4 seconds to first token**

when using the local Ollama model.

### Artifact Render Safety

Target:

**0 XSS vulnerabilities**

for generated artifacts.

---

## 7. User Experience Requirements

The application should provide:

- A responsive interface.
- A chat/session history.
- A provider indicator.
- Streaming assistant responses.
- A collapsible artifact panel.
- Clear source citations.
- Clear handling of insufficient information.
- Safe artifact rendering.

---

## 8. Non-Functional Requirements

### Performance

The system should support streaming responses and target less than
4 seconds to first token for local inference.

### Reliability

The backend should include:

- Structured logging.
- Global exception handling.
- Health checks.
- Database status checks.
- Ollama status checks.

### Security

The application should:

- Sanitize artifact content.
- Use sandboxed iframes for HTML artifacts.
- Avoid `allow-same-origin` on artifact iframes.
- Prevent XSS vulnerabilities.

### Deployment

The application should run using Docker Compose with:

- PostgreSQL + pgvector.
- FastAPI backend.
- Frontend.
- Optional Ollama service.

---

## 9. Key Trade-offs

### Local Model vs Cloud Model

Local Ollama inference provides local execution and avoids cloud inference
costs, but smaller local models may have limitations in reasoning quality.

Cloud models can provide stronger reasoning capabilities but require an
external API and may introduce usage costs.

The system will therefore support both providers.

### Retrieval Size

The system will retrieve approximately 4–6 relevant transcript chunks.

A larger retrieval set may provide more context but can increase prompt size
and potentially introduce less relevant information.

### Local Model Size

The project supports Ollama models such as:

- llama3.2:3b
- llama3.1:8b
- mistral:7b

The local model choice will depend on available hardware and expected
performance.

---

## 10. Out of Scope

The initial version will not attempt to:

- Generate answers unrelated to the podcast archive as factual podcast
  knowledge.
- Replace the original podcast content.
- Provide unrestricted internet-based research.
- Provide autonomous actions outside the application.

---

## 11. Acceptance Criteria

The product is considered complete when:

- Users can create and access chat sessions.
- Users can ask questions about podcast transcripts.
- Relevant transcript chunks are retrieved.
- Answers include source citations.
- Unsupported questions are handled appropriately.
- Ollama can be used as the local provider.
- A cloud provider can be configured.
- Provider switching works.
- Ship 30 for 30 content can be generated.
- Markdown artifacts can be rendered.
- HTML artifacts can be safely rendered.
- PostgreSQL and pgvector are used.
- The application can be started using Docker Compose.
- Automated tests cover retrieval, out-of-domain handling, and model
  switching.