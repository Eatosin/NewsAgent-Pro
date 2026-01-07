<div align="center">

# 🗞️ NewsAgent Pro v2
### *The Autonomous, Self-Correcting AI Newsroom*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangGraph](https://img.shields.io/badge/Orchestrator-LangGraph-1C1C1C?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Inference-Groq_Llama_3.3-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![Flux](https://img.shields.io/badge/Visuals-FLUX.1_Schnell-000?style=for-the-badge&logo=huggingface)](https://huggingface.co/black-forest-labs/FLUX.1-schnell)

[View Live Demo](#-live-demo) • [System Architecture](#-system-architecture) • [Deploy Now](#-deployment)

</div>

---

## ⚡ The Problem: "Content Fatigue"
To run a high-quality media channel today, you need a **Researcher** to find facts, a **Writer** to draft hooks, an **Editor** to fix mistakes, and a **Designer** to make thumbnails.
Doing this manually takes hours. Most "AI Writers" just hallucinate generic slop.

## 🧠 The Solution: Agentic Workflow
**NewsAgent Pro** is not a chatbot. It is a **Multi-Agent Swarm** that mimics a real newsroom.
It reads the internet, plans a strategy, drafts content, **critiques its own work**, and designs branded visuals—all in 60 seconds.

### ✨ Key Innovations (v2.0)
*   **🔄 Self-Correction Loop:** The **Critic Agent** reads the draft and grades it (1-10). If the score is low, it sends it back to the Writer with specific feedback. It iterates until perfection.
*   **⚡ Hyper-Fast Inference:** Powered by **Groq (Llama 3.3)** for sub-second logic and planning.
*   **🕵️‍♂️ Real-Time Truth:** Uses **Tavily API** to scrape live news (last 48 hours), preventing hallucinations.
*   **🎨 AI Graphic Design:** Uses **Flux.1-Schnell** to generate cinematic backgrounds, then uses **Python Pillow** to programmatically overlay "Newsflash" headlines.

---

## ⚙️ System Architecture

The system uses a **Stateful Graph** (LangGraph) with conditional routing.

```mermaid
graph LR
    A[User Input] --> B(🧠 Planner)
    B -->|Strategy| C(🕵️‍♂️ Researcher)
    C -->|Facts| D(✍️ Writer)
    D --> E{⚖️ Critic}
    E -->|Score < 8| D
    E -->|Score > 8| F(🎨 Designer)
    F -->|Visuals| G[Final Output]

    style E fill:#ff9999,stroke:#333,stroke-width:2px,color:black
    style F fill:#99ff99,stroke:#333,stroke-width:2px,color:black
```

### The "Newsroom" Staff
| Role | Model / Tool | Function |
| :--- | :--- | :--- |
| **Planner** | **Llama 3.3 (Groq)** | Analyzes the topic and determines the "Viral Angle." |
| **Researcher** | **Tavily API** | Scrapes the web for facts/quotes from the last 48 hours. |
| **Writer** | **Gemini 2.5 / Groq** | Drafts platform-specific content (Threads vs Posts). |
| **Critic** | **Llama 3.3 (Groq)** | **The Gatekeeper.** Rejects low-quality drafts and forces rewrites. |
| **Designer** | **Flux.1-Schnell** | Generates 16:9 cinematic cover art in <4 steps. |

---
## 🖼️ Sample Outputs

| **Twitter Thread (Viral Style)** | **LinkedIn Post (Professional)** |
| :--- | :--- |
| **Topic:** "AI Agents 2026"<br>![Twitter Sample](X.png/400x225/0f0f23/00ff00?text=AI+AGENTS+TAKEOVER) | **Topic:** "Venezuela Oil Crisis"<br>![LinkedIn Sample](https://assets.LinkedIn.png/400x400/16213e/ffffff?text=MARKET+SHIFT) |
| *Short, punchy, thread-formatted.* | *Deep dive, strategic analysis.* |

---
## 🚀 Live Demo

**Try the Production Build on Hugging Face Spaces:**

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Launch%20App-NewsAgent_Pro-yellow?style=for-the-badge&logo=huggingface)](https://huggingface.co/spaces/EATosin/NewsAgent-Pro)

> *Try searching: "DeepSeek vs OpenAI" or "SpaceX Starship Launch"*

---

## 📦 Installation (Local & Cloud)

### 1. Clone & Setup
```bash
git clone https://github.com/Eatosin/NewsAgent-Pro.git
cd NewsAgent-Pro
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file with your keys (Get Groq for free speed!):
```env
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIza...
TAVILY_API_KEY=tvly-...
HF_TOKEN=hf_...
```

### 3. Run the App
```bash
streamlit run src/app.py
```

### 4. Docker (Production)
We use a custom multi-stage build to handle system dependencies (Fonts, Pillow):
```bash
docker build -t newsagent .
docker run -p 7860:7860 --env-file .env newsagent
```

---

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Eatosin/NewsAgent-Pro&type=Date)](https://star-history.com/#Eatosin/NewsAgent-Pro&Date)

---

## 👨‍💻 Author
**Owadokun Tosin Tobi**
*Senior AI Engineer & Product Builder*

*   **Portfolio:** [GitHub](https://github.com/eatosin)
*   **Connect:** [LinkedIn](https://www.linkedin.com/in/owadokun-tosin-tobi-6159091a3)

---
*Built with the Lexpertz R&D Stack.*
