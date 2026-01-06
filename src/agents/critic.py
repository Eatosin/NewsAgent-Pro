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

def critic_node(state: AgentState):
    """
    Critic Agent: Audits generated content for quality, bias, and platform-fit.
    """
    # 🛠️ Initialize Hybrid Access
    state = HybridState(state)
    
    system_prompt = load_prompt("critic.yaml")

    context = f"""
    Platform: {state.platform}
    Draft: {state.draft}
    Research: {state.research}
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Critique this draft:\n{context}")
    ]

    llm = get_llm("critique")
    response = llm.invoke(messages)

    try:
        parsed = json.loads(response.content)
    except json.JSONDecodeError:
        parsed = {
            "reasoning": response.content,
            "overall_score": 5.0,
            "feedback": "Parsing failed - revise fully",
            "approved": False,
            "revised_draft": response.content
        }

    # Decide whether to move forward or loop back based on the critique
    if parsed.get("approved", False) or parsed.get("overall_score", 0) >= 8.0:
        return {
            "score": parsed.get("overall_score", 9.0),
            "critique": parsed.get("feedback", ""),
            "draft": parsed.get("revised_draft") or state.draft
        }
    else:
        # Trigger revision loop in the graph
        return {
            "draft": parsed.get("revised_draft", state.draft),
            "critique": parsed.get("feedback", ""),
            "score": parsed.get("overall_score", 0)
        }
