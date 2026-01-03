# Contributing to NewsAgent Pro

## Architecture
*   **Orchestrator:** Python/Streamlit
*   **AI Models:** Gemini 2.5 (Text), Flux.1-schnell (Vision)
*   **Search:** Tavily API

## Standards
*   All PRs must pass the `quality_gate` workflow.
*   No hardcoded API keys. Use `os.getenv`.
