import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.config import get_llm
from src.utils.prompt_loader import load_prompt
from src.schema import HybridState, AgentState

def critic_node(state: AgentState):
    """
    Critic Agent: Reviews content quality and enforces editorial standards.
    Uses external YAML prompts for easy tuning.
    """
    # Initialize Hybrid Access (Safety Wrapper)
    state_wrapper = HybridState(state)
    
    draft = state_wrapper.get("draft")
    platform = state_wrapper.get("platform")
    revision_count = state_wrapper.get("revision_count", 0)
    
    print(f"⚖️ Critic is reviewing draft (Revision {revision_count})...")
    
    system_prompt = load_prompt("critic.yaml")
    
    # Construct Context for the Critic
    user_msg = f"""
    TARGET PLATFORM: {platform}
    
    CURRENT DRAFT:
    {draft}
    
    TASK: Score this content and provide specific feedback for improvement.
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_msg)
    ]
    
    # Use Groq (Planning Model) for fast scoring
    llm = get_llm("planning") 
    response = llm.invoke(messages)
    
    # Robust JSON Parsing (Handles Markdown blocks)
    content = response.content.strip()
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    
    try:
        data = json.loads(content)
        return {
            "score": data.get("score", 5),
            "critique": data.get("feedback", "Improve clarity and engagement."),
            "revision_count": revision_count + 1
        }
    except:
        # Fail-safe if JSON breaks
        return {
            "score": 5, 
            "critique": "Format error. Please review structure.", 
            "revision_count": revision_count + 1
        }
