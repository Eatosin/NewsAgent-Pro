from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.config import get_llm
from src.utils.prompt_loader import load_prompt
from src.schema import AgentState

def writer_node(state: AgentState):
    platform = state.platform.lower()
    prompt_file = "writer_twitter.yaml" if "twitter" in platform else "writer_linkedin.yaml"
    
    system_prompt = load_prompt(prompt_file)
    
    # Compile context
    context = f"""
    Research Summary: {state.research or 'No research available'}
    Key Facts: {chr(10).join(state.key_facts or [])}
    Controversies: {chr(10).join(state.controversies or [])}
    Implications: {state.implications or ''}
    Outline: 
    Hook: {state.hook}
    Sections: {chr(10).join(state.outline or [])}
    CTA: {state.cta}
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Write the full thread/post using this context:\n{context}")
    ]
    
    llm = get_llm("writing")  # Gemini fallback for long context if needed
    
    response = llm.invoke(messages)
    
    draft = response.content.strip()
    
    # Twitter-specific: split if needed
    if "twitter" in platform:
        final_thread = draft.split("|||")
    else:
        final_thread = [draft]  # LinkedIn as single post
    
    return {
        "draft": draft,
        "final_thread": final_thread
    }
