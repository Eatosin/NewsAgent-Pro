import json
from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.config import get_llm
from src.utils.prompt_loader import load_prompt
from src.schema import AgentState

class HybridState:
    def __init__(self, state):
        data = state.model_dump() if hasattr(state, 'model_dump') else state
        self.__dict__.update(data)
    def get(self, key, default=None):
        return self.__dict__.get(key, default)

def researcher_node(state: AgentState):
    """
    Researcher Agent: Aggregates raw search results and extracts structured facts.
    """
    state = HybridState(state)
    research_data = state.get('research_data') or []
    
    context = "\n\n".join([
        f"Source: {r['title']} ({r['url']})\nContent: {r['content']}"
        for r in research_data
    ])
    
    if not context:
        context = "No search results found. Use general knowledge cautiously."
    
    system_prompt = load_prompt("researcher.yaml")
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Topic: {state.topic}\n\nSearch Results:\n{context}")
    ]
    
    llm = get_llm("research")
    response = llm.invoke(messages)
    
    try:
        parsed = json.loads(response.content)
    except:
        parsed = {
            "summary": response.content, 
            "key_facts": [], 
            "sources": [], 
            "controversies": [], 
            "implications": "", 
            "suggested_hook_ideas": []
        }
    
    return {
        "research": parsed.get("summary"),
        "sources": parsed.get("sources", []),
        "key_facts": parsed.get("key_facts", []),
        "controversies": parsed.get("controversies", []),
        "implications": parsed.get("implications"),
        "hook": parsed.get("suggested_hook_ideas", [""])[0] if parsed.get("suggested_hook_ideas") else ""
    }
