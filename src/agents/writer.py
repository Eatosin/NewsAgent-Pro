from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.config import get_llm
from src.utils.prompt_loader import import load_prompt
from src.schema import AgentState

class HybridState:
    """
    Production-grade wrapper to ensure compatibility between 
    Pydantic objects and standard Python dictionaries.
    """
    def __init__(self, state):
        # Convert to dict if it's a Pydantic model, otherwise use as is
        data = state.model_dump() if hasattr(state, 'model_dump') else state
        self.__dict__.update(data)
    
    def get(self, key, default=None):
        return self.__dict__.get(key, default)

def writer_node(state: AgentState):
    """
    Writer Agent: Transforms researched facts and outlines into viral content.
    Supports multi-platform branching (Twitter Threads vs LinkedIn Posts).
    """
    # 🛠️ Initialize Hybrid Access
    state = HybridState(state)
    
    # Identify platform and load corresponding prompt template
    platform = state.platform.lower() if state.platform else "twitter"
    prompt_file = "writer_twitter.yaml" if "twitter" in platform else "writer_linkedin.yaml"
    
    system_prompt = load_prompt(prompt_file)

    # Compile context block for the LLM
    # Note: Using .get() here makes the code resilient to missing data
    context = f"""
    Research Summary: {state.get('research', 'No research available')}
    Key Facts: {chr(10).join(state.get('key_facts') or [])}
    Controversies: {chr(10).join(state.get('controversies') or [])}
    Implications: {state.get('implications', '')}
    
    Outline:
    Hook: {state.get('hook', '')}
    Sections: {chr(10).join(state.get('outline') or []) if isinstance(state.get('outline'), list) else state.get('outline', '')}
    CTA: {state.get('cta', '')}
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Write the full thread/post using this context:\n{context}")
    ]

    # Initialize LLM via centralized config
    llm = get_llm("writing") 
    response = llm.invoke(messages)
    draft = response.content.strip()

    # Platform-specific formatting logic
    if "twitter" in platform:
        # Split by the defined delimiter for UI rendering
        final_thread = [t.strip() for t in draft.split("|||") if t.strip()]
    else:
        # LinkedIn is treated as a single cohesive block
        final_thread = [draft]

    return {
        "draft": draft,
        "final_thread": final_thread
    }
