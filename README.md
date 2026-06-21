Technical Architecture & Framework Choices
Core Architecture

The system utilizes a unified, single-state paradigm built entirely on Python 3.11+, wrapping Streamlit for instant UI rendering and OpenAI's Structured Outputs engine (gpt-4o-mini) for deterministic state mutations.

https://www.branch.io/glossary/query-parameters/ ➔ [OpenAI JSON Parser] ➔ [Streamlit Session State]
                                                         │
                                                         ▼
[User Prompt] + [Historical Chat Memory] + [Reference RAG Protocol] ➔ [Adaptive Agent Brain]

Why This Stack?

    Streamlit Framework: Chosen because it eliminates the overhead of managing independent React frontends, FastAPI backends, and CORS configurations. Web serving, UI compilation, and incoming URL query parameter extraction (st.query_params) are managed concurrently.

    In-Memory Session Management (st.session_state): For an MVP bound by a single-session memory constraint, spinning up external Redis or PostgreSQL instances adds architectural bloat. Native session memory keeps read/write loops execution-fast.

    Pydantic + Structured Outputs API: Unstructured patient onboarding text is notoriously high-variance. Passing raw string text directly into standard LLMs often results in brittle downstream evaluation. Utilizing Pydantic schemas enforced by OpenAI's JSON Schema parsing ensures that system attributes (like current_day or sleep_hours) remain strictly type-cast.

    Context-Stuffed RAG (Zero-Hallucination Bound): Since the reference protocol documentation fits securely within the LLM's context window, explicit vector database embeddings and vector retrievers (like Pinecone/Chroma) were omitted. Passing the rule text explicitly through system prompts drastically minimizes token search latencies while guaranteeing factual compliance.