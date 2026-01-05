from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class AgentState(BaseModel):
    topic: str
    platform: str  # "twitter" or "linkedin"
    research_data: Optional[List[Dict]] = None 
    key_facts: Optional[List[str]] = None
    research: Optional[str] = None
    sources: Optional[List[str]] = None
    outline: Optional[str] = None
    draft: Optional[str] = None
    critique: Optional[str] = None
    score: Optional[int] = Field(default=0, ge=0, le=10)
    final_thread: Optional[List[str]] = None  # List of tweet texts
    image_url: Optional[str] = None
    messages: List[Dict] = Field(default_factory=list)  # For LangGraph history
