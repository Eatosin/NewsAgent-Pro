from langgraph.graph import StateGraph, END
from src.schema import AgentState

# Import Agents
from src.agents.planner import planner_node
from src.agents.researcher import researcher_node
from src.agents.writer import writer_node
from src.agents.designer import designer_node

# Initialize Graph
workflow = StateGraph(AgentState)

# Add Nodes (The Employees)
workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("designer", designer_node)

# Define Flow (The Assembly Line)
# 1. Start -> Planner (Create Outline)
workflow.set_entry_point("planner")

# 2. Planner -> Researcher (Get Facts)
workflow.add_edge("planner", "researcher")

# 3. Researcher -> Writer (Draft Content)
workflow.add_edge("researcher", "writer")

# 4. Writer -> Designer (Create Visuals)
workflow.add_edge("writer", "designer")

# 5. Designer -> End
workflow.add_edge("designer", END)

# Compile
graph = workflow.compile()
