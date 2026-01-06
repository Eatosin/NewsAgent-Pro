import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.config import get_llm
from src.utils.prompt_loader import load_prompt
from src.schema import HybridState, AgentState

def planner_node(state: AgentState):
    state_wrapper = HybridState(state)
    topic = state_wrapper.get("topic")
    
    # Load your existing SOTA prompt
    system_prompt = load_prompt("planner.yaml")
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Topic: {topic}")
    ]
    
    # Use Groq for speed
    llm = get_llm("planning")
    response = llm.invoke(messages)
    
    # Robust JSON parsing
    content = response.content.strip()
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    
    try:
        data = json.loads(content)
        outline = data.get("outline", "")
        # Ensure outline is string
        if isinstance(outline, list):
            outline = "\n".join(outline)
            
        return {
            "hook": data.get("hook"),
            "outline": outline,
            "cta": data.get("cta")
        }
    except:
        # Fallback if JSON fails
        return {"outline": content, "hook": f"News: {topic}"}
