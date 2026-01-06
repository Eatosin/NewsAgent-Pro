import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm(task_type: str = "general"):
    """
    Factory to get the best LLM for the job.
    - Planning/Logic -> Groq (Llama 3.3) for speed.
    - Writing/Context -> Groq or Gemini Fallback.
    """
    groq_key = os.getenv("GROQ_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    # PRIMARY: Groq (Llama 3.3 70B)
    if groq_key:
        try:
            return ChatGroq(
                temperature=0.7,
                model_name="llama-3.3-70b-versatile",
                api_key=groq_key
            )
        except Exception as e:
            print(f"⚠️ Groq failed: {e}. Falling back...")

    # FALLBACK: Gemini
    if gemini_key:
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=gemini_key,
            temperature=0.7
        )
    
    raise ValueError("❌ No API Keys found! Please set GROQ_API_KEY or GEMINI_API_KEY.")
