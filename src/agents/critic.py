from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.config import get_llm
from src.utils.prompt_loader import load_prompt
from src.schema import AgentState
import json

def critic_node(state: AgentState):
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
    
    if parsed.get("approved", False) or parsed.get("overall_score", 0) >= 8.5:
        return {
            "score": parsed.get("overall_score", 9.0),
            "critique": parsed.get("feedback", ""),
            "draft": parsed.get("revised_draft") or state.draft  # Use revised if provided
        }
    else:
        # Trigger revision loop
        return {
            "draft": parsed.get("revised_draft", state.draft),
            "critique": parsed.get("feedback", ""),
            "score": parsed.get("overall_score", 0)
        }
