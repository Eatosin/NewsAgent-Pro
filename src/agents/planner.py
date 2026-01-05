from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.config import get_llm
from src.utils.prompt_loader import load_prompt
from src.schema import AgentState
import json

def planner_node(state: AgentState):
    system_prompt = load_prompt("planner.yaml")
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Topic: {state.topic}\nPlatform: {state.platform}")
    ]
    
    llm = get_llm("planning")  # Groq primary for fast iteration
    
    response = llm.invoke(messages)
    
    # Parse JSON (robust)
    try:
        parsed = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback: treat as raw string outline
        parsed = {
            "hook": response.content.split("\n")[0],
            "sections": response.content.split("\n")[1:],
            "cta": "What do you think? Reply below!",
            "estimated_length": "10 parts"
        }
    
    return {
        "hook": parsed.get("hook", ""),
        "outline": parsed.get("sections", []),
        "cta": parsed.get("cta", ""),
        "estimated_length": parsed.get("estimated_length", "")
    }
