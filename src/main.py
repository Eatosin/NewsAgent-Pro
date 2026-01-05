from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.schema import AgentState
from src.agents.planner import planner_node
from src.agents.researcher import researcher_node
from src.agents.writer import writer_node
from src.agents.critic import critic_node
from src.agents.designer import designer_node
from src.tools.research import perform_research  # Direct function for tool node

# Conditional edge logic
def should_revise(state: AgentState) -> str:
    if state.get("score", 0) < 8.5 and state.get("messages", []).__len__() < 6:  # Max ~2 revisions
        return "writer"
    return "designer"

# Build the graph
def create_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("research_tool", perform_research)  # Tool call
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("designer", designer_node)
    
    # Set entry point
    workflow.set_entry_point("planner")
    
    # Edges
    workflow.add_edge("planner", "research_tool")
    workflow.add_edge("research_tool", "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "critic")
    
    # Conditional after critic
    workflow.add_conditional_edges(
        "critic",
        should_revise,
        {
            "writer": "writer",
            "designer": "designer"
        }
    )
    
    # Designer ends
    workflow.add_edge("designer", END)
    
    # Memory for state persistence (optional, but good for debugging)
    memory = MemorySaver()
    
    # Compile
    app = workflow.compile(checkpointer=memory)
    
    return app

# Global graph instance
graph = create_graph()
