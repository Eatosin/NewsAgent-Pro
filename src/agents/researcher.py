from src.tools.research import perform_research
from src.schema import HybridState, AgentState

def researcher_node(state: AgentState):
    """
    Executes the research tool and stores the results.
    """
    # Wrap state for safe access
    state_wrapper = HybridState(state)
    topic = state_wrapper.get("topic")
    
    print(f"🕵️‍♂️ Researching: {topic}")
    
    # Call the Tavily Tool
    research_results = perform_research.invoke(topic)
    
    # Return updates to the state
    return {
        "research_data": research_results
    }
