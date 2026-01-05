import os
from dotenv import load_dotenv
from tavily import TavilyClient
from typing import List, Dict
from langgraph.prebuilt import ToolNode

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def perform_research(state: Dict) -> Dict:
    """
    Research Tool: Performs multi-query search on Tavily based on the topic.
    Useful for gathering comprehensive context from multiple angles.
    """
    topic = state["topic"]

    # Smart query planning (multi-perspective)
    base_queries = [
        topic,
        f"{topic} latest news 2025 OR 2026",
        f"{topic} controversies OR criticisms OR debates",
        f"{topic} statistics OR data OR impact",
        f"{topic} implications OR future outlook"
    ]

    all_results: List[Dict] = []
    seen_urls = set()

    for query in base_queries:
        try:
            response = tavily_client.search(
                query=query,
                max_results=6,
                search_depth="advanced",
                include_raw_content=False
            )
            for result in response.get("results", []):
                if result["url"] not in seen_urls:
                    seen_urls.add(result["url"])
                    all_results.append({
                        "title": result["title"],
                        "url": result["url"],
                        "content": result["content"][:2000]
                    })
        except Exception as e:
            print(f"Tavily error on query '{query}': {e}")
            continue

    return {"research_data": all_results[:20]} # Cap to avoid token blowup

# LangGraph ToolNode
research_tool = ToolNode(tools=[perform_research])
