from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.config import get_llm
from src.utils.prompt_loader import load_prompt
from src.schema import HybridState, AgentState

def writer_node(state: AgentState):
    state_wrapper = HybridState(state)
    platform = state_wrapper.get("platform", "twitter")
    research = state_wrapper.get("research_data")
    outline = state_wrapper.get("outline")
    
    # Select prompt based on platform
    prompt_file = "writer_twitter.yaml" if "twitter" in platform.lower() else "writer_linkedin.yaml"
    system_prompt = load_prompt(prompt_file)
    
    user_msg = f"""
    Research: {research}
    Outline: {outline}
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_msg)
    ]
    
    llm = get_llm("writing")
    response = llm.invoke(messages)
    draft = response.content.strip()
    
    final_thread = []
    if "twitter" in platform.lower():
        # Split threads by delimiter
        final_thread = [t.strip() for t in draft.split("|||") if t.strip()]
    else:
        final_thread = [draft]
        
    return {
        "draft": draft,
        "final_thread": final_thread
    }
