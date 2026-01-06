from langgraph.graph import StateGraph, END
from src.schema import AgentState, HybridState

# Import Agents
from src.agents.planner import planner_node
from src.agents.researcher import researcher_node
from src.agents.writer import writer_node
from src.agents.designer import designer_node
from src.agents.critic import critic_node

# --- CONDITIONAL LOGIC ---
def should_continue(state: AgentState):
    """
    Decides: Go back to Writer? Or move to Designer?
    """
    wrapper = HybridState(state)
    score = wrapper.get("score", 0)
    revisions = wrapper.get("revision_count", 0)
    
    # Rule: If score < 8 AND we haven't tried too many times...
    if score < 8 and revisions < 2:
        print(f"🔄 Quality Check Failed (Score: {score}/10). Revising...")
        return "writer"
    
    if score >= 8:
        print(f"✅ Quality Check Passed (Score: {score}/10).")
    else:
        print("⚠️ Max revisions reached. Moving to publishing.")
        
    return "designer"

# --- BUILD GRAPH ---
workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("critic", critic_node)
workflow.add_node("designer", designer_node)

# Linear flow start
workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "writer")

# The Loop: Writer -> Critic -> (Router)
workflow.add_edge("writer", "critic")

workflow.add_conditional_edges(
    "critic",
    should_continue,
    {
        "writer": "writer",      # Loop back
        "designer": "designer"   # Move forward
    }
)

workflow.add_edge("designer", END)

graph = workflow.compile()
