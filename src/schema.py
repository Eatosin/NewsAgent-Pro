from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any

class AgentState(BaseModel):
    # Universal Unlock
    model_config = ConfigDict(extra='allow')

    topic: str
    platform: str
    
    # Research Fields
    research: Optional[str] = None
    research_data: Optional[List[Dict]] = None
    key_facts: Optional[List[str]] = None
    controversies: Optional[List[str]] = None
    statistics: Optional[List[str]] = None
    implications: Optional[List[str]] = None
    sources: Optional[List[str]] = None

    # Planner/Writer Fields
    hook: Optional[str] = None
    cta: Optional[str] = None
    outline: Optional[str] = None
    draft: Optional[str] = None
    critique: Optional[str] = None
    
    # Output Fields
    score: int = Field(default=0)
    final_thread: Optional[List[str]] = None
    image_url: Optional[str] = None
    
    messages: List[Dict] = Field(default_factory=list)
