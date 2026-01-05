from langgraph.prebuilt import ToolNode
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(state):
    topic = state["topic"]
    queries = [
        topic,
        f"{topic} latest developments 2026",
        f"{topic} controversies OR criticisms",
        f"{topic} statistics OR data"
    ]
    results = []
    for q in queries:
        try:
            resp = tavily_client.search(q, max_results=5, search_depth="advanced")
            results.extend(resp["results"])
        except:
            pass
    return {"research_data": results}

research_tool = ToolNode([tavily_search])
