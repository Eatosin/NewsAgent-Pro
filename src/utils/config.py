import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from huggingface_hub import InferenceClient
from tavily import TavilyClient

load_dotenv()

# LLM Router
def get_llm(task: str):
    try:
        # Primary: Groq for speed/iteration
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
    except Exception:
        # Fallback: Gemini Flash
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7
        )

# Tools
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

hf_client = InferenceClient(token=os.getenv("HF_TOKEN"))
