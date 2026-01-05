from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.config import get_llm
from src.utils.prompt_loader import load_prompt
from src.schema import AgentState

def researcher_node(state: AgentState):
    research_data = state.research_data or []
    
    # Format research as context
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
    
    # Simple JSON parse (in production use Pydantic parser)
    import json
    try:
        parsed = json.loads(response.content)
    except:
        parsed = {"summary": response.content, "key_facts": [], "sources": [], "controversies": [], "implications": "", "suggested_hook_ideas": []}
    
    return {
        "research": parsed.get("summary"),
        "sources": parsed.get("sources", []),
        "key_facts": parsed.get("key_facts", []),
        "controversies": parsed.get("controversies", []),
        "implications": parsed.get("implications"),
        "hook_ideas": parsed.get("suggested_hook_ideas", [])
    }
