import os
from tavily import TavilyClient
from langchain_core.tools import tool

@tool
def perform_research(topic: str):
    """
    Searches the web for recent news using Tavily.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY not found."
        
    client = TavilyClient(api_key=api_key)
    
    try:
        # Search specifically for news
        response = client.search(query=topic, topic="news", days=2)
        results = response.get("results", [])
        
        context = []
        for r in results[:4]:
            context.append(f"Title: {r['title']}\nURL: {r['url']}\nSummary: {r['content']}")
            
        return "\n\n".join(context)
    except Exception as e:
        return f"Search failed: {str(e)}"
