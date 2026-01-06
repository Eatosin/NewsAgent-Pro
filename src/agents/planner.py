import json
from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.config import get_llm
from src.utils.prompt_loader import load_prompt
from src.schema import AgentState

class HybridState:
    """Ensures compatibility between Pydantic models and dictionaries."""
    def __init__(self, state):
        data = state.model_dump() if hasattr(state, 'model_dump') else state
        self.__dict__.update(data)
    
    def get(self, key, default=None):
        return self.__dict__.get(key, default)

def planner_node(state: AgentState):
    """
    Planner Agent: Analyzes research data to create a high-impact content strategy.
    """
    # 🛠️ Initialize Hybrid Access
    state = HybridState(state)
    
    system_prompt = load_prompt("planner.yaml")

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Topic: {state.topic}\nPlatform: {state.platform}")
    ]

    llm = get_llm("planning") 
    response = llm.invoke(messages)

    # Parse JSON output from LLM
    try:
        parsed = json.loads(response.content)
    except json.JSONDecodeError:
        # Robust Fallback for unstructured responses
        parsed = {
            "hook": response.content.split("\n")[0],
            "sections": response.content.split("\n")[1:],
            "cta": "What do you think? Reply below!",
            "estimated_length": "10 parts"
        }

    # CRITICAL: Join list to string to prevent Pydantic validation errors
    return {
        "hook": parsed.get("hook", ""),
        "outline": "\n".join(parsed.get("sections", [])) if isinstance(parsed.get("sections"), list) else parsed.get("sections", ""),
        "cta": parsed.get("cta", ""),
        "estimated_length": parsed.get("estimated_length", "")
        }
