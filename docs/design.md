# Design Specification
# The Lenny Growth Assistant

## 1. Design Overview

The Lenny Growth Assistant uses a responsive two-pane interface inspired by
modern AI assistant applications.

The primary interaction is conversational. Users ask questions in the left
chat pane while generated artifacts can be viewed and interacted with in the
right artifact pane.

The interface should remain simple, readable, and focused on actionable
growth insights.

---

## 2. Desktop Layout

On desktop screens, the application uses two primary areas:

```text
┌────────────────────────────────────────────────────────────────────┐
│                         Application Header                         │
├───────────────────────────────┬────────────────────────────────────┤
│                               │                                    │
│          CHAT PANE             │         ARTIFACT PANE              │
│                               │                                    │
│  Session / History             │  Artifact Header                  │
│                               │                                    │
│  User Message                  │  Markdown / HTML Preview           │
│                               │                                    │
│  Assistant Response            │                                    │
│                               │                                    │
│  Source Citations              │                                    │
│                               │                                    │
│  ┌─────────────────────────┐  │                                    │
│  │ Ask a question...       │  │                                    │
│  └─────────────────────────┘  │                                    │
│                               │                                    │
└───────────────────────────────┴────────────────────────────────────┘